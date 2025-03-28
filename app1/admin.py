# app1/admin.py
from django.contrib import admin
from .models import Account, Transaction, Portfolio

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'symbol', 'transaction_type', 'quantity', 'price', 'total_amount', 'timestamp')
    list_filter = ('transaction_type', 'timestamp')
    search_fields = ('symbol',)

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'symbol', 'quantity', 'avg_buy_price')
    search_fields = ('symbol',)