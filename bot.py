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
    
    def get_technical_analysis(self, coin_id: str, days: int = 90) -> None:
        """
        Get comprehensive technical analysis for a cryptocurrency
        
        Args:
            coin_id: Cryptocurrency ID
            days: Number of days of data to analyze
        """
        print(f"\n{'='*60}")
        print(f"Technical Analysis: {coin_id}")
        print(f"{'='*60}\n")
        
        result = self.crypto_api.get_technical_analysis(coin_id, days=days)
        
        if result['success']:
            analysis = result['analysis']
            
            print(f"✓ Technical analysis completed\n")
            print(f"{'='*60}")
            print(f"OVERALL SENTIMENT: {analysis['sentiment']}")
            print(f"RECOMMENDATION: {analysis['recommendation']}")
            print(f"Sentiment Score: {analysis['sentiment_score']}/100")
            print(f"{'='*60}\n")
            
            # Key signals
            if analysis['signals']:
                print("KEY SIGNALS:")
                for signal in analysis['signals']:
                    print(f"  • {signal}")
                print()
            
            # Trend Analysis
            print(f"{'='*60}")
            print("TREND ANALYSIS")
            print(f"{'='*60}")
            trend = analysis['indicators']['trend']
            if trend.get('trend') not in ['unknown', 'insufficient_data']:
                print(f"Trend: {trend['trend'].upper()}")
                print(f"Strength: {trend['strength']}")
                if 'percent_from_sma200' in trend:
                    print(f"Distance from SMA 200: {trend['percent_from_sma200']:.2f}%")
                print()
            else:
                print("Insufficient data for trend analysis\n")
            
            # Moving Average Crossover
            print(f"{'='*60}")
            print("MOVING AVERAGE CROSSOVER")
            print(f"{'='*60}")
            ma_cross = analysis['indicators']['ma_crossover']
            print(f"Status: {ma_cross.get('signal', 'N/A')}")
            if ma_cross.get('crossover') != 'none':
                print(f"Type: {ma_cross.get('crossover', 'N/A').replace('_', ' ').upper()}")
            print()
            
            # RSI
            print(f"{'='*60}")
            print("RSI (Relative Strength Index)")
            print(f"{'='*60}")
            rsi = analysis['indicators']['rsi']
            if rsi.get('rsi') is not None:
                print(f"RSI Value: {rsi['rsi']:.2f}")
                print(f"Signal: {rsi['signal']}")
                print(f"Interpretation: {rsi['interpretation']}")
                print()
            else:
                print("Insufficient data for RSI\n")
            
            # MACD
            print(f"{'='*60}")
            print("MACD (Moving Average Convergence Divergence)")
            print(f"{'='*60}")
            macd = analysis['indicators']['macd']
            if macd.get('macd') is not None:
                print(f"MACD: {macd['macd']:.2f}")
                print(f"Signal Line: {macd['signal_line']:.2f}")
                print(f"Histogram: {macd['histogram']:.2f}")
                print(f"Signal: {macd['signal']}")
                print(f"Interpretation: {macd['interpretation']}")
                print()
            else:
                print("Insufficient data for MACD\n")
            
            # Bollinger Bands
            print(f"{'='*60}")
            print("BOLLINGER BANDS")
            print(f"{'='*60}")
            bb = analysis['indicators']['bollinger_bands']
            if bb.get('signal') not in ['unknown', 'insufficient_data']:
                print(f"Upper Band: ${bb['upper_band']:,.2f}")
                print(f"Middle Band: ${bb['middle_band']:,.2f}")
                print(f"Lower Band: ${bb['lower_band']:,.2f}")
                print(f"Current Price: ${bb['current_price']:,.2f}")
                print(f"Position: {bb['position']:.2%}")
                print(f"Signal: {bb['signal']}")
                print(f"Interpretation: {bb['interpretation']}")
                print()
            else:
                print("Insufficient data for Bollinger Bands\n")
            
            # Volume Analysis
            print(f"{'='*60}")
            print("VOLUME ANALYSIS")
            print(f"{'='*60}")
            volume = analysis['indicators']['volume']
            if volume.get('signal') not in ['unknown', 'insufficient_data']:
                print(f"Current Volume: {volume['current_volume']:,.0f}")
                print(f"Volume MA (20): {volume['volume_ma']:,.0f}")
                print(f"Volume Ratio: {volume['volume_ratio']:.2f}x")
                print(f"Signal: {volume['signal']}")
                print(f"Interpretation: {volume['interpretation']}")
                print()
            else:
                print("Insufficient data for volume analysis\n")
            
            # Candlestick Patterns
            print(f"{'='*60}")
            print("CANDLESTICK PATTERNS")
            print(f"{'='*60}")
            patterns = analysis['indicators']['candlestick_patterns']
            if patterns['count'] > 0:
                print(f"Patterns Detected: {patterns['count']}")
                for pattern, description in patterns['details'].items():
                    print(f"  • {pattern.replace('_', ' ').title()}: {description}")
                print()
            else:
                print("No significant candlestick patterns detected\n")
            
            # Support and Resistance
            print(f"{'='*60}")
            print("SUPPORT AND RESISTANCE LEVELS")
            print(f"{'='*60}")
            sr = analysis['indicators']['support_resistance']
            
            if sr['support_levels']:
                print("Support Levels:")
                for level in sr['support_levels']:
                    print(f"  ${level:,.2f}")
            else:
                print("Support Levels: Not detected")
            
            if sr['resistance_levels']:
                print("\nResistance Levels:")
                for level in sr['resistance_levels']:
                    print(f"  ${level:,.2f}")
            else:
                print("Resistance Levels: Not detected")
            
            print(f"\nDynamic Support (SMA 50): ${sr['dynamic_support']:,.2f}" if sr['dynamic_support'] else "\nDynamic Support: Not available")
            print(f"Dynamic Resistance (SMA 200): ${sr['dynamic_resistance']:,.2f}" if sr['dynamic_resistance'] else "Dynamic Resistance: Not available")
            print()
            
        else:
            print(f"✗ Failed to get technical analysis: {result.get('error', 'Unknown error')}")


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
  
  # Get technical analysis
  python bot.py --technical bitcoin --days 90
  
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
    parser.add_argument('--technical', metavar='COIN_ID',
                       help='Get technical analysis for a cryptocurrency')
    parser.add_argument('--days', type=int, default=90,
                       help='Number of days for technical analysis (default: 90)')
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
    
    if args.technical:
        bot.get_technical_analysis(args.technical, args.days)
    
    if args.search:
        bot.search_crypto(args.search)
    
    if args.trending:
        bot.get_trending()


if __name__ == '__main__':
    main()
