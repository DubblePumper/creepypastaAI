"""
DeepL API Provider

This module implements the official DeepL API translation provider.
"""

import os
from typing import Optional, Dict, Any, List

from ..base_translator import BaseTranslationProvider


class DeepLAPIProvider(BaseTranslationProvider):
    """
    Official DeepL API translation provider implementation.
    
    Uses the official DeepL Python library to access the DeepL Pro API.
    Requires a valid DeepL API key and subscription.
    """
    
    # Language mappings for DeepL API
    LANGUAGE_MAPPINGS = {
        'en': 'EN',
        'de': 'DE',
        'fr': 'FR',
        'es': 'ES',
        'it': 'IT',
        'pt': 'PT',
        'ru': 'RU',
        'ja': 'JA',
        'zh': 'ZH',
        'nl': 'NL',
        'ko': 'KO',
        'pl': 'PL',
        'da': 'DA',
        'sv': 'SV',
        'fi': 'FI',
        'el': 'EL',
        'cs': 'CS',
        'et': 'ET',
        'lv': 'LV',
        'lt': 'LT',
        'sk': 'SK',
        'sl': 'SL',
        'bg': 'BG',
        'hu': 'HU',
        'ro': 'RO',
        'uk': 'UK',
        'tr': 'TR',
        'ar': 'AR',
        'hi': 'HI',
        'id': 'ID',
        'nb': 'NB'
    }
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize DeepL API provider.
        
        Args:
            config: Configuration dictionary
        """
        self.client = None
        self.api_key = None
        super().__init__(config)
    
    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "DeepL API (Official)"
    
    def _initialize(self) -> None:
        """Initialize DeepL API client."""
        try:
            import deepl
        except ImportError as e:
            raise Exception("deepl library not available. Install with: pip install deepl") from e
        
        # Get API key from environment or config
        self.api_key = os.getenv("DEEPL_API_KEY") or self.config.get("api_key")
        
        if not self.api_key:
            raise Exception("DEEPL_API_KEY not found in environment variables or config")
        
        try:
            self.client = deepl.Translator(self.api_key)
            # Test the connection
            self.client.get_usage()
        except Exception as e:
            raise Exception(f"Failed to initialize DeepL API client: {e}") from e
    
    def translate(self, text: str, target_language: str, source_language: str = "auto") -> str:
        """
        Translate text using DeepL API.
        
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
            raise Exception(f"DeepL API provider not available: {self.error_message}")
        
        if not text or not text.strip():
            return text
        
        try:
            # Convert language codes to DeepL format
            deepl_target = self.convert_language_code(target_language)
            deepl_source = self.convert_language_code(source_language) if source_language != "auto" else None
            
            # Get translation settings from config
            formality = self.config.get("formality", "default")
            preserve_formatting = self.config.get("preserve_formatting", True)
            
            # Perform translation
            result = self.client.translate_text(
                text,
                target_lang=deepl_target,
                source_lang=deepl_source,
                formality=formality,
                preserve_formatting=preserve_formatting
            )
            
            return result.text
            
        except Exception as e:
            self.logger.error(f"DeepL API translation error: {e}")
            raise Exception(f"DeepL API translation failed: {e}") from e
    
    def convert_language_code(self, language_code: str) -> str:
        """
        Convert standard language code to DeepL API format.
        
        Args:
            language_code: Standard ISO 639-1 language code
            
        Returns:
            DeepL API-specific language code
        """
        return self.LANGUAGE_MAPPINGS.get(language_code, language_code.upper())
    
    def get_supported_languages(self) -> List[str]:
        """
        Get supported languages for DeepL API.
        
        Returns:
            List of supported language codes
        """
        return list(self.LANGUAGE_MAPPINGS.keys())
    
    def validate_language_support(self, language_code: str) -> bool:
        """
        Check if language is supported by DeepL API.
        
        Args:
            language_code: Language code to check
            
        Returns:
            True if supported, False otherwise
        """
        return language_code in self.LANGUAGE_MAPPINGS
    
    def get_usage_info(self) -> Dict[str, Any]:
        """
        Get API usage information.
        
        Returns:
            Dictionary containing usage statistics
        """
        if not self.is_available:
            return {"error": "Provider not available"}
        
        try:
            usage = self.client.get_usage()
            return {
                "character_count": usage.character.count,
                "character_limit": usage.character.limit,
                "character_usage_percent": (usage.character.count / usage.character.limit * 100) if usage.character.limit > 0 else 0
            }
        except Exception as e:
            self.logger.error(f"Failed to get DeepL API usage: {e}")
            return {"error": str(e)}
