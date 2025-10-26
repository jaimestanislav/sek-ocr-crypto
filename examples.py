"""
Example usage of the DeepSeek OCR Crypto Bot
"""
from bot import CryptoBot


def example_price_check():
    """Example: Check cryptocurrency prices"""
    print("=" * 60)
    print("EXAMPLE 1: Price Check")
    print("=" * 60)
    
    bot = CryptoBot()
    
    # Check Bitcoin price
    bot.get_crypto_price('bitcoin')
    
    # Check Ethereum price
    bot.get_crypto_price('ethereum')


def example_market_data():
    """Example: Get detailed market data"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Detailed Market Data")
    print("=" * 60)
    
    bot = CryptoBot()
    
    # Get detailed data for Cardano
    bot.get_detailed_market_data('cardano')


def example_search():
    """Example: Search for cryptocurrencies"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Search Cryptocurrencies")
    print("=" * 60)
    
    bot = CryptoBot()
    
    # Search for Solana
    bot.search_crypto('solana')


def example_trending():
    """Example: Get trending cryptocurrencies"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Trending Cryptocurrencies")
    print("=" * 60)
    
    bot = CryptoBot()
    
    # Get trending coins
    bot.get_trending()


def example_ocr_analysis():
    """Example: Analyze crypto image (requires image file)"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: OCR Image Analysis")
    print("=" * 60)

    # Note: This requires an actual image file and DeepSeek API key
    # Uncomment and provide a real image path to test
    # bot = CryptoBot()
    # bot.analyze_image('path/to/crypto_chart.png', 'chart')

    print("\nTo test OCR functionality:")
    print("1. Save a cryptocurrency chart or price screenshot")
    print("2. Run: python bot.py --analyze-image <image_path> --type chart")


if __name__ == '__main__':
    # Run examples that don't require image files
    
    # Example 1: Price checks
    example_price_check()
    
    # Example 2: Market data
    example_market_data()
    
    # Example 3: Search
    example_search()
    
    # Example 4: Trending
    example_trending()
    
    # Example 5: OCR (informational only)
    example_ocr_analysis()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
