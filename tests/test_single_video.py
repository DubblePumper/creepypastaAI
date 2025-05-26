#!/usr/bin/env python3
"""
Test script to generate a single video to verify the MoviePy fixes.
"""

import sys
import logging
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.video.video_generator import VideoGenerator
from src.utils.config_manager import ConfigManager

def test_single_video():
    """Test generating a single video."""
    try:
        # Initialize
        config = ConfigManager("config/settings.yaml")
        video_generator = VideoGenerator(config)
        
        # Find the first audio file
        audio_files = list(Path("assets/output").glob("*.mp3"))
        if not audio_files:
            print("No audio files found!")
            return False
            
        audio_file = audio_files[0]
        print(f"Testing video generation with: {audio_file.name}")
        
        # Generate video
        result = video_generator.create_video(str(audio_file))
        
        if result:
            print(f"✅ Success! Video created: {result}")
            return True
        else:
            print("❌ Video generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        # Cleanup
        try:
            video_generator.cleanup_temp_files()
        except:
            pass

if __name__ == "__main__":
    success = test_single_video()
    sys.exit(0 if success else 1)
