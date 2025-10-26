"""
Tests for technical analysis module
"""
import os
import sys
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from technical_analysis import TechnicalAnalyzer


def test_technical_analyzer_initialization():
    """Test TechnicalAnalyzer initialization"""
    print("Testing TechnicalAnalyzer initialization...")
    
    try:
        ta = TechnicalAnalyzer()
        assert ta is not None
        print("  ✓ PASSED: TechnicalAnalyzer initialized correctly")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False


def test_prepare_dataframe():
    """Test DataFrame preparation from OHLCV data"""
    print("\nTesting DataFrame preparation...")
    
    try:
        ta = TechnicalAnalyzer()
        
        # Sample OHLCV data
        ohlcv_data = [
            [1640000000000, 47000, 48000, 46500, 47500, 1000000],
            [1640086400000, 47500, 48500, 47000, 48000, 1200000],
            [1640172800000, 48000, 49000, 47500, 48500, 1100000]
        ]
        
        df = ta.prepare_dataframe(ohlcv_data)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert 'open' in df.columns
        assert 'high' in df.columns
        assert 'low' in df.columns
        assert 'close' in df.columns
        assert 'volume' in df.columns
        
        print("  ✓ PASSED: DataFrame preparation works correctly")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False


def test_calculate_moving_averages():
    """Test moving average calculations"""
    print("\nTesting moving average calculations...")
    
    try:
        ta = TechnicalAnalyzer()
        
        # Create sample data with enough points for MA calculations
        dates = pd.date_range('2023-01-01', periods=250, freq='D')
        df = pd.DataFrame({
            'open': np.random.uniform(45000, 50000, 250),
            'high': np.random.uniform(46000, 51000, 250),
            'low': np.random.uniform(44000, 49000, 250),
            'close': np.random.uniform(45000, 50000, 250),
            'volume': np.random.uniform(1000000, 2000000, 250)
        }, index=dates)
        
        df = ta.calculate_moving_averages(df)
        
        assert 'SMA_20' in df.columns
        assert 'SMA_50' in df.columns
        assert 'SMA_200' in df.columns
        assert 'EMA_12' in df.columns
        assert 'EMA_26' in df.columns
        
        # Check that the last values are not NaN for adequate data
        assert not pd.isna(df['SMA_20'].iloc[-1])
        assert not pd.isna(df['SMA_50'].iloc[-1])
        assert not pd.isna(df['SMA_200'].iloc[-1])
        
        print("  ✓ PASSED: Moving averages calculated correctly")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False


def test_analyze_trend():
    """Test trend analysis"""
    print("\nTesting trend analysis...")
    
    try:
        ta = TechnicalAnalyzer()
        
        # Create uptrend data
        dates = pd.date_range('2023-01-01', periods=250, freq='D')
        uptrend_prices = np.linspace(40000, 60000, 250)
        df = pd.DataFrame({
            'close': uptrend_prices,
            'open': uptrend_prices * 0.99,
            'high': uptrend_prices * 1.01,
            'low': uptrend_prices * 0.98,
            'volume': np.random.uniform(1000000, 2000000, 250)
        }, index=dates)
        
        df = ta.calculate_moving_averages(df)
        trend = ta.analyze_trend(df)
        
        assert 'trend' in trend
        assert trend['trend'] in ['bullish', 'bearish', 'unknown', 'insufficient_data']
        
        if trend['trend'] in ['bullish', 'bearish']:
            assert 'strength' in trend
            assert trend['strength'] in ['weak', 'moderate', 'strong']
        
        print("  ✓ PASSED: Trend analysis works correctly")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False


