from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from assets.models import Asset
from maintenance.models import MaintenanceRequest, WorkOrder, MaintenanceHistory
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone


@login_required(login_url='/login/')
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')


@login_required(login_url='/login/')
def userguide_view(request):
    return render(request, 'dashboard/userguide.html')


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        total_assets      = Asset.objects.count()
        pending_requests  = MaintenanceRequest.objects.filter(
                                status=MaintenanceRequest.Status.PENDING
                            ).count()
        completed_repairs = MaintenanceRequest.objects.filter(
                                status=MaintenanceRequest.Status.COMPLETED
                            ).count()
        under_maintenance = Asset.objects.filter(
                                current_status=Asset.Status.UNDER_MAINTENANCE
                            ).count()

        data = {
            'total_assets':      total_assets,
            'pending_requests':  pending_requests,
            'completed_repairs': completed_repairs,
            'under_maintenance': under_maintenance,
        }

        if user.is_manager:
            total_cost = MaintenanceHistory.objects.aggregate(
                Sum('maintenance_cost')
            )['maintenance_cost__sum'] or 0
            data['total_maintenance_cost'] = total_cost

        return Response(data)


class RecentActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get recent maintenance activity"""
        user = request.user
        
        # Get recent maintenance requests (last 7 days)
        recent_requests = MaintenanceRequest.objects.select_related(
            'asset', 'requested_by'
        ).order_by('-date_requested')[:5]
        
        # Get recent work orders (last 7 days)
        recent_workorders = WorkOrder.objects.select_related(
            'maintenance_request__asset', 'assigned_technician'
        ).order_by('-date_started')[:5]
        
        # Get recent completed maintenance (last 7 days)
        recent_history = MaintenanceHistory.objects.select_related(
            'asset', 'work_order', 'completed_by'
        ).order_by('-timestamp')[:5]

        requests_data = []
        for req in recent_requests:
            requests_data.append({
                'id': req.id,
                'asset_name': req.asset.asset_name,
                'status': req.status,
                'date_requested': req.date_requested.isoformat(),
                'type': 'request'
            })

        workorders_data = []
        for wo in recent_workorders:
            workorders_data.append({
                'id': wo.id,
                'asset_name': wo.maintenance_request.asset.asset_name,
                'status': wo.status,
                'date_started': wo.date_started.isoformat() if wo.date_started else None,
                'type': 'workorder'
            })

        history_data = []
        for hist in recent_history:
            history_data.append({
                'id': hist.id,
                'asset_name': hist.asset.asset_name,
                'maintenance_cost': float(hist.maintenance_cost),
                'timestamp': hist.timestamp.isoformat(),
                'type': 'completed'
            })

        return Response({
            'recent_requests': requests_data,
            'recent_workorders': workorders_data,
            'recent_completed': history_data,
        })