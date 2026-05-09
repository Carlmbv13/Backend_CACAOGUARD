# users/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, default='Farmer')
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name', 'role']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Check if email already exists
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})
        
        return attrs
    
    def create(self, validated_data):
        role = validated_data.pop('role')
        validated_data.pop('password2')
        
        # Create user with is_active=False until email verified
        user = User.objects.create_user(**validated_data, is_active=False)
        
        # Set role
        user.profile.role = role
        user.profile.save()
        
        # Send verification email (need request from context)
        request = self.context.get('request')
        if request:
            from .email_utils import send_verification_email
            send_verification_email(user, request)
        
        return user


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role')
    is_active_profile = serializers.BooleanField(source='profile.is_active')
    email_verified = serializers.BooleanField(source='profile.email_verified', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active_profile', 'email_verified', 'date_joined']
        read_only_fields = ['date_joined']


# Custom JWT Token Serializer with email verification check
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        if not user.is_active:
            raise serializers.ValidationError('Account not activated. Please verify your email.')
        
        # Check if email is verified
        if hasattr(user, 'profile') and not user.profile.email_verified:
            raise serializers.ValidationError('Email not verified. Please check your inbox.')
        
        return super().validate(attrs)