#!/usr/bin/env python3
"""
Test script to generate a single video using the CreepyPasta AI video generator.

This test validates the complete video generation workflow by:
1. Loading configuration from settings.yaml
2. Finding an existing audio file in assets/output
3. Generating a video using the VideoGenerator class
4. Verifying successful video creation

Requirements:
    - An existing audio file in assets/output/
    - Valid configuration in config/settings.yaml
    - All project dependencies installed
    
Usage:
    python test_single_video.py
    
Returns:
    0 if successful, 1 if failed
"""

import sys
import logging
import traceback
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the project root directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.video.video_generator import VideoGenerator
    from src.utils.config_manager import ConfigManager
except ImportError as e:
    logger.error(f"Failed to import project modules: {e}")
    logger.error("Make sure you're running from the project root directory")
    sys.exit(1)

def test_single_video():
    """Test generating a single video."""
    video_generator = None
    try:
        logger.info("Starting single video generation test...")
        
        # Initialize
        logger.info("Initializing configuration and video generator...")
        config = ConfigManager("config/settings.yaml")
        video_generator = VideoGenerator(config)
        
        # Find the first audio file
        audio_files = list(Path("assets/output").glob("*.mp3"))
        if not audio_files:
            logger.error("No audio files found in assets/output!")
            print("No audio files found!")
            return False
            
        audio_file = audio_files[0]
        logger.info(f"Found {len(audio_files)} audio files, using: {audio_file.name}")
        print(f"Testing video generation with: {audio_file.name}")
        
        # Generate video
        logger.info("Starting video generation...")
        result = video_generator.create_video(str(audio_file))
        
        if result:
            logger.info(f"Video generation successful: {result}")
            print(f"✅ Success! Video created: {result}")
            return True
        else:
            logger.error("Video generation returned None or empty result")
            print("❌ Video generation failed")
            return False
            
    except Exception as e:
        logger.error(f"Error during video generation test: {e}")
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        if video_generator is not None:
            try:
                logger.info("Cleaning up temporary files...")
                video_generator.cleanup_temp_files()
            except Exception as cleanup_error:
                logger.warning(f"Error during cleanup: {cleanup_error}")
                print(f"Warning: Error during cleanup: {cleanup_error}")

if __name__ == "__main__":
    logger.info("Starting CreepyPasta AI video generation test...")
    success = test_single_video()
    
    if success:
        logger.info("✅ Video generation test completed successfully!")
        print("\n🎉 Test passed! Video generation is working correctly.")
    else:
        logger.error("❌ Video generation test failed!")
        print("\n💥 Test failed! Check the logs for details.")
    
    sys.exit(0 if success else 1)
