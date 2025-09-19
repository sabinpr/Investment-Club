from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.models import Meeting
from api.serializers import MeetingSerializer

class MeetingListCreateView(generics.ListCreateAPIView):
    queryset = Meeting.objects.all().order_by('date')
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)
