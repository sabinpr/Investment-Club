from django.db import models
from django.utils import timezone
from datetime import timedelta
from .user import CustomUser


def get_default_deadline():
    return timezone.now() + timedelta(days=7)


class Proposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('expired', 'Expired'),
        ('rejected', 'Rejected'),
    ]

    RISK_CHOICES = [
        ('very_high', 'Very High'),
        ('high', 'High'),
        ('moderate', 'Moderate'),
        ('low', 'Low'),
    ]

    proposer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='proposals')
    asset_name = models.CharField(max_length=255)
    reason = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    expected_return_percentage = models.FloatField(help_text="E.g. 18 for 18%")
    return_duration_months = models.PositiveIntegerField(help_text="Duration of return in months")
    risk_level = models.CharField(max_length=20, choices=RISK_CHOICES)
    deadline = models.DateTimeField(default=get_default_deadline, help_text="Deadline for voting")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.ManyToManyField(CustomUser, through='Vote', related_name='proposal_votes')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def vote_progress(self):
        total_votes = self.vote_set.count()
        total_members = CustomUser.objects.filter(role='member').count()
        return round((total_votes / total_members) * 100, 2) if total_members else 0

    def count_votes(self):
        yes = self.vote_set.filter(vote=True).count()
        no = self.vote_set.filter(vote=False).count()
        return yes, no
    
    def approve(self):
        if self.status in ['approved', 'expired', 'rejected']:
            return

        now = timezone.now()
        if self.deadline < now:
            self.status = 'expired'
            self.save(update_fields=['status'])
            return
        
        yes_votes, no_votes = self.count_votes()
        
        total_votes = yes_votes + no_votes
        total_members = CustomUser.objects.filter(role='member').count()

        minimum_yes_votes = total_members // 2 + 1  # we can set a threshold here if needed according to desired logic

        if total_votes >= minimum_yes_votes:
            if yes_votes > no_votes:
                self.status = 'approved'
            else:
                self.status = 'rejected'
            self.save(update_fields=['status'])

    def is_approved(self):
        return self.status == 'approved'
    
    def has_user_voted(self, user):
        return self.vote_set.filter(voter=user).exists()

    def __str__(self):
        return f"{self.asset_name} ({self.amount}) - {self.status}"


    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
