
from django.shortcuts import render
import csv
from django.http import HttpResponse
from datetime import datetime

# Create your views here.

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import AuditLog
from .serializers import AuditLogSerializer
from accounts.permissions import IsManagerOrAuditor
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def audit_logs_page(request):
    if not (request.user.is_manager or request.user.is_auditor):
        return render(request, 'dashboard/403.html', status=403)
    return render(request, 'audit/logs.html')

@login_required
def export_audit_logs_csv(request):
    """Export audit logs to CSV"""
    if not (request.user.is_manager or request.user.is_auditor):
        return HttpResponse('Unauthorized', status=403)
    
    # Create response object
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="audit_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    # Create CSV writer
    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'User', 'Action', 'Model', 'Object ID', 'Object Display', 'Old Values', 'New Values', 'IP Address'])
    
    # Get all audit logs
    logs = AuditLog.objects.select_related('user').all().order_by('-timestamp')
    
    for log in logs:
        writer.writerow([
            log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            log.user.email if log.user else 'Unknown',
            log.action,
            log.model_name,
            log.object_id,
            log.object_display,
            log.old_values,
            log.new_values,
            log.ip_address,
        ])
    
    return response

class AuditLogListView(generics.ListAPIView):
    permission_classes = [IsManagerOrAuditor]
    serializer_class = AuditLogSerializer
    pagination_class = None

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    
    filterset_fields = ['action', 'model_name', 'user', 'timestamp']
    search_fields = ['object_id', 'object_display', 'user__email', 'ip_address']
    ordering_fields = ['timestamp', 'action', 'model_name', 'user']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        return AuditLog.objects.select_related('user').all()


class AuditLogDetailView(generics.RetrieveAPIView):
    permission_classes = [IsManagerOrAuditor]
    serializer_class = AuditLogSerializer
    queryset = AuditLog.objects.all()