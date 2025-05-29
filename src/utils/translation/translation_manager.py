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
                    provider_instance = provider_class(provider_config)
                    self.providers[provider_name] = provider_instance
                    self.available_providers.append(provider_name)
                    self.logger.info(f"Initialized provider: {provider_name}")
                else:
                    self.logger.warning(f"Unknown provider: {provider_name}")
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
        Get the order of providers (primary first, then fallbacks).
        
        Returns:
            List of provider names in order of preference
        """
        order = []
        if self.primary_provider in self.available_providers:
            order.append(self.primary_provider)
        
        for provider in self.fallback_providers:
            if provider in self.available_providers and provider not in order:
                order.append(provider)
        
        return order
    
    def translate_text(
        self, 
        text: str, 
        target_language: str, 
        source_language: Optional[str] = None,
        preferred_provider: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate text using the best available provider.
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (optional)
            preferred_provider: Preferred provider name (optional)
            
        Returns:
            Translation result dictionary
        """
        if not text.strip():
            return {
                'success': False,
                'error': 'Empty text provided',
                'provider': None
            }
        
        # Determine provider order
        if preferred_provider and preferred_provider in self.available_providers:
            provider_order = [preferred_provider] + [p for p in self.get_provider_order() if p != preferred_provider]
        else:
            provider_order = self.get_provider_order()
        
        if not provider_order:
            return {
                'success': False,
                'error': 'No translation providers available',
                'provider': None
            }
        
        # Try providers in order
        last_error = None
        for provider_name in provider_order:
            try:
                provider = self.providers[provider_name]
                result = provider.translate_text(
                    text, 
                    target_language, 
                    source_language or self.default_source_language
                )
                
                if result.get('success'):
                    self.logger.info(f"Translation successful with provider: {provider_name}")
                    return result
                else:
                    last_error = result.get('error', 'Unknown error')
                    self.logger.warning(f"Provider {provider_name} failed: {last_error}")
                    
            except Exception as e:
                last_error = str(e)
                self.logger.error(f"Exception with provider {provider_name}: {e}")
        
        return {
            'success': False,
            'error': f'All providers failed. Last error: {last_error}',
            'provider': None
        }
    
    def detect_language(self, text: str, preferred_provider: Optional[str] = None) -> Dict[str, Any]:
        """
        Detect the language of text using the best available provider.
        
        Args:
            text: Text to analyze
            preferred_provider: Preferred provider name (optional)
            
        Returns:
            Language detection result dictionary
        """
        if not text.strip():
            return {
                'success': False,
                'error': 'Empty text provided',
                'provider': None
            }
        
        # Determine provider order
        if preferred_provider and preferred_provider in self.available_providers:
            provider_order = [preferred_provider] + [p for p in self.get_provider_order() if p != preferred_provider]
        else:
            provider_order = self.get_provider_order()
        
        if not provider_order:
            return {
                'success': False,
                'error': 'No translation providers available',
                'provider': None
            }
        
        # Try providers in order
        last_error = None
        for provider_name in provider_order:
            try:
                provider = self.providers[provider_name]
                result = provider.detect_language(text)
                
                if result.get('success'):
                    self.logger.info(f"Language detection successful with provider: {provider_name}")
                    return result
                else:
                    last_error = result.get('error', 'Unknown error')
                    self.logger.warning(f"Provider {provider_name} failed: {last_error}")
                    
            except Exception as e:
                last_error = str(e)
                self.logger.error(f"Exception with provider {provider_name}: {e}")
        
        return {
            'success': False,
            'error': f'All providers failed. Last error: {last_error}',
            'provider': None
        }
    
    def get_supported_languages(self, provider_name: Optional[str] = None) -> List[str]:
        """
        Get supported languages for a specific provider or all providers.
        
        Args:
            provider_name: Name of the provider (optional)
            
        Returns:
            List of supported language codes
        """
        if provider_name:
            if provider_name in self.providers:
                return self.providers[provider_name].get_supported_languages()
            else:
                return []
        else:
            # Return union of all providers' supported languages
            all_languages = set()
            for provider in self.providers.values():
                try:
                    languages = provider.get_supported_languages()
                    all_languages.update(languages)
                except Exception as e:
                    self.logger.error(f"Error getting languages from {provider.provider_name}: {e}")
            
            return list(all_languages)
    
    def is_language_supported(self, language_code: str, provider_name: Optional[str] = None) -> bool:
        """
        Check if a language is supported.
        
        Args:
            language_code: Language code to check
            provider_name: Name of the provider (optional)
            
        Returns:
            True if language is supported, False otherwise
        """
        supported_languages = self.get_supported_languages(provider_name)
        return language_code.lower() in [lang.lower() for lang in supported_languages]
    
    def get_provider_info(self, provider_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get information about providers.
        
        Args:
            provider_name: Name of the provider (optional)
            
        Returns:
            Provider information dictionary
        """
        if provider_name:
            if provider_name in self.providers:
                return self.providers[provider_name].get_provider_info()
            else:
                return {}
        else:
            return {
                name: provider.get_provider_info() 
                for name, provider in self.providers.items()
            }
    
    def translate_batch(
        self,
        texts: List[str],
        target_language: str,
        source_language: Optional[str] = None,
        preferred_provider: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Translate multiple texts.
        
        Args:
            texts: List of texts to translate
            target_language: Target language code
            source_language: Source language code (optional)
            preferred_provider: Preferred provider name (optional)
            
        Returns:
            List of translation result dictionaries
        """
        results = []
        for text in texts:
            result = self.translate_text(
                text, 
                target_language, 
                source_language, 
                preferred_provider
            )
            results.append(result)
        
        return results
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health checks on all providers.
        
        Returns:
            Health check results dictionary
        """
        results = {}
        overall_healthy = False
        
        for provider_name, provider in self.providers.items():
            try:
                health = provider.health_check()
                results[provider_name] = health
                if health.get('success'):
                    overall_healthy = True
            except Exception as e:
                results[provider_name] = {
                    'success': False,
                    'provider': provider_name,
                    'status': 'unhealthy',
                    'error': str(e)
                }
        
        return {
            'overall_healthy': overall_healthy,
            'providers': results,
            'available_providers': self.available_providers,
            'primary_provider': self.primary_provider
        }
