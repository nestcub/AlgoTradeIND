import json
import threading
from channels.generic.websocket import AsyncWebsocketConsumer
from yliveticker import YLiveTicker

#Nifty-fifty stocks
Tickers = [
        "TATAMOTORS.NS",
        "ADANIPOWER.NS","NTPC.NS",
        "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
        "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BEL.NS", "BPCL.NS",
        "BHARTIARTL.NS", "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DRREDDY.NS",
        "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS",
        "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "INDUSINDBK.NS",
        "INFY.NS", "ITC.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS"
        # "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS", "ONGC.NS",
        # "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SHRIRAMFIN.NS", "SBIN.NS",
        # "SUNPHARMA.NS", "TCS.NS", "TATACONSUM.NS", "TATASTEEL.NS", "TECHM.NS",
        # "TITAN.NS", "TRENT.NS", "ULTRACEMCO.NS", "WIPRO.NS", "ZEEL.NS"
        ] 

#NASDAQ stocks
# Tickers = [
#     "AAPL",  # Apple Inc.
#     "MSFT",  # Microsoft Corporation
#     "AMZN",  # Amazon.com, Inc.
#     "GOOG",  # Alphabet Inc. Class C
#     "GOOGL", # Alphabet Inc. Class A
#     "META",  # Meta Platforms, Inc.
#     "NVDA",  # NVIDIA Corporation
#     "TSLA",  # Tesla, Inc.
#     "PEP",   # PepsiCo, Inc.
#     "AVGO",  # Broadcom Inc.
#     "COST",  # Costco Wholesale Corporation
#     "CSCO",  # Cisco Systems, Inc.
#     # "ADBE",  # Adobe Inc.
#     # "INTC",  # Intel Corporation
#     # "CMCSA", # Comcast Corporation
#     # "NFLX",  # Netflix, Inc.
#     # "PDD",   # Pinduoduo Inc.
#     # "TXN",   # Texas Instruments Incorporated
#     # "QCOM",  # QUALCOMM Incorporated
#     # "AMGN",  # Amgen Inc.
#     # "SBUX",  # Starbucks Corporation
#     # "INTU",  # Intuit Inc.
#     # "MDLZ",  # Mondelez International, Inc.
#     # "ISRG",  # Intuitive Surgical, Inc.
#     # "BKNG",  # Booking Holdings Inc.
#     # "GILD",  # Gilead Sciences, Inc.
#     # "ADP",   # Automatic Data Processing, Inc.
#     # "VRTX",  # Vertex Pharmaceuticals Incorporated
#     # "ADSK",  # Autodesk, Inc.
#     # "LRCX"   # Lam Research Corporation
# ]

class StockPriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        # Define stock tickers to track
        self.tickers = Tickers


        # Run YLiveTicker in a separate thread to prevent blocking
        self.ticker_thread = threading.Thread(target=self.start_ticker, daemon=True)
        self.ticker_thread.start()

    def start_ticker(self):
        """Runs YLiveTicker in a separate thread to avoid blocking the event loop."""
        self.ticker = YLiveTicker(on_ticker=self.on_ticker, ticker_names=self.tickers)
        self.ticker.start()

    async def disconnect(self, close_code):
        if hasattr(self, "ticker"):
            self.ticker.stop()

    def on_ticker(self, ws, ticker_data):
        """Handles incoming stock price data and ensures proper formatting."""
        from asgiref.sync import async_to_sync

        symbol = ticker_data.get("id", "UNKNOWN")  # Stock symbol is under "id"
        price = ticker_data.get("price", "N/A")    # Stock price is under "price"

        # Send structured JSON data to the frontend
        async_to_sync(self.send)(text_data=json.dumps({"symbol": symbol, "price": price}))

