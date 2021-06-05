from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AccountsBalance, HistoryTransactions, CurrentPortfolio

class AccountsBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')

class HistoryTransactionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'quantity', 'transaction_type', 'symbol', 'unit_price_transaction', 'timestamp', 'total_price_transaction', 'transaction_id')

class CurrentPortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'symbol', 'quantity', 'company_name', 'average_price_portfolio')

admin.site.register(User, UserAdmin)
admin.site.register(AccountsBalance, AccountsBalanceAdmin)
admin.site.register(HistoryTransactions, HistoryTransactionsAdmin)
admin.site.register(CurrentPortfolio, CurrentPortfolioAdmin)


