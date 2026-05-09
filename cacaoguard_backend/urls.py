from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

# Import your views
from farms.views import FarmViewSet
from scans.views import ScanViewSet
from alerts.views import AlertViewSet
from users.views import (
    UserViewSet, 
    RegisterView, 
    CustomTokenObtainPairView,
    VerifyEmailView,           # ← ADD THIS
    ResendVerificationEmailView,  # ← ADD THIS
    TestEmailView              # ← ADD THIS
)
from dashboard.views import DashboardStatsView

# Create router
router = DefaultRouter()
router.register(r'farms', FarmViewSet, basename='farm')
router.register(r'scans', ScanViewSet, basename='scan')
router.register(r'alerts', AlertViewSet, basename='alert')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # Authentication endpoints
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Email verification endpoints
    path('api/verify-email/<uuid:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('api/resend-verification/', ResendVerificationEmailView.as_view(), name='resend-verification'),
    
    # Test email endpoint
    path('api/test-email/', TestEmailView.as_view(), name='test-email'),
    
    # Dashboard stats
    path('api/dashboard/stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
]