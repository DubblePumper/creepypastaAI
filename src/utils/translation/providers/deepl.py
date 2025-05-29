"""
DeepL Translation Provider (using deep-translator)

This module provides DeepL translation functionality using the deep-translator library.
This is a free service that doesn't require API keys but has usage limitations.
"""

from typing import Dict, List, Optional, Any
from ..base_translator import BaseTranslationProvider

try:
    from deep_translator import DeeplTranslator
    DEEPL_AVAILABLE = True
except ImportError:
    DEEPL_AVAILABLE = False
    DeeplTranslator = None


class DeepLProvider(BaseTranslationProvider):
    """
    DeepL translation provider using the deep-translator library.
    
    This provider uses the free DeepL service through the deep-translator    library. It doesn't require API keys but has rate limits.
    """
    
    def _initialize(self):
        """Initialize the DeepL translator."""
        if not DEEPL_AVAILABLE or DeeplTranslator is None:
            raise ImportError(
                "deep-translator library is not installed. "
                "Install it with: pip install deep-translator"
            )
        
        try:
            # Get supported languages using static method
            try:
                # Try to call the static method
                get_langs_method = getattr(DeeplTranslator, 'get_supported_languages', None)
                if get_langs_method and callable(get_langs_method):
                    self.supported_langs = get_langs_method(as_dict=False)
                else:
                    # Fallback if method doesn't exist
                    self.supported_langs = ['en', 'de', 'fr', 'it', 'ja', 'es', 'nl', 'pl', 'pt', 'ru', 'zh']
            except Exception:
                # Fallback if method call fails
                self.supported_langs = ['en', 'de', 'fr', 'it', 'ja', 'es', 'nl', 'pl', 'pt', 'ru', 'zh']
            
            self.logger.info("DeepL provider initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize DeepL: {e}")
            # Fallback to a basic list if the method fails
            self.supported_langs = ['en', 'de', 'fr', 'it', 'ja', 'es', 'nl', 'pl', 'pt', 'ru', 'zh']
            self.logger.warning("Using fallback language list for DeepL")
    
    def translate_text(
        self, 
        text: str, 
        target_language: str, 
        source_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate text using DeepL.
        
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
            # Create translator instance
            if DeeplTranslator is None:
                return self._create_error_response("DeepL translator not available")
                
            translator = DeeplTranslator(
                source=source_language or 'auto',
                target=target_language
            )
            
            # Perform translation
            translated = translator.translate(text)
            
            return self._create_success_response(
                translated_text=translated,
                source_language=source_language or 'auto',
                target_language=target_language
            )
            
        except Exception as e:
            error_msg = f"DeepL translation error: {str(e)}"
            self.logger.error(error_msg)
            return self._create_error_response(error_msg)
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect language using DeepL.
        
        Note: DeepL through deep-translator doesn't have dedicated language detection,
        so this returns a not supported message.
        
        Args:
            text: Text to analyze
            
        Returns:
            Language detection result dictionary
        """
        return self._create_error_response(
            "Language detection not supported by DeepL through deep-translator"
        )
    
    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported language codes.
        
        Returns:
            List of supported language codes
        """
        if hasattr(self, 'supported_langs') and isinstance(self.supported_langs, list):
            return self.supported_langs
        return []