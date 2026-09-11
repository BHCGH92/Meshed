from django.urls import path
from . import views

urlpatterns = [
    path('company/', views.company_info, name='company_info'),
    path('users/', views.admin_user_list, name='admin_user_list'),
]
