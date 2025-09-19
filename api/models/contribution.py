from django.db import models
from .user import CustomUser

class Contribution(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=2000.00)
    month = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.month} - Rs. {self.amount}"
