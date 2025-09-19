from rest_framework import serializers
from api.models import Notification
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.timesince import timesince
from drf_spectacular.utils import extend_schema_field


User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    time_since_created = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'title',
            'message',
            'notification_type',
            'is_read',
            'created_at',
            'related_url',
            'time_since_created'
        ]
        read_only_fields = ['id', 'created_at']
        
    @extend_schema_field(str)
    def get_time_since_created(self, obj):
        return timesince(obj.created_at, timezone.now())

