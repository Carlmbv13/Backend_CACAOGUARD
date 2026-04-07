from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role')
    is_active_profile = serializers.BooleanField(source='profile.is_active')
    phone = serializers.CharField(source='profile.phone', required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'role', 'is_active_profile', 'phone', 'date_joined']
        read_only_fields = ['date_joined']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, default='Farmer')
    phone = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name', 'role', 'phone']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        role = validated_data.pop('role')
        phone = validated_data.pop('phone', '')
        validated_data.pop('password2')
        
        user = User.objects.create_user(**validated_data)
        user.profile.role = role
        user.profile.phone = phone
        user.profile.save()
        
        return user