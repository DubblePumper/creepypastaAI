"""
Translation Package

This package provides a comprehensive translation system with support for multiple
translation providers and automatic fallback mechanisms.

Main Components:
- BaseTranslationProvider: Abstract base class for all translation providers
- TranslationManager: Main interface for managing multiple providers
- Individual providers in the providers subpackage

Usage:
    from src.utils.translation import TranslationManager
    
    config = {
        'primary_provider': 'google',
        'fallback_providers': ['deepl', 'azure'],
        'providers': {
            'google': {},
            'deepl': {'api_key': 'your-deepl-key'},
            'azure': {
                'api_key': 'your-azure-key',
                'region': 'your-region'
            }
        }
    }
    
    translator = TranslationManager(config)
    result = translator.translate_text("Hello world", "es")
    print(result['translated_text'])  # "Hola mundo"
"""

from typing import Dict, Optional
from .base_translator import BaseTranslationProvider
from .translation_manager import TranslationManager
from .providers import (
    GoogleTranslateProvider,
    DeepLProvider,
    DeepLAPIProvider,
    AzureTranslatorProvider,
    OpenAITranslationProvider,
    LibreTranslateProvider,
    AVAILABLE_PROVIDERS,
    get_provider_class,
    list_available_providers
)

__version__ = "1.0.0"

__all__ = [
    # Core classes
    'BaseTranslationProvider',
    'TranslationManager',
    
    # Provider classes
    'GoogleTranslateProvider',
    'DeepLProvider',
    'DeepLAPIProvider',
    'AzureTranslatorProvider',
    'OpenAITranslationProvider',
    'LibreTranslateProvider',
    
    # Utility functions
    'AVAILABLE_PROVIDERS',
    'get_provider_class',
    'list_available_providers'
]

# Quick access functions
def create_translator(config: Optional[Dict] = None) -> 'TranslationManager':
    """
    Create a TranslationManager with default or provided configuration.
    
    Args:
        config: Configuration dictionary (optional)
        
    Returns:
        TranslationManager instance
    """
    if config is None:
        # Default configuration with Google Translate
        config = {
            'primary_provider': 'google',
            'fallback_providers': [],
            'providers': {
                'google': {}
            }
        }
    
    return TranslationManager(config)

def quick_translate(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    """
    Quick translation using default configuration.
    
    Args:
        text: Text to translate
        target_language: Target language code
        source_language: Source language code (optional)
        
    Returns:
        Translated text
    """
    translator = create_translator()
    result = translator.translate_text(text, target_language, source_language)
    
    if result['success']:
        return result['translated_text']
    else:
        raise Exception(f"Translation failed: {result['error']}")

def detect_language(text: str) -> str:
    """
    Quick language detection using default configuration.
    
    Args:
        text: Text to analyze
        
    Returns:
        Detected language code
    """
    translator = create_translator()
    result = translator.detect_language(text)
    
    if result['success']:
        return result['language_code']
    else:
        raise Exception(f"Language detection failed: {result['error']}")
