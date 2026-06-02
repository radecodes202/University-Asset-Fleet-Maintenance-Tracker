from django.urls import path
from . import views

urlpatterns = [
    path('', views.AssetListCreateView.as_view(), name='asset-list'),
    path('<int:pk>/', views.AssetDetailView.as_view(), name='asset-detail'),
    path('categories/', views.AssetCategoryListCreateView.as_view(), name='category-list'),
    path('page/', views.assets_page, name='assets'),
    path('page/<int:pk>/', views.asset_detail_page, name='asset-detail-page'),
]
