from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Proposal, Meeting

User = get_user_model()

@shared_task
def expire_old_proposals():
    proposals = Proposal.objects.filter(status='pending', deadline__lt=timezone.now())
    members = User.objects.filter(role='member')
    emails = list(members.values_list('email', flat=True))

    for proposal in proposals:
        previous_status = proposal.status
        proposal.approve()

        # If it got marked as expired just now, send an email
        if proposal.status == 'expired' and previous_status != 'expired':
            send_mail(
                subject=f'Proposal Expired: {proposal.asset_name}',
                message=f'The proposal "{proposal.asset_name}" has expired without enough votes.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails,
                fail_silently=False,
            )


@shared_task
def send_meeting_reminders():
    now = timezone.now()
    reminder_time = now + timedelta(hours=24)
    start_time = reminder_time - timedelta(minutes=30)
    end_time = reminder_time + timedelta(minutes=30)
    meetings = Meeting.objects.filter(date__range=(start_time, end_time))

    emails = list(User.objects.filter(role='member').values_list('email', flat=True))

    for meeting in meetings:
        msg = (
            f"📅 Reminder:\n"
            f"🕓 Meeting on {meeting.date.strftime('%Y-%m-%d %H:%M')}\n"
            f"📝 Agenda: {meeting.agenda}"
        )
        if meeting.zoom_link:
            msg += f"\n🔗 Zoom: {meeting.zoom_link}"


        send_mail(
            subject="Meeting Reminder",
            message=msg,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=emails,
            fail_silently=False,
        )


@shared_task
def test_celery_task():
    print("✅ Celery task is running!")
    return "Task completed"