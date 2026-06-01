from rest_framework import generics, status
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import MaintenanceRequest, WorkOrder, MaintenanceHistory
from accounts.permissions import IsManager, IsManagerOrAuditor
from .serializers import (
    MaintenanceRequestSerializer,
    WorkOrderSerializer,
    StaffMaintenanceHistorySerializer,
    ManagerMaintenanceHistorySerializer,
)


class MaintenanceRequestListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MaintenanceRequestSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_manager or user.is_auditor:
            return MaintenanceRequest.objects.all()
        
        return MaintenanceRequest.objects.filter(requested_by=user)

    def perform_create(self, serializer):
        if self.request.user.is_read_only:
            return Response(
                {'detail': 'Auditors cannot submit requests.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(requested_by=self.request.user)


class MaintenanceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MaintenanceRequestSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_manager or user.is_auditor:
            return MaintenanceRequest.objects.all()

        return MaintenanceRequest.objects.filter(requested_by=user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.filter(pk=self.kwargs['pk']).first()

        if not obj:
            from rest_framework.exceptions import NotFound
            raise NotFound('Request not found.')

        return obj


class BulkUpdateRequestStatusView(generics.GenericAPIView):
    permission_classes = [IsManager]

    def post(self, request):
        request_ids = request.data.get('request_ids', [])
        new_status  = request.data.get('status', None)

        if not request_ids or not new_status:
            return Response(
                {'detail': 'request_ids and status are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_statuses = [
            MaintenanceRequest.Status.APPROVED,
            MaintenanceRequest.Status.REJECTED,
            MaintenanceRequest.Status.COMPLETED,
        ]

        if new_status not in valid_statuses:
            return Response(
                {'detail': f'Invalid status. Choose from {valid_statuses}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        updated = MaintenanceRequest.objects.filter(
            id__in=request_ids
        ).update(status=new_status)

        return Response({
            'detail': f'{updated} requests updated to {new_status}.'
        }, status=status.HTTP_200_OK)


class WorkOrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkOrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_manager or user.is_auditor:
            return WorkOrder.objects.all()

        return WorkOrder.objects.filter(
            maintenance_request__requested_by=user
        )

    def perform_create(self, serializer):
        if not self.request.user.is_manager:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only Managers can create work orders.')
        serializer.save()


class WorkOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkOrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_manager or user.is_auditor:
            return WorkOrder.objects.all()

        return WorkOrder.objects.filter(
            maintenance_request__requested_by=user
        )

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.filter(pk=self.kwargs['pk']).first()

        if not obj:
            from rest_framework.exceptions import NotFound
            raise NotFound('Work order not found.')

        return obj


class MaintenanceHistoryListView(generics.ListAPIView):
    permission_classes = [IsManagerOrAuditor]

    def get_serializer_class(self):
        if self.request.user.is_manager:
            return ManagerMaintenanceHistorySerializer
        return StaffMaintenanceHistorySerializer
    
    def get_queryset(self):
        user = self.request.user

        if user.is_manager or user.is_auditor:
            return MaintenanceHistory.objects.all()

        return MaintenanceHistory.objects.filter(
            asset__maintenance_requests__requested_by=user
        )

@login_required(login_url='/login/')
def requests_page(request):
    return render(request, 'maintenance/requests.html')

@login_required(login_url='/login/')
def workorders_page(request):
    return render(request, 'maintenance/workorders.html')