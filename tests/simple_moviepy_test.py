#!/usr/bin/env python3
"""
Simple test to debug MoviePy issues.
"""

from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips
from pathlib import Path
import tempfile

def simple_test():
    try:
        print("Testing basic MoviePy functionality...")
        
        # Test 1: Load an audio file
        audio_files = list(Path("assets/output").glob("*.mp3"))
        if not audio_files:
            print("No audio files found!")
            return
            
        audio_file = audio_files[0]
        print(f"Loading audio: {audio_file}")
        audio = AudioFileClip(str(audio_file))
        print(f"Audio duration: {audio.duration:.2f} seconds")
        
        # Test 2: Load an image
        image_files = list(Path("assets/images").glob("*.png"))
        if not image_files:
            print("No image files found!")
            return
            
        image_file = image_files[0]
        print(f"Loading image: {image_file}")
        
        # Create a simple video clip from the image
        img_clip = ImageClip(str(image_file), duration=5.0)
        print(f"Image clip created: {img_clip.duration} seconds")
        
        # Set the audio
        final_clip = img_clip.set_audio(audio.subclip(0, 5.0))
        print("Audio attached to video clip")
        
        # Try to write the video
        output_path = Path("assets/videos/test_simple.mp4")
        print(f"Attempting to write video to: {output_path}")
        
        final_clip.write_videofile(
            str(output_path),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        print("✅ Success! Simple video test passed")
        
        # Cleanup
        audio.close()
        img_clip.close()
        final_clip.close()
        
    except Exception as e:
        print(f"❌ Error in simple test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_test()
