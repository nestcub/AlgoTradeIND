from django.urls import path
from .views import get_started, stock_prices,paper_trading_view, trade_stock,static_charts
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'),name='home'),
    path('services/', TemplateView.as_view(template_name='services.html'),name='services'),
    path('get_started/', get_started, name='get_started'),
    path('stock-prices/', stock_prices, name='stock_prices'),
    path('paper-trading/', paper_trading_view, name='paper_trading'),
    path('trade/', trade_stock, name='trade_stock'),
    path('static_charts/', static_charts, name='static_charts'),
]
