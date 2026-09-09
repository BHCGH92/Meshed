from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from accounts.models import CompanySettings

class HolidayRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='holiday_requests')
    start_date = models.DateField()
    end_date = models.DateField()

    HOLIDAY_TYPE_CHOICES = [
        ('Standard', 'Standard'),
        ('Flexi', 'Flexi')
    ]
    
    holiday_type = models.CharField(max_length=20, choices=HOLIDAY_TYPE_CHOICES, default='Standard')

    STATUS_CHOICES = [
        ('Pending', 'Pending'), 
        ('Approved', 'Approved'), 
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled')
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_holiday_requests')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.start_date} to {self.end_date} ({self.status})"

    def working_days_count(self):
        settings = CompanySettings.get()
        count = 0
        current_date = self.start_date
        while current_date <= self.end_date:
            if settings.include_weekends or current_date.weekday() < 5:
                count += 1
            current_date += timedelta(days=1)
        return count

    def get_all_dates(self):
        dates = []
        current_date = self.start_date
        while current_date <= self.end_date:
            dates.append(current_date)
            current_date += timedelta(days=1)
        return dates
    
class CompanyHoliday(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_company_holidays')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"

    def working_days_count(self):
        settings = CompanySettings.get()
        count = 0
        current_date = self.start_date
        while current_date <= self.end_date:
            if settings.include_weekends or current_date.weekday() < 5:
                count += 1
            current_date += timedelta(days=1)
        return count
