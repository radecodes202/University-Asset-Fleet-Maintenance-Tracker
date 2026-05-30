from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    can_view_costs = serializers.BooleanField(read_only=True)
    can_approve_requests = serializers.BooleanField(read_only=True)
    is_read_only = serializers.BooleanField(read_only=True)

    class Meta:
        model = User

        fields = ['id', 'email', 'first_name', 'last_name', 'employee_id', 'department', 'role', 'can_view_costs', 'can_approve_requests', 'is_read_only']