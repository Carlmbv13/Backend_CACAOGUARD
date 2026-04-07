from rest_framework import serializers
from .models import Alert

class AlertSerializer(serializers.ModelSerializer):
    farm_name = serializers.ReadOnlyField(source='farm.name')
    
    class Meta:
        model = Alert
        fields = ['id', 'farm', 'farm_name', 'severity', 'message', 
                  'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']