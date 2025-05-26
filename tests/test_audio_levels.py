#!/usr/bin/env python3
"""
Test script to verify and analyze audio levels in generated videos.
"""

import os
import sys
from pathlib import Path
import logging

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from moviepy.editor import VideoFileClip, AudioFileClip
import numpy as np

def analyze_audio_file(file_path: str, label: str):
    """Analyze audio levels in a file."""
    try:
        print(f"\n=== Analyzing {label}: {Path(file_path).name} ===")
        
        if not Path(file_path).exists():
            print(f"❌ File not found: {file_path}")
            return
        
        # Load audio
        audio = AudioFileClip(file_path)
        print(f"⏱️  Duration: {audio.duration:.2f} seconds")
        
        # Get audio array for analysis
        audio_array = audio.to_soundarray()
        
        # Calculate statistics
        if len(audio_array.shape) > 1:
            # Stereo - average the channels
            audio_mono = np.mean(audio_array, axis=1)
        else:
            audio_mono = audio_array
        
        rms = np.sqrt(np.mean(audio_mono**2))
        peak = np.max(np.abs(audio_mono))
        
        print(f"🔊 RMS Level: {rms:.6f}")
        print(f"📈 Peak Level: {peak:.6f}")
        print(f"📊 Peak dB: {20 * np.log10(peak) if peak > 0 else -np.inf:.2f} dB")
        print(f"🎵 RMS dB: {20 * np.log10(rms) if rms > 0 else -np.inf:.2f} dB")
        
        # Check if audio has significant content
        if rms > 0.001:
            print("✅ Audio has significant content")
        else:
            print("⚠️  Audio level very low")
        
        audio.close()
        return rms, peak
        
    except Exception as e:
        print(f"❌ Error analyzing {label}: {e}")
        return None, None

def test_background_music_isolation():
    """Test the background music file directly."""
    music_file = Path("assets/music/creepy-music.mp3")
    
    if not music_file.exists():
        print("❌ Background music file not found!")
        return False
    
    rms, peak = analyze_audio_file(str(music_file), "Background Music")
    return rms is not None and rms > 0.001

def test_video_audio_separation():
    """Test a generated video to see if we can detect background music."""
    videos_path = Path("assets/videos")
    video_files = list(videos_path.glob("*.mp4"))
    
    if not video_files:
        print("❌ No video files found to test")
        return False
    
    # Get the most recent video
    latest_video = max(video_files, key=lambda x: x.stat().st_mtime)
    
    print(f"\n=== Testing Video Audio Separation ===")
    print(f"📁 Testing: {latest_video.name}")
    
    try:
        # Load video
        video = VideoFileClip(str(latest_video))
        
        if video.audio is None:
            print("❌ Video has no audio!")
            video.close()
            return False
        
        # Analyze the combined audio
        rms, peak = analyze_audio_file(str(latest_video), "Video Audio")
        
        # Try to extract just first few seconds for comparison
        print(f"\n--- Analyzing Audio Segments ---")
        
        # Sample different parts of the audio
        duration = min(video.audio.duration, 30)  # Max 30 seconds
        segment_duration = 5
        
        for i in range(0, int(duration), segment_duration):
            end_time = min(i + segment_duration, duration)
            segment = video.audio.subclip(i, end_time)
            
            audio_array = segment.to_soundarray()
            if len(audio_array.shape) > 1:
                audio_mono = np.mean(audio_array, axis=1)
            else:
                audio_mono = audio_array
            
            rms_segment = np.sqrt(np.mean(audio_mono**2))
            peak_segment = np.max(np.abs(audio_mono))
            
            print(f"⏰ Segment {i}-{end_time}s: RMS={rms_segment:.6f}, Peak={peak_segment:.6f}")
            
            segment.close()
        
        video.close()
        return True
        
    except Exception as e:
        print(f"❌ Error testing video: {e}")
        return False

def create_test_audio_mix():
    """Create a test audio mix with higher background music volume."""
    try:
        print(f"\n=== Creating Test Audio Mix ===")
        
        # Find an audio file to work with
        audio_files = list(Path("assets/output").glob("*.mp3"))
        if not audio_files:
            print("❌ No audio files found for testing")
            return False
        
        # Use the first audio file
        test_narration = audio_files[0]
        music_file = Path("assets/music/creepy-music.mp3")
        
        if not music_file.exists():
            print("❌ Background music file not found")
            return False
        
        print(f"🎵 Using narration: {test_narration.name}")
        print(f"🎶 Using music: {music_file.name}")
        
        # Load audio files
        narration = AudioFileClip(str(test_narration))
        background_music = AudioFileClip(str(music_file))
        
        # Trim music to match narration
        if background_music.duration < narration.duration:
            # Loop music if needed
            loops_needed = int(narration.duration / background_music.duration) + 1
            from moviepy.editor import concatenate_audioclips
            background_music = concatenate_audioclips([background_music] * loops_needed)
        
        background_music = background_music.subclip(0, narration.duration)
        
        # Test different volume levels
        test_volumes = [0.1, 0.3, 0.5, 0.7, 0.9]
        
        test_results_dir = Path("tests/results")
        test_results_dir.mkdir(parents=True, exist_ok=True)
        
        for volume in test_volumes:
            print(f"🔊 Creating test mix with background volume: {volume}")
            
            # Adjust background music volume
            bg_music_adjusted = background_music.volumex(volume)
            
            # Create composite audio
            from moviepy.editor import CompositeAudioClip
            composite = CompositeAudioClip([narration, bg_music_adjusted])
            
            # Export test file
            output_file = test_results_dir / f"test_audio_mix_bg_{volume:.1f}.mp3"
            composite.write_audiofile(str(output_file), verbose=False, logger=None)
            
            print(f"✅ Created: {output_file.name}")
            
            # Cleanup
            bg_music_adjusted.close()
            composite.close()
        
        # Cleanup
        narration.close()
        background_music.close()
        
        print(f"\n✅ Test audio files created in: {test_results_dir}")
        print("🎧 Play these files to find the optimal background music volume!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test mix: {e}")
        return False

def main():
    """Main test function."""
    print("🎵 CreepyPasta AI - Audio Level Analysis")
    print("=" * 60)
    
    # Test 1: Background music file
    print("Step 1: Testing background music file...")
    music_ok = test_background_music_isolation()
    
    # Test 2: Video audio analysis
    print("\nStep 2: Testing video audio...")
    video_ok = test_video_audio_separation()
    
    # Test 3: Create test mixes
    print("\nStep 3: Creating test audio mixes...")
    test_ok = create_test_audio_mix()
    
    print("\n" + "=" * 60)
    print("📋 ANALYSIS SUMMARY:")
    print("=" * 60)
    
    if music_ok:
        print("✅ Background music file is valid and audible")
    else:
        print("❌ Background music file has issues")
    
    if video_ok:
        print("✅ Video audio analysis completed")
    else:
        print("❌ Video audio analysis failed")
    
    if test_ok:
        print("✅ Test audio mixes created successfully")
        print("\n🎧 RECOMMENDATION:")
        print("   Listen to the test files in tests/results/")
        print("   Find the optimal background volume and update the config!")
    else:
        print("❌ Test audio mix creation failed")
    
    return music_ok and video_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
