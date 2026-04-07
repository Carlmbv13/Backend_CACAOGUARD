from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Alert
from .serializers import AlertSerializer

class AlertViewSet(viewsets.ModelViewSet):
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Alert.objects.all()  # Add this line
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Alert.objects.all()
        return Alert.objects.filter(farm__owner=user)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        alert = self.get_object()
        new_status = request.data.get('status')
        
        if new_status in dict(Alert.STATUS_CHOICES):
            alert.status = new_status
            alert.save()
            return Response({
                'status': 'updated',
                'alert_id': alert.id,
                'new_status': alert.status
            })
        return Response(
            {'error': 'Invalid status. Choose from: new, acknowledged, resolved'},
            status=status.HTTP_400_BAD_REQUEST
        )