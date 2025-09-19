from rest_framework import generics, filters, status, serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime
import csv

from api.models import Contribution
from api.serializers import ContributionSerializer
from api.permissions import IsAdminOrMemberGetPostOnly

class ContributionListCreateView(generics.ListCreateAPIView):
    serializer_class = ContributionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrMemberGetPostOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['month', 'amount']
    ordering = ['-month']

    def get_queryset(self):
        user = self.request.user
        queryset = Contribution.objects.filter(user=user)

        month = self.request.query_params.get('month')
        if month:
            try:
                month_start = datetime.strptime(month, '%Y-%m')
                if month_start.month == 12:
                    month_end = datetime(month_start.year + 1, 1, 1)
                else:
                    month_end = datetime(month_start.year, month_start.month + 1, 1)
                queryset = queryset.filter(month__gte=month_start, month__lt=month_end)
            except ValueError:
                pass
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EmptySerializer(serializers.Serializer):
    pass

class ContributionCSVExportView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    def get(self, request):
        contributions = Contribution.objects.filter(user=request.user)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="contributions.csv"'

        writer = csv.writer(response)
        writer.writerow(['Month', 'Amount'])

        for c in contributions:
            writer.writerow([c.month.strftime('%Y-%m'), c.amount])

        return response
