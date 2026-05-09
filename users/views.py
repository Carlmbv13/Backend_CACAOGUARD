# users/views.py
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime

from .serializers import UserSerializer, RegisterSerializer, CustomTokenObtainPairSerializer
from .models import UserProfile
from .email_utils import is_verification_token_valid


# Use custom token view
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    
    @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    """Verify user email with token"""
    permission_classes = [AllowAny]
    
    def get(self, request, token):
        try:
            # Find user with this verification token
            user = User.objects.get(profile__email_verification_token=token)
            
            # Check if token is still valid
            if is_verification_token_valid(user.profile):
                # Activate user account
                user.is_active = True
                user.profile.email_verified = True
                user.save()
                user.profile.save()
                
                return Response({
                    'success': True,
                    'message': 'Email verified successfully! You can now login.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Verification link has expired. Please register again.'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Invalid verification token.'
            }, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationEmailView(APIView):
    """Resend verification email"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email, is_active=False)
            from .email_utils import send_verification_email
            success = send_verification_email(user, request)
            
            if success:
                return Response({
                    'success': True,
                    'message': 'Verification email resent. Please check your inbox.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Failed to send email. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User not found or already verified.'
            }, status=status.HTTP_404_NOT_FOUND)


class TestEmailView(APIView):
    """Test email functionality endpoint"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({
                'error': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            send_mail(
                subject='CacaoGuard Email Test',
                message=f'This is a test email from CacaoGuard.\n\nSent to: {email}\nTime: {datetime.now()}',
                from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            
            return Response({
                'success': True,
                'message': f'Test email sent to {email}',
                'email': email,
                'backend': str(settings.EMAIL_BACKEND).split('.')[-1]
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Failed to send email: {str(e)}',
                'email': email,
                'error_type': type(e).__name__
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)