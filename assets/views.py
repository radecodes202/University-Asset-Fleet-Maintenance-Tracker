from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Asset, AssetCategory
from accounts.permissions import IsManager, IsManagerOrReadOnly, CanViewCosts


class AssetCategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsManagerOrReadOnly]
    queryset = AssetCategory.objects.all()


class AssetListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsManagerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        queryset = Asset.objects.all()

        # Filter by category if provided
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__name__icontains=category)

        # Filter by status if provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(current_status=status_filter)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AssetDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsManagerOrReadOnly]

    def get_queryset(self):
        return Asset.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.filter(pk=self.kwargs['pk']).first()

        if not obj:
            from rest_framework.exceptions import NotFound
            raise NotFound('Asset not found.')

        return obj

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current_status == Asset.Status.UNDER_MAINTENANCE:
            return Response(
                {'detail': 'Cannot delete an asset that is under maintenance.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        obj.current_status = Asset.Status.RETIRED
        obj.save()
        return Response(
            {'detail': f'{obj.asset_name} has been retired.'},
            status=status.HTTP_200_OK
        )