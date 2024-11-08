// frontend/src/types/stock.ts
export interface Predictions {
    trend_coefficient: number;
    predicted_prices: number[];
    confidence_score: number;
  }
  
  export interface PriceAnalysis {
    current_price: number;
    fifty_week_high: number;
    fifty_week_low: number;
    price_trend: string;
    predicted_low: number;
    volatility: number;
    predictions: Predictions;
  }
  
  export interface MarketFactors {
    sector: string;
    industry: string;
    beta: number;
    market_cap: number;
  }
  
  export interface StockAnalysis {
    symbol: string;
    analysis_date: string;
    price_analysis: PriceAnalysis;
    market_factors: MarketFactors;
  }