def test_detect_ma_crossover():
    """Test MA crossover detection"""
    print("\nTesting MA crossover detection...")
    
    try:
        ta = TechnicalAnalyzer()
        
        # Create data with enough points
        dates = pd.date_range('2023-01-01', periods=250, freq='D')
        df = pd.DataFrame({
            'close': np.random.uniform(45000, 50000, 250),
            'open': np.random.uniform(45000, 50000, 250),
            'high': np.random.uniform(46000, 51000, 250),
            'low': np.random.uniform(44000, 49000, 250),
            'volume': np.random.uniform(1000000, 2000000, 250)
        }, index=dates)
        
        df = ta.calculate_moving_averages(df)
        crossover = ta.detect_ma_crossover(df)
        
        assert 'crossover' in crossover
        assert crossover['crossover'] in ['none', 'golden_cross', 'death_cross']
        
        if crossover['crossover'] != 'none':
            assert 'type' in crossover
        
        print("  ✓ PASSED: MA crossover detection works correctly")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False


def test_calculate_rsi():
    """Test RSI calculation"""
    print("\nTesting RSI calculation...")
    
    try:
        ta = TechnicalAnalyzer()
        
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        df = pd.DataFrame({
            'close': np.random.uniform(45000, 50000, 100),
            'open': np.random.uniform(45000, 50000, 100),
            'high': np.random.uniform(46000, 51000, 100),
            'low': np.random.uniform(44000, 49000, 100),
            'volume': np.random.uniform(1000000, 2000000, 100)
        }, index=dates)
        
        df = ta.calculate_rsi(df)
        
        assert 'RSI' in df.columns, "RSI column not found in DataFrame"
        
        # RSI should be between 0 and 100 for valid values
        rsi_values = df['RSI'].dropna()
        if len(rsi_values) > 0:
            invalid_values = rsi_values[(rsi_values < 0) | (rsi_values > 100)]
            assert len(invalid_values) == 0, f"Found {len(invalid_values)} RSI values outside [0, 100] range"
        
        print("  ✓ PASSED: RSI calculation works correctly")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_analyze_rsi():
    """Test RSI analysis"""
    print("\nTesting RSI analysis...")
    
    try:
        ta = TechnicalAnalyzer()
        
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        df = pd.DataFrame({
            'close': np.random.uniform(45000, 50000, 100),
            'open': np.random.uniform(45000, 50000, 100),
            'high': np.random.uniform(46000, 51000, 100),
            'low': np.random.uniform(44000, 49000, 100),
            'volume': np.random.uniform(1000000, 2000000, 100)
        }, index=dates)
        
        df = ta.calculate_rsi(df)
        rsi_analysis = ta.analyze_rsi(df)
        
        assert 'signal' in rsi_analysis
        assert rsi_analysis['signal'] in ['overbought', 'oversold', 'bullish', 'bearish', 'neutral', 'insufficient_data']
        
        print("  ✓ PASSED: RSI analysis works correctly")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False


def test_calculate_macd():
    """Test MACD calculation"""
    print("\nTesting MACD calculation...")
    
    try:
        ta = TechnicalAnalyzer()
        
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        df = pd.DataFrame({
            'close': np.random.uniform(45000, 50000, 100),
            'open': np.random.uniform(45000, 50000, 100),
            'high': np.random.uniform(46000, 51000, 100),
            'low': np.random.uniform(44000, 49000, 100),
            'volume': np.random.uniform(1000000, 2000000, 100)
        }, index=dates)
        
        df = ta.calculate_macd(df)
        
        # Check if MACD columns exist
        assert 'MACD_12_26_9' in df.columns or len(df.columns) > 5
        
        print("  ✓ PASSED: MACD calculation works correctly")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False


def test_calculate_bollinger_bands():
    """Test Bollinger Bands calculation"""
    print("\nTesting Bollinger Bands calculation...")
    
    try:
        ta = TechnicalAnalyzer()
        
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        df = pd.DataFrame({
            'close': np.random.uniform(45000, 50000, 100),
            'open': np.random.uniform(45000, 50000, 100),
            'high': np.random.uniform(46000, 51000, 100),
            'low': np.random.uniform(44000, 49000, 100),
            'volume': np.random.uniform(1000000, 2000000, 100)
        }, index=dates)
        
        df = ta.calculate_bollinger_bands(df)
        
        # Check if Bollinger Bands columns exist
        assert 'BBL_20_2.0' in df.columns or len(df.columns) > 5
        
        print("  ✓ PASSED: Bollinger Bands calculation works correctly")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False


