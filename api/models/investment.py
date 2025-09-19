from django.db import models
from .user import CustomUser
from .proposal import Proposal


class Investment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='investments')
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name='investments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    invested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'proposal')

    def __str__(self):
        return f"{self.user.username} invested Rs. {self.amount} in {self.proposal.asset_name}"


class AssetInvestment(models.Model):
    TYPE_CHOICES = [
        ('MUTUAL', 'Mutual Fund'),
        ('GOLD', 'Digital Gold'),
        ('STOCK', 'NEPSE Stock'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    quantity = models.FloatField()
    current_value = models.DecimalField(max_digits=12, decimal_places=2)
    invested_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_invested = models.DateField(auto_now_add=True)


    def total_return(self):
        return float(self.current_value) - float(self.invested_value)

    def return_percentage(self):
        if self.invested_value:
            return (float(self.total_return()) / float(self.invested_value)) * 100
        return 0

    def __str__(self):
        return f"{self.name} ({self.type})"
