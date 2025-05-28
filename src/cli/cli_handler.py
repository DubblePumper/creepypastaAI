"""
Command Line Interface Handler for CreepyPasta AI

This module provides command-line interface functionality for running
different components of the CreepyPasta AI application independently.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from src.utils.logger import setup_logger
from src.utils.config_manager import ConfigManager
from src.utils.language_manager import LanguageManager


class CLIHandler:
    """
    Handles command-line interface for CreepyPasta AI application.
    
    Allows users to run different components independently:
    - Scraping only
    - Audio generation only  
    - Video generation only
    - Complete workflow
    """
    
    def __init__(self):
        """Initialize the CLI handler."""
        self.logger = setup_logger("CLIHandler", "INFO")
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create the argument parser for the CLI.
        
        Returns:
            Configured ArgumentParser instance
        """
        parser = argparse.ArgumentParser(
            description="CreepyPasta AI - Generate atmospheric horror content",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Run complete workflow for 5 stories
  python main.py --stories 5
  
  # Scrape stories only
  python main.py --mode scrape --stories 10
  
  # Generate audio for existing stories only
  python main.py --mode audio
  
  # Generate videos for existing audio files only
  python main.py --mode video
  
  # Display system information
  python main.py --info
  
  # Display tracking statistics
  python main.py --stats
            """
        )
        
        # Mode selection
        parser.add_argument(
            "--mode", "-m",
            choices=["complete", "scrape", "audio", "video"],
            default="complete",
            help="Execution mode: complete workflow, scraping only, audio only, or video only (default: complete)"
        )
        
        # Number of stories
        parser.add_argument(
            "--stories", "-s",
            type=int,
            help="Number of stories to process (for scraping mode or complete workflow)"
        )
        
        # Configuration file
        parser.add_argument(
            "--config", "-c",
            type=str,
            default="config/settings.yaml",
            help="Path to configuration file (default: config/settings.yaml)"
        )
        
        # System information
        parser.add_argument(
            "--info", "-i",
            action="store_true",
            help="Display system information and exit"
        )
        
        # Statistics
        parser.add_argument(
            "--stats",
            action="store_true",
            help="Display tracking statistics and exit"
        )
        
        # Video generation options
        parser.add_argument(
            "--video-all",
            action="store_true",
            help="Generate videos for all existing audio files (only for video mode)"
        )
        
        # Verbose output
        parser.add_argument(
            "--verbose", "-v",
            action="store_true",
            help="Enable verbose output"
        )
        
        # Force regeneration
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force regeneration of existing files"
        )
        
        # Multilingual support
        parser.add_argument(
            "--language", "-l",
            type=str,
            help="Target language for TTS and translation (e.g., 'en', 'es', 'fr', 'de')"        )
        
        parser.add_argument(
            "--translate",
            action="store_true",
            help="Enable automatic translation of stories to target language"
        )
        
        parser.add_argument(
            "--translation-provider",
            choices=["google", "azure", "openai"],
            help="Translation service provider (overrides config setting)"
        )
        
        parser.add_argument(
            "--list-languages",
            action="store_true",
            help="List all available languages and exit"
        )
        
        # Language management
        parser.add_argument(
            "--enable-language",
            type=str,
            metavar="LANG_CODE",
            help="Enable a specific language (e.g., 'nl', 'de', 'fr'). This is runtime only."
        )
        
        parser.add_argument(
            "--disable-language",
            type=str,
            metavar="LANG_CODE",
            help="Disable a specific language (e.g., 'it', 'pt', 'ru'). Cannot disable default language. Runtime only."
        )
        
        parser.add_argument(
            "--list-enabled",
            action="store_true",
            help="List only currently enabled languages and exit"
        )
        
        parser.add_argument(
            "--language-status",
            action="store_true",
            help="Show detailed language configuration status and exit"
        )
        
        return parser
    
    def parse_args(self, args: Optional[list] = None) -> argparse.Namespace:
        """
        Parse command line arguments.
        
        Args:
            args: List of arguments to parse (uses sys.argv if None)
            
        Returns:
            Parsed arguments namespace
        """
        return self.parser.parse_args(args)
    
    def validate_args(self, args: argparse.Namespace) -> bool:
        """
        Validate parsed arguments.
        
        Args:
            args: Parsed arguments namespace
            
        Returns:
            True if arguments are valid, False otherwise
        """
        try:
            # Check if config file exists
            config_path = Path(args.config)
            if not config_path.exists():
                self.logger.error(f"Configuration file not found: {args.config}")
                return False
            
            # Validate stories count
            if args.stories is not None and args.stories <= 0:
                self.logger.error("Number of stories must be greater than 0")
                return False
              # Check mode-specific requirements
            if args.mode == "scrape" and args.stories is None:
                self.logger.warning("No story count specified for scraping mode, will use config default")
            
            if args.video_all and args.mode != "video":
                self.logger.warning("--video-all flag is only relevant for video mode")
              # Validate multilingual arguments
            if hasattr(args, 'language') and args.language:
                # Validate language code format (basic check)
                if len(args.language) < 2 or len(args.language) > 5:
                    self.logger.error("Language code should be 2-5 characters (e.g., 'en', 'es', 'fr')")
                    return False
            
            if hasattr(args, 'translate') and args.translate and not hasattr(args, 'language'):
                self.logger.warning("Translation enabled but no target language specified")
            
            # Validate language management arguments
            if hasattr(args, 'enable_language') and args.enable_language:
                if len(args.enable_language) < 2 or len(args.enable_language) > 3:
                    self.logger.error("Language code for --enable-language should be 2-3 characters (e.g., 'nl', 'de')")
                    return False
            
            if hasattr(args, 'disable_language') and args.disable_language:
                if len(args.disable_language) < 2 or len(args.disable_language) > 3:
                    self.logger.error("Language code for --disable-language should be 2-3 characters (e.g., 'it', 'pt')")
                    return False
                # Cannot disable English as it's the default
                if args.disable_language.lower() == 'en':
                    self.logger.error("Cannot disable English (en) as it's the default language")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating arguments: {e}")
            return False
    
    def display_help(self):
        """Display help message."""
        self.parser.print_help()
    
    def display_banner(self):
        """Display application banner."""
        banner = """
        ╔══════════════════════════════════════════════╗
        ║              CreepyPasta AI                  ║
        ║      Horror Story Audio & Video Generator    ║
        ╚══════════════════════════════════════════════╝
        """
        print(banner)
    
    def display_all_languages(self, language_manager: LanguageManager):
        """
        Display all available languages with their status.
        
        Args:
            language_manager: LanguageManager instance
        """
        print("\n🌍 Available Languages:")
        print("=" * 50)
        
        all_languages = language_manager.get_all_languages()
        enabled_languages = language_manager.get_enabled_languages()
        
        for code, name in all_languages.items():
            status = "✅ Enabled" if code in enabled_languages else "❌ Disabled"
            default_marker = " (default)" if code == language_manager.default_language else ""
            print(f"   {code}: {name} - {status}{default_marker}")
        
        print(f"\n💡 Use --enable-language <code> to enable a language")
        print(f"💡 Use --disable-language <code> to disable a language")
        print(f"💡 Use --list-enabled to see only enabled languages")
    
    def display_enabled_languages(self, language_manager: LanguageManager) -> None:
        """
        Display only currently enabled languages.
        
        Args:
            language_manager: LanguageManager instance
        """
        print("\n🌍 Currently Enabled Languages:")
        print("=" * 40)
        
        enabled_languages = language_manager.get_enabled_languages_with_names()
        
        if not enabled_languages:
            print("   No languages enabled (this should not happen!)")
            return
        
        for code, name in enabled_languages.items():
            default_marker = " (default)" if code == language_manager.default_language else ""
            print(f"   ✅ {code}: {name}{default_marker}")
        
        print(f"\n💡 Use --language <code> to select a language for generation")
        print(f"💡 Use --list-languages to see all available languages")
    
    def display_language_status(self, language_manager: LanguageManager) -> None:
        """
        Display comprehensive language status information.
        
        Args:
            language_manager: LanguageManager instance
        """
        print("\n🌍 Language Status Report:")
        print("=" * 50)
        
        # Overall status
        multilingual_enabled = language_manager.config.get("multilingual.enabled", False)
        default_language = language_manager.default_language
        
        print(f"🔧 Multilingual Support: {'✅ Enabled' if multilingual_enabled else '❌ Disabled'}")
        print(f"🏠 Default Language: {default_language} ({language_manager.get_language_name(default_language)})")
        
        # Enabled languages count
        enabled_count = len(language_manager.get_enabled_languages())
        total_count = len(language_manager.get_all_languages())
        print(f"📊 Languages Status: {enabled_count}/{total_count} enabled")
        
        # Translation settings
        translation_enabled = language_manager.config.get("multilingual.translate_stories", False)
        translation_provider = language_manager.config.get("multilingual.translation.provider", "google")
        print(f"🔄 Auto Translation: {'✅ Enabled' if translation_enabled else '❌ Disabled'}")
        print(f"🔧 Translation Provider: {translation_provider}")
        
        # Show enabled languages
        print(f"\n✅ Enabled Languages ({enabled_count}):")
        enabled_languages = language_manager.get_enabled_languages_with_names()
        for code, name in enabled_languages.items():
            default_marker = " (default)" if code == default_language else ""
            print(f"   • {code}: {name}{default_marker}")
        
        # Show disabled languages
        disabled_languages = {
            code: name for code, name in language_manager.get_all_languages().items()
            if code not in enabled_languages
        }
        
        if disabled_languages:
            print(f"\n❌ Disabled Languages ({len(disabled_languages)}):")
            for code, name in disabled_languages.items():
                print(f"   • {code}: {name}")
        
        print(f"\n💡 Use --enable-language <code> or --disable-language <code> to manage languages")

    def handle_language_management(self, args: argparse.Namespace, language_manager: LanguageManager) -> bool:
        """
        Handle language enable/disable commands.
        
        Args:
            args: Parsed command line arguments
            language_manager: LanguageManager instance
            
        Returns:
            True if a language management command was handled (should exit), False otherwise
        """
        # Handle enable language
        if hasattr(args, 'enable_language') and args.enable_language:
            lang_code = args.enable_language.lower()
            
            if language_manager.enable_language(lang_code):
                lang_name = language_manager.get_language_name(lang_code)
                print(f"\n✅ Successfully enabled language: {lang_name} ({lang_code})")
                print(f"💡 This change is runtime only. To make it permanent, edit config/settings.yaml")
                
                # Show updated enabled languages
                print(f"\n🌍 Currently enabled languages:")
                for code, name in language_manager.get_enabled_languages_with_names().items():
                    marker = " (default)" if code == language_manager.default_language else ""
                    marker += " (newly enabled)" if code == lang_code else ""
                    print(f"   ✅ {code}: {name}{marker}")
            else:
                lang_name = language_manager.get_language_name(lang_code)
                print(f"\n❌ Failed to enable language: {lang_name} ({lang_code})")
                print(f"💡 Make sure the language code is valid. Use --list-languages to see all supported languages.")
            
            return True
        
        # Handle disable language
        if hasattr(args, 'disable_language') and args.disable_language:
            lang_code = args.disable_language.lower()
            
            if language_manager.disable_language(lang_code):
                lang_name = language_manager.get_language_name(lang_code)
                print(f"\n✅ Successfully disabled language: {lang_name} ({lang_code})")
                print(f"💡 This change is runtime only. To make it permanent, edit config/settings.yaml")
                
                # Show updated enabled languages
                print(f"\n🌍 Currently enabled languages:")
                for code, name in language_manager.get_enabled_languages_with_names().items():
                    marker = " (default)" if code == language_manager.default_language else ""
                    print(f"   ✅ {code}: {name}{marker}")
            else:
                lang_name = language_manager.get_language_name(lang_code)
                print(f"\n❌ Failed to disable language: {lang_name} ({lang_code})")
                print(f"💡 Cannot disable the default language or invalid language codes.")
            
            return True
        
        # Handle list enabled languages
        if hasattr(args, 'list_enabled') and args.list_enabled:
            self.display_enabled_languages(language_manager)
            return True
        
        # Handle language status
        if hasattr(args, 'language_status') and args.language_status:
            self.display_language_status(language_manager)
            return True
        
        return False
    
    def handle_language_management_commands(self, args: argparse.Namespace, language_manager: LanguageManager) -> bool:
        """
        Handle language management commands.
        
        Args:
            args: Parsed command line arguments  
            language_manager: LanguageManager instance
            
        Returns:
            True if a language management command was executed, False otherwise
        """
        # Handle list all languages
        if hasattr(args, 'list_languages') and args.list_languages:
            self.display_all_languages(language_manager)
            return True
        
        # Handle enable language
        if hasattr(args, 'enable_language') and args.enable_language:
            lang_code = args.enable_language.lower()
            
            if language_manager.enable_language(lang_code):
                lang_name = language_manager.get_language_name(lang_code)
                print(f"\n✅ Successfully enabled language: {lang_name} ({lang_code})")
                print(f"💡 This change is runtime only. To make it permanent, edit config/settings.yaml")
                
                # Show updated enabled languages
                print(f"\n🌍 Currently enabled languages:")
                for code, name in language_manager.get_enabled_languages_with_names().items():
                    marker = " (default)" if code == language_manager.default_language else ""
                    print(f"   ✅ {code}: {name}{marker}")
            else:
                lang_name = language_manager.get_language_name(lang_code)
                print(f"\n❌ Failed to enable language: {lang_name} ({lang_code})")
                print(f"💡 Make sure the language code is valid. Use --list-languages to see all supported languages.")
            
            return True
        
        # Handle disable language
        if hasattr(args, 'disable_language') and args.disable_language:
            lang_code = args.disable_language.lower()
            
            if language_manager.disable_language(lang_code):
                lang_name = language_manager.get_language_name(lang_code)
                print(f"\n✅ Successfully disabled language: {lang_name} ({lang_code})")
                print(f"💡 This change is runtime only. To make it permanent, edit config/settings.yaml")
                
                # Show updated enabled languages
                print(f"\n🌍 Currently enabled languages:")
                for code, name in language_manager.get_enabled_languages_with_names().items():
                    marker = " (default)" if code == language_manager.default_language else ""
                    print(f"   ✅ {code}: {name}{marker}")
            else:
                lang_name = language_manager.get_language_name(lang_code)
                print(f"\n❌ Failed to disable language: {lang_name} ({lang_code})")
                print(f"💡 Cannot disable the default language or invalid language codes.")
            
            return True
        
        # Handle list enabled languages
        if hasattr(args, 'list_enabled') and args.list_enabled:
            self.display_enabled_languages(language_manager)
            return True
        
        # Handle language status
        if hasattr(args, 'language_status') and args.language_status:
            self.display_language_status(language_manager)
            return True
        
        return False

    def validate_language_selection(self, args: argparse.Namespace, language_manager: LanguageManager) -> bool:
        """
        Validate language selection against enabled languages.
        
        Args:
            args: Parsed command line arguments
            language_manager: LanguageManager instance
            
        Returns:
            True if language selection is valid, False otherwise
        """
        if hasattr(args, 'language') and args.language:
            is_valid, error_message = language_manager.validate_language_selection(args.language)
            
            if not is_valid:
                self.logger.error(f"Language validation failed: {error_message}")
                print(f"\n❌ {error_message}")
                print(f"\n💡 Use --list-enabled to see currently enabled languages")
                print(f"💡 Use --enable-language <code> to enable a specific language")
                return False
        
        return True
