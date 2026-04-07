from rest_framework import viewsets, permissions
from .models import Farm
from .serializers import FarmSerializer

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.owner == request.user

class FarmViewSet(viewsets.ModelViewSet):
    serializer_class = FarmSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    queryset = Farm.objects.all() 
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Farm.objects.all()
        return Farm.objects.filter(owner=user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)