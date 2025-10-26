"""
Integration test for crypto API with technical analysis using mock data
"""
import os
import sys
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crypto_api import CryptoDataFetcher


def test_get_ohlc_data():
    """Test OHLC data fetching method exists and structure"""
    print("Testing get_ohlc_data method...")
    
    fetcher = CryptoDataFetcher()
    assert hasattr(fetcher, 'get_ohlc_data')
    print("  ✓ PASSED: get_ohlc_data method exists")
    return True


def test_get_market_chart():
    """Test market chart data fetching method exists"""
    print("\nTesting get_market_chart method...")
    
    fetcher = CryptoDataFetcher()
    assert hasattr(fetcher, 'get_market_chart')
    print("  ✓ PASSED: get_market_chart method exists")
    return True


def test_get_technical_analysis():
    """Test technical analysis method exists"""
    print("\nTesting get_technical_analysis method...")
    
    fetcher = CryptoDataFetcher()
    assert hasattr(fetcher, 'get_technical_analysis')
    print("  ✓ PASSED: get_technical_analysis method exists")
    return True


def test_technical_analysis_integration():
    """Test technical analysis integration with mock data"""
    print("\nTesting technical analysis integration with mock data...")
    
    try:
        # Create mock OHLC data (90 days)
        import numpy as np
        import time
        
        current_time = int(time.time() * 1000)
        day_ms = 24 * 60 * 60 * 1000
        
        # Generate realistic-looking OHLC data
        base_price = 45000
        mock_ohlc = []
        
        for i in range(90):
            timestamp = current_time - (90 - i) * day_ms
            # Add some randomness to make it realistic
            price_change = np.random.uniform(-0.05, 0.05)
            base_price = base_price * (1 + price_change)
            
            open_price = base_price
            high_price = base_price * (1 + abs(np.random.uniform(0, 0.02)))
            low_price = base_price * (1 - abs(np.random.uniform(0, 0.02)))
            close_price = np.random.uniform(low_price, high_price)
            
            mock_ohlc.append([
                timestamp,
                open_price,
                high_price,
                low_price,
                close_price
            ])
        
        # Mock the API response
        mock_response = {
            'success': True,
            'coin': 'bitcoin',
            'vs_currency': 'usd',
            'days': 90,
            'data': mock_ohlc
        }
        
        fetcher = CryptoDataFetcher()
        
        # Mock the get_ohlc_data method
        with patch.object(fetcher, 'get_ohlc_data', return_value=mock_response):
            result = fetcher.get_technical_analysis('bitcoin', days=90)
            
            assert result['success'] == True
            assert 'analysis' in result
            
            analysis = result['analysis']
            assert 'sentiment' in analysis
            assert 'recommendation' in analysis
            assert 'sentiment_score' in analysis
            assert 'indicators' in analysis
            
            # Check all indicator categories
            indicators = analysis['indicators']
            assert 'trend' in indicators
            assert 'ma_crossover' in indicators
            assert 'rsi' in indicators
            assert 'macd' in indicators
            assert 'bollinger_bands' in indicators
            assert 'volume' in indicators
            assert 'candlestick_patterns' in indicators
            assert 'support_resistance' in indicators
            
            print(f"  ✓ Analysis completed successfully")
            print(f"  Sentiment: {analysis['sentiment']}")
            print(f"  Recommendation: {analysis['recommendation']}")
            print(f"  Sentiment Score: {analysis['sentiment_score']}")
            print("  ✓ PASSED: Technical analysis integration works correctly")
            return True
            
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_technical_analyzer_initialization():
    """Test that TechnicalAnalyzer is initialized in CryptoDataFetcher"""
    print("\nTesting TechnicalAnalyzer initialization in CryptoDataFetcher...")
    
    fetcher = CryptoDataFetcher()
    assert hasattr(fetcher, 'ta')
    assert fetcher.ta is not None
    print("  ✓ PASSED: TechnicalAnalyzer initialized correctly")
    return True


def run_all_tests():
    """Run all integration tests"""
    print("=" * 60)
    print("Running Integration Tests")
    print("=" * 60)
    
    tests = [
        test_get_ohlc_data,
        test_get_market_chart,
        test_get_technical_analysis,
        test_technical_analyzer_initialization,
        test_technical_analysis_integration
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ✗ Test crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    return all(results)


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
