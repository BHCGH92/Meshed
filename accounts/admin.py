from django.contrib import admin
from .models import Department, UserProfile, CompanySettings

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'contracted_hours', 'department')
    list_filter = ('role', 'department')
    search_fields = ('user__username',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)  

@admin.register(CompanySettings)
class CompanySettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo', 'default_contracted_hours', 'default_holiday_allowance', 'include_weekends')
    search_fields = ('name',)
