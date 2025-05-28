"""
Translation Manager

This module provides a unified interface for managing multiple translation providers
and handling translation operations with fallback support and provider selection.
"""

import logging
from typing import Dict, List, Optional, Any, Union
from .base_translator import BaseTranslationProvider
from .providers import AVAILABLE_PROVIDERS, get_provider_class


class TranslationManager:
    """
    Manages multiple translation providers with fallback support.
    
    This class provides a unified interface for translation operations,
    allowing configuration of multiple providers with automatic fallback
    when the primary provider fails.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Translation Manager.
        
        Args:
            config: Configuration dictionary containing:
                - providers: Dict of provider configurations
                - primary_provider: Name of the primary provider
                - fallback_providers: List of fallback provider names
                - default_source_language: Default source language (optional)
                - default_target_language: Default target language (optional)
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Provider instances
        self.providers: Dict[str, BaseTranslationProvider] = {}
        self.available_providers: List[str] = []
        
        # Provider order
        self.primary_provider = config.get('primary_provider', 'google')
        self.fallback_providers = config.get('fallback_providers', ['deepl', 'azure'])
        
        # Default languages
        self.default_source_language = config.get('default_source_language')
        self.default_target_language = config.get('default_target_language', 'en')
        
        # Initialize providers
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize translation providers based on configuration."""
        provider_configs = self.config.get('providers', {})
        
        for provider_name, provider_config in provider_configs.items():
            try:
                provider_class = get_provider_class(provider_name)
                if provider_class:
                    provider = provider_class(provider_config)
                    if provider.is_available():
                        self.providers[provider_name] = provider
                        self.available_providers.append(provider_name)
                        self.logger.info(f"Initialized provider: {provider_name}")
                    else:
                        self.logger.warning(f"Provider {provider_name} is not available")
                else:
                    self.logger.error(f"Unknown provider: {provider_name}")
                    
            except Exception as e:
                self.logger.error(f"Failed to initialize provider {provider_name}: {e}")
    
    def get_available_providers(self) -> List[str]:
        """
        Get list of available provider names.
        
        Returns:
            List of available provider names
        """
        return self.available_providers.copy()
    
    def get_provider_order(self) -> List[str]:
        """
        Get the provider order (primary + fallbacks) filtered by availability.
        
        Returns:
            List of provider names in order of preference
        """
        order = [self.primary_provider] + self.fallback_providers
        return [provider for provider in order if provider in self.available_providers]
    
    def translate_text(
        self, 
        text: str, 
        target_language: str, 
        source_language: Optional[str] = None,
        preferred_provider: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate text using available providers with fallback support.
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (optional)
            preferred_provider: Preferred provider name (optional)
            
        Returns:
            Dict containing:
                - translated_text: The translated text
                - provider_used: Name of the provider that was used
                - detected_language: Detected source language (if applicable)
                - success: Whether translation was successful
                - error: Error message if failed
        """
        if not text.strip():
            return {
                'translated_text': text,
                'provider_used': None,
                'detected_language': source_language,
                'success': True,
                'error': None
            }
        
        # Use default source language if not provided
        if not source_language:
            source_language = self.default_source_language
        
        # Determine provider order
        if preferred_provider and preferred_provider in self.available_providers:
            provider_order = [preferred_provider] + [p for p in self.get_provider_order() if p != preferred_provider]
        else:
            provider_order = self.get_provider_order()
        
        # Try providers in order
        last_error = None
        for provider_name in provider_order:
            try:
                provider = self.providers[provider_name]
                
                # Check if target language is supported
                if not provider.is_language_supported(target_language):
                    self.logger.warning(f"Provider {provider_name} doesn't support target language: {target_language}")
                    continue
                
                # Check source language support if specified
                if source_language and not provider.is_language_supported(source_language):
                    self.logger.warning(f"Provider {provider_name} doesn't support source language: {source_language}")
                    continue
                
                # Attempt translation
                translated_text = provider.translate_text(text, target_language, source_language)
                
                # Detect source language if not provided
                detected_language = source_language
                if not source_language:
                    try:
                        detected_language = provider.detect_language(text)
                    except Exception as e:
                        self.logger.warning(f"Language detection failed with {provider_name}: {e}")
                
                return {
                    'translated_text': translated_text,
                    'provider_used': provider_name,
                    'detected_language': detected_language,
                    'success': True,
                    'error': None
                }
                
            except Exception as e:
                last_error = str(e)
                self.logger.warning(f"Translation failed with provider {provider_name}: {e}")
                continue
        
        # All providers failed
        return {
            'translated_text': text,
            'provider_used': None,
            'detected_language': source_language,
            'success': False,
            'error': f"All translation providers failed. Last error: {last_error}"
        }
    
    def detect_language(self, text: str, preferred_provider: Optional[str] = None) -> Dict[str, Any]:
        """
        Detect language of text using available providers.
        
        Args:
            text: Text to analyze
            preferred_provider: Preferred provider name (optional)
            
        Returns:
            Dict containing:
                - language_code: Detected language code
                - provider_used: Name of the provider that was used
                - confidence: Confidence score if available
                - success: Whether detection was successful
                - error: Error message if failed
        """
        if not text.strip():
            return {
                'language_code': 'en',
                'provider_used': None,
                'confidence': None,
                'success': True,
                'error': None
            }
        
        # Determine provider order
        if preferred_provider and preferred_provider in self.available_providers:
            provider_order = [preferred_provider] + [p for p in self.get_provider_order() if p != preferred_provider]
        else:
            provider_order = self.get_provider_order()
        
        # Try providers in order
        last_error = None
        for provider_name in provider_order:
            try:
                provider = self.providers[provider_name]
                language_code = provider.detect_language(text)
                
                return {
                    'language_code': language_code,
                    'provider_used': provider_name,
                    'confidence': None,  # Most providers don't return confidence
                    'success': True,
                    'error': None
                }
                
            except Exception as e:
                last_error = str(e)
                self.logger.warning(f"Language detection failed with provider {provider_name}: {e}")
                continue
        
        # All providers failed
        return {
            'language_code': 'en',  # Default to English
            'provider_used': None,
            'confidence': None,
            'success': False,
            'error': f"All language detection providers failed. Last error: {last_error}"
        }
    
    def get_supported_languages(self, provider_name: Optional[str] = None) -> List[str]:
        """
        Get supported languages for a specific provider or all providers.
        
        Args:
            provider_name: Specific provider name (optional)
            
        Returns:
            List of supported language codes
        """
        if provider_name:
            if provider_name in self.providers:
                return self.providers[provider_name].get_supported_languages()
            else:
                return []
        
        # Get union of all supported languages
        all_languages = set()
        for provider in self.providers.values():
            try:
                languages = provider.get_supported_languages()
                all_languages.update(languages)
            except Exception as e:
                self.logger.warning(f"Failed to get supported languages from {provider.PROVIDER_NAME}: {e}")
        
        return sorted(list(all_languages))
    
    def is_language_supported(self, language_code: str, provider_name: Optional[str] = None) -> bool:
        """
        Check if a language is supported by a specific provider or any provider.
        
        Args:
            language_code: Language code to check
            provider_name: Specific provider name (optional)
            
        Returns:
            bool: True if language is supported
        """
        if provider_name:
            if provider_name in self.providers:
                return self.providers[provider_name].is_language_supported(language_code)
            else:
                return False
        
        # Check if any provider supports the language
        for provider in self.providers.values():
            if provider.is_language_supported(language_code):
                return True
        
        return False
    
    def get_provider_info(self, provider_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get information about providers.
        
        Args:
            provider_name: Specific provider name (optional)
            
        Returns:
            Dict containing provider information
        """
        if provider_name:
            if provider_name in self.providers:
                return self.providers[provider_name].get_provider_info()
            else:
                return {}
        
        # Get info for all providers
        provider_info = {}
        for name, provider in self.providers.items():
            try:
                provider_info[name] = provider.get_provider_info()
            except Exception as e:
                self.logger.warning(f"Failed to get info from {name}: {e}")
                provider_info[name] = {'error': str(e)}
        
        return provider_info
    
    def translate_batch(
        self,
        texts: List[str],
        target_language: str,
        source_language: Optional[str] = None,
        preferred_provider: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Translate multiple texts efficiently.
        
        Args:
            texts: List of texts to translate
            target_language: Target language code
            source_language: Source language code (optional)
            preferred_provider: Preferred provider name (optional)
            
        Returns:
            List of translation results
        """
        results = []
        for text in texts:
            result = self.translate_text(text, target_language, source_language, preferred_provider)
            results.append(result)
        
        return results
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on all providers.
        
        Returns:
            Dict containing health status of all providers
        """
        health_status = {
            'overall_health': True,
            'available_providers': len(self.available_providers),
            'total_providers': len(self.providers),
            'providers': {}
        }
        
        for name, provider in self.providers.items():
            try:
                is_available = provider.is_available()
                health_status['providers'][name] = {
                    'available': is_available,
                    'error': None
                }
                if not is_available:
                    health_status['overall_health'] = False
            except Exception as e:
                health_status['providers'][name] = {
                    'available': False,
                    'error': str(e)
                }
                health_status['overall_health'] = False
        
        return health_status
