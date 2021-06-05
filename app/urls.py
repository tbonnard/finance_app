from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('get_symbols/', views.get_symbols, name='get_symbols'),
    path('symbol/<str:symbol>/', views.symbol_view, name='symbol'),
    path('get_user/', views.get_user, name='get_user'),
    path('profile/', views.profile, name='profile'),
    path('transactions/', views.transactions, name='transactions'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('get_stock_price/<str:symbol>/', views.get_stock_price_api, name='get_stock_price'),
]