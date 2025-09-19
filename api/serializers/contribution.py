from rest_framework import serializers
from api.models import Contribution

class ContributionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Contribution
        fields = ['id', 'user', 'amount', 'month']
