from django.shortcuts import render
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
    
    return render(request, 'service1/stock_prices.html', context)
