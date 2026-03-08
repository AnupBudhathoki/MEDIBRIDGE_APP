from django.contrib import admin
from .models import UserRole, HealthReport, Slot


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone')
    list_filter = ('role',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')


@admin.register(HealthReport)
class HealthReportAdmin(admin.ModelAdmin):
    list_display = ('patient', 'blood_pressure', 'heart_rate', 'weight', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('patient__email',)


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'start_time', 'end_time', 'fee', 'is_booked')
    list_filter = ('is_booked',)
