"""
DeepSeek OCR Crypto Bot Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for the crypto bot"""
    
    # DeepSeek API Configuration
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
    DEEPSEEK_API_BASE = os.getenv('DEEPSEEK_API_BASE', 'https://api.deepseek.com')
    
    # Telegram Bot Configuration (optional)
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    
    # Crypto API Configuration
    CRYPTO_API_URL = os.getenv('CRYPTO_API_URL', 'https://api.coingecko.com/api/v3')
    
    # OCR Model Configuration
    OCR_MODEL = os.getenv('OCR_MODEL', 'deepseek-chat')
    OCR_TEMPERATURE = float(os.getenv('OCR_TEMPERATURE', '0.0'))
    OCR_MAX_TOKENS = int(os.getenv('OCR_MAX_TOKENS', '2000'))
    
    # Bot Configuration
    MAX_IMAGE_SIZE = int(os.getenv('MAX_IMAGE_SIZE', '5242880'))  # 5MB default
    SUPPORTED_IMAGE_FORMATS = ['png', 'jpg', 'jpeg', 'webp']
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY is required. Set it in .env file")
        return True
