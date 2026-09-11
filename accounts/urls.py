from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('company/', views.company_info, name='company_info'),
    path('users/', views.admin_user_list, name='admin_user_list'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
