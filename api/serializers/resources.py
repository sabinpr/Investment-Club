from rest_framework import serializers
from api.models import EducationalResources

class EducationalResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalResources
        fields = ['id', 'title', 'description', 'url', 'created_at', 'updated_at']