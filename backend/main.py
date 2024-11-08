from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import Optional
from sklearn.linear_model import LinearRegression

class StockRequest(BaseModel):
    symbol: str
    period: Optional[str] = "1y"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def calculate_volatility(hist_data):
    """Calculate stock volatility"""
    returns = hist_data['Close'].pct_change()
    return float(returns.std() * np.sqrt(252))  # Annualized volatility

def calculate_predictions(hist_data):
    """Calculate future price predictions using linear regression"""
    df = hist_data.copy()
    df['Date_Num'] = range(len(df))
    
    # Prepare data for linear regression
    X = df['Date_Num'].values.reshape(-1, 1)
    y = df['Close'].values
    
    # Fit linear regression
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict future values
    future_dates = np.array(range(len(df), len(df) + 180)).reshape(-1, 1)  # 6 months
    future_prices = model.predict(future_dates)
    
    return {
        'trend_coefficient': float(model.coef_[0]),
        'predicted_prices': [float(p) for p in future_prices[-30:]],  # Last month predictions
        'confidence_score': float(model.score(X, y))
    }

@app.post("/stock/")
async def analyze_stock(request: StockRequest):
    try:
        # Get stock data
        stock = yf.Ticker(request.symbol)
        hist = stock.history(period="2y")  # Get 2 years of data for better analysis
        
        if hist.empty:
            raise HTTPException(status_code=404, detail="No data found for this symbol")
        
        # Get basic metrics
        current_price = float(hist['Close'].iloc[-1])
        high_52week = float(hist['High'].tail(252).max())
        low_52week = float(hist['Low'].tail(252).min())
        
        # Calculate predictions and volatility
        predictions = calculate_predictions(hist)
        volatility = calculate_volatility(hist)
        
        # Calculate price trend
        price_trend = "Upward" if hist['Close'].iloc[-1] > hist['Close'].iloc[0] else "Downward"
        
        return {
            "symbol": request.symbol,
            "analysis_date": str(datetime.now()),
            "price_analysis": {
                "current_price": current_price,
                "fifty_week_high": high_52week,
                "fifty_week_low": low_52week,
                "price_trend": price_trend,
                "predicted_low": low_52week * 0.95,
                "volatility": volatility,
                "predictions": predictions
            },
            "market_factors": {
                "sector": stock.info.get('sector', 'Unknown'),
                "industry": stock.info.get('industry', 'Unknown'),
                "beta": stock.info.get('beta', 0),
                "market_cap": stock.info.get('marketCap', 0)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "active", "timestamp": str(datetime.now())}