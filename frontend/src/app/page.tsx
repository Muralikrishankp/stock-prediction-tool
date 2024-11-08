'use client';

import { useState } from 'react';
import type { StockAnalysis } from '@/types/stock.ts';

export default function StockDashboard() {
  const [symbol, setSymbol] = useState('');
  const [analysis, setAnalysis] = useState<StockAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyzeStock = async () => {
    if (!symbol) return;
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/stock/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symbol: symbol.toUpperCase(),
          period: "1y"
        })
      });

      if (!response.ok) {
        throw new Error('Failed to fetch stock data');
      }

      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      setError('Failed to analyze stock. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Stock Analysis Dashboard</h1>

        {/* Search Box */}
        <div className="bg-white p-6 rounded-lg shadow-lg mb-6">
          <div className="flex gap-4">
            <input
              type="text"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value)}
              placeholder="Enter stock symbol (e.g., AAPL)"
              className="flex-1 p-2 border rounded"
            />
            <button
              onClick={analyzeStock}
              disabled={loading || !symbol}
              className="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400"
            >
              {loading ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="p-4 mb-6 bg-red-100 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* Results */}
        {analysis && (
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-bold mb-4">{analysis.symbol} Analysis</h2>
            
            {/* Current Price */}
            <div className="mb-6">
              <h3 className="font-bold text-gray-600">Current Price</h3>
              <p className="text-2xl">${analysis.price_analysis.current_price.toFixed(2)}</p>
              <p className={analysis.price_analysis.price_trend === 'Upward' ? 'text-green-600' : 'text-red-600'}>
                Trend: {analysis.price_analysis.price_trend}
              </p>
            </div>

            {/* Price Range */}
            <div className="mb-6">
              <h3 className="font-bold text-gray-600">52-Week Range</h3>
              <p>Low: ${analysis.price_analysis.fifty_week_low.toFixed(2)}</p>
              <p>High: ${analysis.price_analysis.fifty_week_high.toFixed(2)}</p>
              <p>Predicted Low: ${analysis.price_analysis.predicted_low.toFixed(2)}</p>
            </div>

            {/* Market Info */}
            <div>
              <h3 className="font-bold text-gray-600">Market Information</h3>
              <p>Sector: {analysis.market_factors.sector}</p>
              <p>Industry: {analysis.market_factors.industry}</p>
              <p>Beta: {analysis.market_factors.beta.toFixed(2)}</p>
              <p>Market Cap: ${(analysis.market_factors.market_cap / 1e9).toFixed(2)}B</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}