from django.db import models
from django.conf import settings
from api.models import Proposal

class MeetingTag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Meeting(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('captured', 'Captured'),
    )

    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    agenda = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    meeting_link = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    tags = models.ManyToManyField(MeetingTag, blank=True)
    proposal = models.ForeignKey(Proposal, on_delete=models.SET_NULL, null=True, blank=True, related_name="meetings")
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="hosted_meetings")

    def __str__(self):
        return self.title
