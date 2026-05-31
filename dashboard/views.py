from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from assets.models import Asset
from maintenance.models import MaintenanceRequest


@login_required(login_url='/login/')
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')


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
            from maintenance.models import MaintenanceHistory
            from django.db.models import Sum
            total_cost = MaintenanceHistory.objects.aggregate(
                Sum('maintenance_cost')
            )['maintenance_cost__sum'] or 0
            data['total_maintenance_cost'] = total_cost

        return Response(data)