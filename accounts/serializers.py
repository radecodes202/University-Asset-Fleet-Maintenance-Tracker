from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, Role


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer that uses email instead of username.
    SimpleJWT's default serializer expects 'username', but our User model
    uses email as the USERNAME_FIELD.
    """
    username_field = 'email'


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer for creating new users (Manager only)"""
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'employee_id', 'department', 'role']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            employee_id=validated_data.get('employee_id'),
            department=validated_data.get('department'),
            role=validated_data.get('role', Role.STAFF)
        )
        return user


class UserManagementSerializer(serializers.ModelSerializer):
    """Serializer for viewing and managing users"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'employee_id', 'department', 'role', 'is_active', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def get_full_name(self, obj):
        return obj.get_full_name()