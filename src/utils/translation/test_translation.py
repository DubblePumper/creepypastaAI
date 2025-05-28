"""
Test script for the new modular translation system.

This script tests the reorganized translation system to ensure all components
work correctly together.
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

def test_basic_imports():
    """Test that all imports work correctly."""
    print("Testing imports...")
    
    try:
        # Test new modular system imports
        from src.utils.translation import TranslationManager
        from src.utils.translation import GoogleTranslateProvider
        from src.utils.translation.config_examples import BASIC_CONFIG
        print("✓ New modular system imports successful")
        
        # Test legacy imports
        from src.utils.translation_manager import TranslationManager as LegacyManager
        print("✓ Legacy system imports successful")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_basic_translation():
    """Test basic translation functionality."""
    print("\nTesting basic translation...")
    
    try:
        from src.utils.translation import TranslationManager
        from src.utils.translation.config_examples import BASIC_CONFIG
        
        # Create translation manager
        manager = TranslationManager(BASIC_CONFIG)
        
        # Test basic translation
        result = manager.translate_text("Hello world", "es")
        
        if result['success']:
            print(f"✓ Translation successful: '{result['translated_text']}'")
            print(f"  Provider used: {result['provider_used']}")
            return True
        else:
            print(f"✗ Translation failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"✗ Translation test failed: {e}")
        return False

def test_language_detection():
    """Test language detection functionality."""
    print("\nTesting language detection...")
    
    try:
        from src.utils.translation import TranslationManager
        from src.utils.translation.config_examples import BASIC_CONFIG
        
        manager = TranslationManager(BASIC_CONFIG)
        
        # Test language detection
        result = manager.detect_language("Bonjour le monde")
        
        if result['success']:
            print(f"✓ Language detection successful: '{result['language_code']}'")
            print(f"  Provider used: {result['provider_used']}")
            return True
        else:
            print(f"✗ Language detection failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"✗ Language detection test failed: {e}")
        return False

def test_provider_info():
    """Test provider information functionality."""
    print("\nTesting provider information...")
    
    try:
        from src.utils.translation import TranslationManager
        from src.utils.translation.config_examples import BASIC_CONFIG
        
        manager = TranslationManager(BASIC_CONFIG)
        
        # Get available providers
        providers = manager.get_available_providers()
        print(f"✓ Available providers: {providers}")
        
        # Get provider info
        info = manager.get_provider_info()
        for provider_name, provider_info in info.items():
            print(f"  - {provider_name}: {provider_info.get('description', 'No description')}")
        
        return True
        
    except Exception as e:
        print(f"✗ Provider info test failed: {e}")
        return False

def test_legacy_compatibility():
    """Test legacy compatibility."""
    print("\nTesting legacy compatibility...")
    
    try:
        from src.utils.translation_manager import TranslationManager
        
        # Test legacy manager creation
        manager = TranslationManager()
        
        # Test legacy translate method
        result = manager.translate("Hello world", "es")
        print(f"✓ Legacy translation successful: '{result}'")
        
        # Test legacy language detection
        detected = manager.detect_language_legacy("Bonjour le monde")
        print(f"✓ Legacy language detection successful: '{detected}'")
        
        return True
        
    except Exception as e:
        print(f"✗ Legacy compatibility test failed: {e}")
        return False

def test_health_check():
    """Test health check functionality."""
    print("\nTesting health check...")
    
    try:
        from src.utils.translation import TranslationManager
        from src.utils.translation.config_examples import BASIC_CONFIG
        
        manager = TranslationManager(BASIC_CONFIG)
        
        # Perform health check
        health = manager.health_check()
        
        print(f"✓ Overall health: {health['overall_health']}")
        print(f"  Available providers: {health['available_providers']}/{health['total_providers']}")
        
        for provider_name, provider_health in health['providers'].items():
            status = "✓" if provider_health['available'] else "✗"
            print(f"  {status} {provider_name}: {'Available' if provider_health['available'] else 'Unavailable'}")
            if provider_health['error']:
                print(f"    Error: {provider_health['error']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Health check test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("TESTING MODULAR TRANSLATION SYSTEM")
    print("=" * 60)
    
    tests = [
        test_basic_imports,
        test_basic_translation,
        test_language_detection,
        test_provider_info,
        test_legacy_compatibility,
        test_health_check
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All tests passed! The translation system is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
