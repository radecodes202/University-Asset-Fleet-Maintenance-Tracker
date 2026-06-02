from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('requests/', views.MaintenanceRequestListCreateView.as_view(), name='request-list'),
    path('requests/<int:pk>/', views.MaintenanceRequestDetailView.as_view(), name='request-detail'),
    path('requests/bulk-update/', views.BulkUpdateRequestStatusView.as_view(), name='request-bulk-update'),
    path('workorders/', views.WorkOrderListCreateView.as_view(), name='workorder-list'),
    path('workorders/<int:pk>/', views.WorkOrderDetailView.as_view(), name='workorder-detail'),
    path('history/', views.MaintenanceHistoryListView.as_view(), name='history-list'),
    path('history-export-csv/', views.export_maintenance_history_csv, name='history-export-csv'),
    path('technicians/', views.TechnicianListView.as_view(), name='technician-list'),
    path('requests/page/', views.requests_page, name='requests'),
    path('workorders/page/', views.workorders_page, name='workorders'),
    path('history/page/', views.history_page, name='history'),
]
