"""
Azure Translator Provider

This module provides Azure Cognitive Services Translator functionality.
Requires an Azure Translator API key and has usage-based pricing.
"""

import requests
import json
from typing import Dict, List, Optional, Any
from ..base_translator import BaseTranslationProvider


class AzureTranslatorProvider(BaseTranslationProvider):
    """
    Azure Translator provider using Azure Cognitive Services.
    
    This provider uses Azure Translator which requires an API key
    and provides high-quality translations with good language support.
    """
    
    def _initialize(self):
        """Initialize the Azure Translator client."""
        self.api_key = self.config.get('api_key')
        self.region = self.config.get('region', 'global')
        self.endpoint = self.config.get('endpoint', 'https://api.cognitive.microsofttranslator.com')
        
        if not self.api_key:
            raise ValueError("Azure Translator API key is required")
        
        # Set up headers
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Content-type': 'application/json',
        }
        
        if self.region and self.region != 'global':
            self.headers['Ocp-Apim-Subscription-Region'] = self.region
        
        try:
            # Test the connection by getting supported languages
            self._get_languages()
            self.logger.info("Azure Translator provider initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Azure Translator: {e}")
            raise
    
    def _get_languages(self) -> Dict[str, Any]:
        """Get supported languages from Azure Translator."""
        try:
            url = f"{self.endpoint}/languages?api-version=3.0"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error getting languages: {e}")
            return {}
    
    def translate_text(
        self, 
        text: str, 
        target_language: str, 
        source_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate text using Azure Translator.
        
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
            # Prepare the request
            url = f"{self.endpoint}/translate?api-version=3.0&to={target_language}"
            if source_language:
                url += f"&from={source_language}"
            
            body = [{'text': text}]
            
            response = requests.post(url, headers=self.headers, json=body, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if result and len(result) > 0:
                translation = result[0]
                translated_text = translation['translations'][0]['text']
                detected_lang = translation.get('detectedLanguage', {}).get('language', source_language)
                
                return self._create_success_response(
                    translated_text=translated_text,
                    source_language=detected_lang,
                    target_language=target_language,
                    confidence=translation.get('detectedLanguage', {}).get('score')
                )
            else:
                return self._create_error_response("No translation result received")
                
        except Exception as e:
            error_msg = f"Azure Translator error: {str(e)}"
            self.logger.error(error_msg)
            return self._create_error_response(error_msg)
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect language using Azure Translator.
        
        Args:
            text: Text to analyze
            
        Returns:
            Language detection result dictionary
        """
        if not text.strip():
            return self._create_error_response("Empty text provided")
        
        try:
            url = f"{self.endpoint}/detect?api-version=3.0"
            body = [{'text': text}]
            
            response = requests.post(url, headers=self.headers, json=body, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if result and len(result) > 0:
                detection = result[0]
                
                return self._create_success_response(
                    language_code=detection['language'],
                    confidence=detection.get('score')
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
            languages_data = self._get_languages()
            translation_langs = languages_data.get('translation', {})
            return list(translation_langs.keys())
        except Exception as e:
            self.logger.error(f"Error getting supported languages: {e}")
            return []