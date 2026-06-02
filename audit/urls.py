from django.urls import path
from .views import AuditLogListView, AuditLogDetailView, audit_logs_page, export_audit_logs_csv

app_name = 'audit'

urlpatterns = [
    path('logs/', audit_logs_page, name='logs-page'),
    path('export-csv/', export_audit_logs_csv, name='export-csv'),
    path('', AuditLogListView.as_view(), name='auditlog-list'),
    path('<int:pk>/', AuditLogDetailView.as_view(), name='auditlog-detail'),
]