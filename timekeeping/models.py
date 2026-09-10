from django.db import models
from django.contrib.auth.models import User

class TimeEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='time_entries')
    date = models.DateField()
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} — {self.date}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'date'],
                name='unique_time_entry_per_user_per_day',
                violation_error_message='You already have a time entry for this date.'
            )
        ]

    def total_break_minutes(self):
        completed_breaks = self.break_entries.filter(break_end__isnull=False)
        return sum(b.duration_minutes() for b in completed_breaks)

    def total_hours_worked(self):
        if not self.clock_in or not self.clock_out:
            return None
        total_time = (self.clock_out - self.clock_in).total_seconds() / 3600  # Convert seconds to hours
        total_break_time = self.total_break_minutes() / 60  # Convert minutes to hours
        return round(max(total_time - total_break_time, 0), 2) # Return hours worked rounded to 2 decimal places

    def is_clocked_in(self):
        return self.clock_in is not None and self.clock_out is None

    def active_break(self):
        return self.break_entries.filter(break_end__isnull=True).first()

class BreakEntry(models.Model):
    time_entry = models.ForeignKey(TimeEntry, on_delete=models.CASCADE, related_name='break_entries')
    break_start = models.DateTimeField()
    break_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Break for {self.time_entry.user.username} on {self.time_entry.date}"

    def duration_minutes(self):
        if not self.break_end:
            return None
        return int((self.break_end - self.break_start).total_seconds() // 60)


class TimeAuditEntry(models.Model):
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_changes_made')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_entries')
    entry_date = models.DateField()
    changes = models.JSONField(default=list)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.changed_by} edited {self.target_user} ({self.entry_date})"
