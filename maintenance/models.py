from django.db import models
from django.conf import settings
from assets.models import Asset


class MaintenanceRequest(models.Model):

    class Status(models.TextChoices):
        PENDING   = 'PENDING',   'Pending'
        APPROVED  = 'APPROVED',  'Approved'
        REJECTED  = 'REJECTED',  'Rejected'
        COMPLETED = 'COMPLETED', 'Completed'

    asset               = models.ForeignKey(
                            Asset,
                            on_delete=models.PROTECT,
                            related_name='maintenance_requests'
                          )
    requested_by        = models.ForeignKey(
                            settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL,
                            null=True,
                            related_name='maintenance_requests'
                          )
    problem_description = models.TextField()
    date_requested      = models.DateTimeField(auto_now_add=True)
    status              = models.CharField(
                            max_length=10,
                            choices=Status.choices,
                            default=Status.PENDING,
                            db_index=True,
                          )
    manager_notes       = models.TextField(blank=True, null=True)
    date_resolved       = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name        = 'Maintenance Request'
        verbose_name_plural = 'Maintenance Requests'
        ordering            = ['-date_requested']

    def __str__(self):
        return f'{self.asset.asset_name} - {self.status} - {self.date_requested.strftime("%Y-%m-%d")}'

class WorkOrder(models.Model):

    class Status(models.TextChoices):
        OPEN        = 'OPEN',        'Open'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED   = 'COMPLETED',   'Completed'
        CANCELLED   = 'CANCELLED',   'Cancelled'

    maintenance_request  = models.OneToOneField(
                            MaintenanceRequest,
                            on_delete=models.PROTECT,
                            related_name='work_order'
                           )
    assigned_technician  = models.ForeignKey(
                            settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL,
                            null=True,
                            related_name='work_orders'
                           )
    work_description     = models.TextField()
    date_started         = models.DateTimeField(blank=True, null=True)
    date_completed       = models.DateTimeField(blank=True, null=True)
    status               = models.CharField(
                            max_length=15,
                            choices=Status.choices,
                            default=Status.OPEN,
                            db_index=True,
                           )

    class Meta:
        verbose_name        = 'Work Order'
        verbose_name_plural = 'Work Orders'
        ordering            = ['-date_started']

    def __str__(self):
        return f'WO-{self.id} | {self.maintenance_request.asset.asset_name} | {self.status}'

class MaintenanceHistory(models.Model):
    asset            = models.ForeignKey(
                        Asset,
                        on_delete=models.PROTECT,
                        related_name='maintenance_history'
                       )
    work_order       = models.OneToOneField(
                        WorkOrder,
                        on_delete=models.PROTECT,
                        related_name='history'
                       )
    maintenance_cost = models.DecimalField(
                        max_digits=10,
                        decimal_places=2
                       )
    remarks          = models.TextField(blank=True, null=True)
    completed_by     = models.ForeignKey(
                        settings.AUTH_USER_MODEL,
                        on_delete=models.SET_NULL,
                        null=True,
                        related_name='completed_maintenance'
                       )
    timestamp        = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Maintenance History'
        verbose_name_plural = 'Maintenance Histories'
        ordering            = ['-timestamp']

    def __str__(self):
        return f'{self.asset.asset_name} | ₱{self.maintenance_cost} | {self.timestamp.strftime("%Y-%m-%d")}'

