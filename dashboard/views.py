from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg, Q
from farms.models import Farm
from scans.models import Scan
from alerts.models import Alert

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Filter based on user role
        if user.is_staff:
            farms = Farm.objects.all()
            scans = Scan.objects.all()
            alerts = Alert.objects.all()
        else:
            farms = Farm.objects.filter(owner=user)
            scans = Scan.objects.filter(farm__owner=user)
            alerts = Alert.objects.filter(farm__owner=user)
        
        # Calculate statistics
        total_farms = farms.count()
        total_scans = scans.count()
        total_alerts = alerts.count()
        active_alerts = alerts.filter(status='new').count()
        critical_alerts = alerts.filter(severity='critical', status='new').count()
        
        avg_health_score = farms.aggregate(Avg('health_score'))['health_score__avg'] or 0
        
        # Risk breakdown
        risk_breakdown = {
            'Low': farms.filter(risk_level='Low').count(),
            'Medium': farms.filter(risk_level='Medium').count(),
            'High': farms.filter(risk_level='High').count(),
            'Critical': farms.filter(risk_level='Critical').count(),
        }
        
        # Severity breakdown
        severity_breakdown = {
            'Healthy': scans.filter(severity='Healthy').count(),
            'Mild': scans.filter(severity='Mild').count(),
            'Moderate': scans.filter(severity='Moderate').count(),
            'Severe': scans.filter(severity='Severe').count(),
        }
        
        # Recent alerts (last 5)
        recent_alerts = AlertSerializer(alerts[:5], many=True).data
        
        stats = {
            'total_farms': total_farms,
            'total_scans': total_scans,
            'total_alerts': total_alerts,
            'active_alerts': active_alerts,
            'critical_alerts': critical_alerts,
            'avg_health_score': round(avg_health_score, 2),
            'risk_breakdown': risk_breakdown,
            'severity_breakdown': severity_breakdown,
            'recent_alerts': recent_alerts,
        }
        
        return Response(stats)

# Import for recent_alerts
from alerts.serializers import AlertSerializer