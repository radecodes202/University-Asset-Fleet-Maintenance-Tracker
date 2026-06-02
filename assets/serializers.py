from rest_framework import serializers
from .models import Asset, AssetCategory

class AssetCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = AssetCategory 
        fields = ['id', 'name', 'description']

class StaffAssetSerializer(serializers.ModelSerializer):
    category    = AssetCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
                    queryset=AssetCategory.objects.all(),
                    source='category',
                    write_only=True
                  )

    class Meta:
        model = Asset
        fields = [
            'id',
            'asset_image',
            'asset_name',
            'category',
            'category_id',
            'serial_number',
            'purchase_date',
            'current_status',
            'date_added',
            'notes',
        ]

class ManagerAssetSerializer(serializers.ModelSerializer):
    category    = AssetCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
                    queryset=AssetCategory.objects.all(),
                    source='category',
                    write_only=True
                  )

    class Meta:
        model = Asset
        fields = [
            'id',
            'asset_image',
            'asset_name',
            'category',
            'category_id',
            'serial_number',
            'purchase_cost',
            'purchase_date',
            'current_status',
            'date_added',
            'created_by',
            'notes',
        ]