from django.contrib import admin
from .models import HolidayRequest, CompanyHoliday


@admin.register(HolidayRequest)
class HolidayRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'holiday_type', 'status', 'reviewed_by', 'reviewed_at', 'rejection_reason')
    list_filter = ('status', 'holiday_type')
    search_fields = ('user__username',)


@admin.register(CompanyHoliday)
class CompanyHolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'created_by', 'created_at')
    search_fields = ('name',)