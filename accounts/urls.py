from django.urls import path
from . import views

urlpatterns = [
    # Frontend pages
    path('login/',  views.login_view,  name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/',  views.users_page,  name='users'),

    # API
    path('users/list/', views.UserListCreateView.as_view(), name='user-list'),
]