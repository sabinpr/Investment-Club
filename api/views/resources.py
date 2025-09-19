from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAdminOrReadOnly
from api.serializers import EducationalResourcesSerializer
from api.models import EducationalResources


class EducationalResourcesView(ListCreateAPIView):
    queryset = EducationalResources.objects.all()
    serializer_class = EducationalResourcesSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
