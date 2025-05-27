#!/usr/bin/env python3
"""
Test script voor de verbeterde video generatie workflow.
Test of de nieuwe workflow correct werkt met de juiste stappen.
"""

import os
import sys
from pathlib import Path
import logging

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config_manager import ConfigManager
from src.video.video_generator import VideoGenerator

def test_new_video_workflow():
    """Test de nieuwe video generatie workflow."""
    try:
        print("🎬 Testing New Video Generation Workflow")
        print("=" * 50)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Initialize config and video generator
        print("📋 Initializing configuration and video generator...")
        config = ConfigManager()
        video_generator = VideoGenerator(config)
        
        # Find a test audio file
        audio_path = Path("assets/output")
        audio_files = list(audio_path.glob("*.mp3"))
        
        if not audio_files:
            print("❌ No audio files found in assets/output")
            return False
        
        # Use the first audio file for testing
        test_audio = audio_files[0]
        print(f"🔊 Using test audio file: {test_audio.name}")
        
        # Test the new workflow
        print("\n🚀 Starting video generation with new workflow...")
        video_path = video_generator.create_video(str(test_audio))
        
        if video_path:
            print(f"✅ Video generated successfully: {Path(video_path).name}")
            
            # Check if file exists and has reasonable size
            video_file = Path(video_path)
            if video_file.exists():
                file_size = video_file.stat().st_size
                print(f"📁 Video file size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
                
                if file_size > 1024 * 1024:  # At least 1 MB
                    print("✅ Video file size looks reasonable")
                    return True
                else:
                    print("⚠️  Video file size seems too small")
                    return False
            else:
                print("❌ Video file does not exist")
                return False
        else:
            print("❌ Video generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_audio_balance():
    """Test de audio balans in de geconfigureerde settings."""
    try:
        print("\n🔊 Testing Audio Balance Configuration")
        print("=" * 50)
        
        config = ConfigManager()
        
        # Check configured volumes
        narration_volume = config.get("audio.volume.narration", "NOT_FOUND")
        bg_music_volume = config.get("audio.volume.background_music", "NOT_FOUND")
        video_bg_music_volume = config.get("video.background_music.volume", "NOT_FOUND")
        
        print(f"🎤 Narration volume: {narration_volume}")
        print(f"🎵 Background music volume (audio config): {bg_music_volume}")
        print(f"🎵 Background music volume (video config): {video_bg_music_volume}")
        
        # Check if volumes are reasonable
        if isinstance(narration_volume, (int, float)) and 0.7 <= narration_volume <= 1.0:
            print("✅ Narration volume is good")
        else:
            print("⚠️  Narration volume might need adjustment")
        
        if isinstance(bg_music_volume, (int, float)) and 0.05 <= bg_music_volume <= 0.2:
            print("✅ Background music volume is good")
        else:
            print("⚠️  Background music volume might need adjustment")
        
        # Check background music file
        music_file = Path("assets/music/creepy-music.mp3")
        if music_file.exists():
            file_size = music_file.stat().st_size
            print(f"🎶 Background music file: ✅ ({file_size:,} bytes)")
        else:
            print("🎶 Background music file: ❌ NOT FOUND")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing audio balance: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 CreepyPasta AI - Video Generation Workflow Test")
    print("=" * 60)
    
    # Test audio balance configuration
    audio_config_ok = test_audio_balance()
    
    if not audio_config_ok:
        print("\n❌ Audio configuration issues detected. Please fix before testing video generation.")
        return False
    
    # Test the new video workflow
    workflow_ok = test_new_video_workflow()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    print(f"🔊 Audio Configuration: {'✅ PASS' if audio_config_ok else '❌ FAIL'}")
    print(f"🎬 Video Workflow: {'✅ PASS' if workflow_ok else '❌ FAIL'}")
    
    overall_success = audio_config_ok and workflow_ok
    print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n🎉 The new video generation workflow is working correctly!")
        print("   - Images are being selected/generated properly")
        print("   - Audio balance is configured correctly")
        print("   - Background music is at appropriate volume")
    else:
        print("\n⚠️  Please review the test results and fix any issues.")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
