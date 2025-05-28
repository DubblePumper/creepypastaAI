"""
Google Translate Provider

This module implements the Google Translate translation provider
using the googletrans library.
"""

import os
from typing import Optional, Dict, Any, List

from ..base_translator import BaseTranslationProvider


class GoogleTranslateProvider(BaseTranslationProvider):
    """
    Google Translate translation provider implementation.
    
    Uses the unofficial googletrans library to provide translation services.
    This is a free service but may have rate limitations.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Google Translate provider.
        
        Args:
            config: Configuration dictionary
        """
        self.client = None
        super().__init__(config)
    
    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "Google Translate"
    
    def _initialize(self) -> None:
        """Initialize Google Translate client."""
        try:
            from googletrans import Translator
            self.client = Translator()
        except ImportError as e:
            raise Exception("googletrans library not available. Install with: pip install googletrans==4.0.0-rc1") from e
    
    def translate(self, text: str, target_language: str, source_language: str = "auto") -> str:
        """
        Translate text using Google Translate.
        
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
            raise Exception(f"Google Translate provider not available: {self.error_message}")
        
        if not text or not text.strip():
            return text
        
        try:
            result = self.client.translate(text, dest=target_language, src=source_language)
            return result.text
        except Exception as e:
            self.logger.error(f"Google Translate error: {e}")
            raise Exception(f"Google Translate failed: {e}") from e
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect language using Google Translate.
        
        Args:
            text: Text to analyze
            
        Returns:
            Detected language code or None if detection fails
        """
        if not self.is_available or not text or not text.strip():
            return None
        
        try:
            result = self.client.detect(text)
            return result.lang
        except Exception as e:
            self.logger.debug(f"Google Translate language detection failed: {e}")
            return None
    
    def get_supported_languages(self) -> List[str]:
        """
        Get supported languages for Google Translate.
        
        Returns:
            List of supported language codes
        """
        # Google Translate supports a wide range of languages
        # This is a subset of the most commonly used ones
        return [
            'af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs',
            'bg', 'ca', 'ceb', 'zh', 'co', 'hr', 'cs', 'da', 'nl', 'en',
            'eo', 'et', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu',
            'ht', 'ha', 'haw', 'he', 'hi', 'hmn', 'hu', 'is', 'ig', 'id',
            'ga', 'it', 'ja', 'jv', 'kn', 'kk', 'km', 'rw', 'ko', 'ku',
            'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml',
            'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'ny', 'or', 'ps',
            'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st',
            'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv',
            'tl', 'tg', 'ta', 'tt', 'te', 'th', 'tr', 'tk', 'uk', 'ur',
            'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu'
        ]
