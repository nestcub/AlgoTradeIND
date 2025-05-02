from django.shortcuts import render, redirect
from .utils import calculate_macd, calculate_rsi, calculate_ema, calculate_support_resistance, determine_action
import yfinance as yf
from .consumers import Tickers
import pandas as pd

def get_started(request):
    return render(request, 'get_started.html')

def stock_prices(request):
    # Get the ticker list from StockPriceConsumer
    tickers = Tickers
    
    # Dictionary to store results
    signals = {}
    
    # Get historical data (last 60 days) for all tickers
    for ticker in tickers:
        try:
            # Download data using yfinance
            stock_data = yf.download(ticker, period="60d", interval="1d")
            
            if not stock_data.empty:
                # Extract 1D array of closing prices
                close_prices = stock_data['Close'].values.flatten()  # Flatten to ensure 1D array
                
                # Create a DataFrame with just Close prices for consistency
                df = pd.DataFrame({'Close': close_prices}, index=stock_data.index)
                # Calculate technical indicators
                macd, signal = calculate_macd(df)
                rsi = calculate_rsi(df)
                ema_short, ema_long = calculate_ema(df)
                support, resistance = calculate_support_resistance(df)
                
                # Get current price (last closing price)
                entry_price = df['Close'].iloc[-1]
                
                # Determine action
                action, target_price = determine_action(
                    macd, signal, rsi, ema_short, ema_long, 
                    entry_price, support
                )
                
                # Store results
                signals[ticker] = {
                    'current_price': round(entry_price, 2),
                    'action': action,
                    'target_price': round(target_price, 2),
                    'rsi': round(rsi.iloc[-1], 2),
                    'support': round(support, 2),
                    'resistance': round(resistance, 2)
                }
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")
            continue
    
    context = {
        'signals': signals,
        'last_updated': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'tickers': tickers
    }
    
    return render(request, 'services/stock_prices.html', context)


from .models import Account, Portfolio, Transaction
from decimal import Decimal
from django.db import transaction
from django.contrib.auth.models import User

def paper_trading_view(request):
    # Get or create account for dummy user
    dummy_user = User.objects.get(username='test1')
    account, created = Account.objects.get_or_create(user=dummy_user, defaults={'balance': Decimal('1000000.00')})
    
    # Get signals for trading
    tickers = Tickers
    signals = {}
    for ticker in tickers:
        try:
            stock_data = yf.download(ticker, period="60d", interval="1d")
            if not stock_data.empty:
                close_prices = stock_data['Close'].values.flatten()
                df = pd.DataFrame({'Close': close_prices}, index=stock_data.index)
                entry_price = df['Close'].iloc[-1]
                signals[ticker] = {'current_price': round(entry_price, 2)}
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")
            continue
    
    # Get portfolio and precompute values
    portfolio = Portfolio.objects.filter(account=account)
    portfolio_data = []
    for item in portfolio:
        current_price = Decimal(str(signals.get(item.symbol, {}).get('current_price', 0)))
        current_value = current_price * item.quantity
        profit_loss = current_value - (item.avg_buy_price * item.quantity)
        portfolio_data.append({
            'symbol': item.symbol,
            'quantity': item.quantity,
            'avg_buy_price': item.avg_buy_price,
            'current_value': current_value,
            'profit_loss': profit_loss,
        })
    
    # Get transactions
    transactions = Transaction.objects.filter(account=account).order_by('-timestamp')[:10]
    
    context = {
        'account': account,
        'signals': signals,
        'portfolio_data': portfolio_data,  # Precomputed portfolio data
        'transactions': transactions,
    }
    return render(request, 'services/paper_trading.html', context)

