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

    class Meta:
        model = WorkOrder
        fields = [
                  'id',
                  'maintenance_request',
                  'assigned_technician',
                  'work_description',
                  'date_started',
                  'date_completed',
                  'status',
                  ]

class StaffMaintenanceHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MaintenanceHistory
        fields = ['asset',
                  'work_order',
                  'remarks',
                  'completed_by',
                  'timestamp',]

class ManagerMaintenanceHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MaintenanceHistory
        fields = ['asset',
                  'work_order',
                  'maintenance_cost',
                  'remarks',
                  'completed_by',
                  'timestamp',]