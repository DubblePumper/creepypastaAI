"""
DeepL Translation Provider

This module implements the DeepL translation provider using the deep-translator library.
"""

import os
from typing import Optional, Dict, Any, List

from ..base_translator import BaseTranslationProvider


class DeepLProvider(BaseTranslationProvider):
    """
    DeepL translation provider implementation using deep-translator.
    
    Provides high-quality translations through the DeepL service
    using the deep-translator library wrapper.
    """
    
    # Language mappings for DeepL
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
        Initialize DeepL provider.
        
        Args:
            config: Configuration dictionary
        """
        self.deepl_class = None
        super().__init__(config)
    
    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "DeepL (deep-translator)"
    
    def _initialize(self) -> None:
        """Initialize DeepL client using deep-translator."""
        try:
            from deep_translator import DeepL
            self.deepl_class = DeepL
        except ImportError as e:
            raise Exception("deep-translator library not available. Install with: pip install deep-translator") from e
    
    def translate(self, text: str, target_language: str, source_language: str = "auto") -> str:
        """
        Translate text using DeepL.
        
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
            raise Exception(f"DeepL provider not available: {self.error_message}")
        
        if not text or not text.strip():
            return text
        
        try:
            # Convert language codes to DeepL format
            deepl_target = self.convert_language_code(target_language)
            deepl_source = self.convert_language_code(source_language) if source_language != "auto" else "auto"
            
            # Create translator instance
            translator = self.deepl_class(source=deepl_source, target=deepl_target)
            
            # Perform translation
            result = translator.translate(text)
            return result
            
        except Exception as e:
            self.logger.error(f"DeepL translation error: {e}")
            raise Exception(f"DeepL translation failed: {e}") from e
    
    def convert_language_code(self, language_code: str) -> str:
        """
        Convert standard language code to DeepL format.
        
        Args:
            language_code: Standard ISO 639-1 language code
            
        Returns:
            DeepL-specific language code
        """
        return self.LANGUAGE_MAPPINGS.get(language_code, language_code.upper())
    
    def get_supported_languages(self) -> List[str]:
        """
        Get supported languages for DeepL.
        
        Returns:
            List of supported language codes
        """
        return list(self.LANGUAGE_MAPPINGS.keys())
    
    def validate_language_support(self, language_code: str) -> bool:
        """
        Check if language is supported by DeepL.
        
        Args:
            language_code: Language code to check
            
        Returns:
            True if supported, False otherwise
        """
        return language_code in self.LANGUAGE_MAPPINGS
