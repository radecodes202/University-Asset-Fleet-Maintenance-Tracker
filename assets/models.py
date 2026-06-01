from django.db import models
from django.conf import settings

# Create your models here.

class AssetCategory(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name        = 'Asset Category'
        verbose_name_plural = 'Asset Categories'
        ordering            = ['name']

    def __str__(self):
        return self.name

class Asset(models.Model):

    class Status(models.TextChoices):
        ACTIVE            = 'ACTIVE',            'Active'
        UNDER_MAINTENANCE = 'UNDER_MAINTENANCE', 'Under Maintenance'
        RETIRED           = 'RETIRED',           'Retired'

    asset_name    = models.CharField(max_length=200)
    asset_image = models.ImageField(
                        upload_to='assets/',
                        blank=True,
                        null=True
                    )

    category      = models.ForeignKey(
                        AssetCategory,
                        on_delete=models.PROTECT,
                        related_name='assets'
                    )
    serial_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2)
    current_status = models.CharField(
                        max_length=20,
                        choices=Status.choices,
                        default=Status.ACTIVE,
                        db_index=True,
                    )
    created_by    = models.ForeignKey(
                        settings.AUTH_USER_MODEL,
                        on_delete=models.SET_NULL,
                        null=True,
                        related_name='assets_created'
                    )
    date_added    = models.DateTimeField(auto_now_add=True)
    notes         = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name        = 'Asset'
        verbose_name_plural = 'Assets'
        ordering            = ['asset_name']

    def __str__(self):
        return f'{self.asset_name} [{self.current_status}]'