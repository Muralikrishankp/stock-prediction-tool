import yfinance as yf
import os
from dotenv import load_dotenv
from newsapi import NewsApiClient

def test_setup():
    print("Testing system setup...")
    
    # Test yfinance with improved error handling
    print("\nTesting stock data fetch:")
    try:
        tesla = yf.Ticker("TSLA")
        hist = tesla.history(period="1d")
        current_price = hist['Close'].iloc[-1]
        print(f"Tesla current price: ${current_price:.2f}")
        print("✓ yfinance working")
    except Exception as e:
        print(f"× Error with yfinance: {e}")

    # Test NewsAPI
    print("\nTesting NewsAPI:")
    try:
        load_dotenv()
        newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))
        tesla_news = newsapi.get_everything(q='Tesla', language='en', page_size=1)
        print(f"Found {tesla_news['totalResults']} news articles about Tesla")
        print("✓ NewsAPI working")
    except Exception as e:
        print(f"× Error with NewsAPI: {e}")

if __name__ == "__main__":
    test_setup()