from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('recent-activity/', views.RecentActivityView.as_view(), name='recent-activity'),
    path('', views.dashboard_view, name='dashboard'),
    path('userguide/', views.userguide_view, name='userguide'),
]
