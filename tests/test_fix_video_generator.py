#!/usr/bin/env python3
"""
Test script to verify MoviePy video generation without deprecated progress_bar parameter.

This test creates a simple video clip and exports it to verify that the MoviePy
write_videofile method works correctly without the deprecated progress_bar parameter
that was causing issues in newer versions of MoviePy.

Requirements:
    - moviepy: For video generation and processing
    
Usage:
    python test_fix_video_generator.py
    
Returns:
    0 if successful, 1 if failed
"""

import sys
import os
import traceback
from pathlib import Path
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent))

# Import the necessary modules
try:
    from moviepy.editor import ImageClip, AudioFileClip
except ImportError as e:
    logger.error(f"Failed to import MoviePy: {e}")
    logger.error("Please install MoviePy: pip install moviepy")
    sys.exit(1)

def test_write_videofile_no_progress_bar():
    """Test that the write_videofile method works without a progress_bar parameter"""
    img_clip = None
    try:
        # Create a simple clip
        logger.info("Creating a simple test clip...")
        
        # Create a blank image
        img_clip = ImageClip(size=(640, 360), color=(0, 0, 0), duration=3)
        
        # Set up output path
        output_path = Path("temp/test_no_progress_bar.mp4")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Try to write the clip to a file without the progress_bar parameter
        logger.info(f"Writing clip to {output_path}...")
        img_clip.write_videofile(
            str(output_path),
            fps=24,
            codec='libx264',
            verbose=False,
            logger=None
        )
        
        # Check if the file was created
        if output_path.exists():
            logger.info("✅ Success! Video file was created successfully without progress_bar parameter")
            return True
        else:
            logger.error("❌ Failed: Video file was not created")
            return False
    
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        traceback.print_exc()
        return False
    finally:
        # Clean up
        if img_clip is not None:
            try:
                img_clip.close()
            except Exception as cleanup_error:
                logger.warning(f"Error during cleanup: {cleanup_error}")
        
        # Clean up the test file if it exists
        try:
            test_file = Path("temp/test_no_progress_bar.mp4")
            if test_file.exists():
                test_file.unlink()
                logger.info("Test file cleaned up successfully")
        except Exception as cleanup_error:
            logger.warning(f"Error cleaning up test file: {cleanup_error}")

if __name__ == "__main__":
    logger.info("Starting MoviePy progress_bar parameter test...")
    success = test_write_videofile_no_progress_bar()
    
    if success:
        logger.info("✅ All tests passed!")
        sys.exit(0)
    else:
        logger.error("❌ Tests failed!")
        sys.exit(1)
