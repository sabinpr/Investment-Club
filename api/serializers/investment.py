from rest_framework import serializers
from api.models import Investment, AssetInvestment
from drf_spectacular.utils import extend_schema_field

class InvestmentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    proposal_name = serializers.CharField(source='proposal.asset_name', read_only=True)
    invested_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Investment
        fields = ['id', 'user_email', 'proposal_name', 'amount', 'invested_at']

class AssetInvestmentSerializer(serializers.ModelSerializer):
    total_return = serializers.SerializerMethodField()
    return_percentage = serializers.SerializerMethodField()
    date_invested = serializers.DateField(read_only=True)

    class Meta:
        model = AssetInvestment
        fields = [
            'id', 'name', 'type', 'quantity', 'current_value',
            'invested_value', 'date_invested',
            'total_return', 'return_percentage'
        ]

    @extend_schema_field(float)
    def get_total_return(self, obj):
        return obj.total_return()

    @extend_schema_field(float)
    def get_return_percentage(self, obj):
        return obj.return_percentage()

     
class ManualUpdateInvestmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    current_value = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate_id(self, value):
        if not AssetInvestment.objects.filter(id=value).exists():
            raise serializers.ValidationError("AssetInvestment with this ID does not exist.")
        return value

    

class OwnershipShareSerializer(serializers.Serializer):
    user = serializers.CharField()
    your_total = serializers.FloatField()
    club_total = serializers.FloatField()
    ownership_percent = serializers.FloatField()