@transaction.atomic
def trade_stock(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        quantity = int(request.POST.get('quantity', 0))
        price = Decimal(request.POST.get('price'))
        action = request.POST.get('action')
        
        dummy_user = User.objects.get(username='test1')
        account = Account.objects.get(user=dummy_user)
        total_cost = price * quantity
        
        if action == 'BUY':
            if account.balance >= total_cost:
                account.balance -= total_cost
                portfolio, created = Portfolio.objects.get_or_create(account=account, symbol=symbol)
                
                if created:
                    portfolio.quantity = quantity
                    portfolio.avg_buy_price = price
                else:
                    total_shares = portfolio.quantity + quantity
                    portfolio.avg_buy_price = ((portfolio.avg_buy_price * portfolio.quantity) + total_cost) / total_shares
                    portfolio.quantity = total_shares
                
                Transaction.objects.create(
                    account=account, symbol=symbol, transaction_type='BUY',
                    quantity=quantity, price=price
                )
                account.save()
                portfolio.save()
            else:
                return render(request, 'services/paper_trading.html', {'error': 'Insufficient balance'})
        
        elif action == 'SELL':
            portfolio = Portfolio.objects.filter(account=account, symbol=symbol).first()
            if portfolio and portfolio.quantity >= quantity:
                account.balance += total_cost
                portfolio.quantity -= quantity
                
                Transaction.objects.create(
                    account=account, symbol=symbol, transaction_type='SELL',
                    quantity=quantity, price=price
                )
                
                if portfolio.quantity == 0:
                    portfolio.delete()
                else:
                    portfolio.save()
                account.save()
            else:
                return render(request, 'services/paper_trading.html', {'error': 'Insufficient shares'})
    
    return redirect('paper_trading')


import plotly.graph_objects as go
from plotly.subplots import make_subplots

def static_charts(request):
    # Get the ticker list from StockPriceConsumer
    tickers = Tickers
    
    # Dictionary to store results
    signals = {}
    # Dictionary to store plot HTML for each ticker
    plots = {}
    
    # Get historical data (last 60 days) for all tickers
    for ticker in tickers:
        try:
            # Download data using yfinance
            stock_data = yf.download(ticker, period="60d", interval="1d")
            
            if not stock_data.empty:
                # Extract 1D array of closing prices
                close_prices = stock_data['Close'].values.flatten()
                
                # Create a DataFrame with just Close prices for consistency
                df = pd.DataFrame({'Close': close_prices}, index=stock_data.index)
                # Calculate technical indicators
                macd, signal = calculate_macd(df)
                rsi = calculate_rsi(df)
                ema_short, ema_long = calculate_ema(df)
                support, resistance = calculate_support_resistance(df)
                
                # Get current price (last closing price)
                entry_price = df['Close'].iloc[-1]
                
                # Determine action
                action, target_price = determine_action(
                    macd, signal, rsi, ema_short, ema_long, 
                    entry_price, support
                )
                
                # Store results
                signals[ticker] = {
                    'current_price': round(entry_price, 2),
                    'action': action,
                    'target_price': round(target_price, 2),
                    'rsi': round(rsi.iloc[-1], 2),
                    'support': round(support, 2),
                    'resistance': round(resistance, 2)
                }
                
                # Create visualization
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                                   vertical_spacing=0.05, 
                                   row_heights=[0.7, 0.3])
                
                # Price chart with EMAs
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], 
                                       name='Price', line=dict(color='blue')), 
                            row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=ema_short, 
                                       name='EMA Short', line=dict(color='orange')), 
                            row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=ema_long, 
                                       name='EMA Long', line=dict(color='green')), 
                            row=1, col=1)
                
                # Add support/resistance lines
                fig.add_hline(y=support, line_dash="dot", 
                             annotation_text=f"Support: {support:.2f}", 
                             line_color="green", row=1, col=1)
                fig.add_hline(y=resistance, line_dash="dot", 
                             annotation_text=f"Resistance: {resistance:.2f}", 
                             line_color="red", row=1, col=1)
                
                # MACD
                fig.add_trace(go.Scatter(x=df.index, y=macd, 
                                     name='MACD', line=dict(color='blue')), 
                            row=2, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=signal, 
                                     name='Signal', line=dict(color='orange')), 
                            row=2, col=1)
                
                # RSI
                fig.add_trace(go.Scatter(x=df.index, y=rsi, 
                                     name='RSI', line=dict(color='purple')), 
                            row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", 
                             annotation_text="Oversold", 
                             line_color="green", row=2, col=1)
                fig.add_hline(y=70, line_dash="dash", 
                             annotation_text="Overbought", 
                             line_color="red", row=2, col=1)
                
                # Update layout
                fig.update_layout(
                    height=600,
                    title=f"{ticker} Technical Analysis",
                    hovermode="x unified"
                )
                
                # Convert plot to HTML
                plot_html = fig.to_html(full_html=False)
                plots[ticker] = plot_html
                
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")
            continue
    
    context = {
        'signals': signals,
        'plots': plots,  # Make sure this is passed to the template
        'last_updated': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'tickers': tickers
    }
    
    return render(request, 'services/static_charts.html', context)
