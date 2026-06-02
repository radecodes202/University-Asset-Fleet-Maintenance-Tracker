from rest_framework import serializers
from .models import MaintenanceRequest, WorkOrder, MaintenanceHistory
from assets.serializers import StaffAssetSerializer
from assets.models import Asset

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    asset        = StaffAssetSerializer(read_only=True)
    asset_id     = serializers.PrimaryKeyRelatedField(
                        queryset=Asset.objects.all(),
                        source='asset',
                        write_only=True
                    )

    class Meta:
        model = MaintenanceRequest
        fields = [
            'id',
            'asset',
            'asset_id',
            'requested_by',
            'problem_description',
            'date_requested',
            'status',
            'manager_notes',
            'date_resolved',
        ]

class WorkOrderSerializer(serializers.ModelSerializer):

    # Human-readable name of the assigned technician. Read-only.
    assigned_technician_name = serializers.SerializerMethodField()

    class Meta:
        model = WorkOrder
        fields = [
                  'id',
                  'maintenance_request',
                  'assigned_technician',
                  'assigned_technician_name',
                  'work_description',
                  'date_started',
                  'date_completed',
                  'status',
                  ]

    def get_assigned_technician_name(self, obj):
        tech = obj.assigned_technician
        if not tech:
            return None
        full = tech.get_full_name().strip()
        return full or tech.email

class StaffMaintenanceHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MaintenanceHistory
        fields = [
                  'id',
                  'asset',
                  'work_order',
                  'remarks',
                  'completed_by',
                  'timestamp',]

class ManagerMaintenanceHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MaintenanceHistory
        fields = [
                  'id',
                  'asset',
                  'work_order',
                  'maintenance_cost',
                  'remarks',
                  'completed_by',
                  'timestamp',]
