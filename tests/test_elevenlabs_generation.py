#!/usr/bin/env python3
"""
Test ElevenLabs TTS generation with actual API call
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

def test_elevenlabs_generation():
    """Test ElevenLabs TTS actual generation."""
    print("Testing ElevenLabs TTS Generation...")
    
    try:
        # Initialize config manager
        config = ConfigManager()
        
        # Initialize TTS manager with ElevenLabs
        tts_manager = TTSManager(config)
        tts_manager.provider = "elevenlabs"
        tts_manager._initialize_provider()
        
        # Check if ElevenLabs is properly initialized
        if hasattr(tts_manager, 'elevenlabs_client'):
            print("✅ ElevenLabs client is initialized")
            print(f"   Voice ID: {tts_manager.elevenlabs_voice_id}")
            print(f"   Model: {tts_manager.elevenlabs_model}")
            print(f"   Stability: {tts_manager.elevenlabs_stability}")
            print(f"   Similarity Boost: {tts_manager.elevenlabs_similarity_boost}")
            
            # Test with a short text
            test_text = "Hello, this is a test of ElevenLabs text to speech integration."
            print(f"\nTesting with text: '{test_text}'")
            
            result = tts_manager.text_to_speech(test_text, title="elevenlabs_test")
            
            if result:
                print(f"✅ ElevenLabs TTS generation successful!")
                print(f"   Generated file: {result}")
                
                # Check file size
                if os.path.exists(result):
                    file_size = os.path.getsize(result)
                    print(f"   File size: {file_size} bytes")
                    
                    if file_size > 1000:  # Reasonable audio file size
                        print("✅ Generated audio file appears valid")
                    else:
                        print("⚠️ Generated audio file seems small, may have issues")
                else:
                    print("❌ Generated file does not exist")
            else:
                print("❌ ElevenLabs TTS generation failed")
        else:
            print("❌ ElevenLabs client not properly initialized")
            
    except Exception as e:
        print(f"Error during ElevenLabs testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_elevenlabs_generation()
