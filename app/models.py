from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class User(AbstractUser):
    pass

    def serialize(self):
        return {
            "id":self.pk,
            "username":self.username,
            "email":self.email,
        }


class AccountsBalance(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name='AccountsBalance_user')
    balance = models.DecimalField(null=False, blank=False, default=5000, decimal_places=2, max_digits=10)

    def serialize(self):
        return {
            "id":self.user.pk,
            "username":self.user.username,
            "email":self.user.email,
            "account": self.balance
        }

class HistoryTransactions(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name='History_user')
    quantity = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    type_options = (("1", "buy"),('2','sell'))
    transaction_type = models.CharField(choices=type_options, null=False, blank=False, max_length=4)
    symbol = models.CharField(null=False, blank=False, max_length=10)
    timestamp = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    unit_price_transaction = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=10)
    total_price_transaction = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=10)
    transaction_id = models.CharField(null=False, blank=False, max_length=15)

class CurrentPortfolio(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name='Portfolio_user')
    quantity = models.IntegerField(null=False, blank=False, default=0)
    symbol = models.CharField(null=True, blank=True, max_length=10)
    company_name = models.CharField(null=False, blank=False, max_length=256)
    average_price_portfolio = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=10)