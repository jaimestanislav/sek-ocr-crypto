"""
Real-time cryptocurrency analysis with DEBUG information display
"""
import argparse
import sys
import pandas as pd
from datetime import datetime
from crypto_api import CryptoDataFetcher
from technical_analysis import TechnicalAnalyzer


def display_debug_data(df: pd.DataFrame, coin_id: str) -> None:
    """
    Display DEBUG information showing latest row data with technical indicators
    
    Args:
        df: DataFrame with technical indicators
        coin_id: Cryptocurrency ID
    """
    # Get the latest row
    latest_row = df.iloc[-1]
    
    print("--- DEBUG: Latest Row Data ---")
    # Display key technical indicators
    print(f"open           {latest_row['open']:.6f}")
    print(f"high           {latest_row['high']:.6f}")
    print(f"low            {latest_row['low']:.6f}")
    print(f"close          {latest_row['close']:.6f}")
    
    # Moving averages
    if 'SMA_50' in latest_row and not pd.isna(latest_row['SMA_50']):
        print(f"SMA_50         {latest_row['SMA_50']:.6f}")
    if 'SMA_200' in latest_row and not pd.isna(latest_row['SMA_200']):
        print(f"SMA_200        {latest_row['SMA_200']:.6f}")
    
    # RSI
    if 'RSI' in latest_row and not pd.isna(latest_row['RSI']):
        print(f"RSI_14             {latest_row['RSI']:.6f}")
    
    # MACD
    if 'MACD_12_26_9' in latest_row and not pd.isna(latest_row['MACD_12_26_9']):
        print(f"MACD            {latest_row['MACD_12_26_9']:.6f}")
    if 'MACDh_12_26_9' in latest_row and not pd.isna(latest_row['MACDh_12_26_9']):
        print(f"MACD_hist         {latest_row['MACDh_12_26_9']:.6f}")
    if 'MACDs_12_26_9' in latest_row and not pd.isna(latest_row['MACDs_12_26_9']):
        print(f"MACD_signal     {latest_row['MACDs_12_26_9']:.6f}")
    
    # Bollinger Bands - check for both possible column name formats
    bb_lower_col = 'BBL_20_2.0' if 'BBL_20_2.0' in latest_row else 'BBL_20_2.0_2.0'
    bb_upper_col = 'BBU_20_2.0' if 'BBU_20_2.0' in latest_row else 'BBU_20_2.0_2.0'
    
    if bb_lower_col in latest_row and not pd.isna(latest_row[bb_lower_col]):
        print(f"BB_lower       {latest_row[bb_lower_col]:.6f}")
    if bb_upper_col in latest_row and not pd.isna(latest_row[bb_upper_col]):
        print(f"BB_upper       {latest_row[bb_upper_col]:.6f}")
    
    print(f"Name: {latest_row.name}, dtype: float64")
    print("--------------------------------")


