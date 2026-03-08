from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    transaction_uuid = models.CharField(max_length=100, unique=True)
    transaction_code = models.CharField(max_length=100, blank=True, null=True)
    product_code = models.CharField(max_length=50)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_uuid} — Rs {self.fee} ({self.status})"
