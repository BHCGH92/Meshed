from django.urls import path
from . import views

urlpatterns = [
    path('timesheet/', views.timesheet, name='timesheet'),
    path('export/', views.export_timesheet, name='export_timesheet'),
    path('audit/', views.audit_log, name='audit_log'),
]
