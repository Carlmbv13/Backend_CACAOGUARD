# users/urls.py
from django.urls import path
from .views import (
    RegisterView, 
    CustomTokenObtainPairView,
    UserViewSet,
    VerifyEmailView,
    ResendVerificationEmailView,
    TestEmailView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('verify-email/<uuid:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification/', ResendVerificationEmailView.as_view(), name='resend-verification'),
    path('test-email/', TestEmailView.as_view(), name='test-email'),
]

# For ViewSet (users list - admin only)
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')