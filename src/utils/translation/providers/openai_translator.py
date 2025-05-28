"""
OpenAI Translation Provider

This module provides translation functionality using OpenAI's GPT models.
Supports high-quality translation with context awareness and natural language processing.
"""

import openai
from typing import Dict, List, Optional, Any
from ..base_translator import BaseTranslationProvider


class OpenAITranslationProvider(BaseTranslationProvider):
    """
    OpenAI translation provider using GPT models for translation.
    
    This provider offers high-quality contextual translations using OpenAI's
    language models, particularly useful for creative or nuanced content.
    """
    
    PROVIDER_NAME = "openai"
    
    # Language codes mapping for OpenAI (using ISO 639-1 codes)
    LANGUAGE_CODES = {
        'af': 'Afrikaans', 'ar': 'Arabic', 'az': 'Azerbaijani', 'be': 'Belarusian',
        'bg': 'Bulgarian', 'bn': 'Bengali', 'bs': 'Bosnian', 'ca': 'Catalan',
        'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish', 'de': 'German',
        'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
        'eu': 'Basque', 'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French',
        'ga': 'Irish', 'gl': 'Galician', 'gu': 'Gujarati', 'he': 'Hebrew',
        'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'hy': 'Armenian',
        'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'ja': 'Japanese',
        'ka': 'Georgian', 'kk': 'Kazakh', 'kn': 'Kannada', 'ko': 'Korean',
        'ky': 'Kyrgyz', 'la': 'Latin', 'lt': 'Lithuanian', 'lv': 'Latvian',
        'mk': 'Macedonian', 'ml': 'Malayalam', 'mn': 'Mongolian', 'mr': 'Marathi',
        'ms': 'Malay', 'mt': 'Maltese', 'ne': 'Nepali', 'nl': 'Dutch',
        'no': 'Norwegian', 'pa': 'Punjabi', 'pl': 'Polish', 'pt': 'Portuguese',
        'ro': 'Romanian', 'ru': 'Russian', 'si': 'Sinhala', 'sk': 'Slovak',
        'sl': 'Slovenian', 'sq': 'Albanian', 'sr': 'Serbian', 'sv': 'Swedish',
        'sw': 'Swahili', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai',
        'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
        'uz': 'Uzbek', 'vi': 'Vietnamese', 'yi': 'Yiddish', 'zh': 'Chinese'
    }
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize OpenAI translation provider.
        
        Args:
            config: Configuration dictionary containing:
                - api_key: OpenAI API key
                - model: Model to use (default: gpt-3.5-turbo)
                - max_tokens: Maximum tokens per request (default: 2000)
                - temperature: Model temperature (default: 0.3)
        """
        super().__init__(config)
        
        self.api_key = config.get('api_key')
        self.model = config.get('model', 'gpt-3.5-turbo')
        self.max_tokens = config.get('max_tokens', 2000)
        self.temperature = config.get('temperature', 0.3)
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        # Set up OpenAI client
        openai.api_key = self.api_key
        self.client = openai
    
    def is_available(self) -> bool:
        """
        Check if OpenAI translation service is available.
        
        Returns:
            bool: True if the service is available, False otherwise
        """
        try:
            # Test with a simple API call
            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            self.logger.error(f"OpenAI service unavailable: {e}")
            return False
    
    def translate_text(self, text: str, target_language: str, source_language: Optional[str] = None) -> str:
        """
        Translate text using OpenAI GPT models.
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (optional)
            
        Returns:
            str: Translated text
            
        Raises:
            Exception: If translation fails
        """
        try:
            # Get language names for the prompt
            target_lang_name = self.LANGUAGE_CODES.get(target_language, target_language)
            source_lang_name = self.LANGUAGE_CODES.get(source_language, source_language) if source_language else "auto-detected language"
            
            # Create translation prompt
            if source_language:
                prompt = f"Translate the following text from {source_lang_name} to {target_lang_name}. Maintain the original tone, style, and meaning. Only return the translated text without any additional commentary:\n\n{text}"
            else:
                prompt = f"Translate the following text to {target_lang_name}. Maintain the original tone, style, and meaning. Only return the translated text without any additional commentary:\n\n{text}"
            
            # Make API call
            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional translator. Translate the given text accurately while preserving the original meaning, tone, and style."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            translated_text = response.choices[0].message.content.strip()
            return translated_text
            
        except Exception as e:
            self.logger.error(f"OpenAI translation failed: {e}")
            raise Exception(f"Translation failed: {e}")
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the given text using OpenAI.
        
        Args:
            text: Text to analyze
            
        Returns:
            str: Detected language code
            
        Raises:
            Exception: If language detection fails
        """
        try:
            prompt = f"Detect the language of the following text and return only the ISO 639-1 language code (2 letters, lowercase):\n\n{text}"
            
            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a language detection expert. Return only the ISO 639-1 language code (2 letters, lowercase) for the given text."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.1
            )
            
            detected_lang = response.choices[0].message.content.strip().lower()
            
            # Validate the detected language code
            if detected_lang in self.LANGUAGE_CODES:
                return detected_lang
            else:
                # Try to map common variations
                lang_mapping = {
                    'english': 'en', 'spanish': 'es', 'french': 'fr', 'german': 'de',
                    'italian': 'it', 'portuguese': 'pt', 'russian': 'ru', 'chinese': 'zh',
                    'japanese': 'ja', 'korean': 'ko', 'arabic': 'ar', 'hindi': 'hi'
                }
                return lang_mapping.get(detected_lang.lower(), 'en')
                
        except Exception as e:
            self.logger.error(f"OpenAI language detection failed: {e}")
            raise Exception(f"Language detection failed: {e}")
    
    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported language codes.
        
        Returns:
            List[str]: List of supported language codes
        """
        return list(self.LANGUAGE_CODES.keys())
    
    def is_language_supported(self, language_code: str) -> bool:
        """
        Check if a language is supported by this provider.
        
        Args:
            language_code: Language code to check
            
        Returns:
            bool: True if language is supported, False otherwise
        """
        return language_code.lower() in self.LANGUAGE_CODES
    
    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get provider information and capabilities.
        
        Returns:
            Dict containing provider information
        """
        return {
            'name': self.PROVIDER_NAME,
            'description': 'OpenAI GPT-based translation service with context awareness',
            'supported_languages': len(self.LANGUAGE_CODES),
            'features': [
                'High-quality contextual translation',
                'Creative content translation',
                'Tone and style preservation',
                'Multiple GPT models support'
            ],
            'model': self.model,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature
        }
