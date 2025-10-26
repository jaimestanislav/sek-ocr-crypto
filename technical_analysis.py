"""
Technical Analysis Module for Cryptocurrency Data
"""
import pandas as pd
import pandas_ta as ta
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime


class TechnicalAnalyzer:
    """Perform technical analysis on cryptocurrency data"""
    
    def __init__(self):
        """Initialize the technical analyzer"""
        pass
    
    def prepare_dataframe(self, ohlcv_data: List[List]) -> pd.DataFrame:
        """
        Convert OHLCV data to pandas DataFrame
        
        Args:
            ohlcv_data: List of [timestamp, open, high, low, close, volume]
            
        Returns:
            DataFrame with OHLCV data
        """
        df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        # Ensure numeric types
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def calculate_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate Simple and Exponential Moving Averages
        
        Args:
            df: DataFrame with OHLC data
            
        Returns:
            DataFrame with MA columns added
        """
        # Simple Moving Averages
        df['SMA_20'] = ta.sma(df['close'], length=20)
        df['SMA_50'] = ta.sma(df['close'], length=50)
        df['SMA_200'] = ta.sma(df['close'], length=200)
        
        # Exponential Moving Averages
        df['EMA_12'] = ta.ema(df['close'], length=12)
        df['EMA_26'] = ta.ema(df['close'], length=26)
        
        return df
    
    def analyze_trend(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze trend based on price vs MA 200
        
        Args:
            df: DataFrame with price and MA data
            
        Returns:
            Dictionary with trend analysis
        """
        if df.empty or 'SMA_200' not in df.columns:
            return {'trend': 'unknown', 'strength': 'unknown'}
        
        current_price = df['close'].iloc[-1]
        sma_200 = df['SMA_200'].iloc[-1]
        
        if pd.isna(sma_200):
            return {'trend': 'insufficient_data', 'strength': 'unknown'}
        
        if current_price > sma_200:
            percent_above = ((current_price - sma_200) / sma_200) * 100
            if percent_above > 10:
                strength = 'strong'
            elif percent_above > 5:
                strength = 'moderate'
            else:
                strength = 'weak'
            
            return {
                'trend': 'bullish',
                'strength': strength,
                'percent_from_sma200': percent_above,
                'current_price': current_price,
                'sma_200': sma_200
            }
        else:
            percent_below = ((sma_200 - current_price) / sma_200) * 100
            if percent_below > 10:
                strength = 'strong'
            elif percent_below > 5:
                strength = 'moderate'
            else:
                strength = 'weak'
            
            return {
                'trend': 'bearish',
                'strength': strength,
                'percent_from_sma200': -percent_below,
                'current_price': current_price,
                'sma_200': sma_200
            }
    
    def detect_ma_crossover(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect Golden Cross and Death Cross
        
        Args:
            df: DataFrame with MA data
            
        Returns:
            Dictionary with crossover information
        """
        if len(df) < 2 or 'SMA_50' not in df.columns or 'SMA_200' not in df.columns:
            return {'crossover': 'none', 'type': None}
        
        # Get last two values
        sma_50_prev = df['SMA_50'].iloc[-2]
        sma_50_curr = df['SMA_50'].iloc[-1]
        sma_200_prev = df['SMA_200'].iloc[-2]
        sma_200_curr = df['SMA_200'].iloc[-1]
        
        # Check for NaN values
        if any(pd.isna(val) for val in [sma_50_prev, sma_50_curr, sma_200_prev, sma_200_curr]):
            return {'crossover': 'none', 'type': None}
        
        # Golden Cross: SMA 50 crosses above SMA 200
        if sma_50_prev < sma_200_prev and sma_50_curr > sma_200_curr:
            return {
                'crossover': 'golden_cross',
                'type': 'bullish',
                'sma_50': sma_50_curr,
                'sma_200': sma_200_curr,
                'signal': 'Strong bullish signal - SMA 50 crossed above SMA 200'
            }
        
        # Death Cross: SMA 50 crosses below SMA 200
        if sma_50_prev > sma_200_prev and sma_50_curr < sma_200_curr:
            return {
                'crossover': 'death_cross',
                'type': 'bearish',
                'sma_50': sma_50_curr,
                'sma_200': sma_200_curr,
                'signal': 'Strong bearish signal - SMA 50 crossed below SMA 200'
            }
        
        # Current position
        if sma_50_curr > sma_200_curr:
            return {
                'crossover': 'none',
                'type': 'bullish_alignment',
                'sma_50': sma_50_curr,
                'sma_200': sma_200_curr,
                'signal': 'SMA 50 above SMA 200 (bullish alignment)'
            }
        else:
            return {
                'crossover': 'none',
                'type': 'bearish_alignment',
                'sma_50': sma_50_curr,
                'sma_200': sma_200_curr,
                'signal': 'SMA 50 below SMA 200 (bearish alignment)'
            }
    
    def calculate_rsi(self, df: pd.DataFrame, length: int = 14) -> pd.DataFrame:
        """
        Calculate Relative Strength Index
        
        Args:
            df: DataFrame with close prices
            length: RSI period (default: 14)
            
        Returns:
            DataFrame with RSI column added
        """
        df['RSI'] = ta.rsi(df['close'], length=length)
        return df
    
    def analyze_rsi(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze RSI values
        
        Args:
            df: DataFrame with RSI data
            
        Returns:
            Dictionary with RSI analysis
        """
        if df.empty or 'RSI' not in df.columns:
            return {'rsi': None, 'signal': 'unknown'}
        
        rsi = df['RSI'].iloc[-1]
        
        if pd.isna(rsi):
            return {'rsi': None, 'signal': 'insufficient_data'}
        
        if rsi >= 70:
            signal = 'overbought'
            interpretation = 'Potentially overbought - consider selling'
        elif rsi >= 60:
            signal = 'bullish'
            interpretation = 'Bullish momentum'
        elif rsi <= 30:
            signal = 'oversold'
            interpretation = 'Potentially oversold - consider buying'
        elif rsi <= 40:
            signal = 'bearish'
            interpretation = 'Bearish momentum'
        else:
            signal = 'neutral'
            interpretation = 'Neutral zone'
        
        return {
            'rsi': rsi,
            'signal': signal,
            'interpretation': interpretation
        }
    
    def calculate_macd(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            df: DataFrame with close prices
            
        Returns:
            DataFrame with MACD columns added
        """
        macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
        if macd is not None:
            df = pd.concat([df, macd], axis=1)
        return df
    
    def analyze_macd(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze MACD values
        
        Args:
            df: DataFrame with MACD data
            
        Returns:
            Dictionary with MACD analysis
        """
        if df.empty or 'MACD_12_26_9' not in df.columns:
            return {'macd': None, 'signal': 'unknown'}
        
        macd = df['MACD_12_26_9'].iloc[-1]
        signal = df['MACDs_12_26_9'].iloc[-1]
        histogram = df['MACDh_12_26_9'].iloc[-1]
        
        if any(pd.isna(val) for val in [macd, signal, histogram]):
            return {'macd': None, 'signal': 'insufficient_data'}
        
        # Determine signal based on MACD and signal line
        if macd > signal and histogram > 0:
            macd_signal = 'bullish'
            interpretation = 'MACD above signal line - bullish momentum'
        elif macd < signal and histogram < 0:
            macd_signal = 'bearish'
            interpretation = 'MACD below signal line - bearish momentum'
        else:
            macd_signal = 'neutral'
            interpretation = 'MACD crossing signal line'
        
        # Check for crossover in last period
        if len(df) >= 2:
            prev_histogram = df['MACDh_12_26_9'].iloc[-2]
            if not pd.isna(prev_histogram):
                if prev_histogram < 0 and histogram > 0:
                    macd_signal = 'bullish_crossover'
                    interpretation = 'MACD crossed above signal line - buy signal'
                elif prev_histogram > 0 and histogram < 0:
                    macd_signal = 'bearish_crossover'
                    interpretation = 'MACD crossed below signal line - sell signal'
        
        return {
            'macd': macd,
            'signal_line': signal,
            'histogram': histogram,
            'signal': macd_signal,
            'interpretation': interpretation
        }
    
    def calculate_bollinger_bands(self, df: pd.DataFrame, length: int = 20, std: float = 2.0) -> pd.DataFrame:
        """
        Calculate Bollinger Bands
        
        Args:
            df: DataFrame with close prices
            length: Period for moving average (default: 20)
            std: Standard deviations (default: 2.0)
            
        Returns:
            DataFrame with Bollinger Bands columns added
        """
        bbands = ta.bbands(df['close'], length=length, std=std)
        if bbands is not None:
            df = pd.concat([df, bbands], axis=1)
        return df
    
    def analyze_bollinger_bands(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze Bollinger Bands
        
        Args:
            df: DataFrame with Bollinger Bands data
            
        Returns:
            Dictionary with Bollinger Bands analysis
        """
        if df.empty or 'BBL_20_2.0' not in df.columns:
            return {'signal': 'unknown'}
        
        current_price = df['close'].iloc[-1]
        bb_lower = df['BBL_20_2.0'].iloc[-1]
        bb_middle = df['BBM_20_2.0'].iloc[-1]
        bb_upper = df['BBU_20_2.0'].iloc[-1]
        
        if any(pd.isna(val) for val in [bb_lower, bb_middle, bb_upper]):
            return {'signal': 'insufficient_data'}
        
        # Calculate position within bands
        bb_range = bb_upper - bb_lower
        if bb_range > 0:
            position = (current_price - bb_lower) / bb_range
        else:
            position = 0.5
        
        # Determine signal
        if current_price > bb_upper:
            signal = 'overbought'
            interpretation = 'Price above upper band - potentially overbought'
        elif current_price < bb_lower:
            signal = 'oversold'
            interpretation = 'Price below lower band - potentially oversold'
        elif position > 0.7:
            signal = 'approaching_upper'
            interpretation = 'Price approaching upper band'
        elif position < 0.3:
            signal = 'approaching_lower'
            interpretation = 'Price approaching lower band'
        else:
            signal = 'neutral'
            interpretation = 'Price within normal range'
        
        return {
            'lower_band': bb_lower,
            'middle_band': bb_middle,
            'upper_band': bb_upper,
            'current_price': current_price,
            'position': position,
            'signal': signal,
            'interpretation': interpretation
        }
    
    def calculate_volume_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate volume moving average
        
        Args:
            df: DataFrame with volume data
            
        Returns:
            DataFrame with volume MA added
        """
        df['Volume_MA_20'] = ta.sma(df['volume'], length=20)
        return df
    
    def analyze_volume(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze volume
        
        Args:
            df: DataFrame with volume data
            
        Returns:
            Dictionary with volume analysis
        """
        if df.empty or 'volume' not in df.columns or 'Volume_MA_20' not in df.columns:
            return {'signal': 'unknown'}
        
        current_volume = df['volume'].iloc[-1]
        volume_ma = df['Volume_MA_20'].iloc[-1]
        
        if pd.isna(volume_ma):
            return {
                'current_volume': current_volume,
                'volume_ma': None,
                'signal': 'insufficient_data'
            }
        
        volume_ratio = current_volume / volume_ma if volume_ma > 0 else 1
        
        if volume_ratio > 1.5:
            signal = 'high_volume'
            interpretation = 'Volume significantly above average - strong interest'
        elif volume_ratio > 1.2:
            signal = 'above_average'
            interpretation = 'Volume above average'
        elif volume_ratio < 0.5:
            signal = 'low_volume'
            interpretation = 'Volume significantly below average - low interest'
        elif volume_ratio < 0.8:
            signal = 'below_average'
            interpretation = 'Volume below average'
        else:
            signal = 'normal'
            interpretation = 'Volume near average'
        
        return {
            'current_volume': current_volume,
            'volume_ma': volume_ma,
            'volume_ratio': volume_ratio,
            'signal': signal,
            'interpretation': interpretation
        }
    
    def detect_candlestick_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect candlestick patterns
        
        Args:
            df: DataFrame with OHLC data
            
        Returns:
            Dictionary with detected patterns
        """
        patterns = {}
        
        try:
            # Doji pattern
            doji = ta.cdl_doji(df['open'], df['high'], df['low'], df['close'])
            if doji is not None and not doji.empty and doji.iloc[-1] != 0:
                patterns['doji'] = 'Doji pattern detected - potential reversal'
            
            # Inside bar pattern
            inside = ta.cdl_inside(df['open'], df['high'], df['low'], df['close'])
            if inside is not None and not inside.empty and inside.iloc[-1] != 0:
                patterns['inside_bar'] = 'Inside bar pattern detected - consolidation'
            
            # Z-score based pattern (extreme candles)
            cdl_z = ta.cdl_z(df['open'], df['high'], df['low'], df['close'])
            if cdl_z is not None and not cdl_z.empty:
                z_value = cdl_z.iloc[-1]
                if not pd.isna(z_value):
                    if z_value > 2:
                        patterns['bullish_extreme'] = 'Strong bullish candle detected'
                    elif z_value < -2:
                        patterns['bearish_extreme'] = 'Strong bearish candle detected'
        
        except Exception as e:
            # If pattern detection fails, return empty patterns
            pass
        
        return {
            'patterns_detected': list(patterns.keys()),
            'details': patterns,
            'count': len(patterns)
        }
    
    def identify_support_resistance(self, df: pd.DataFrame, window: int = 10) -> Dict[str, Any]:
        """
        Identify support and resistance levels using pivot points
        
        Args:
            df: DataFrame with OHLC data
            window: Window for finding local extrema
            
        Returns:
            Dictionary with support and resistance levels
        """
        if len(df) < window * 2:
            return {
                'support_levels': [],
                'resistance_levels': [],
                'dynamic_support': None,
                'dynamic_resistance': None
            }
        
        # Find local minima (support) and maxima (resistance)
        support_levels = []
        resistance_levels = []
        
        for i in range(window, len(df) - window):
            # Check for local minimum (support)
            if df['low'].iloc[i] == df['low'].iloc[i - window:i + window].min():
                support_levels.append(df['low'].iloc[i])
            
            # Check for local maximum (resistance)
            if df['high'].iloc[i] == df['high'].iloc[i - window:i + window].max():
                resistance_levels.append(df['high'].iloc[i])
        
        # Get unique levels and sort
        support_levels = sorted(set(support_levels))[-3:]  # Keep last 3 support levels
        resistance_levels = sorted(set(resistance_levels))[-3:]  # Keep last 3 resistance levels
        
        # Dynamic support/resistance from moving averages
        dynamic_support = None
        dynamic_resistance = None
        
        if 'SMA_50' in df.columns and not pd.isna(df['SMA_50'].iloc[-1]):
            dynamic_support = df['SMA_50'].iloc[-1]
        
        if 'SMA_200' in df.columns and not pd.isna(df['SMA_200'].iloc[-1]):
            dynamic_resistance = df['SMA_200'].iloc[-1]
        
        return {
            'support_levels': support_levels,
            'resistance_levels': resistance_levels,
            'dynamic_support': dynamic_support,
            'dynamic_resistance': dynamic_resistance
        }
    
    def comprehensive_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform comprehensive technical analysis
        
        Args:
            df: DataFrame with OHLC data
            
        Returns:
            Dictionary with complete analysis and recommendation
        """
        # Calculate all indicators
        df = self.calculate_moving_averages(df)
        df = self.calculate_rsi(df)
        df = self.calculate_macd(df)
        df = self.calculate_bollinger_bands(df)
        df = self.calculate_volume_analysis(df)
        
        # Perform analyses
        trend = self.analyze_trend(df)
        ma_cross = self.detect_ma_crossover(df)
        rsi_analysis = self.analyze_rsi(df)
        macd_analysis = self.analyze_macd(df)
        bb_analysis = self.analyze_bollinger_bands(df)
        volume_analysis = self.analyze_volume(df)
        patterns = self.detect_candlestick_patterns(df)
        support_resistance = self.identify_support_resistance(df)
        
        # Generate sentiment and recommendation
        sentiment_score = 0
        signals = []
        
        # Trend analysis (weight: 25%)
        if trend['trend'] == 'bullish':
            if trend['strength'] == 'strong':
                sentiment_score += 25
                signals.append('Strong bullish trend')
            elif trend['strength'] == 'moderate':
                sentiment_score += 15
                signals.append('Moderate bullish trend')
            else:
                sentiment_score += 10
                signals.append('Weak bullish trend')
        elif trend['trend'] == 'bearish':
            if trend['strength'] == 'strong':
                sentiment_score -= 25
                signals.append('Strong bearish trend')
            elif trend['strength'] == 'moderate':
                sentiment_score -= 15
                signals.append('Moderate bearish trend')
            else:
                sentiment_score -= 10
                signals.append('Weak bearish trend')
        
        # MA Crossover (weight: 20%)
        if ma_cross['crossover'] == 'golden_cross':
            sentiment_score += 20
            signals.append('Golden Cross detected!')
        elif ma_cross['crossover'] == 'death_cross':
            sentiment_score -= 20
            signals.append('Death Cross detected!')
        elif ma_cross['type'] == 'bullish_alignment':
            sentiment_score += 10
            signals.append('Bullish MA alignment')
        elif ma_cross['type'] == 'bearish_alignment':
            sentiment_score -= 10
            signals.append('Bearish MA alignment')
        
        # RSI (weight: 15%)
        if rsi_analysis['signal'] == 'oversold':
            sentiment_score += 15
            signals.append('RSI oversold - buy opportunity')
        elif rsi_analysis['signal'] == 'overbought':
            sentiment_score -= 15
            signals.append('RSI overbought - sell signal')
        elif rsi_analysis['signal'] == 'bullish':
            sentiment_score += 8
            signals.append('RSI bullish')
        elif rsi_analysis['signal'] == 'bearish':
            sentiment_score -= 8
            signals.append('RSI bearish')
        
        # MACD (weight: 15%)
        if macd_analysis['signal'] == 'bullish_crossover':
            sentiment_score += 15
            signals.append('MACD bullish crossover')
        elif macd_analysis['signal'] == 'bearish_crossover':
            sentiment_score -= 15
            signals.append('MACD bearish crossover')
        elif macd_analysis['signal'] == 'bullish':
            sentiment_score += 8
            signals.append('MACD bullish')
        elif macd_analysis['signal'] == 'bearish':
            sentiment_score -= 8
            signals.append('MACD bearish')
        
        # Bollinger Bands (weight: 10%)
        if bb_analysis['signal'] == 'oversold':
            sentiment_score += 10
            signals.append('Price below lower Bollinger Band')
        elif bb_analysis['signal'] == 'overbought':
            sentiment_score -= 10
            signals.append('Price above upper Bollinger Band')
        
        # Volume (weight: 10%)
        if volume_analysis['signal'] == 'high_volume':
            if sentiment_score > 0:
                sentiment_score += 10
                signals.append('High volume confirms bullish movement')
            else:
                sentiment_score -= 10
                signals.append('High volume confirms bearish movement')
        
        # Candlestick patterns (weight: 5%)
        if 'bullish_extreme' in patterns['patterns_detected']:
            sentiment_score += 5
            signals.append('Bullish extreme candle pattern')
        elif 'bearish_extreme' in patterns['patterns_detected']:
            sentiment_score -= 5
            signals.append('Bearish extreme candle pattern')
        elif 'doji' in patterns['patterns_detected']:
            signals.append('Doji pattern - potential reversal')
        
        # Generate recommendation
        if sentiment_score >= 50:
            recommendation = 'STRONG BUY'
            sentiment = 'Very Bullish'
        elif sentiment_score >= 30:
            recommendation = 'BUY'
            sentiment = 'Bullish'
        elif sentiment_score >= 10:
            recommendation = 'WEAK BUY'
            sentiment = 'Slightly Bullish'
        elif sentiment_score <= -50:
            recommendation = 'STRONG SELL'
            sentiment = 'Very Bearish'
        elif sentiment_score <= -30:
            recommendation = 'SELL'
            sentiment = 'Bearish'
        elif sentiment_score <= -10:
            recommendation = 'WEAK SELL'
            sentiment = 'Slightly Bearish'
        else:
            recommendation = 'HOLD'
            sentiment = 'Neutral'
        
        return {
            'timestamp': datetime.now().isoformat(),
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'recommendation': recommendation,
            'signals': signals,
            'indicators': {
                'trend': trend,
                'ma_crossover': ma_cross,
                'rsi': rsi_analysis,
                'macd': macd_analysis,
                'bollinger_bands': bb_analysis,
                'volume': volume_analysis,
                'candlestick_patterns': patterns,
                'support_resistance': support_resistance
            }
        }
