"""
OpenAI Translation Provider

This module provides translation functionality using OpenAI's GPT models.
Requires an OpenAI API key and has usage-based pricing.
"""

from typing import Dict, List, Optional, Any
from ..base_translator import BaseTranslationProvider

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None


class OpenAITranslationProvider(BaseTranslationProvider):
    """
    OpenAI translation provider using GPT models.
    
    This provider uses OpenAI's GPT models for translation, which can provide
    high-quality contextual translations but may be more expensive than
    dedicated translation services.
    """
    
    def _initialize(self):
        """Initialize the OpenAI client."""
        if not OPENAI_AVAILABLE:            raise ImportError(
                "openai library is not installed. "
                "Install it with: pip install openai"
            )
        
        api_key = self.config.get('api_key')
        if not api_key:
            raise ValueError("OpenAI API key is required")
        
        try:
            if openai is None:
                raise ImportError("OpenAI module not available")
            self.client = openai.OpenAI(api_key=api_key)
            self.model = self.config.get('model', 'gpt-3.5-turbo')
            self.max_tokens = self.config.get('max_tokens', 1000)
            self.temperature = self.config.get('temperature', 0.1)
            
            self.logger.info("OpenAI translation provider initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize OpenAI: {e}")
            raise
    
    def translate_text(
        self, 
        text: str, 
        target_language: str, 
        source_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate text using OpenAI GPT.
        
        Args:
            text: Text to translate
            target_language: Target language code or name
            source_language: Source language code or name (optional)
            
        Returns:
            Translation result dictionary
        """
        if not text.strip():
            return self._create_error_response("Empty text provided")
        
        try:
            # Create the translation prompt
            if source_language:
                prompt = f"Translate the following text from {source_language} to {target_language}. Only return the translation, no explanations:\n\n{text}"
            else:
                prompt = f"Translate the following text to {target_language}. Only return the translation, no explanations:\n\n{text}"
            
            # Make the API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional translator. Translate accurately and preserve the original meaning."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            translated_text = response.choices[0].message.content
            if translated_text is None:
                return self._create_error_response("OpenAI returned empty response")
            
            translated_text = translated_text.strip()
            
            return self._create_success_response(
                translated_text=translated_text,
                source_language=source_language or 'auto',
                target_language=target_language
            )
            
        except Exception as e:
            error_msg = f"OpenAI translation error: {str(e)}"
            self.logger.error(error_msg)
            return self._create_error_response(error_msg)
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect language using OpenAI GPT.
        
        Args:
            text: Text to analyze
            
        Returns:
            Language detection result dictionary
        """
        if not text.strip():
            return self._create_error_response("Empty text provided")
        
        try:
            prompt = f"Detect the language of the following text and return only the language code (e.g., 'en', 'es', 'fr'). Text:\n\n{text}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a language detection expert. Return only the language code."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0
            )
            
            language_code = response.choices[0].message.content
            if language_code is None:
                return self._create_error_response("OpenAI returned empty detection response")
            
            language_code = language_code.strip().lower()
            
            return self._create_success_response(
                language_code=language_code
            )
            
        except Exception as e:
            error_msg = f"Language detection error: {str(e)}"
            self.logger.error(error_msg)
            return self._create_error_response(error_msg)
    
    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported language codes.
        
        OpenAI models support many languages, but we return a common set.
        
        Returns:
            List of supported language codes
        """
        return [
            'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh',
            'ar', 'hi', 'tr', 'pl', 'nl', 'sv', 'da', 'no', 'fi', 'el',
            'he', 'th', 'vi', 'id', 'ms', 'tl', 'sw', 'cs', 'sk', 'hu',
            'ro', 'bg', 'hr', 'sr', 'sl', 'et', 'lv', 'lt', 'mt', 'ga',
            'cy', 'eu', 'ca', 'gl', 'is', 'fo', 'mk', 'sq', 'az', 'be',
            'ka', 'hy', 'ky', 'kk', 'uz', 'tg', 'mn', 'my', 'km', 'lo',
            'si', 'ne', 'bn', 'gu', 'ta', 'te', 'kn', 'ml', 'ur', 'fa'
        ]