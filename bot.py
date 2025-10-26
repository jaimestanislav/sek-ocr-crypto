"""
Main Cryptocurrency Bot with DeepSeek OCR Integration
"""
import argparse
import sys
from pathlib import Path

from config import Config
from ocr_module import DeepSeekOCR
from crypto_api import CryptoDataFetcher


class CryptoBot:
    """Main cryptocurrency bot class"""
    
    def __init__(self):
        """Initialize the crypto bot"""
        try:
            Config.validate()
            self.ocr = DeepSeekOCR()
            self.crypto_api = CryptoDataFetcher()
            print("✓ Crypto Bot initialized successfully")
        except ValueError as e:
            print(f"✗ Configuration error: {e}")
            sys.exit(1)
    
    def analyze_image(self, image_path: str, analysis_type: str = 'general') -> None:
        """
        Analyze a cryptocurrency-related image
        
        Args:
            image_path: Path to the image file
            analysis_type: Type of analysis ('general', 'chart', 'price')
        """
        print(f"\n{'='*60}")
        print(f"Analyzing image: {image_path}")
        print(f"Analysis type: {analysis_type}")
        print(f"{'='*60}\n")
        
        if not Path(image_path).exists():
            print(f"✗ Error: Image file not found: {image_path}")
            return
        
        # Perform OCR analysis based on type
        if analysis_type == 'chart':
            result = self.ocr.analyze_chart(image_path)
        elif analysis_type == 'price':
            result = self.ocr.read_price_screenshot(image_path)
        else:
            result = self.ocr.extract_crypto_data(image_path)
        
        # Display results
        if result['success']:
            print("✓ Analysis completed successfully\n")
            print("EXTRACTED DATA:")
            print("-" * 60)
            print(result['extracted_data'])
            print("-" * 60)
            print(f"\nTokens used: {result.get('tokens_used', 'N/A')}")
            print(f"Model: {result.get('model', 'N/A')}")
        else:
            print(f"✗ Analysis failed: {result.get('error', 'Unknown error')}")
    
    def get_crypto_price(self, coin_id: str) -> None:
        """
        Get current price for a cryptocurrency
        
        Args:
            coin_id: Cryptocurrency ID (e.g., 'bitcoin', 'ethereum')
        """
        print(f"\n{'='*60}")
        print(f"Fetching price data for: {coin_id}")
        print(f"{'='*60}\n")
        
        result = self.crypto_api.get_price(coin_id)
        
        if result['success']:
            data = result['data']
            print(f"✓ Price data retrieved successfully\n")
            print(f"Coin: {coin_id.upper()}")
            print(f"Price (USD): ${data.get('usd', 'N/A'):,.2f}" if isinstance(data.get('usd'), (int, float)) else f"Price (USD): {data.get('usd', 'N/A')}")
            
            if 'usd_24h_change' in data:
                change = data['usd_24h_change']
                emoji = "📈" if change > 0 else "📉"
                print(f"24h Change: {emoji} {change:+.2f}%")
            
            if 'usd_market_cap' in data:
                print(f"Market Cap: ${data['usd_market_cap']:,.0f}")
            
            if 'usd_24h_vol' in data:
                print(f"24h Volume: ${data['usd_24h_vol']:,.0f}")
        else:
            print(f"✗ Failed to get price: {result.get('error', 'Unknown error')}")
    
    def get_detailed_market_data(self, coin_id: str) -> None:
        """
        Get detailed market data for a cryptocurrency
        
        Args:
            coin_id: Cryptocurrency ID
        """
        print(f"\n{'='*60}")
        print(f"Fetching detailed market data for: {coin_id}")
        print(f"{'='*60}\n")
        
        result = self.crypto_api.get_market_data(coin_id)
        
        if result['success']:
            print(f"✓ Market data retrieved successfully\n")
            print(f"Name: {result.get('name', 'N/A')}")
            print(f"Symbol: {result.get('symbol', 'N/A')}")
            print(f"Current Price: ${result.get('current_price', 0):,.2f}")
            print(f"Market Cap: ${result.get('market_cap', 0):,.0f}")
            print(f"24h Volume: ${result.get('total_volume', 0):,.0f}")
            print(f"\nPrice Changes:")
            print(f"  24h: {result.get('price_change_24h', 0):+.2f}%")
            print(f"  7d:  {result.get('price_change_7d', 0):+.2f}%")
            print(f"  30d: {result.get('price_change_30d', 0):+.2f}%")
            print(f"\n24h Range:")
            print(f"  High: ${result.get('high_24h', 0):,.2f}")
            print(f"  Low:  ${result.get('low_24h', 0):,.2f}")
            print(f"\nAll-Time:")
            print(f"  High: ${result.get('ath', 0):,.2f}")
            print(f"  Low:  ${result.get('atl', 0):,.2f}")
        else:
            print(f"✗ Failed to get market data: {result.get('error', 'Unknown error')}")
    
    def search_crypto(self, query: str) -> None:
        """
        Search for cryptocurrencies
        
        Args:
            query: Search query
        """
        print(f"\n{'='*60}")
        print(f"Searching for: {query}")
        print(f"{'='*60}\n")
        
        result = self.crypto_api.search_coins(query)
        
        if result['success']:
            results = result['results']
            if results:
                print(f"✓ Found {len(results)} result(s):\n")
                for i, coin in enumerate(results, 1):
                    print(f"{i}. {coin.get('name', 'N/A')} ({coin.get('symbol', 'N/A').upper()})")
                    print(f"   ID: {coin.get('id', 'N/A')}")
                    print(f"   Market Cap Rank: #{coin.get('market_cap_rank', 'N/A')}")
                    print()
            else:
                print("No results found")
        else:
            print(f"✗ Search failed: {result.get('error', 'Unknown error')}")
    
    def get_trending(self) -> None:
        """Get trending cryptocurrencies"""
        print(f"\n{'='*60}")
        print("Trending Cryptocurrencies")
        print(f"{'='*60}\n")
        
        result = self.crypto_api.get_trending_coins()
        
        if result['success']:
            trending = result['trending']
            if trending:
                print(f"✓ Top {len(trending)} trending coins:\n")
                for i, item in enumerate(trending, 1):
                    coin = item.get('item', {})
                    print(f"{i}. {coin.get('name', 'N/A')} ({coin.get('symbol', 'N/A')})")
                    print(f"   Rank: #{coin.get('market_cap_rank', 'N/A')}")
                    if 'price_btc' in coin:
                        print(f"   Price (BTC): {coin['price_btc']}")
                    print()
            else:
                print("No trending data available")
        else:
            print(f"✗ Failed to get trending data: {result.get('error', 'Unknown error')}")


