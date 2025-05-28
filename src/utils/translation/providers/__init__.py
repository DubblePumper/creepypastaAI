"""
Translation Providers Package

This package contains individual translation provider implementations.
Each provider follows the BaseTranslationProvider interface for consistency.
"""

from .google_translate import GoogleTranslateProvider
from .deepl import DeepLProvider
from .deepl_api import DeepLAPIProvider
from .azure_translator import AzureTranslatorProvider
from .openai_translator import OpenAITranslationProvider
from .libretranslate import LibreTranslateProvider

__all__ = [
    'GoogleTranslateProvider',
    'DeepLProvider', 
    'DeepLAPIProvider',
    'AzureTranslatorProvider',
    'OpenAITranslationProvider',
    'LibreTranslateProvider'
]

# Provider registry for easy access
AVAILABLE_PROVIDERS = {
    'google': GoogleTranslateProvider,
    'deepl': DeepLProvider,
    'deepl_api': DeepLAPIProvider,
    'azure': AzureTranslatorProvider,
    'openai': OpenAITranslationProvider,
    'libretranslate': LibreTranslateProvider
}

def get_provider_class(provider_name: str):
    """
    Get provider class by name.
    
    Args:
        provider_name: Name of the provider
        
    Returns:
        Provider class or None if not found
    """
    return AVAILABLE_PROVIDERS.get(provider_name.lower())

def list_available_providers():
    """
    Get list of available provider names.
    
    Returns:
        List of available provider names
    """
    return list(AVAILABLE_PROVIDERS.keys())
