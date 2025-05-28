"""
Base Translation Provider Module

This module defines the abstract base class for all translation providers
in the CreepyPasta AI multilingual system.
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List


class BaseTranslationProvider(ABC):
    """
    Abstract base class for translation providers.
    
    This class defines the interface that all translation providers must implement,
    ensuring consistency across different translation services.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the translation provider.
        
        Args:
            config: Configuration dictionary for the provider
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self._is_available = False
        self._error_message = ""
        
        # Initialize the provider
        try:
            self._initialize()
            self._is_available = True
            self.logger.debug(f"{self.provider_name} initialized successfully")
        except Exception as e:
            self._error_message = str(e)
            self.logger.debug(f"{self.provider_name} initialization failed: {e}")
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the name of the translation provider."""
        pass
    
    @property
    def is_available(self) -> bool:
        """Check if the provider is available for use."""
        return self._is_available
    
    @property
    def error_message(self) -> str:
        """Get the last error message if provider is not available."""
        return self._error_message
    
    @abstractmethod
    def _initialize(self) -> None:
        """
        Initialize the provider-specific client or configuration.
        
        This method should set up the necessary clients, API keys, and
        configurations required for the specific translation provider.
        
        Raises:
            Exception: If initialization fails
        """
        pass
    
    @abstractmethod
    def translate(self, text: str, target_language: str, source_language: str = "auto") -> str:
        """
        Translate text from source language to target language.
        
        Args:
            text: Text to translate
            target_language: Target language code (ISO 639-1)
            source_language: Source language code ("auto" for detection)
            
        Returns:
            Translated text
            
        Raises:
            Exception: If translation fails
        """
        pass
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the language of the given text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Detected language code or None if detection is not supported
        """
        # Default implementation returns None
        # Providers can override this if they support language detection
        return None
    
    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported language codes.
        
        Returns:
            List of ISO 639-1 language codes supported by this provider
        """
        # Default implementation returns empty list
        # Providers should override this with their supported languages
        return []
    
    def convert_language_code(self, language_code: str) -> str:
        """
        Convert standard language code to provider-specific format.
        
        Args:
            language_code: Standard ISO 639-1 language code
            
        Returns:
            Provider-specific language code
        """
        # Default implementation returns the code as-is
        # Providers can override this for custom mappings
        return language_code
    
    def validate_language_support(self, language_code: str) -> bool:
        """
        Check if a language is supported by this provider.
        
        Args:
            language_code: Language code to check
            
        Returns:
            True if language is supported, False otherwise
        """
        supported_languages = self.get_supported_languages()
        if not supported_languages:
            # If provider doesn't specify supported languages, assume all are supported
            return True
        
        return language_code in supported_languages
    
    def __str__(self) -> str:
        """String representation of the provider."""
        status = "Available" if self.is_available else f"Unavailable ({self.error_message})"
        return f"{self.provider_name}: {status}"
    
    def __repr__(self) -> str:
        """Detailed representation of the provider."""
        return f"{self.__class__.__name__}(available={self.is_available})"
