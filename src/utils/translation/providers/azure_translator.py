"""
Azure Translator Provider

This module implements the Azure Translator translation provider.
"""

import os
import uuid
from typing import Optional, Dict, Any, List

from ..base_translator import BaseTranslationProvider


class AzureTranslatorProvider(BaseTranslationProvider):
    """
    Azure Translator translation provider implementation.
    
    Uses Microsoft Azure Cognitive Services Translator API
    for high-quality translations with enterprise features.
    """
    
    # Language mappings for Azure Translator
    LANGUAGE_MAPPINGS = {
        'zh': 'zh-Hans',  # Simplified Chinese for Azure
        'pt': 'pt-BR',    # Brazilian Portuguese as default
        'nb': 'no',       # Norwegian Bokmål
        'nn': 'no'        # Norwegian Nynorsk
    }
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Azure Translator provider.
        
        Args:
            config: Configuration dictionary
        """
        self.api_key = None
        self.region = None
        self.endpoint = None
        super().__init__(config)
    
    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "Azure Translator"
    
    def _initialize(self) -> None:
        """Initialize Azure Translator client."""
        try:
            import requests
        except ImportError as e:
            raise Exception("requests library not available. Install with: pip install requests") from e
        
        # Get API credentials from environment or config
        self.api_key = os.getenv("AZURE_TRANSLATOR_KEY") or self.config.get("api_key")
        self.region = self.config.get("region", "global")
        self.endpoint = self.config.get("endpoint", "https://api.cognitive.microsofttranslator.com/")
        
        if not self.api_key:
            raise Exception("AZURE_TRANSLATOR_KEY not found in environment variables or config")
        
        # Test the connection
        try:
            self._test_connection()
        except Exception as e:
            raise Exception(f"Failed to connect to Azure Translator: {e}") from e
    
    def _test_connection(self) -> None:
        """Test the Azure Translator connection."""
        import requests
        
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-type': 'application/json'
        }
        
        # Test with a simple request to get supported languages
        response = requests.get(
            f"{self.endpoint}/languages?api-version=3.0",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
    
    def translate(self, text: str, target_language: str, source_language: str = "auto") -> str:
        """
        Translate text using Azure Translator.
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code
            
        Returns:
            Translated text
            
        Raises:
            Exception: If translation fails
        """
        if not self.is_available:
            raise Exception(f"Azure Translator provider not available: {self.error_message}")
        
        if not text or not text.strip():
            return text
        
        try:
            import requests
            
            # Convert language codes for Azure if needed
            azure_target = self.convert_language_code(target_language)
            
            headers = {
                'Ocp-Apim-Subscription-Key': self.api_key,
                'Ocp-Apim-Subscription-Region': self.region,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4())
            }
            
            params = {
                'api-version': '3.0',
                'to': azure_target
            }
            
            if source_language != "auto":
                azure_source = self.convert_language_code(source_language)
                params['from'] = azure_source
            
            body = [{'text': text}]
            
            response = requests.post(
                f"{self.endpoint}/translate",
                params=params,
                headers=headers,
                json=body,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result[0]['translations'][0]['text']
            
        except Exception as e:
            self.logger.error(f"Azure Translator error: {e}")
            raise Exception(f"Azure Translator failed: {e}") from e
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect language using Azure Translator.
        
        Args:
            text: Text to analyze
            
        Returns:
            Detected language code or None if detection fails
        """
        if not self.is_available or not text or not text.strip():
            return None
        
        try:
            import requests
            
            headers = {
                'Ocp-Apim-Subscription-Key': self.api_key,
                'Ocp-Apim-Subscription-Region': self.region,
                'Content-type': 'application/json'
            }
            
            params = {'api-version': '3.0'}
            body = [{'text': text}]
            
            response = requests.post(
                f"{self.endpoint}/detect",
                params=params,
                headers=headers,
                json=body,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result[0]['language']
            
        except Exception as e:
            self.logger.debug(f"Azure Translator language detection failed: {e}")
            return None
    
    def convert_language_code(self, language_code: str) -> str:
        """
        Convert standard language code to Azure format.
        
        Args:
            language_code: Standard ISO 639-1 language code
            
        Returns:
            Azure-specific language code
        """
        return self.LANGUAGE_MAPPINGS.get(language_code, language_code)
    
    def get_supported_languages(self) -> List[str]:
        """
        Get supported languages for Azure Translator.
        
        This method fetches the current list of supported languages from Azure.
        
        Returns:
            List of supported language codes
        """
        if not self.is_available:
            return []
        
        try:
            import requests
            
            response = requests.get(
                f"{self.endpoint}/languages?api-version=3.0",
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            return list(result.get('translation', {}).keys())
            
        except Exception as e:
            self.logger.debug(f"Failed to fetch Azure supported languages: {e}")
            # Return a fallback list of common languages
            return [
                'af', 'ar', 'bg', 'bn', 'bs', 'ca', 'cs', 'cy', 'da', 'de',
                'el', 'en', 'es', 'et', 'fa', 'fi', 'fr', 'ga', 'gu', 'he',
                'hi', 'hr', 'hu', 'hy', 'id', 'is', 'it', 'ja', 'ka', 'kk',
                'km', 'kn', 'ko', 'ku', 'ky', 'lo', 'lt', 'lv', 'mg', 'mi',
                'mk', 'ml', 'mn', 'mr', 'ms', 'mt', 'my', 'nb', 'ne', 'nl',
                'nn', 'or', 'pa', 'pl', 'ps', 'pt', 'ro', 'ru', 'sk', 'sl',
                'sm', 'so', 'sq', 'sr-Cyrl', 'sr-Latn', 'sv', 'sw', 'ta',
                'te', 'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tr', 'tt', 'ty',
                'ug', 'uk', 'ur', 'uz', 'vi', 'xh', 'yi', 'yo', 'yua', 'yue',
                'zh-Hans', 'zh-Hant', 'zu'
            ]
