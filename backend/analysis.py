import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class StockAnalysis:
    def __init__(self):
        """Initialize with API keys from environment variables"""
        self.newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))
        
    def get_stock_data(self, ticker, period='5y'):
        """Fetch stock data from Yahoo Finance"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            return hist
        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return None

    def get_news_sentiment(self, company_name):
        """Fetch news articles and calculate basic sentiment"""
        try:
            news = self.newsapi.get_everything(
                q=company_name,
                language='en',
                sort_by='publishedAt',
                page_size=100
            )
            return news
        except Exception as e:
            print(f"Error fetching news: {e}")
            return None

    def calculate_technical_indicators(self, df):
        """Calculate basic technical indicators"""
        if df is None or df.empty:
            return None
        
        df = df.copy()
        
        # Calculate Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        
        # Calculate RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        return df

    def analyze_stock(self, ticker):
        """Complete stock analysis"""
        # Get stock data
        stock_data = self.get_stock_data(ticker)
        if stock_data is None:
            return {"error": "Failed to fetch stock data"}
            
        # Calculate indicators
        analysis = self.calculate_technical_indicators(stock_data)
        if analysis is None:
            return {"error": "Failed to calculate indicators"}
            
        # Get recent price data
        latest_price = analysis['Close'].iloc[-1]
        price_change = ((latest_price - analysis['Close'].iloc[-2]) / analysis['Close'].iloc[-2]) * 100
        
        # Get news sentiment
        news = self.get_news_sentiment(ticker)
        
        return {
            "ticker": ticker,
            "current_price": round(latest_price, 2),
            "price_change_percent": round(price_change, 2),
            "sma_20": round(analysis['SMA_20'].iloc[-1], 2),
            "sma_50": round(analysis['SMA_50'].iloc[-1], 2),
            "rsi": round(analysis['RSI'].iloc[-1], 2),
            "news_count": len(news['articles']) if news and 'articles' in news else 0
        }