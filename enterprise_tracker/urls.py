from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
)
from accounts.serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT login view that uses email instead of username.
    """
    serializer_class = CustomTokenObtainPairSerializer

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Auth
    path('api/auth/login/',   CustomTokenObtainPairView.as_view(),  name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(),           name='token_refresh'),
    path('api/auth/logout/',  TokenBlacklistView.as_view(),         name='token_blacklist'),

    # API endpoints
    path('api/assets/',      include('assets.urls')),
    path('api/maintenance/', include('maintenance.urls')),
    path('api/dashboard/',   include('dashboard.urls')),
    path('api/accounts/',    include('accounts.urls')),
    path('api/audit/',       include('audit.urls')),

    # Frontend
    path('', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),

    # Root redirect
    path('', RedirectView.as_view(url='/login/')),
]

# Serve media files only in development (DEBUG=True)
# In production, Cloudinary serves images directly from their CDN
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
