#!/usr/bin/env python3
"""
Simple MoviePy Video Test

Test basic video creation with MoviePy to diagnose the logger issue.
"""

import logging
import tempfile
from pathlib import Path
from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_moviepy_video():
    """Test basic MoviePy video creation."""
    
    print("🎬 Testing MoviePy Video Creation")
    print("=" * 50)
    
    # Check files exist
    audio_file = Path("assets/output/Evil_20250526_140518.mp3")
    image_dir = Path("assets/images")
    output_file = Path("test_output.mp4")
    
    print(f"Audio file exists: {audio_file.exists()}")
    print(f"Images dir exists: {image_dir.exists()}")
    
    if not audio_file.exists():
        print("❌ Audio file not found")
        return
    
    # Get an image
    image_files = list(image_dir.glob("*.png"))
    if not image_files:
        print("❌ No image files found")
        return
    
    image_file = image_files[0]
    print(f"Using image: {image_file}")
    
    try:
        # Load audio
        print("🎵 Loading audio...")
        audio = AudioFileClip(str(audio_file))
        print(f"Audio duration: {audio.duration} seconds")
        
        # Create image clip
        print("🖼️ Creating image clip...")
        image_clip = ImageClip(str(image_file), duration=audio.duration)
        image_clip = image_clip.resize((1920, 1080))
        
        # Create video
        print("🎬 Creating video...")
        video = CompositeVideoClip([image_clip])
        video = video.set_audio(audio)
        
        # Configure temp directory
        temp_dir = Path("temp/video")
        temp_dir.mkdir(parents=True, exist_ok=True)
        old_tempdir = tempfile.tempdir
        tempfile.tempdir = str(temp_dir)
        
        print("💾 Writing video file...")
        try:
            # Test the most minimal write approach
            video.write_videofile(
                str(output_file),
                fps=24,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            print("✅ Video created successfully!")
            
        except Exception as e:
            print(f"❌ Write error: {e}")
            
            # Try alternative approach
            print("🔄 Trying alternative approach...")
            try:
                video.write_videofile(
                    str(output_file),
                    fps=24
                )
                print("✅ Alternative approach worked!")
            except Exception as e2:
                print(f"❌ Alternative approach failed: {e2}")
                
        finally:
            tempfile.tempdir = old_tempdir
            video.close()
            audio.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_moviepy_video()
