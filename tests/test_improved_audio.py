#!/usr/bin/env python3
"""
Simple test to generate one video with improved background music settings.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config_manager import ConfigManager
from src.video.video_generator import VideoGenerator

def test_single_video():
    """Test generating a single video with improved audio settings."""
    try:
        print("🎬 Testing improved background music settings...")
        
        # Initialize config and video generator
        config = ConfigManager()
        video_gen = VideoGenerator(config)
        
        # Find the first audio file
        audio_files = list(Path("assets/output").glob("*.mp3"))
        if not audio_files:
            print("❌ No audio files found")
            return False
        
        test_audio = audio_files[0]
        print(f"🎵 Using audio file: {test_audio.name}")
        
        # Create output directory for test
        test_output_dir = Path("tests/results/videos")
        test_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate video
        print("🎬 Generating test video...")
        video_path = video_gen.create_video(
            str(test_audio),
            output_dir=str(test_output_dir)
        )
        
        if video_path:
            print(f"✅ Test video created: {Path(video_path).name}")
            print(f"📁 Location: {video_path}")
            print("\n🎧 LUISTER NAAR DE TEST VIDEO om te checken of de achtergrondmuziek nu hoorbaar is!")
            return True
        else:
            print("❌ Failed to create test video")
            return False
            
    except Exception as e:
        print(f"❌ Error in test: {e}")
        return False

if __name__ == "__main__":
    success = test_single_video()
    if success:
        print("\n🎯 Test completed successfully!")
        print("🔊 Background music volume is now set to 80%")
        print("🎤 Narration volume is reduced to 70%")
        print("🎵 This should make the background music much more audible!")
    else:
        print("\n❌ Test failed!")
    
    sys.exit(0 if success else 1)
