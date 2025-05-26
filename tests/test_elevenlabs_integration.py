#!/usr/bin/env python3
"""
Test script for ElevenLabs TTS integration
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from src.utils.config_manager import ConfigManager
from src.audio.tts_manager import TTSManager

def test_tts_providers():
    """Test TTS provider availability and functionality."""
    print("Testing TTS Manager Integration...")
    
    try:
        # Initialize config manager
        config = ConfigManager()
        
        # Initialize TTS manager
        tts_manager = TTSManager(config)
        
        # Check available providers
        providers = tts_manager.get_available_providers()
        print(f"\nAvailable TTS providers: {providers}")
        
        # Test if ElevenLabs is in the list
        if "elevenlabs" in providers:
            print("✅ ElevenLabs TTS is available and configured!")
        else:
            print("ℹ️ ElevenLabs TTS is not available (check API key and installation)")
        
        # Test each provider (if available)
        test_text = "This is a test of the text-to-speech system."
        
        for provider in providers:
            print(f"\nTesting {provider} provider...")
            
            # Temporarily set the provider
            original_provider = tts_manager.provider
            tts_manager.provider = provider
            tts_manager._initialize_provider()
            
            # Try to generate a short test
            if provider == "elevenlabs":
                print(f"  - ElevenLabs configured with voice: {getattr(tts_manager, 'elevenlabs_voice_id', 'N/A')}")
                print(f"  - ElevenLabs model: {getattr(tts_manager, 'elevenlabs_model', 'N/A')}")
                print("  - Note: ElevenLabs requires a valid API key for actual generation")
            else:
                # Test with a very short text for non-ElevenLabs providers
                result = tts_manager.text_to_speech("Test", title="test_audio")
                if result:
                    print(f"  ✅ {provider} TTS generation successful: {result}")
                    # Clean up test file
                    try:
                        os.unlink(result)
                    except:
                        pass
                else:
                    print(f"  ❌ {provider} TTS generation failed")
            
            # Restore original provider
            tts_manager.provider = original_provider
            tts_manager._initialize_provider()
            
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tts_providers()
