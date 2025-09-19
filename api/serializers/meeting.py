from rest_framework import serializers
from api.models import Meeting, MeetingTag
from django.contrib.auth import get_user_model
from api.serializers import ProposalSerializer 

User = get_user_model()

class MeetingTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingTag
        fields = ['id', 'name']

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email'] 

class MeetingSerializer(serializers.ModelSerializer):
    tags = MeetingTagSerializer(many=True, read_only=True)
    proposal = ProposalSerializer(read_only=True)
    host = HostSerializer(read_only=True)

    class Meta:
        model = Meeting
        fields = [
            'id', 'title', 'date', 'agenda', 'status',
            'meeting_link', 'location', 'tags',
            'proposal', 'host'
        ]
