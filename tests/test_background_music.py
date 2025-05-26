#!/usr/bin/env python3
"""
Test script to verify background music is properly added to generated videos.
"""

import os
import sys
from pathlib import Path
import logging

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from moviepy.editor import VideoFileClip
from src.utils.config_manager import ConfigManager

def test_video_has_background_music(video_path: str):
    """
    Test if a video file contains background music by analyzing its audio track.
    
    Args:
        video_path: Path to the video file to test
        
    Returns:
        bool: True if background music is detected, False otherwise
    """
    try:
        print(f"\n=== Testing Video: {Path(video_path).name} ===")
        
        # Load the video
        video = VideoFileClip(video_path)
        
        if video.audio is None:
            print("❌ Video has no audio track!")
            video.close()
            return False
        
        # Get audio information
        audio_duration = video.audio.duration
        video_duration = video.duration
        
        print(f"📊 Video duration: {video_duration:.2f} seconds")
        print(f"🔊 Audio duration: {audio_duration:.2f} seconds")
        
        # Check if audio duration matches video duration (indicates combined audio)
        duration_match = abs(audio_duration - video_duration) < 0.5
        print(f"⏱️  Audio/Video duration match: {'✅' if duration_match else '❌'}")
        
        # Extract a sample of audio to check if it contains more than just speech
        # This is a simple test - in a real scenario, you might want to do
        # spectral analysis to detect different frequency patterns
        sample_audio = video.audio.subclip(5, min(10, audio_duration))
        
        # Check if the audio array has variations that suggest background music
        audio_array = sample_audio.to_soundarray()
        
        # Calculate basic audio statistics
        audio_mean = audio_array.mean()
        audio_std = audio_array.std()
        audio_max = audio_array.max()
        audio_min = audio_array.min()
        
        print(f"🎵 Audio statistics:")
        print(f"   Mean amplitude: {audio_mean:.6f}")
        print(f"   Standard deviation: {audio_std:.6f}")
        print(f"   Max amplitude: {audio_max:.6f}")
        print(f"   Min amplitude: {audio_min:.6f}")
        
        # Cleanup
        sample_audio.close()
        video.close()
        
        # Simple heuristic: if there's significant audio variation, likely contains music
        has_background_music = audio_std > 0.01 and duration_match
        
        result = "✅ Background music detected!" if has_background_music else "❌ No background music detected"
        print(f"🎼 Result: {result}")
        
        return has_background_music
        
    except Exception as e:
        print(f"❌ Error testing video: {e}")
        return False

def test_background_music_config():
    """Test that background music configuration is properly loaded."""
    try:
        print("\n=== Testing Background Music Configuration ===")
        
        config = ConfigManager()
        
        # Test various config paths that the video generator checks
        config_paths = [
            "video.background_music.volume",
            "audio.volume.background_music", 
            "audio.background_music.volume",
            "video.background_music_volume"
        ]
        
        print("🔧 Configuration values:")
        for path in config_paths:
            value = config.get(path, "NOT_FOUND")
            print(f"   {path}: {value}")
        
        # Check if background music is enabled
        bg_music_enabled = config.get("audio.background_music.enabled", False)
        print(f"🎵 Background music enabled: {'✅' if bg_music_enabled else '❌'} ({bg_music_enabled})")
        
        # Check music file path
        music_path = Path("assets/music/creepy-music.mp3")
        music_exists = music_path.exists()
        print(f"🎶 Music file exists: {'✅' if music_exists else '❌'} ({music_path})")
        
        if music_exists:
            file_size = music_path.stat().st_size
            print(f"   File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
        
        return bg_music_enabled and music_exists
        
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")
        return False

def main():
    """Main test function."""
    print("🎬 CreepyPasta AI - Background Music Test")
    print("=" * 50)
    
    # Test configuration first
    config_ok = test_background_music_config()
    
    if not config_ok:
        print("\n❌ Configuration issues detected. Please fix before testing videos.")
        return False
    
    # Find the most recent video files
    videos_path = Path("assets/videos")
    if not videos_path.exists():
        print(f"\n❌ Videos directory not found: {videos_path}")
        return False
    
    video_files = list(videos_path.glob("*.mp4"))
    if not video_files:
        print(f"\n❌ No video files found in {videos_path}")
        return False
    
    # Sort by modification time (most recent first)
    video_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    print(f"\n📁 Found {len(video_files)} video files. Testing the 3 most recent...")
    
    # Test the 3 most recent videos
    test_results = []
    for i, video_file in enumerate(video_files[:3]):
        result = test_video_has_background_music(str(video_file))
        test_results.append((video_file.name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY:")
    print("=" * 50)
    
    successful_tests = sum(1 for _, result in test_results if result)
    total_tests = len(test_results)
    
    for filename, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {filename}")
    
    print(f"\n🎯 Overall Result: {successful_tests}/{total_tests} videos have background music")
    
    if successful_tests == total_tests:
        print("🎉 All tests passed! Background music is working correctly.")
        return True
    else:
        print("⚠️  Some videos are missing background music. Check the logs for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
