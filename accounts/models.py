from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import time


class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )

    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.role})"


class HealthReport(models.Model):
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='health_reports'
    )
    disease_status = models.CharField(max_length=255, blank=True, null=True)
    blood_pressure = models.CharField(max_length=20)
    heart_rate = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    report_file = models.FileField(upload_to='health_reports/', blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='reports_created'
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.updated_at.date()}"


class Slot(models.Model):
    doctor = models.ForeignKey(UserRole, on_delete=models.CASCADE, related_name="slots")
    start_time = models.TimeField()
    end_time = models.TimeField()
    fee = models.DecimalField(max_digits=8, decimal_places=2)
    is_booked = models.BooleanField(default=False)

    def clean(self):
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError("End time must be after start time.")
            if self.end_time > time(14, 0):
                raise ValidationError("End time cannot be after 2:00 PM.")

    def __str__(self):
        return (
            f"Dr. {self.doctor.user.get_full_name()} | "
            f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')} | "
            f"Rs {self.fee}"
        )
