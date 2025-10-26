"""
Test script for latest_analysis.py using mock data
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from technical_analysis import TechnicalAnalyzer


def generate_mock_ohlc_data(days=250):
    """Generate mock OHLC data for testing"""
    np.random.seed(42)
    
    # Start with a base price around 110,000 (Bitcoin-like)
    base_price = 110000
    
    # Generate timestamps
    end_time = datetime.now()
    timestamps = []
    for i in range(days):
        ts = end_time - timedelta(days=days-i)
        timestamps.append(int(ts.timestamp() * 1000))
    
    # Generate realistic price movements
    data = []
    current_price = base_price
    
    for ts in timestamps:
        # Random walk with some trend
        change = np.random.normal(0, 2000)  # Random change
        current_price += change
        current_price = max(current_price, base_price * 0.8)  # Floor
        current_price = min(current_price, base_price * 1.2)  # Ceiling
        
        # Generate OHLC for the day
        open_price = current_price + np.random.normal(0, 500)
        close_price = current_price + np.random.normal(0, 500)
        high_price = max(open_price, close_price) + abs(np.random.normal(0, 300))
        low_price = min(open_price, close_price) - abs(np.random.normal(0, 300))
        volume = np.random.uniform(20000000000, 40000000000)
        
        data.append([ts, open_price, high_price, low_price, close_price, volume])
    
    return data


def test_latest_analysis():
    """Test the latest analysis functionality with mock data"""
    print("Testing Latest Analysis Script with Mock Data\n")
    print("="*60)
    
    # Generate mock data with 250 days to have SMA_200
    ohlcv_data = generate_mock_ohlc_data(250)
    
    # Initialize technical analyzer
    ta = TechnicalAnalyzer()
    
    # Convert to DataFrame
    df = ta.prepare_dataframe(ohlcv_data)
    
    # Calculate all technical indicators
    df = ta.calculate_moving_averages(df)
    df = ta.calculate_rsi(df, length=14)
    df = ta.calculate_macd(df)
    df = ta.calculate_bollinger_bands(df)
    
    # Get the latest row
    latest_row = df.iloc[-1]
    
    # Display DEBUG information
    print("--- DEBUG: Latest Row Data ---")
    print(f"open           {latest_row['open']:.6f}")
    print(f"high           {latest_row['high']:.6f}")
    print(f"low            {latest_row['low']:.6f}")
    print(f"close          {latest_row['close']:.6f}")
    
    if 'SMA_50' in latest_row and not pd.isna(latest_row['SMA_50']):
        print(f"SMA_50         {latest_row['SMA_50']:.6f}")
    if 'SMA_200' in latest_row and not pd.isna(latest_row['SMA_200']):
        print(f"SMA_200        {latest_row['SMA_200']:.6f}")
    
    if 'RSI' in latest_row and not pd.isna(latest_row['RSI']):
        print(f"RSI_14             {latest_row['RSI']:.6f}")
    
    if 'MACD_12_26_9' in latest_row and not pd.isna(latest_row['MACD_12_26_9']):
        print(f"MACD            {latest_row['MACD_12_26_9']:.6f}")
    if 'MACDh_12_26_9' in latest_row and not pd.isna(latest_row['MACDh_12_26_9']):
        print(f"MACD_hist         {latest_row['MACDh_12_26_9']:.6f}")
    if 'MACDs_12_26_9' in latest_row and not pd.isna(latest_row['MACDs_12_26_9']):
        print(f"MACD_signal     {latest_row['MACDs_12_26_9']:.6f}")
    
    if 'BBL_20_2.0' in latest_row and not pd.isna(latest_row['BBL_20_2.0']):
        print(f"BB_lower       {latest_row['BBL_20_2.0']:.6f}")
    elif 'BBL_20_2.0_2.0' in latest_row and not pd.isna(latest_row['BBL_20_2.0_2.0']):
        print(f"BB_lower       {latest_row['BBL_20_2.0_2.0']:.6f}")
    
    if 'BBU_20_2.0' in latest_row and not pd.isna(latest_row['BBU_20_2.0']):
        print(f"BB_upper       {latest_row['BBU_20_2.0']:.6f}")
    elif 'BBU_20_2.0_2.0' in latest_row and not pd.isna(latest_row['BBU_20_2.0_2.0']):
        print(f"BB_upper       {latest_row['BBU_20_2.0_2.0']:.6f}")
    
    print(f"Name: {latest_row.name}, dtype: float64")
    print("--------------------------------")
    
    # Display formatted analysis
    latest_close = latest_row['close']
    
    print("Latest Analysis for bitcoin:")
    
    # --- Price & Moving Averages ---
    print("--- Price & Moving Averages ---")
    print(f"Latest Close Price: ${latest_close:.2f}")
    
    trend_text = "Unknown"
    if 'SMA_50' in latest_row and 'SMA_200' in latest_row:
        sma_50 = latest_row['SMA_50']
        sma_200 = latest_row['SMA_200']
        
        if not pd.isna(sma_50) and not pd.isna(sma_200):
            if latest_close > sma_50 and latest_close > sma_200:
                trend_text = "Bullish - Price is above both SMA 50 and SMA 200."
            elif latest_close < sma_50 and latest_close < sma_200:
                trend_text = "Bearish - Price is below both SMA 50 and SMA 200."
            elif sma_50 < latest_close < sma_200 or sma_200 < latest_close < sma_50:
                trend_text = "Neutral/Sideways - Price is between SMA 50 and SMA 200."
            else:
                trend_text = "Mixed signals."
    
    print(f"Trend: {trend_text}")
    print()
    
    # --- Oscillators ---
    print("--- Oscillators ---")
    
    if 'RSI' in latest_row and not pd.isna(latest_row['RSI']):
        rsi = latest_row['RSI']
        print(f"RSI (14): {rsi:.2f}")
        
        if rsi >= 70:
            rsi_status = "Overbought (>70)."
        elif rsi <= 30:
            rsi_status = "Oversold (<30)."
        else:
            rsi_status = "Neutral (30-70)."
        
        print(f"RSI Status: {rsi_status}")
    
    if 'MACD_12_26_9' in latest_row and 'MACDs_12_26_9' in latest_row and 'MACDh_12_26_9' in latest_row:
        macd = latest_row['MACD_12_26_9']
        macd_signal = latest_row['MACDs_12_26_9']
        macd_hist = latest_row['MACDh_12_26_9']
        
        if not pd.isna(macd) and not pd.isna(macd_signal) and not pd.isna(macd_hist):
            print(f"MACD ({macd:.2f}) | Signal ({macd_signal:.2f}) | Histogram ({macd_hist:.2f})")
            
            if macd_hist > 0:
                macd_status = "Bullish momentum."
            elif macd_hist < 0:
                macd_status = "Bearish momentum."
            else:
                macd_status = "Neutral."
            
            print(f"MACD Status: {macd_status}")
    print()
    
    # --- Volatility ---
    print("--- Volatility ---")
    
    # Check for both possible column name formats
    bb_lower_col = 'BBL_20_2.0' if 'BBL_20_2.0' in latest_row else 'BBL_20_2.0_2.0'
    bb_upper_col = 'BBU_20_2.0' if 'BBU_20_2.0' in latest_row else 'BBU_20_2.0_2.0'
    
    if bb_lower_col in latest_row and bb_upper_col in latest_row:
        bb_lower = latest_row[bb_lower_col]
        bb_upper = latest_row[bb_upper_col]
        
        if not pd.isna(bb_lower) and not pd.isna(bb_upper):
            print(f"Bollinger Bands: Upper=${bb_upper:.2f}, Lower=${bb_lower:.2f}")
            
            if latest_close > bb_upper:
                bb_status = "Price is above the upper band."
            elif latest_close < bb_lower:
                bb_status = "Price is below the lower band."
            else:
                bb_status = "Price is within the bands."
            
            print(f"BB Status: {bb_status}")
    print()
    
    # --- Strategy ---
    print("[Strategy]:")
    
    bullish_signals = 0
    bearish_signals = 0
    
    if 'SMA_50' in latest_row and 'SMA_200' in latest_row:
        sma_50 = latest_row['SMA_50']
        sma_200 = latest_row['SMA_200']
        if not pd.isna(sma_50) and not pd.isna(sma_200):
            if latest_close > sma_50 and latest_close > sma_200:
                bullish_signals += 1
            elif latest_close < sma_50 and latest_close < sma_200:
                bearish_signals += 1
    
    if 'RSI' in latest_row and not pd.isna(latest_row['RSI']):
        rsi = latest_row['RSI']
        if rsi >= 70:
            bearish_signals += 1
        elif rsi <= 30:
            bullish_signals += 1
        elif rsi > 50:
            bullish_signals += 0.5
        else:
            bearish_signals += 0.5
    
    if 'MACDh_12_26_9' in latest_row and not pd.isna(latest_row['MACDh_12_26_9']):
        macd_hist = latest_row['MACDh_12_26_9']
        if macd_hist > 0:
            bullish_signals += 1
        else:
            bearish_signals += 1
    
    # Check for both possible column name formats
    bb_lower_col = 'BBL_20_2.0' if 'BBL_20_2.0' in latest_row else 'BBL_20_2.0_2.0'
    bb_upper_col = 'BBU_20_2.0' if 'BBU_20_2.0' in latest_row else 'BBU_20_2.0_2.0'
    
    if bb_lower_col in latest_row and bb_upper_col in latest_row:
        bb_lower = latest_row[bb_lower_col]
        bb_upper = latest_row[bb_upper_col]
        if not pd.isna(bb_lower) and not pd.isna(bb_upper):
            if latest_close > bb_upper:
                bearish_signals += 0.5
            elif latest_close < bb_lower:
                bullish_signals += 0.5
    
    if bullish_signals > bearish_signals + 1:
        strategy = "BUY - Multiple bullish indicators suggest an upward trend."
    elif bearish_signals > bullish_signals + 1:
        strategy = "SELL - Multiple bearish indicators suggest a downward trend."
    else:
        strategy = "HOLD - Mixed signals, wait for clearer market direction."
    
    print(strategy)
    print()
    print("="*60)
    print("Test completed successfully!")
    print("="*60)


if __name__ == '__main__':
    test_latest_analysis()
