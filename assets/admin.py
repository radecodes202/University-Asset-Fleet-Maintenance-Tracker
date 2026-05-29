from django.contrib import admin
from .models import Asset, AssetCategory

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'description')
    search_fields = ('name',)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display  = ('asset_name', 'category', 'serial_number', 'current_status', 'purchase_date')
    list_filter   = ('current_status', 'category')
    search_fields = ('asset_name', 'serial_number')