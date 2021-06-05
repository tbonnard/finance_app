from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
import requests
from django.http import JsonResponse
from django.http import HttpResponse
import decimal
import string
import random

from . import keys

from .forms import UserCreationForm, UserAuthenticationForm, TransactionForm
from .models import User, AccountsBalance, CurrentPortfolio, HistoryTransactions

#used to ease the visualization of the API data in the python IDE
from pprint import pprint


# Create your views here.

def index_view(request):
    url_most_active = f"https://cloud.iexapis.com/stable/stock/market/collection/list?collectionName=mostactive&token={keys.publishable_1}"
    try:
        resp = requests.get(url_most_active).json()
        return render(request, 'app/index.html', {'data': resp})
    except:
        return render(request, 'app/index.html', {})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        form = UserCreationForm()
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                username = request.POST['username']
                pwd = request.POST['password2']
                user = User.objects.create_user(username=username, password=pwd)
                user.save()
                AccountsBalance.objects.create(user=user)
                login(request, user)
                return redirect('index')
            return render(request, 'app/signup.html', {'form': form})
        return render(request, 'app/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        form = UserAuthenticationForm()
        if request.method == 'POST':
            form = UserAuthenticationForm(data=request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
                return render(request, 'app/login.html', {'form': form})
            return render(request, 'app/login.html', {'form': form})
        return render(request, 'app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def get_symbols(request):
    try:
        url_list_symbol = "https://api.iextrading.com/1.0/ref-data/symbols"
        symbols= requests.get(url_list_symbol).json()
        return JsonResponse(symbols, safe=False)
    except:
        return HttpResponseRedirect(reverse("index"))


# check if ID already in DB
def generate_transaction_id():
        transaction_id = [random.choice(string.ascii_letters + string.digits) for i in range(15)]
        if HistoryTransactions.objects.filter(transaction_id = transaction_id):
            generate_transaction_id()
        return "".join(transaction_id)

def symbol_view(request, symbol):
    try:
        symbol_query = get_stock_price(symbol)
        if request.method == 'GET':
            form = TransactionForm(initial={'user': request.user.pk,'symbol' : symbol})
            if request.user.is_authenticated:
                user_portfolio = CurrentPortfolio.objects.filter(user=request.user, symbol=symbol)
                if user_portfolio:
                    stock_qty = user_portfolio[0].quantity
                    stock_avg_price = user_portfolio[0].average_price_portfolio
                    return render(request, 'app/symbol.html', {"symbol": symbol_query, 'form': form, 'stock_qty':stock_qty, 'stock_avg_price':stock_avg_price})
            return render(request, 'app/symbol.html', {"symbol": symbol_query, 'form':form})
        if request.method == 'POST':
            form = TransactionForm(request.POST)
            if form.is_valid():
                qty = request.POST['quantity']
                tr_type = request.POST['transaction_type']
                quote_price_all = get_stock_price(symbol)
                quote_price = quote_price_all['latestPrice']
                total_price = quote_price*float(qty)
                user_balance = AccountsBalance.objects.get(user=request.user)
                if tr_type == '1':
                    if total_price <= user_balance.balance:
                        transaction_id=generate_transaction_id()
                        transaction = HistoryTransactions.objects.create(user=request.user, quantity = int(qty), transaction_type = tr_type, symbol = symbol, unit_price_transaction = quote_price, total_price_transaction=total_price, transaction_id=transaction_id)
                        transaction.save()
                        user_balance.balance -= decimal.Decimal(total_price)
                        user_balance.save()
                        if CurrentPortfolio.objects.filter(user=request.user, symbol = symbol):
                            portfolio = CurrentPortfolio.objects.get(user=request.user, symbol = symbol)
                            portfolio.average_price_portfolio = ((portfolio.quantity * portfolio.average_price_portfolio) + decimal.Decimal((float(qty) * quote_price))) / (int(portfolio.quantity) + int(qty))
                            portfolio.quantity = int(qty) + portfolio.quantity
                            portfolio.save()
                            return HttpResponseRedirect(reverse("confirmation"))
                        else:
                            portfolio = CurrentPortfolio(user=request.user, quantity = int(qty), symbol = symbol, company_name = symbol_query['companyName'], average_price_portfolio=quote_price)
                            portfolio.save()
                        return HttpResponseRedirect(reverse("confirmation"))
                    return render(request, 'app/symbol.html', {"symbol": symbol_query, 'form': form, 'message':"You do not have enough to buy that amount."})
                if CurrentPortfolio.objects.filter(user=request.user, symbol = symbol):
                    portfolio = CurrentPortfolio.objects.get(user=request.user, symbol = symbol)
                    if portfolio.quantity >= int(qty):
                        transaction_id=generate_transaction_id()
                        transaction = HistoryTransactions.objects.create(user=request.user, quantity = int(qty), transaction_type = tr_type, symbol = symbol, unit_price_transaction = quote_price, total_price_transaction=total_price, transaction_id=transaction_id)
                        transaction.save()
                        user_balance.balance += decimal.Decimal(total_price)
                        user_balance.save()
                        portfolio.quantity = portfolio.quantity - int(qty)
                        portfolio.save()
                        return HttpResponseRedirect(reverse("confirmation"))
                    return render(request, 'app/symbol.html', {"symbol": symbol_query, 'form': form, 'message':"The number you want to sell is superior than what you hold. Short sale is not allowed."})
                return render(request, 'app/symbol.html', {"symbol": symbol_query, 'form': form, 'message':"Your portfolio does not hold that stock. Short sale is not allowed."})
            return render(request, 'app/symbol.html', {"symbol": symbol_query, 'form': form, 'message':"Sorry, the content provided is not valid. Please try again"})
        return HttpResponseRedirect(reverse("index"))
    except:
        return render(request, 'app/symbol.html', {'message':"Sorry, an error occured. Please refresh and try again"})


def get_user(request):
    try:
        users = []
        user = AccountsBalance.objects.get(user=request.user)
        users.append(user)
        return JsonResponse([user.serialize() for user in users], safe=False)
    except:
        return HttpResponse('')


def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    user_portfolio = CurrentPortfolio.objects.filter(user=request.user)
    return render(request, 'app/profile.html', {'portfolio': user_portfolio})


def transactions(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    elif not HistoryTransactions.objects.filter(user=request.user):
        return HttpResponseRedirect(reverse("profile"))
    user_history = HistoryTransactions.objects.filter(user=request.user)
    return render(request, 'app/transactions.html', {'histo':sorted(user_history, key=lambda x: x.timestamp, reverse=True)})


# ID to add
def confirmation(request):
    return render(request, 'app/confirmation.html')

def get_stock_price(symbol):
    try:
        url_stock_API = f"https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={keys.publishable_1}"
        return requests.get(url_stock_API).json()
    except:
        return HttpResponseRedirect(reverse("index"))


def get_stock_price_api(request, symbol):
    try:
        url_stock_API = f"https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={keys.publishable_1}"
        stock = requests.get(url_stock_API).json()
        return JsonResponse(stock, safe=False)
    except:
        return HttpResponseRedirect(reverse("index"))