def main():
    """Main entry point for the crypto bot"""
    parser = argparse.ArgumentParser(
        description='DeepSeek OCR Cryptocurrency Bot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a crypto chart image
  python bot.py --analyze-image chart.png --type chart
  
  # Extract prices from screenshot
  python bot.py --analyze-image prices.png --type price
  
  # Get Bitcoin price
  python bot.py --price bitcoin
  
  # Get detailed market data
  python bot.py --market ethereum
  
  # Search for a cryptocurrency
  python bot.py --search cardano
  
  # Get trending cryptocurrencies
  python bot.py --trending
        """
    )
    
    parser.add_argument('--analyze-image', metavar='PATH', 
                       help='Analyze a cryptocurrency image')
    parser.add_argument('--type', choices=['general', 'chart', 'price'], 
                       default='general',
                       help='Type of image analysis (default: general)')
    parser.add_argument('--price', metavar='COIN_ID',
                       help='Get current price for a cryptocurrency')
    parser.add_argument('--market', metavar='COIN_ID',
                       help='Get detailed market data for a cryptocurrency')
    parser.add_argument('--search', metavar='QUERY',
                       help='Search for cryptocurrencies')
    parser.add_argument('--trending', action='store_true',
                       help='Get trending cryptocurrencies')
    
    args = parser.parse_args()
    
    # Show help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    # Initialize bot
    bot = CryptoBot()
    
    # Execute commands
    if args.analyze_image:
        bot.analyze_image(args.analyze_image, args.type)
    
    if args.price:
        bot.get_crypto_price(args.price)
    
    if args.market:
        bot.get_detailed_market_data(args.market)
    
    if args.search:
        bot.search_crypto(args.search)
    
    if args.trending:
        bot.get_trending()


if __name__ == '__main__':
    main()
