"""
Language Manager Module

This module handles language configuration, validation, and management for the
CreepyPasta AI multilingual system. It provides functionality to enable/disable
languages and validate language selections.
"""

import logging
from typing import Dict, List, Optional, Set, Any
from ..utils.config_manager import ConfigManager


class LanguageManager:
    """
    Manages language configurations and validation for multilingual support.
    
    Handles enabling/disabling languages, validating language codes, and providing
    language-specific configurations for TTS and translation services.
    """
    
    # ISO 639-1 language codes with their full names
    LANGUAGE_NAMES = {
        'en': 'English',
        'nl': 'Dutch (Nederlands)',
        'de': 'German (Deutsch)',
        'fr': 'French (Français)',
        'es': 'Spanish (Español)',
        'it': 'Italian (Italiano)',
        'pt': 'Portuguese (Português)',
        'ru': 'Russian (Русский)',
        'ja': 'Japanese (日本語)',
        'ko': 'Korean (한국어)',
        'zh': 'Chinese (中文)',
        'ar': 'Arabic (العربية)',
        'hi': 'Hindi (हिन्दी)'
    }
    
    def __init__(self, config: ConfigManager):
        """
        Initialize the Language Manager.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Load language configurations
        self._load_language_settings()
        
        self.logger.info(f"Language Manager initialized with {len(self.enabled_languages)} enabled languages")
    
    def _load_language_settings(self) -> None:
        """Load language settings from configuration."""
        try:
            # Get enabled languages from config
            enabled_config = self.config.get("multilingual.enabled_languages", {})
            
            # Ensure English is always enabled as default
            enabled_config['en'] = True
            
            # Filter only enabled languages
            self.enabled_languages: Set[str] = {
                lang_code for lang_code, enabled in enabled_config.items() 
                if enabled and lang_code in self.LANGUAGE_NAMES
            }
            
            # Get default language
            self.default_language = self.config.get("multilingual.default_language", "en")
            
            # Ensure default language is enabled
            if self.default_language not in self.enabled_languages:
                self.logger.warning(f"Default language '{self.default_language}' is not enabled. Enabling it automatically.")
                self.enabled_languages.add(self.default_language)
            
            self.logger.info(f"Loaded language settings: {sorted(self.enabled_languages)}")
            
        except Exception as e:
            self.logger.error(f"Error loading language settings: {e}")
            # Fallback to English only
            self.enabled_languages = {'en'}
            self.default_language = 'en'
    
    def get_enabled_languages(self) -> List[str]:
        """
        Get list of enabled language codes.
        
        Returns:
            List of enabled language codes sorted alphabetically
        """
        return sorted(self.enabled_languages)
    
    def get_enabled_languages_with_names(self) -> Dict[str, str]:
        """
        Get dictionary of enabled languages with their full names.
        
        Returns:
            Dictionary mapping language codes to full language names
        """
        return {
            code: self.LANGUAGE_NAMES[code] 
            for code in sorted(self.enabled_languages)
        }
    
    def is_language_enabled(self, language_code: str) -> bool:
        """
        Check if a language is enabled.
        
        Args:
            language_code: ISO 639-1 language code
            
        Returns:
            True if language is enabled, False otherwise
        """
        return language_code.lower() in self.enabled_languages
    
    def is_valid_language_code(self, language_code: str) -> bool:
        """
        Check if a language code is valid (supported by the system).
        
        Args:
            language_code: ISO 639-1 language code
            
        Returns:
            True if language code is valid, False otherwise
        """
        return language_code.lower() in self.LANGUAGE_NAMES
    
    def validate_language_selection(self, language_code: str) -> tuple[bool, str]:
        """
        Validate a language selection and return detailed feedback.
        
        Args:
            language_code: ISO 639-1 language code to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        lang_code = language_code.lower()
        
        # Check if language code is valid
        if not self.is_valid_language_code(lang_code):
            available_codes = ', '.join(sorted(self.LANGUAGE_NAMES.keys()))
            return False, f"Invalid language code '{language_code}'. Available codes: {available_codes}"
        
        # Check if language is enabled
        if not self.is_language_enabled(lang_code):
            enabled_names = [f"{code} ({self.LANGUAGE_NAMES[code]})" for code in sorted(self.enabled_languages)]
            return False, f"Language '{self.LANGUAGE_NAMES[lang_code]}' is not enabled. Enabled languages: {', '.join(enabled_names)}"
        
        return True, ""
    
    def get_language_name(self, language_code: str) -> str:
        """
        Get the full name of a language from its code.
        
        Args:
            language_code: ISO 639-1 language code
            
        Returns:
            Full language name or the code itself if not found
        """
        return self.LANGUAGE_NAMES.get(language_code.lower(), language_code)
    
    def enable_language(self, language_code: str) -> bool:
        """
        Enable a language (runtime only, doesn't persist to config).
        
        Args:
            language_code: ISO 639-1 language code
            
        Returns:
            True if successfully enabled, False if invalid code
        """
        lang_code = language_code.lower()
        
        if not self.is_valid_language_code(lang_code):
            self.logger.error(f"Cannot enable invalid language code: {language_code}")
            return False
        
        if lang_code not in self.enabled_languages:
            self.enabled_languages.add(lang_code)
            self.logger.info(f"Enabled language: {self.LANGUAGE_NAMES[lang_code]} ({lang_code})")
        
        return True
    
    def disable_language(self, language_code: str) -> bool:
        """
        Disable a language (runtime only, doesn't persist to config).
        Cannot disable the default language.
        
        Args:
            language_code: ISO 639-1 language code
            
        Returns:
            True if successfully disabled, False if it's the default language or invalid
        """
        lang_code = language_code.lower()
        
        # Cannot disable default language
        if lang_code == self.default_language:
            self.logger.error(f"Cannot disable default language: {self.LANGUAGE_NAMES[lang_code]}")
            return False
        
        if not self.is_valid_language_code(lang_code):
            self.logger.error(f"Cannot disable invalid language code: {language_code}")
            return False
        
        if lang_code in self.enabled_languages:
            self.enabled_languages.remove(lang_code)
            self.logger.info(f"Disabled language: {self.LANGUAGE_NAMES[lang_code]} ({lang_code})")
        
        return True
    
    def get_voice_config(self, language_code: str, tts_provider: str) -> Optional[str]:
        """
        Get voice configuration for a specific language and TTS provider.
        
        Args:
            language_code: ISO 639-1 language code
            tts_provider: TTS provider name (elevenlabs, openai, azure, gtts)
            
        Returns:
            Voice identifier for the provider or None if not configured
        """
        try:
            voices_config = self.config.get("multilingual.voices", {})
            lang_voices = voices_config.get(language_code.lower(), {})
            return lang_voices.get(tts_provider.lower())
        except Exception as e:
            self.logger.error(f"Error getting voice config for {language_code}/{tts_provider}: {e}")
            return None
    
    def get_translation_target_languages(self, source_language: str = "en") -> List[str]:
        """
        Get list of enabled languages that can be translation targets.
        
        Args:
            source_language: Source language to exclude from targets
            
        Returns:
            List of language codes that can be translation targets
        """
        targets = [lang for lang in self.enabled_languages if lang != source_language.lower()]
        return sorted(targets)
    
    def display_language_status(self) -> str:
        """
        Generate a formatted string showing current language status.
        
        Returns:
            Formatted string with language status information
        """
        lines = []
        lines.append("🌍 Language Configuration Status:")
        lines.append(f"   Default Language: {self.LANGUAGE_NAMES[self.default_language]} ({self.default_language})")
        lines.append(f"   Total Enabled: {len(self.enabled_languages)}")
        lines.append("")
        lines.append("📋 Enabled Languages:")
        
        for lang_code in sorted(self.enabled_languages):
            lang_name = self.LANGUAGE_NAMES[lang_code]
            default_marker = " (default)" if lang_code == self.default_language else ""
            lines.append(f"   ✅ {lang_code}: {lang_name}{default_marker}")
        
        # Show disabled languages
        disabled_languages = set(self.LANGUAGE_NAMES.keys()) - self.enabled_languages
        if disabled_languages:
            lines.append("")
            lines.append("❌ Disabled Languages:")
            for lang_code in sorted(disabled_languages):
                lang_name = self.LANGUAGE_NAMES[lang_code]
                lines.append(f"   ⚫ {lang_code}: {lang_name}")
        
        return "\n".join(lines)
    
    def get_language_statistics(self) -> Dict[str, Any]:
        """
        Get statistical information about language configuration.
        
        Returns:
            Dictionary with language statistics
        """
        total_supported = len(self.LANGUAGE_NAMES)
        enabled_count = len(self.enabled_languages)
        disabled_count = total_supported - enabled_count
        
        return {
            'total_supported': total_supported,
            'enabled_count': enabled_count,
            'disabled_count': disabled_count,
            'enabled_percentage': round((enabled_count / total_supported) * 100, 1),
            'default_language': self.default_language,
            'enabled_languages': sorted(self.enabled_languages),
            'disabled_languages': sorted(set(self.LANGUAGE_NAMES.keys()) - self.enabled_languages)
        }
    
    def get_all_languages(self) -> Dict[str, str]:
        """
        Get dictionary of all supported languages (both enabled and disabled).
        
        Returns:
            Dictionary mapping language codes to full language names
        """
        return self.LANGUAGE_NAMES.copy()
