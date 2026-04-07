from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from farms.views import FarmViewSet
from scans.views import ScanViewSet
from alerts.views import AlertViewSet
from users.views import UserViewSet, RegisterView
from dashboard.views import DashboardStatsView

# Create a simple home view
def home(request):
    return JsonResponse({
        'message': 'Welcome to CacaoGuard API',
        'version': '1.0.0',
        'endpoints': {
            'Authentication': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'refresh': '/api/auth/refresh/',
            },
            'Resources': {
                'farms': '/api/farms/',
                'scans': '/api/scans/',
                'alerts': '/api/alerts/',
                'users': '/api/users/',
            },
            'Dashboard': {
                'stats': '/api/dashboard/stats/',
            },
            'Admin': '/admin/'
        }
    })

# Create router
router = DefaultRouter()
router.register(r'farms', FarmViewSet, basename='farm')
router.register(r'scans', ScanViewSet, basename='scan')
router.register(r'alerts', AlertViewSet, basename='alert')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', home, name='home'),  # Add this line for root URL
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/dashboard/stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
]