#!/usr/bin/env python3
"""
Test script for DeepL integration in CreepyPasta AI

This script tests the DeepL translation functionality.
Run this script to verify DeepL integration is working correctly.
"""

import os
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.config_manager import ConfigManager
from src.utils.translation_manager import TranslationManager


def test_deepl_providers():
    """Test DeepL translation providers."""
    print("🧪 Testing DeepL Translation Integration")
    print("=" * 50)
    
    try:
        # Initialize config and translation manager
        config = ConfigManager()
        
        # Test text
        test_text = "This is a dark and scary story about mysterious shadows lurking in the night."
        target_language = "de"  # German
        
        print(f"📝 Test text: {test_text}")
        print(f"🎯 Target language: {target_language}")
        print()
        
        # Test DeepL (deep-translator)
        print("🔧 Testing DeepL (deep-translator)...")
        config.set("multilingual.translation.provider", "deepl")
        translator = TranslationManager(config)
        
        if translator.deepl_client:
            result = translator.translate_text(test_text, target_language)
            print(f"✅ DeepL Translation: {result}")
        else:
            print("❌ DeepL (deep-translator) not available")
        print()
        
        # Test DeepL API
        print("🔧 Testing DeepL API (official client)...")
        config.set("multilingual.translation.provider", "deepl-api")
        translator_api = TranslationManager(config)
        
        if translator_api.deepl_api_client:
            result_api = translator_api.translate_text(test_text, target_language)
            print(f"✅ DeepL API Translation: {result_api}")
        else:
            print("❌ DeepL API not available")
        print()
        
        # Test provider switching
        print("🔄 Testing provider switching...")
        success = translator.set_provider("deepl-api")
        if success:
            print("✅ Successfully switched to deepl-api")
        else:
            print("❌ Failed to switch to deepl-api")
        
        success = translator.set_provider("deepl")
        if success:
            print("✅ Successfully switched to deepl")
        else:
            print("❌ Failed to switch to deepl")
        
        print()
        
        # Test language code conversion
        print("🌐 Testing language code conversion...")
        test_codes = ["en", "de", "fr", "es", "nl", "pt", "ja", "ko"]
        for code in test_codes:
            deepl_code = translator._convert_to_deepl_lang(code)
            print(f"   {code} -> {deepl_code}")
        
        print()
        print("🎉 DeepL integration test completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


def check_deepl_availability():
    """Check if DeepL libraries and API keys are available."""
    print("🔍 Checking DeepL Requirements")
    print("=" * 40)
    
    # Check deep-translator library
    try:
        from deep_translator import DeepL
        print("✅ deep-translator library available")
    except ImportError:
        print("❌ deep-translator library not found")
        print("   Install with: pip install deep-translator")
    
    # Check deepl library
    try:
        import deepl
        print("✅ deepl library available")
    except ImportError:
        print("❌ deepl library not found")
        print("   Install with: pip install deepl")
    
    # Check API key
    deepl_key = os.getenv("DEEPL_API_KEY")
    if deepl_key:
        is_free = deepl_key.endswith(":fx")
        api_type = "free" if is_free else "pro"
        print(f"✅ DeepL API key found ({api_type})")
    else:
        print("❌ DEEPL_API_KEY not found in environment")
        print("   Set your DeepL API key in .env file")
    
    print()


if __name__ == "__main__":
    print("🌍 CreepyPasta AI - DeepL Translation Test")
    print("=" * 50)
    print()
    
    check_deepl_availability()
    test_deepl_providers()
