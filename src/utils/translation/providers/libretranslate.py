"""
LibreTranslate Provider

This module provides LibreTranslate functionality, an open-source translation service.
Can be used with the public instance or self-hosted instances.
"""

import requests
from typing import Dict, List, Optional, Any
from ..base_translator import BaseTranslationProvider


class LibreTranslateProvider(BaseTranslationProvider):
    """
    LibreTranslate provider for open-source translation.
    
    This provider uses LibreTranslate, which can be either the public instance
    or a self-hosted instance. It's free but may have limitations.
    """
    
    def _initialize(self):
        """Initialize the LibreTranslate client."""
        self.base_url = self.config.get('base_url', 'https://libretranslate.de')
        self.api_key = self.config.get('api_key')  # Optional for public instance
        
        # Ensure base_url doesn't end with slash
        self.base_url = self.base_url.rstrip('/')
        
        try:
            # Test the connection
            self._get_languages()
            self.logger.info("LibreTranslate provider initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize LibreTranslate: {e}")
            raise
    
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to LibreTranslate API."""
        url = f"{self.base_url}/{endpoint}"
        
        # Add API key if provided
        if self.api_key:
            data['api_key'] = self.api_key
        
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def _get_languages(self) -> List[Dict[str, str]]:
        """Get supported languages from LibreTranslate."""
        url = f"{self.base_url}/languages"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def translate_text(
        self, 
        text: str, 
        target_language: str, 
        source_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate text using LibreTranslate.
        
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
            data = {
                'q': text,
                'source': source_language or 'auto',
                'target': target_language,
                'format': 'text'            }
            
            result = self._make_request('translate', data)
            translated_text = result.get('translatedText', '')
            
            return self._create_success_response(
                translated_text=translated_text,
                source_language=source_language or 'auto',
                target_language=target_language
            )
            
        except Exception as e:
            error_msg = f"LibreTranslate error: {str(e)}"
            self.logger.error(error_msg)
            return self._create_error_response(error_msg)
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect language using LibreTranslate.
        
        Args:
            text: Text to analyze
            
        Returns:
            Language detection result dictionary
        """
        if not text.strip():
            return self._create_error_response("Empty text provided")
        
        try:
            data = {'q': text}
            result = self._make_request('detect', data)
            
            if isinstance(result, list) and len(result) > 0:
                detection = result[0]  # type: ignore
                return self._create_success_response(
                    language_code=detection['language'],
                    confidence=detection.get('confidence')
                )
            elif isinstance(result, dict) and 'language' in result:
                return self._create_success_response(
                    language_code=result['language'],
                    confidence=result.get('confidence')
                )
            else:
                return self._create_error_response("No detection result received")
                
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
            languages = self._get_languages()
            return [lang['code'] for lang in languages]
        except Exception as e:
            self.logger.error(f"Error getting supported languages: {e}")
            return []