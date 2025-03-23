from django.shortcuts import render
from django.http import JsonResponse

# def home(request):
#     return render(request, 'index.html')  # Changed template path

def get_started(request):
    return render(request, 'get_started.html')

def stock_prices(request):
    return render(request, 'service1/stock_prices.html')
