from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth endpoints
    path('api/auth/login/',   TokenObtainPairView.as_view(),  name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(),     name='token_refresh'),
    path('api/auth/logout/',  TokenBlacklistView.as_view(),   name='token_blacklist'),

    # App endpoints
    path('api/assets/',      include('assets.urls')),
    path('api/maintenance/', include('maintenance.urls')),
    path('api/dashboard/',   include('dashboard.urls')),

    # Frontend
    path('', include('accounts.urls')),
]