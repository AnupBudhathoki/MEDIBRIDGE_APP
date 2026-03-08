from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_uuid', 'fee', 'status', 'user', 'created_at')
    list_filter = ('status',)
    search_fields = ('transaction_uuid', 'transaction_code')
