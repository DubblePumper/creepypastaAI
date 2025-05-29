"""
DeepL API Provider

This module provides DeepL translation functionality using the official DeepL API.
Requires a DeepL API key and has usage-based pricing.
"""

from typing import Dict, List, Optional, Any
from ..base_translator import BaseTranslationProvider

try:
    import deepl
    DEEPL_API_AVAILABLE = True
except ImportError:
    DEEPL_API_AVAILABLE = False
    deepl = None


class DeepLAPIProvider(BaseTranslationProvider):
    """
    DeepL translation provider using the official DeepL API.
    
    This provider uses the official DeepL API which requires an API key
    but provides higher quality translations and better rate limits.
    """
    
    def _initialize(self):
        """Initialize the DeepL API client."""
        if not DEEPL_API_AVAILABLE or deepl is None:
            raise ImportError(
                "deepl library is not installed. "
                "Install it with: pip install deepl"
            )
        
        api_key = self.config.get('api_key')
        if not api_key:
            raise ValueError("DeepL API key is required")
        
        try:
            self.translator = deepl.Translator(api_key)
            self.logger.info("DeepL API provider initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize DeepL API: {e}")
            raise
    
    def translate_text(
        self, 
        text: str, 
        target_language: str, 
        source_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate text using DeepL API.
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (auto-detect if None)
              Returns:
            Translation result dictionary
        """
        if not text.strip():
            return self._create_error_response("Empty text provided")
        
        try:
            # Perform translation
            result = self.translator.translate_text(
                text,
                target_lang=target_language.upper(),
                source_lang=source_language.upper() if source_language else None
            )
            
            # Handle both single result and list of results
            if isinstance(result, list):
                if len(result) > 0:
                    first_result = result[0]
                    translated_text = first_result.text
                    detected_lang = first_result.detected_source_lang
                else:
                    return self._create_error_response("No translation result received")
            else:
                translated_text = result.text
                detected_lang = result.detected_source_lang
            
            return self._create_success_response(
                translated_text=translated_text,
                source_language=detected_lang.lower() if detected_lang else (source_language or 'auto').lower(),
                target_language=target_language.lower()
            )
            
        except Exception as e:
            error_msg = f"DeepL API error: {str(e)}"
            self.logger.error(error_msg)
            return self._create_error_response(error_msg)
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect language using DeepL API.
        
        Note: DeepL API doesn't have a dedicated language detection endpoint,
        but detection happens during translation.
        
        Args:
            text: Text to analyze
            
        Returns:
            Language detection result dictionary        """
        if not text.strip():
            return self._create_error_response("Empty text provided")
        
        try:
            # Use translation to English to detect source language
            result = self.translator.translate_text(text, target_lang="EN")
            
            # Handle both single result and list of results
            if isinstance(result, list):
                if len(result) > 0:
                    detected_lang = result[0].detected_source_lang
                else:
                    return self._create_error_response("No detection result received")
            else:
                detected_lang = result.detected_source_lang
            
            return self._create_success_response(
                language_code=detected_lang.lower() if detected_lang else 'unknown'
            )
            
        except Exception as e:
            error_msg = f"Language detection error: {str(e)}"
            self.logger.error(error_msg)
            return self._create_error_response(error_msg)
    
    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported language codes.
        
        Returns:
            List of supported language codes
        """
        try:
            source_langs = self.translator.get_source_languages()
            target_langs = self.translator.get_target_languages()
            
            # Combine and deduplicate
            all_langs = set()
            for lang in source_langs:
                all_langs.add(lang.code.lower())
            for lang in target_langs:
                all_langs.add(lang.code.lower())
            
            return list(all_langs)
            
        except Exception as e:
            self.logger.error(f"Error getting supported languages: {e}")
            return []