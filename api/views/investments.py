from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.db.models import Sum

from api.models import Investment, AssetInvestment, Contribution
from api.serializers import InvestmentSerializer, AssetInvestmentSerializer, ManualUpdateInvestmentSerializer, OwnershipShareSerializer
from api.permissions import IsAdminOrSuperAdmin, IsAdminOrReadOnly


class AssetInvestmentListCreateView(generics.ListCreateAPIView):
    queryset = AssetInvestment.objects.all()
    serializer_class = AssetInvestmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class InvestmentListCreateView(generics.ListCreateAPIView):
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.role == 'superadmin':
            return Investment.objects.all()
        return Investment.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class ManualUpdateInvestmentView(GenericAPIView):
    permission_classes = [IsAdminOrSuperAdmin]
    serializer_class = ManualUpdateInvestmentSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        investment_id = serializer.validated_data["id"]
        new_value = serializer.validated_data["current_value"]

        investment = get_object_or_404(AssetInvestment, id=investment_id)
        investment.current_value = new_value
        investment.save()

        return Response(AssetInvestmentSerializer(investment).data, status=status.HTTP_200_OK)



class OwnershipShareView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OwnershipShareSerializer

    def get(self, request):
        total_all = Contribution.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0')
        total_user = Contribution.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        if total_all == 0:
            share = Decimal("0")
        else:
            share = (total_user / total_all) * Decimal("100")

        data = {
            "user": request.user.username,
            "your_total": round(total_user, 2),
            "club_total": round(total_all, 2),
            "ownership_percent": round(share, 2),
        }
        serializer = self.get_serializer(instance=data)
        return Response(serializer.data, status=status.HTTP_200_OK)