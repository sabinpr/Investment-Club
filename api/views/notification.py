import logging
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import Notification
from api.serializers.notification import NotificationSerializer
from django.contrib.auth import get_user_model
from api.permissions import IsAdminOrReadOnly
from django.shortcuts import get_object_or_404

User = get_user_model()

logger = logging.getLogger('api')

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def get_object(self):
        return get_object_or_404(Notification, pk=self.kwargs['pk'], user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        logger.debug(f"Fetching notifications for user: {user.email}")
        return self.queryset.filter(user=user)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        unread_notifications = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(unread_notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=["is_read"])
        logger.info(f"Notification {notification.id} marked as read for user {request.user.email}")
        return Response({'status': 'Notification marked as read'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        unread_notifications = self.get_queryset().filter(is_read=False)
        unread_notifications.update(is_read=True)
        return Response({'status': 'All notifications marked as read'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def count_unread(self, request):
        unread_count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': unread_count}, status=status.HTTP_200_OK)