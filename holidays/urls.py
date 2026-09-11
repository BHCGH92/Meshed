from django.urls import path
from . import views

urlpatterns = [
    path('calendar/', views.holiday_calendar, name='holiday_calendar'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('pending/', views.pending_requests, name='pending_requests'),
    path('company/', views.company_holidays, name='company_holidays'),
]
