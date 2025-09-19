from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from api.models import Proposal

class ProposalSerializer(serializers.ModelSerializer):
    proposer = serializers.ReadOnlyField(source='proposer.email')
    vote_count = serializers.SerializerMethodField(read_only=True)
    vote_progress = serializers.SerializerMethodField(read_only=True)
    is_approved = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Proposal
        fields = [
            'id', 'proposer', 'asset_name', 'amount', 'reason',
            'expected_return_percentage', 'return_duration_months', 'risk_level', 'deadline',
            'created_at', 'vote_count', 'vote_progress', 'is_approved', 'status'
        ]
        read_only_fields = ['created_at', 'vote_count', 'vote_progress', 'is_approved', 'status']

    @extend_schema_field(serializers.IntegerField())
    def get_vote_count(self, obj):
        return obj.vote_set.count()

    @extend_schema_field(serializers.FloatField())
    def get_vote_progress(self, obj):
        return obj.vote_progress()

    @extend_schema_field(serializers.BooleanField())
    def get_is_approved(self, obj):
        return obj.is_approved()