def test_calculate_volume_analysis():
    """Test volume analysis calculation"""
    print("\nTesting volume analysis calculation...")
    
    try:
        ta = TechnicalAnalyzer()
        
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        df = pd.DataFrame({
            'close': np.random.uniform(45000, 50000, 100),
            'open': np.random.uniform(45000, 50000, 100),
            'high': np.random.uniform(46000, 51000, 100),
            'low': np.random.uniform(44000, 49000, 100),
            'volume': np.random.uniform(1000000, 2000000, 100)
        }, index=dates)
        
        df = ta.calculate_volume_analysis(df)
        
        assert 'Volume_MA_20' in df.columns
        
        print("  ✓ PASSED: Volume analysis calculation works correctly")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False


def test_identify_support_resistance():
    """Test support and resistance identification"""
    print("\nTesting support and resistance identification...")
    
    try:
        ta = TechnicalAnalyzer()
        
        dates = pd.date_range('2023-01-01', periods=250, freq='D')
        df = pd.DataFrame({
            'close': np.random.uniform(45000, 50000, 250),
            'open': np.random.uniform(45000, 50000, 250),
            'high': np.random.uniform(46000, 51000, 250),
            'low': np.random.uniform(44000, 49000, 250),
            'volume': np.random.uniform(1000000, 2000000, 250)
        }, index=dates)
        
        df = ta.calculate_moving_averages(df)
        sr = ta.identify_support_resistance(df)
        
        assert 'support_levels' in sr
        assert 'resistance_levels' in sr
        assert isinstance(sr['support_levels'], list)
        assert isinstance(sr['resistance_levels'], list)
        
        print("  ✓ PASSED: Support and resistance identification works correctly")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False


def test_comprehensive_analysis():
    """Test comprehensive analysis"""
    print("\nTesting comprehensive analysis...")
    
    try:
        ta = TechnicalAnalyzer()
        
        dates = pd.date_range('2023-01-01', periods=250, freq='D')
        df = pd.DataFrame({
            'close': np.random.uniform(45000, 50000, 250),
            'open': np.random.uniform(45000, 50000, 250),
            'high': np.random.uniform(46000, 51000, 250),
            'low': np.random.uniform(44000, 49000, 250),
            'volume': np.random.uniform(1000000, 2000000, 250)
        }, index=dates)
        
        analysis = ta.comprehensive_analysis(df)
        
        assert 'sentiment' in analysis
        assert 'sentiment_score' in analysis
        assert 'recommendation' in analysis
        assert 'signals' in analysis
        assert 'indicators' in analysis
        
        # Check that all indicator categories are present
        indicators = analysis['indicators']
        assert 'trend' in indicators
        assert 'ma_crossover' in indicators
        assert 'rsi' in indicators
        assert 'macd' in indicators
        assert 'bollinger_bands' in indicators
        assert 'volume' in indicators
        assert 'candlestick_patterns' in indicators
        assert 'support_resistance' in indicators
        
        # Check recommendation values
        valid_recommendations = ['STRONG BUY', 'BUY', 'WEAK BUY', 'HOLD', 'WEAK SELL', 'SELL', 'STRONG SELL']
        assert analysis['recommendation'] in valid_recommendations
        
        print("  ✓ PASSED: Comprehensive analysis works correctly")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False


def run_all_tests():
    """Run all technical analysis tests"""
    print("=" * 60)
    print("Running Technical Analysis Tests")
    print("=" * 60)
    
    tests = [
        test_technical_analyzer_initialization,
        test_prepare_dataframe,
        test_calculate_moving_averages,
        test_analyze_trend,
        test_detect_ma_crossover,
        test_calculate_rsi,
        test_analyze_rsi,
        test_calculate_macd,
        test_calculate_bollinger_bands,
        test_calculate_volume_analysis,
        test_identify_support_resistance,
        test_comprehensive_analysis
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ✗ Test crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    return all(results)


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
