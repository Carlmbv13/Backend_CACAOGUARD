from rest_framework import serializers
from .models import Farm

class FarmSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Farm
        fields = ['id', 'name', 'owner', 'owner_name', 'location', 'size_hectares', 
                  'health_score', 'risk_level', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']