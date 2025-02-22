from decimal import Decimal
from typing import Any

from django.db import models, transaction
from rest_framework.serializers import ValidationError


class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=128, blank=False, null=False)
    balance = models.DecimalField(
        max_digits=30,
        decimal_places=8,
        blank=False,
        null=False,
        help_text='Wallet balance, cannot be negative. Can accommodate up to a 10^12 transactions of maximum amount',
    )

    class Meta:
        indexes = [
            models.Index(fields=['balance']),
        ]


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    wallet = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.CASCADE)
    txid = models.CharField(
        max_length=64, unique=True, blank=False, null=False, help_text='Unique transaction ID (usually sha256 hash)'
    )
    amount = models.DecimalField(
        max_digits=18, decimal_places=8, blank=False, null=False, help_text='Transaction amount, can be negative'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args: Any, **kwargs: Any) -> None:
        with transaction.atomic():
            # Refresh the wallet from the database to ensure we have the latest balance.
            self.wallet.refresh_from_db()
            new_balance = self.wallet.balance + Decimal(self.amount)
            if new_balance < 0:
                raise ValidationError('Amount exceeds wallet balance.')
            self.wallet.balance = new_balance
            self.wallet.save()
            super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['amount']),
            models.Index(fields=['wallet']),
            models.Index(fields=['created_at']),
        ]
