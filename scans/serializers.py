from rest_framework import serializers
from .models import Scan

class ScanSerializer(serializers.ModelSerializer):
    farm_name = serializers.ReadOnlyField(source='farm.name')
    
    class Meta:
        model = Scan
        fields = ['id', 'farm', 'farm_name', 'zone_name', 'date', 'severity', 
                  'confidence', 'affected_area', 'image', 'created_at']
        read_only_fields = ['date', 'created_at']