from rest_framework import serializers


class MemberDashboardSerializer(serializers.Serializer):
    total_club_value = serializers.DecimalField(max_digits=12, decimal_places=2)
    monthly_growth_percent = serializers.FloatField()
    your_contributions = serializers.DecimalField(max_digits=12, decimal_places=2)
    ownership_percentage = serializers.FloatField()
    pending_votes = serializers.IntegerField()
    missed_payments = serializers.IntegerField()
    your_votes = serializers.IntegerField()
    next_meeting_date = serializers.DateTimeField()
    next_meeting_name = serializers.CharField()
    quick_stats = serializers.DictField()  
    your_next_payment = serializers.DecimalField(max_digits=10, decimal_places=2)
    next_payment_due_date = serializers.DateField()
    club_growth_data = serializers.ListField() 
    upcoming_activities = serializers.ListField()  
    recent_activity = serializers.ListField()
    tip_of_the_week = serializers.CharField()


class AdminDashboardSerializer(serializers.Serializer):
    total_club_value = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_assets = serializers.IntegerField()
    monthly_growth_percent = serializers.FloatField()
    pending_actions = serializers.ListField()
    avg_monthly_contribution = serializers.DecimalField(max_digits=10, decimal_places=2)
    monthly_contribution_graph = serializers.ListField()
    voting_summary = serializers.DictField()
    recent_proposals = serializers.ListField()
    upcoming_meetings = serializers.ListField()
    member_health = serializers.ListField()
    recent_reports = serializers.ListField()
