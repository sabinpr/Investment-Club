from django.db import models
from .proposal import Proposal
from .user import CustomUser

class Vote(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name='vote_set')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='votes')
    vote = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('proposal', 'user')

    def __str__(self):
        return f"{self.user.username} voted {'Yes' if self.vote else 'No'} on {self.proposal.asset_name}"