def display_formatted_analysis(df: pd.DataFrame, coin_id: str, ta: TechnicalAnalyzer) -> None:
    """
    Display formatted analysis with Price, Moving Averages, Oscillators, Volatility, and Strategy
    
    Args:
        df: DataFrame with technical indicators
        coin_id: Cryptocurrency ID
        ta: TechnicalAnalyzer instance
    """
    latest_row = df.iloc[-1]
    latest_close = latest_row['close']
    
    print(f"Latest Analysis for {coin_id}:")
    
    # --- Price & Moving Averages ---
    print("--- Price & Moving Averages ---")
    print(f"Latest Close Price: ${latest_close:.2f}")
    
    # Determine trend based on SMA positions
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
    
    # RSI
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
    
    # MACD
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
    
    # Bollinger Bands - check for both possible column name formats
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
    
    # Generate strategy recommendation based on indicators
    bullish_signals = 0
    bearish_signals = 0
    
    # Check trend
    if 'SMA_50' in latest_row and 'SMA_200' in latest_row:
        sma_50 = latest_row['SMA_50']
        sma_200 = latest_row['SMA_200']
        if not pd.isna(sma_50) and not pd.isna(sma_200):
            if latest_close > sma_50 and latest_close > sma_200:
                bullish_signals += 1
            elif latest_close < sma_50 and latest_close < sma_200:
                bearish_signals += 1
    
    # Check RSI
    if 'RSI' in latest_row and not pd.isna(latest_row['RSI']):
        rsi = latest_row['RSI']
        if rsi >= 70:
            bearish_signals += 1  # Overbought
        elif rsi <= 30:
            bullish_signals += 1  # Oversold
        elif rsi > 50:
            bullish_signals += 0.5
        else:
            bearish_signals += 0.5
    
    # Check MACD
    if 'MACDh_12_26_9' in latest_row and not pd.isna(latest_row['MACDh_12_26_9']):
        macd_hist = latest_row['MACDh_12_26_9']
        if macd_hist > 0:
            bullish_signals += 1
        else:
            bearish_signals += 1
    
    # Check Bollinger Bands - check for both possible column name formats
    bb_lower_col = 'BBL_20_2.0' if 'BBL_20_2.0' in latest_row else 'BBL_20_2.0_2.0'
    bb_upper_col = 'BBU_20_2.0' if 'BBU_20_2.0' in latest_row else 'BBU_20_2.0_2.0'
    
    if bb_lower_col in latest_row and bb_upper_col in latest_row:
        bb_lower = latest_row[bb_lower_col]
        bb_upper = latest_row[bb_upper_col]
        if not pd.isna(bb_lower) and not pd.isna(bb_upper):
            if latest_close > bb_upper:
                bearish_signals += 0.5  # Potentially overbought
            elif latest_close < bb_lower:
                bullish_signals += 0.5  # Potentially oversold
    
    # Determine recommendation
    if bullish_signals > bearish_signals + 1:
        strategy = "BUY - Multiple bullish indicators suggest an upward trend."
    elif bearish_signals > bullish_signals + 1:
        strategy = "SELL - Multiple bearish indicators suggest a downward trend."
    else:
        strategy = "HOLD - Mixed signals, wait for clearer market direction."
    
    print(strategy)
    print()


def main():
    """Main entry point for the latest analysis script"""
    parser = argparse.ArgumentParser(
        description='Real-time Cryptocurrency Analysis with DEBUG Information',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze Bitcoin with latest data
  python latest_analysis.py bitcoin
  
  # Analyze Ethereum with 90 days of data
  python latest_analysis.py ethereum --days 90
  
  # Analyze Bitcoin with 30 days of data
  python latest_analysis.py bitcoin --days 30
        """
    )
    
    parser.add_argument('coin_id', nargs='?', default='bitcoin',
                       help='Cryptocurrency ID (e.g., bitcoin, ethereum, cardano). Default: bitcoin')
    parser.add_argument('--days', type=int, default=90,
                       help='Number of days of historical data to fetch (default: 90)')
    
    args = parser.parse_args()
    
    # Initialize API and analyzer
    crypto_api = CryptoDataFetcher()
    ta = TechnicalAnalyzer()
    
    print(f"\n{'='*60}")
    print(f"Fetching latest data for: {args.coin_id}")
    print(f"{'='*60}\n")
    
    # Get OHLC data
    ohlc_result = crypto_api.get_ohlc_data(args.coin_id, days=args.days)
    
    if not ohlc_result['success']:
        print(f"✗ Failed to fetch data: {ohlc_result.get('error', 'Unknown error')}")
        sys.exit(1)
    
    ohlc_data = ohlc_result['data']
    
    if not ohlc_data or len(ohlc_data) < 20:
        print("✗ Insufficient data for technical analysis")
        sys.exit(1)
    
    # Get volume data
    market_chart_result = crypto_api.get_market_chart(args.coin_id, days=args.days)
    
    # Merge volume data if available
    if market_chart_result['success'] and market_chart_result.get('total_volumes'):
        volumes = market_chart_result['total_volumes']
        volume_dict = {vol[0]: vol[1] for vol in volumes}
        
        # Add volume to OHLC data
        ohlcv_data = []
        for ohlc in ohlc_data:
            timestamp = ohlc[0]
            volume = volume_dict.get(timestamp, 0)
            ohlcv_data.append(ohlc + [volume])
    else:
        ohlcv_data = ohlc_data
    
    # Convert to DataFrame
    df = ta.prepare_dataframe(ohlcv_data)
    
    # Calculate all technical indicators
    df = ta.calculate_moving_averages(df)
    df = ta.calculate_rsi(df, length=14)
    df = ta.calculate_macd(df)
    df = ta.calculate_bollinger_bands(df)
    
    # Display DEBUG information
    display_debug_data(df, args.coin_id)
    
    # Display formatted analysis
    display_formatted_analysis(df, args.coin_id, ta)
    
    print(f"{'='*60}")
    print("Analysis completed!")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
