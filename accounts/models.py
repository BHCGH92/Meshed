from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Employee', 'Employee'),
        ('Manager', 'Manager')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Employee')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    holiday_allowance = models.PositiveSmallIntegerField(default=28) # UK Minimum holiday allowance is 28 days for full-time employees
    contracted_hours = models.DecimalField(default=37, max_digits=4, decimal_places=1) # Default to 37 hours per week
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approver_for')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    @property
    def daily_contracted_hours(self):
        return round(float(self.contracted_hours / 5), 2)

    def is_manager(self):
        return self.role in ('Manager', 'Admin')

class CompanySettings(models.Model):
    name = models.CharField(max_length=100, blank=True, default='HR Management System')
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    default_contracted_hours = models.DecimalField(default=37, max_digits=4, decimal_places=1) # Default to 37 hours per week
    default_holiday_allowance = models.PositiveSmallIntegerField(default=28) # UK Minimum holiday allowance is 28 days for full-time employees

    def __str__(self):
        return self.name

    @classmethod
    def get(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        company = CompanySettings.get()
        UserProfile.objects.create(
            user=instance,
            contracted_hours=company.default_contracted_hours,
            holiday_allowance=company.default_holiday_allowance,
        )