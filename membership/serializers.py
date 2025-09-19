from rest_framework import serializers
from .models import MembershipRequest

class MembershipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipRequest
        fields = '__all__'
        read_only_fields = ('requested_at', 'responded_at', 'status')
        

class MembershipRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipRequest
        fields = ('full_name', 'email', 'phone', 'document', 'picture', 'note')