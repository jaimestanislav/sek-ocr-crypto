"""
Basic tests for the crypto bot modules
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unittest.mock import patch
from config import Config
from crypto_api import CryptoDataFetcher
from ocr_module import DeepSeekOCR


def test_config_validation():
    """Test configuration validation"""
    print("Testing configuration validation...")
    
    # Save original key
    original_key = os.environ.get('DEEPSEEK_API_KEY', '')
    
    # Test missing key
    os.environ['DEEPSEEK_API_KEY'] = ''
    Config.DEEPSEEK_API_KEY = ''
    
    try:
        Config.validate()
        print("  ✗ FAILED: Should raise ValueError for missing key")
        return False
    except ValueError as e:
        print(f"  ✓ PASSED: Correctly raised ValueError: {e}")
    
    # Test with key
    os.environ['DEEPSEEK_API_KEY'] = 'test_key'
    Config.DEEPSEEK_API_KEY = 'test_key'
    
    try:
        Config.validate()
        print("  ✓ PASSED: Validation successful with key")
    except ValueError as e:
        print(f"  ✗ FAILED: Should not raise error with key: {e}")
        return False
    
    # Restore original key
    if original_key:
        os.environ['DEEPSEEK_API_KEY'] = original_key
        Config.DEEPSEEK_API_KEY = original_key
    
    return True


def test_crypto_api_initialization():
    """Test CryptoDataFetcher initialization"""
    print("\nTesting CryptoDataFetcher initialization...")
    
    try:
        fetcher = CryptoDataFetcher()
        assert fetcher.api_url == Config.CRYPTO_API_URL
        print("  ✓ PASSED: CryptoDataFetcher initialized correctly")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False


def test_ocr_initialization():
    """Test DeepSeekOCR initialization"""
    print("\nTesting DeepSeekOCR initialization...")
    
    # Set test API key
    os.environ['DEEPSEEK_API_KEY'] = 'test_key'
    Config.DEEPSEEK_API_KEY = 'test_key'
    
    try:
        with patch('ocr_module.OpenAI'):
            ocr = DeepSeekOCR()
            assert ocr.model == Config.OCR_MODEL
            print("  ✓ PASSED: DeepSeekOCR initialized correctly")
            return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False


def test_image_validation():
    """Test image validation"""
    print("\nTesting image validation...")
    
    os.environ['DEEPSEEK_API_KEY'] = 'test_key'
    Config.DEEPSEEK_API_KEY = 'test_key'
    
    try:
        with patch('ocr_module.OpenAI'):
            ocr = DeepSeekOCR()
            
            # Test non-existent file
            result = ocr.validate_image('nonexistent.png')
            assert result is False
            print("  ✓ PASSED: Correctly rejects non-existent file")
            
            return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False


def test_crypto_api_methods():
    """Test CryptoDataFetcher methods structure"""
    print("\nTesting CryptoDataFetcher methods...")
    
    try:
        fetcher = CryptoDataFetcher()
        
        # Check that methods exist
        assert hasattr(fetcher, 'get_price')
        assert hasattr(fetcher, 'get_multiple_prices')
        assert hasattr(fetcher, 'get_market_data')
        assert hasattr(fetcher, 'search_coins')
        assert hasattr(fetcher, 'get_trending_coins')
        
        print("  ✓ PASSED: All required methods exist")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False


def test_ocr_methods():
    """Test DeepSeekOCR methods structure"""
    print("\nTesting DeepSeekOCR methods...")
    
    os.environ['DEEPSEEK_API_KEY'] = 'test_key'
    Config.DEEPSEEK_API_KEY = 'test_key'
    
    try:
        with patch('ocr_module.OpenAI'):
            ocr = DeepSeekOCR()
            
            # Check that methods exist
            assert hasattr(ocr, 'encode_image')
            assert hasattr(ocr, 'validate_image')
            assert hasattr(ocr, 'extract_crypto_data')
            assert hasattr(ocr, 'analyze_chart')
            assert hasattr(ocr, 'read_price_screenshot')
            
            print("  ✓ PASSED: All required methods exist")
            return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Crypto Bot Tests")
    print("=" * 60)
    
    tests = [
        test_config_validation,
        test_crypto_api_initialization,
        test_ocr_initialization,
        test_image_validation,
        test_crypto_api_methods,
        test_ocr_methods
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
