"""
Base Translation Provider

This module defines the abstract base class for all translation providers.
All translation providers must inherit from this class and implement its methods.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
import logging


class BaseTranslationProvider(ABC):
    """
    Abstract base class for all translation providers.
    
    This class defines the interface that all translation providers must implement.
    It ensures consistency across different translation services and enables
    seamless switching between providers.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the translation provider.
        
        Args:
            config: Configuration dictionary specific to the provider
        """
        self.config = config or {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self.provider_name = self.__class__.__name__.replace('Provider', '').lower()
        
        # Initialize the provider
        self._initialize()
    
    @abstractmethod
    def _initialize(self):
        """
        Initialize the provider-specific settings.
        
        This method should handle any provider-specific initialization,
        such as setting up API clients, validating credentials, etc.
        """
        pass
    
    @abstractmethod
    def translate_text(
        self, 
        text: str, 
        target_language: str, 
        source_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate text from source language to target language.
        
        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'es', 'fr', 'de')
            source_language: Source language code (optional, auto-detect if None)
            
        Returns:
            Dictionary containing:
                - success: bool - Whether translation was successful
                - translated_text: str - The translated text (if successful)
                - source_language: str - Detected or provided source language
                - target_language: str - Target language
                - provider: str - Name of the provider used
                - error: str - Error message (if unsuccessful)
                - confidence: float - Confidence score (if available)
        """
        pass
    
    @abstractmethod
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of the given text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing:
                - success: bool - Whether detection was successful
                - language_code: str - Detected language code (if successful)
                - confidence: float - Confidence score (if available)
                - provider: str - Name of the provider used
                - error: str - Error message (if unsuccessful)
        """
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported language codes.
        
        Returns:
            List of supported language codes
        """
        pass
    
    def is_language_supported(self, language_code: str) -> bool:
        """
        Check if a language is supported by this provider.
        
        Args:
            language_code: Language code to check
            
        Returns:
            True if language is supported, False otherwise
        """
        supported_languages = self.get_supported_languages()
        return language_code.lower() in [lang.lower() for lang in supported_languages]
    
    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get information about this provider.
        
        Returns:
            Dictionary containing provider information
        """
        return {
            'name': self.provider_name,
            'class_name': self.__class__.__name__,
            'supported_languages': self.get_supported_languages(),
            'config': self.config
        }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the provider.
        
        Returns:
            Dictionary containing health status
        """
        try:
            # Try a simple translation to test the provider
            result = self.translate_text("Hello", "es")
            return {
                'success': result.get('success', False),
                'provider': self.provider_name,
                'status': 'healthy' if result.get('success') else 'unhealthy',
                'error': result.get('error') if not result.get('success') else None
            }
        except Exception as e:
            return {
                'success': False,
                'provider': self.provider_name,
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """
        Create a standardized error response.
        
        Args:
            error_message: Error message
            
        Returns:
            Standardized error response dictionary
        """
        return {
            'success': False,
            'error': error_message,
            'provider': self.provider_name
        }
    
    def _create_success_response(self, **kwargs) -> Dict[str, Any]:
        """
        Create a standardized success response.
        
        Args:
            **kwargs: Additional response data
            
        Returns:
            Standardized success response dictionary
        """
        response = {
            'success': True,
            'provider': self.provider_name
        }
        response.update(kwargs)
        return response