from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField, Value
from api.models import Contribution, Proposal, Meeting, CustomUser, Vote
from api.permissions import IsAdminOrSuperAdmin
from api.serializers.dashboard import AdminDashboardSerializer, MemberDashboardSerializer


class DashboardView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if IsAdminOrSuperAdmin().has_permission(self.request, self):
            return AdminDashboardSerializer
        return MemberDashboardSerializer

    def get(self, request):
        user = request.user
        now = timezone.now()
        is_admin = IsAdminOrSuperAdmin().has_permission(request, self)

        if is_admin:
            data = self.get_admin_dashboard_data(now)
            serializer = AdminDashboardSerializer(data)
        else:
            data = self.get_member_dashboard_data(user, now)
            serializer = MemberDashboardSerializer(data)

        return Response(serializer.data)

    def get_admin_dashboard_data(self, now):
        last_month_date = (now - timedelta(days=30)).date()
        last_90_days_date = (now - timedelta(days=90)).date()

        total_contributions = Contribution.objects.aggregate(Sum("amount"))["amount__sum"] or 0

        monthly_growth_sum = Contribution.objects.filter(
            month__gte=last_month_date
        ).aggregate(Sum("amount"))["amount__sum"] or 0

        monthly_growth_percent = (
            (monthly_growth_sum / total_contributions) * 100 if total_contributions else 0
        )

        avg_monthly_contribution = (
            Contribution.objects.filter(
                month__gte=last_90_days_date
            )
            .values('month')
            .annotate(month_sum=Sum('amount'))
            .aggregate(
                avg_month=ExpressionWrapper(
                    Sum('month_sum') / Value(90.0),
                    output_field=DecimalField(max_digits=12, decimal_places=2)
                )
            )['avg_month'] or 0
        )

        # Monthly contribution graph for all months (can limit to last 6 if you want)
        monthly_data = (
            Contribution.objects.order_by('month')
            .values('month')
            .annotate(total=Sum('amount'))
        )

        monthly_contribution_graph = [
            {"month": m['month'].strftime("%b %Y"), "amount": m['total']} for m in monthly_data
        ]

        data = {
            "total_club_value": total_contributions,
            "total_assets": Proposal.objects.filter(status="approved").count(),
            "monthly_growth_percent": round(monthly_growth_percent, 2),
            "pending_actions": [
                f"{Proposal.objects.filter(status='pending').count()} proposals pending",
                f"{CustomUser.objects.filter(is_active=True).count()} active members",
            ],
            "avg_monthly_contribution": round(avg_monthly_contribution, 2),
            "monthly_contribution_graph": monthly_contribution_graph,
            "voting_summary": {
                "approved": Proposal.objects.filter(status="approved").count(),
                "rejected": Proposal.objects.filter(status="rejected").count(),
                "ongoing": Proposal.objects.filter(status="pending").count(),
            },
            "recent_proposals": [
                {
                    "title": p.asset_name,
                    "status": p.status,
                    "votes": p.votes.count(),
                    "date": p.created_at,
                }
                for p in Proposal.objects.all().order_by("-created_at")[:5]
            ],
            "upcoming_meetings": [
                {
                    "title": m.title,
                    "date": m.date,
                    "hosted_by": m.created_by.email,
                    "zoom_link": m.meeting_link,
                }
                for m in Meeting.objects.filter(date__gte=now).order_by("date")[:3]
            ],
            "member_health": [
                {
                    "name": u.full_name,
                    "amount": Contribution.objects.filter(user=u).aggregate(Sum("amount"))["amount__sum"] or 0,
                    "tag": "Top Performer" if i == 0 else "Active",
                }
                for i, u in enumerate(CustomUser.objects.all().order_by('-date_joined')[:5])
            ],
            "recent_reports": [
                {"title": "Monthly Performance Report", "date": (now - timedelta(days=15)).strftime("%b %d, %Y")}
            ],
        }

        return data

    def get_member_dashboard_data(self, user, now):
        last_month_date = (now - timedelta(days=30)).date()

        your_contributions = Contribution.objects.filter(user=user).aggregate(Sum("amount"))["amount__sum"] or 0
        total_contributions = Contribution.objects.aggregate(total=Sum("amount"))["total"] or 1
        ownership_percentage = round((your_contributions / total_contributions) * 100, 2)

        next_meeting = Meeting.objects.filter(date__gte=now).order_by("date").first()

        monthly_growth_sum = Contribution.objects.filter(
            month__gte=last_month_date
        ).aggregate(Sum("amount"))["amount__sum"] or 0

        monthly_growth_percent = (monthly_growth_sum / total_contributions) * 100 if total_contributions else 0

        missed_payments = 0  # Placeholder for actual payment tracking

        your_next_payment = 1000  # Example fixed monthly contribution

        # Calculate next payment due date (assuming due on 5th of each month)
        if now.day <= 5:
            days_until_due = 5 - now.day
        else:
            days_until_due = 35 - now.day  # next month's 5th day

        next_payment_due_date = (now + timedelta(days=days_until_due)).date()

        # Club growth data (monthly totals)
        monthly_data = (
            Contribution.objects.order_by('month')
            .values('month')
            .annotate(total=Sum('amount'))
        )
        club_growth_data = [
            {"month": m['month'].strftime("%b %Y"), "value": m['total']} for m in monthly_data
        ]

        # Upcoming activities
        pending_votes = Vote.objects.filter(user=user, has_voted=False).count()
        upcoming_meetings_count = Meeting.objects.filter(date__gte=now).count()

        upcoming_activities = []
        if pending_votes > 0:
            upcoming_activities.append({"title": f"Vote on {pending_votes} proposal(s)", "due": "Soon"})
        if upcoming_meetings_count > 0:
            upcoming_activities.append({"title": "Monthly Meeting", "due": "Check calendar"})

        # Recent activity (last 3 votes + last 2 contributions)
        last_votes = Vote.objects.filter(user=user).order_by("-created_at")[:3]
        last_contributions = Contribution.objects.filter(user=user).order_by("-month")[:2]

        recent_activity = []

        for vote in last_votes:
            recent_activity.append({
                "activity": f"You voted on {vote.proposal.asset_name} Proposal",
                "time": timezone.localtime(vote.created_at).strftime("%b %d, %H:%M"),
            })

        for contrib in last_contributions:
            recent_activity.append({
                "activity": "You made a contribution",
                "time": contrib.month.strftime("%b %d"),
            })

        recent_activity.sort(key=lambda x: x["time"], reverse=True)

        tip_of_the_week = "Investing is not about timing the market, but time in the market."

        return {
            "total_club_value": total_contributions,
            "monthly_growth_percent": round(monthly_growth_percent, 2),
            "your_contributions": your_contributions,
            "ownership_percentage": ownership_percentage,
            "pending_votes": pending_votes,
            "missed_payments": missed_payments,
            "your_votes": Vote.objects.filter(user=user, has_voted=True).count(),
            "next_meeting_date": next_meeting.date if next_meeting else None,
            "next_meeting_name": next_meeting.title if next_meeting else "",
            "quick_stats": {
                "total_members": CustomUser.objects.count(),
                "proposals_passed": Proposal.objects.filter(status="approved").count(),
                "avg_monthly_contribution": round(
                    Contribution.objects.filter(
                        month__gte=last_month_date
                    ).aggregate(Sum("amount"))["amount__sum"] or 0,
                    2,
                ),
            },
            "your_next_payment": your_next_payment,
            "next_payment_due_date": next_payment_due_date,
            "club_growth_data": club_growth_data,
            "upcoming_activities": upcoming_activities,
            "recent_activity": recent_activity,
            "tip_of_the_week": tip_of_the_week,
        }
