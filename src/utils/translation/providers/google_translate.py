"""
Google Translate Provider

This module provides Google Translate functionality using the googletrans library.
This is a free service that doesn't require API keys but has usage limitations.

Dependencies:
    googletrans (optional): Install with `pip install googletrans==4.0.0-rc1`
    
Note:
    The googletrans import error is expected if the library is not installed.
    The provider will gracefully handle missing dependencies and provide 
    appropriate error messages during initialization.
"""

from typing import Dict, List, Optional, Any
from ..base_translator import BaseTranslationProvider

try:
    from googletrans import Translator, LANGUAGES  # type: ignore[import-untyped]
    GOOGLETRANS_AVAILABLE = True
except ImportError:
    GOOGLETRANS_AVAILABLE = False
    Translator = None  # type: ignore[misc,assignment]
    LANGUAGES = {}


class GoogleTranslateProvider(BaseTranslationProvider):
    """
    Google Translate provider using the googletrans library.
    
    This provider uses the free Google Translate service through the googletrans
    library. It doesn't require API keys but has rate limits and usage restrictions.
    """
    
    def _initialize(self):
        """
        Initialize the Google Translate client.
        
        Raises:
            ImportError: If googletrans library is not installed
            Exception: If initialization fails for other reasons
        """
        if not GOOGLETRANS_AVAILABLE:
            raise ImportError(
                "googletrans library is not installed. "
                "Install it with: pip install googletrans==4.0.0-rc1"
            )
        
        try:
            if Translator is None:
                raise ImportError("Translator class not available")
            self.translator = Translator()
            self.languages = LANGUAGES or {}
            self.logger.info("Google Translate provider initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Google Translate: {e}")
            raise
    
    def translate_text(
        self, 
        text: str, 
        target_language: str, 
        source_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate text using Google Translate.
        
        Args:
            text: Text to translate (non-empty string)
            target_language: Target language code (e.g., 'es', 'fr', 'de')
            source_language: Source language code (auto-detect if None)
            
        Returns:
            Translation result dictionary with success/error status
            
        Example:
            >>> provider.translate_text("Hello", "es")
            {'success': True, 'translated_text': 'Hola', ...}
        """
        # Input validation
        if not text or not text.strip():
            return self._create_error_response("Empty text provided")
        
        if not target_language or not target_language.strip():
            return self._create_error_response("Target language is required")
        
        try:
            # Perform translation
            result = self.translator.translate(
                text, 
                dest=target_language.lower(),
                src=source_language.lower() if source_language else 'auto'
            )
            
            return self._create_success_response(
                translated_text=result.text,
                source_language=result.src,
                target_language=target_language.lower(),
                confidence=getattr(result, 'confidence', None)
            )
        except Exception as e:
            error_msg = f"Google Translate error: {str(e)}"
            self.logger.error(error_msg)
            return self._create_error_response(error_msg)
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect language using Google Translate.
        
        Args:
            text: Text to analyze (non-empty string)
            
        Returns:
            Language detection result dictionary with success/error status
            
        Example:
            >>> provider.detect_language("Hola mundo")
            {'success': True, 'language_code': 'es', 'confidence': 0.99}
        """
        # Input validation
        if not text or not text.strip():
            return self._create_error_response("Empty text provided")
        
        try:
            detection = self.translator.detect(text)
            
            return self._create_success_response(
                language_code=detection.lang,
                confidence=detection.confidence
            )
        except Exception as e:
            error_msg = f"Language detection error: {str(e)}"
            self.logger.error(error_msg)
            return self._create_error_response(error_msg)
    
    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported language codes.
        
        Returns:
            List of supported language codes, empty list if languages not available
        """
        if not isinstance(self.languages, dict):
            self.logger.warning("Languages dictionary not available")
            return []
        return list(self.languages.keys())