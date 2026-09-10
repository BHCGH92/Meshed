from django.contrib import admin
from .models import TimeEntry, BreakEntry, TimeAuditEntry


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'clock_in', 'clock_out', 'total_hours_worked')
    list_filter = ('date',)
    search_fields = ('user__username',)


@admin.register(BreakEntry)
class BreakEntryAdmin(admin.ModelAdmin):
    list_display = ('time_entry', 'break_start', 'break_end', 'duration_minutes')
    search_fields = ('time_entry__user__username',)


@admin.register(TimeAuditEntry)
class TimeAuditEntryAdmin(admin.ModelAdmin):
    list_display = ('changed_by', 'target_user', 'entry_date', 'changed_at')
    list_filter = ('entry_date',)
    search_fields = ('target_user__username', 'changed_by__username')
