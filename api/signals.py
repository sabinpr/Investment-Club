from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import Notification, Proposal, Vote, Meeting
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger('api')

User = get_user_model()

@receiver(post_save, sender=Proposal)
def notify_proposal_creation(sender, instance, created, **kwargs):
    if created:
        # Notify all users about the new proposal
        users = User.objects.all()
        for user in users:
            Notification.objects.create(
                user=user,
                title="New Proposal Created",
                message=f"A new proposal titled '{instance.title}' has been created.",
                notification_type='proposal',
                related_url=f"/proposals/{instance.id}/"
            )
            logger.info(f"Notification created for user {user.email} regarding proposal {instance.id}")


@receiver(post_save, sender=Vote)
def notify_vote_cast(sender, instance, created, **kwargs):
    if created:
        # Notify the proposal creator about the new vote
        proposal = instance.proposal
        if proposal and proposal.creator:
            Notification.objects.create(
                user=proposal.creator,
                title="New Vote Cast",
                message=f"A new vote has been cast on your proposal titled '{proposal.title}'.",
                notification_type='vote',
                related_url=f"/proposals/{proposal.id}/"
            )
            logger.info(f"Notification created for user {proposal.creator.email} regarding vote on proposal {proposal.id}")


@receiver(post_save, sender=Meeting)
def notify_meeting_creation(sender, instance, created, **kwargs):
    if created:
        # Notify all users about the new meeting
        users = User.objects.all()
        for user in users:
            Notification.objects.create(
                user=user,
                title="New Meeting Scheduled",
                message=f"A new meeting titled '{instance.title}' has been scheduled.",
                notification_type='system',
                related_url=f"/meetings/{instance.id}/"
            )
            logger.info(f"Notification created for user {user.email} regarding meeting {instance.id}")