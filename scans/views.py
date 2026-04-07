from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Scan
from .serializers import ScanSerializer
from alerts.models import Alert

class ScanViewSet(viewsets.ModelViewSet):
    serializer_class = ScanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['farm', 'severity']
    queryset = Scan.objects.all()  # Add this line
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Scan.objects.all()
        return Scan.objects.filter(farm__owner=user)
    
    def perform_create(self, serializer):
        scan = serializer.save()
        farm = scan.farm
        
        # Update farm health score based on scan severity
        severity_scores = {'Healthy': 0, 'Mild': 20, 'Moderate': 50, 'Severe': 80}
        score_reduction = severity_scores.get(scan.severity, 0)
        new_health_score = max(0, farm.health_score - score_reduction)
        
        # Update risk level
        if new_health_score >= 70:
            risk_level = 'Low'
        elif new_health_score >= 40:
            risk_level = 'Medium'
        elif new_health_score >= 20:
            risk_level = 'High'
        else:
            risk_level = 'Critical'
        
        farm.health_score = new_health_score
        farm.risk_level = risk_level
        farm.save()
        
        # Create alert based on severity
        if scan.severity == 'Severe':
            Alert.objects.create(
                farm=farm,
                severity='critical',
                message=f"⚠️ CRITICAL: Severe Black Pod Disease detected in {scan.zone_name}. Affected area: {scan.affected_area} m². Immediate action required!",
                status='new'
            )
        elif scan.severity == 'Moderate':
            Alert.objects.create(
                farm=farm,
                severity='warning',
                message=f"⚠️ WARNING: Moderate infection detected in {scan.zone_name}. Affected area: {scan.affected_area} m². Treatment recommended.",
                status='new'
            )