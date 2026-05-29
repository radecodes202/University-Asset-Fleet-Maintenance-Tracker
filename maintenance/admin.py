from django.contrib import admin
from .models import MaintenanceRequest, WorkOrder, MaintenanceHistory

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display  = ('asset', 'requested_by', 'status', 'date_requested')
    list_filter   = ('status',)
    search_fields = ('asset__asset_name', 'problem_description')

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display  = ('__str__', 'assigned_technician', 'status', 'date_started', 'date_completed')
    list_filter   = ('status',)
    search_fields = ('work_description',)

@admin.register(MaintenanceHistory)
class MaintenanceHistoryAdmin(admin.ModelAdmin):
    list_display  = ('asset', 'maintenance_cost', 'completed_by', 'timestamp')
    search_fields = ('asset__asset_name', 'remarks')