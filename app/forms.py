from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models.base import Model
from django import forms
from .models import User, HistoryTransactions


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

class UserAuthenticationForm(AuthenticationForm):
    pass

class TransactionForm(forms.ModelForm):
    class Meta:
        model = HistoryTransactions
        #fields = '__all__'
        fields = ['transaction_type', 'quantity']

