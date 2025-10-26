"""
DeepSeek OCR Module for processing crypto-related images
"""
import base64
import os
from typing import Optional, Dict, Any
from pathlib import Path
from openai import OpenAI
from PIL import Image

from config import Config


class DeepSeekOCR:
    """DeepSeek OCR class for processing images with vision capabilities"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize DeepSeek OCR client
        
        Args:
            api_key: DeepSeek API key (optional, will use config if not provided)
        """
        self.api_key = api_key or Config.DEEPSEEK_API_KEY
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=Config.DEEPSEEK_API_BASE
        )
        self.model = Config.OCR_MODEL
    
    def encode_image(self, image_path: str) -> str:
        """
        Encode image to base64 string
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Base64 encoded image string
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def validate_image(self, image_path: str) -> bool:
        """
        Validate image file
        
        Args:
            image_path: Path to the image file
            
        Returns:
            True if valid, False otherwise
        """
        if not os.path.exists(image_path):
            return False
        
        # Check file size
        file_size = os.path.getsize(image_path)
        if file_size > Config.MAX_IMAGE_SIZE:
            return False
        
        # Check file format
        extension = Path(image_path).suffix.lower().strip('.')
        if extension not in Config.SUPPORTED_IMAGE_FORMATS:
            return False
        
        # Validate it's a valid image
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except Exception:
            return False
    
    def extract_crypto_data(self, image_path: str, custom_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Extract cryptocurrency data from an image using DeepSeek OCR
        
        Args:
            image_path: Path to the image containing crypto information
            custom_prompt: Custom prompt for OCR (optional)
            
        Returns:
            Dictionary containing extracted data and analysis
        """
        if not self.validate_image(image_path):
            return {
                "success": False,
                "error": "Invalid image file"
            }
        
        # Default prompt for crypto data extraction
        default_prompt = """Analyze this image and extract any cryptocurrency-related information.
        Look for:
        - Cryptocurrency names and symbols (BTC, ETH, etc.)
        - Prices and price changes
        - Trading volumes
        - Market cap information
        - Chart patterns and trends
        - Any other relevant crypto data
        
        Provide a structured analysis of what you find."""
        
        prompt = custom_prompt or default_prompt
        
        try:
            # Encode the image
            base64_image = self.encode_image(image_path)
            
            # Create the message with image
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                temperature=Config.OCR_TEMPERATURE,
                max_tokens=Config.OCR_MAX_TOKENS
            )
            
            # Extract the response
            extracted_text = response.choices[0].message.content
            
            return {
                "success": True,
                "extracted_data": extracted_text,
                "model": self.model,
                "tokens_used": response.usage.total_tokens
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def analyze_chart(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze a cryptocurrency chart image
        
        Args:
            image_path: Path to the chart image
            
        Returns:
            Dictionary containing chart analysis
        """
        chart_prompt = """Analyze this cryptocurrency chart in detail.
        
        Please provide:
        1. Trend direction (bullish, bearish, or sideways)
        2. Key support and resistance levels visible
        3. Any chart patterns (triangles, head and shoulders, etc.)
        4. Volume analysis if visible
        5. Time frame if visible
        6. Overall market sentiment based on the chart
        
        Be specific and provide actionable insights."""
        
        return self.extract_crypto_data(image_path, chart_prompt)
    
    def read_price_screenshot(self, image_path: str) -> Dict[str, Any]:
        """
        Read cryptocurrency prices from a screenshot
        
        Args:
            image_path: Path to the screenshot
            
        Returns:
            Dictionary containing price information
        """
        price_prompt = """Extract all cryptocurrency prices from this screenshot.
        
        For each cryptocurrency found, provide:
        1. Symbol/Name
        2. Current price
        3. Price change (if visible)
        4. Percentage change (if visible)
        
        Format the output in a clear, structured way."""
        
        return self.extract_crypto_data(image_path, price_prompt)
