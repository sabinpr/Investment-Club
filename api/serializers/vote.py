from rest_framework import serializers
from api.models import Vote

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'proposal', 'user', 'vote']
        read_only_fields = ['user', 'proposal']

    def validate_vote(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("Vote must be a boolean value (true or false).")
        return value

    def validate(self, attrs):
        proposal = self.context['proposal']
        user = self.context['user']

        if Vote.objects.filter(proposal=proposal, user=user).exists():
            raise serializers.ValidationError("You have already voted on this proposal.")
        
        if proposal.status != 'pending':
            raise serializers.ValidationError("Voting is closed for this proposal.")

        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['user']
        validated_data['proposal'] = self.context['proposal']

        vote = Vote.objects.create(**validated_data)
        return vote
