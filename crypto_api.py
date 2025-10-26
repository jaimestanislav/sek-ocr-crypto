"""
Cryptocurrency data fetching module
"""
import requests
from typing import Dict, List, Optional, Any
from config import Config


class CryptoDataFetcher:
    """Fetch cryptocurrency data from public APIs"""
    
    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize crypto data fetcher
        
        Args:
            api_url: Base URL for crypto API (optional)
        """
        self.api_url = api_url or Config.CRYPTO_API_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'DeepSeek-OCR-Crypto-Bot/1.0'
        })
    
    def get_price(self, coin_id: str, vs_currency: str = 'usd') -> Dict[str, Any]:
        """
        Get current price for a cryptocurrency
        
        Args:
            coin_id: Cryptocurrency ID (e.g., 'bitcoin', 'ethereum')
            vs_currency: Currency to compare against (default: 'usd')
            
        Returns:
            Dictionary with price information
        """
        try:
            url = f"{self.api_url}/simple/price"
            params = {
                'ids': coin_id,
                'vs_currencies': vs_currency,
                'include_24hr_change': 'true',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if coin_id in data:
                return {
                    'success': True,
                    'coin': coin_id,
                    'data': data[coin_id]
                }
            else:
                return {
                    'success': False,
                    'error': f'Coin {coin_id} not found'
                }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_multiple_prices(self, coin_ids: List[str], vs_currency: str = 'usd') -> Dict[str, Any]:
        """
        Get prices for multiple cryptocurrencies
        
        Args:
            coin_ids: List of cryptocurrency IDs
            vs_currency: Currency to compare against (default: 'usd')
            
        Returns:
            Dictionary with price information for all coins
        """
        try:
            url = f"{self.api_url}/simple/price"
            params = {
                'ids': ','.join(coin_ids),
                'vs_currencies': vs_currency,
                'include_24hr_change': 'true',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return {
                'success': True,
                'data': response.json()
            }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_market_data(self, coin_id: str) -> Dict[str, Any]:
        """
        Get detailed market data for a cryptocurrency
        
        Args:
            coin_id: Cryptocurrency ID
            
        Returns:
            Dictionary with detailed market data
        """
        try:
            url = f"{self.api_url}/coins/{coin_id}"
            params = {
                'localization': 'false',
                'tickers': 'false',
                'community_data': 'false',
                'developer_data': 'false'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract key information
            market_data = data.get('market_data', {})
            
            return {
                'success': True,
                'coin': coin_id,
                'name': data.get('name'),
                'symbol': data.get('symbol', '').upper(),
                'current_price': market_data.get('current_price', {}).get('usd'),
                'market_cap': market_data.get('market_cap', {}).get('usd'),
                'total_volume': market_data.get('total_volume', {}).get('usd'),
                'price_change_24h': market_data.get('price_change_percentage_24h'),
                'price_change_7d': market_data.get('price_change_percentage_7d'),
                'price_change_30d': market_data.get('price_change_percentage_30d'),
                'high_24h': market_data.get('high_24h', {}).get('usd'),
                'low_24h': market_data.get('low_24h', {}).get('usd'),
                'ath': market_data.get('ath', {}).get('usd'),
                'atl': market_data.get('atl', {}).get('usd')
            }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_coins(self, query: str) -> Dict[str, Any]:
        """
        Search for cryptocurrencies by name or symbol
        
        Args:
            query: Search query
            
        Returns:
            Dictionary with search results
        """
        try:
            url = f"{self.api_url}/search"
            params = {'query': query}
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            coins = data.get('coins', [])
            
            return {
                'success': True,
                'results': coins[:10]  # Limit to top 10 results
            }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_trending_coins(self) -> Dict[str, Any]:
        """
        Get currently trending cryptocurrencies
        
        Returns:
            Dictionary with trending coins
        """
        try:
            url = f"{self.api_url}/search/trending"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'success': True,
                'trending': data.get('coins', [])
            }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }
