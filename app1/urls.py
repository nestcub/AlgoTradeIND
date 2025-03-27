from django.urls import path
from .views import get_started, stock_prices
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'),name='home'),
    path('get_started/', get_started, name='get_started'),
    path('stock-prices/', stock_prices, name='stock_prices'),
    path('paper-trading/', TemplateView.as_view(template_name='service2/paper_trading.html'), name='paper_trading'),
]
