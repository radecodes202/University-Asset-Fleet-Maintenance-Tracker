from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    can_view_costs = serializers.BooleanField(read_only=True)
    can_approve_requests = serializers.BooleanField(read_only=True)
    is_read_only = serializers.BooleanField(read_only=True)

    class Meta:
        model = User

        fields = ['id',
                  'email', 
                  'first_name', 
                  'last_name', 
                  'employee_id', 
                  'department', 
                  'role', 
                  'can_view_costs', 
                  'can_approve_requests', 
                  'is_read_only']

class UserManagementSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'employee_id',
            'department',
            'role',
            'is_active',
            'full_name',
        ]

    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_full_name()

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'employee_id',
            'department',
            'role',
            'password',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user