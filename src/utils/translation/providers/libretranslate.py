"""
LibreTranslate Translation Provider

This module provides translation functionality using LibreTranslate API.
LibreTranslate is a free and open source machine translation API.
"""

import requests
from typing import Dict, List, Optional, Any
from ..base_translator import BaseTranslationProvider


class LibreTranslateProvider(BaseTranslationProvider):
    """
    LibreTranslate translation provider.
    
    This provider uses LibreTranslate API for translation services.
    LibreTranslate is a free, open-source, and self-hostable translation API.
    """
    
    PROVIDER_NAME = "libretranslate"
    
    # Default LibreTranslate instance
    DEFAULT_URL = "https://libretranslate.de"
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize LibreTranslate translation provider.
        
        Args:
            config: Configuration dictionary containing:
                - url: LibreTranslate instance URL (default: https://libretranslate.de)
                - api_key: API key if required by the instance (optional)
                - timeout: Request timeout in seconds (default: 30)
        """
        super().__init__(config)
        
        self.url = config.get('url', self.DEFAULT_URL).rstrip('/')
        self.api_key = config.get('api_key')
        self.timeout = config.get('timeout', 30)
        self.session = requests.Session()
        
        # Cache for supported languages
        self._supported_languages = None
        self._language_cache_valid = False
    
    def is_available(self) -> bool:
        """
        Check if LibreTranslate service is available.
        
        Returns:
            bool: True if the service is available, False otherwise
        """
        try:
            response = self.session.get(
                f"{self.url}/languages",
                timeout=self.timeout
            )
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"LibreTranslate service unavailable: {e}")
            return False
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Get request headers including API key if provided.
        
        Returns:
            Dict containing request headers
        """
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'CreepyPastaAI-Translation/1.0'
        }
        
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        
        return headers
    
    def _fetch_supported_languages(self) -> List[Dict[str, str]]:
        """
        Fetch supported languages from LibreTranslate API.
        
        Returns:
            List of language dictionaries
            
        Raises:
            Exception: If fetching languages fails
        """
        try:
            response = self.session.get(
                f"{self.url}/languages",
                headers=self._get_headers(),
                timeout=self.timeout
            )
            response.raise_for_status()
            
            languages = response.json()
            self._supported_languages = languages
            self._language_cache_valid = True
            
            return languages
            
        except Exception as e:
            self.logger.error(f"Failed to fetch supported languages: {e}")
            raise Exception(f"Failed to fetch supported languages: {e}")
    
    def translate_text(self, text: str, target_language: str, source_language: Optional[str] = None) -> str:
        """
        Translate text using LibreTranslate API.
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (optional, auto-detect if None)
            
        Returns:
            str: Translated text
            
        Raises:
            Exception: If translation fails
        """
        try:
            # Prepare request data
            data = {
                'q': text,
                'target': target_language,
                'format': 'text'
            }
            
            if source_language:
                data['source'] = source_language
            else:
                data['source'] = 'auto'
            
            if self.api_key:
                data['api_key'] = self.api_key
            
            # Make translation request
            response = self.session.post(
                f"{self.url}/translate",
                json=data,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('translatedText', '')
            else:
                error_msg = f"Translation failed with status {response.status_code}"
                if response.text:
                    try:
                        error_data = response.json()
                        error_msg += f": {error_data.get('error', response.text)}"
                    except:
                        error_msg += f": {response.text}"
                raise Exception(error_msg)
                
        except Exception as e:
            self.logger.error(f"LibreTranslate translation failed: {e}")
            raise Exception(f"Translation failed: {e}")
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the given text using LibreTranslate.
        
        Args:
            text: Text to analyze
            
        Returns:
            str: Detected language code
            
        Raises:
            Exception: If language detection fails
        """
        try:
            # Prepare request data
            data = {
                'q': text
            }
            
            if self.api_key:
                data['api_key'] = self.api_key
            
            # Make detection request
            response = self.session.post(
                f"{self.url}/detect",
                json=data,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                # LibreTranslate returns a list of detected languages with confidence
                if result and len(result) > 0:
                    return result[0].get('language', 'en')
                else:
                    return 'en'  # Default to English if no detection
            else:
                error_msg = f"Language detection failed with status {response.status_code}"
                if response.text:
                    try:
                        error_data = response.json()
                        error_msg += f": {error_data.get('error', response.text)}"
                    except:
                        error_msg += f": {response.text}"
                raise Exception(error_msg)
                
        except Exception as e:
            self.logger.error(f"LibreTranslate language detection failed: {e}")
            raise Exception(f"Language detection failed: {e}")
    
    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported language codes.
        
        Returns:
            List[str]: List of supported language codes
        """
        try:
            if not self._language_cache_valid or self._supported_languages is None:
                self._fetch_supported_languages()
            
            return [lang.get('code', '') for lang in self._supported_languages if lang.get('code')]
            
        except Exception as e:
            self.logger.error(f"Failed to get supported languages: {e}")
            # Return basic language set if API call fails
            return ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ko', 'ar']
    
    def is_language_supported(self, language_code: str) -> bool:
        """
        Check if a language is supported by this provider.
        
        Args:
            language_code: Language code to check
            
        Returns:
            bool: True if language is supported, False otherwise
        """
        try:
            supported_languages = self.get_supported_languages()
            return language_code.lower() in [lang.lower() for lang in supported_languages]
        except Exception:
            return False
    
    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get provider information and capabilities.
        
        Returns:
            Dict containing provider information
        """
        try:
            supported_count = len(self.get_supported_languages())
        except:
            supported_count = "Unknown"
        
        return {
            'name': self.PROVIDER_NAME,
            'description': 'Free and open source machine translation API',
            'url': self.url,
            'supported_languages': supported_count,
            'features': [
                'Free and open source',
                'Self-hostable',
                'No API key required (optional)',
                'Language detection',
                'Multiple format support'
            ],
            'requires_api_key': bool(self.api_key),
            'timeout': self.timeout
        }
    
    def get_language_pairs(self) -> List[Dict[str, str]]:
        """
        Get available translation language pairs.
        
        Returns:
            List of dictionaries containing source and target language information
        """
        try:
            if not self._language_cache_valid or self._supported_languages is None:
                self._fetch_supported_languages()
            
            # LibreTranslate typically supports translation between any supported languages
            languages = self._supported_languages
            pairs = []
            
            for source_lang in languages:
                for target_lang in languages:
                    if source_lang['code'] != target_lang['code']:
                        pairs.append({
                            'source': source_lang['code'],
                            'target': target_lang['code'],
                            'source_name': source_lang.get('name', source_lang['code']),
                            'target_name': target_lang.get('name', target_lang['code'])
                        })
            
            return pairs
            
        except Exception as e:
            self.logger.error(f"Failed to get language pairs: {e}")
            return []
