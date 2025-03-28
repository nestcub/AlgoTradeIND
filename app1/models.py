# models.py
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=1000000.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Account"

class Transaction(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'
    TRANSACTION_TYPES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calculate total_amount before saving
        self.total_amount = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} {self.symbol} @ {self.price}"

class Portfolio(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField(default=0)
    avg_buy_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ('account', 'symbol')  # One entry per stock per account

    def __str__(self):
        return f"{self.symbol} - {self.quantity} shares"