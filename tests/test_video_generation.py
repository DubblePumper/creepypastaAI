#!/usr/bin/env python3
"""
Test module for video generation functionality.

This module contains comprehensive tests for the video generation system,
including tests with and without OpenAI API integration. Follows best practices
for test organization, naming conventions, and output management.
"""

import os
import sys
import logging
import unittest
from pathlib import Path
from datetime import datetime
from unittest.mock import patch

# Add the parent directory to Python path to access src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config_manager import ConfigManager
from src.video.video_generator import VideoGenerator


class TestVideoGeneration(unittest.TestCase):
    """Test cases for video generation functionality."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class with necessary configurations."""
        cls.setup_test_logging()
        cls.logger = logging.getLogger(__name__)
        cls.test_results_dir = Path(__file__).parent / "results" / "videos"
        cls.test_results_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize test timestamp for unique file naming
        cls.test_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            cls.config = ConfigManager()
            cls.video_generator = VideoGenerator(cls.config)
            cls.logger.info("Test setup completed successfully")
        except Exception as e:
            cls.logger.error(f"Test setup failed: {e}")
            raise
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests complete."""
        cls.logger.info("Video generation tests completed")
    
    @staticmethod
    def setup_test_logging():
        """Configure logging for test execution."""
        # Create logs directory if it doesn't exist
        logs_dir = Path(__file__).parent.parent / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        # Configure logging with timestamp
        log_filename = f"test_video_generation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_filepath = logs_dir / log_filename
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filepath),
                logging.StreamHandler()
            ]
        )
    
    def create_test_images_for_video_generation(self, num_images=3):
        """
        Create dummy horror images for testing video generation.
        
        Args:
            num_images: Number of test images to create
            
        Returns:
            List of paths to created test images
        """
        from PIL import Image, ImageDraw, ImageFont
        
        test_images = []
        test_images_dir = Path(__file__).parent / "results" / "images"
        test_images_dir.mkdir(parents=True, exist_ok=True)
        
        for i in range(num_images):
            # Create atmospheric horror-themed test image
            img = Image.new('RGB', (1792, 1024), color=(15, 15, 25))  # Dark blue background
            draw = ImageDraw.Draw(img)
            
            # Try to use system font, fall back to default
            try:
                font = ImageFont.truetype("arial.ttf", 80)
            except OSError:
                font = ImageFont.load_default()
            
            # Add creepy text
            text = f"Test Horror Scene {i+1}"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Center the text
            x = (1792 - text_width) // 2
            y = (1024 - text_height) // 2
            
            draw.text((x, y), text, fill=(180, 180, 190), font=font)
            
            # Add atmospheric elements
            draw.ellipse([100, 100, 200, 200], fill=(80, 20, 20))  # Dark red circle
            draw.rectangle([1500, 800, 1600, 900], fill=(20, 80, 20))  # Dark green rectangle
            draw.polygon([(300, 300), (350, 250), (400, 300), (350, 350)], fill=(60, 60, 100))  # Diamond shape
              # Save with descriptive naming convention
            filename = f"test_horror_image_{i+1}_{self.test_timestamp}.png"
            image_path = test_images_dir / filename
            img.save(image_path)
            test_images.append(str(image_path))
            
            self.logger.info(f"Created test image: {filename}")
        
        return test_images
    
    def test_video_generator_initialization(self):
        """Test that the video generator can be initialized properly."""
        self.assertIsNotNone(self.video_generator)
        self.assertIsNotNone(self.video_generator.config)
        self.assertTrue(self.video_generator.videos_path.exists())
        self.logger.info("PASSED: Video generator initialization test passed")
    
    def test_dummy_image_creation(self):
        """Test creation of dummy images for video generation."""
        test_images = self.create_test_images_for_video_generation(num_images=2)
        
        self.assertEqual(len(test_images), 2)
        
        for image_path in test_images:
            image_file = Path(image_path)
            self.assertTrue(image_file.exists(), f"Image file should exist: {image_path}")
            self.assertGreater(image_file.stat().st_size, 1000, "Image file should have reasonable size")
            
        self.logger.info("PASSED: Dummy image creation test passed")
    
    def test_video_creation_with_dummy_images(self):
        """Test video creation using dummy images instead of OpenAI generation."""
        # Find an audio file to test with
        audio_files = list(self.video_generator.audio_path.glob("*.mp3"))
        if not audio_files:
            self.skipTest("No audio files found in assets/output directory")
        
        test_audio = audio_files[0]
        self.logger.info(f"Using test audio file: {test_audio.name}")
        
        # Create dummy images
        test_images = self.create_test_images_for_video_generation(num_images=3)
        
        # Temporarily override the generate_horror_images method
        original_method = self.video_generator.generate_horror_images
        self.video_generator.generate_horror_images = lambda story_title, story_content, num_images=None: test_images
        
        try:
            # Create the test video with output to test results directory
            video_path = self.video_generator.create_video(
                str(test_audio),
                story_title="Test Horror Story",
                story_content="A spooky test story for video generation testing.",
                output_dir=str(self.test_results_dir)
            )
            
            if video_path:
                # Check if the video file exists and has reasonable size
                video_file = Path(video_path)
                self.assertTrue(video_file.exists(), "Video file should exist")
                self.assertGreater(video_file.stat().st_size, 1000, "Video file should have reasonable size")
                self.logger.info(f"Test video created successfully: {video_file.name}")
                self.logger.info(f"Video file size: {video_file.stat().st_size} bytes")
            else:
                self.fail("Video creation failed - no video path returned")
                
        except Exception as e:
            self.fail(f"Video creation failed with error: {e}")
        finally:
            # Restore the original method
            self.video_generator.generate_horror_images = original_method
    
    def test_openai_image_generation_with_api_key(self):
        """Test actual OpenAI image generation if API key is available."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            self.skipTest("OPENAI_API_KEY not set. Skipping OpenAI image generation test.")
        
        try:
            # Test image generation with OpenAI
            images = self.video_generator.generate_horror_images(
                "Test Story",
                "A mysterious house with strange shadows and eerie sounds.",
                num_images=2
            )
            
            self.assertIsNotNone(images, "Image generation should return a list")
            self.assertGreater(len(images), 0, "Should generate at least one image")
            
            # Verify that generated images exist
            for image_path in images:
                image_file = Path(image_path)
                self.assertTrue(image_file.exists(), f"Generated image should exist: {image_path}")
                
            self.logger.info(f"Generated {len(images)} images successfully with OpenAI")
            
        except Exception as e:
            self.fail(f"OpenAI image generation test failed: {e}")
    
    def test_openai_image_generation_without_api_key(self):
        """Test graceful handling when OpenAI API key is not available."""
        with patch.dict(os.environ, {}, clear=True):
            # This should either skip gracefully or raise an appropriate exception
            try:
                images = self.video_generator.generate_horror_images(
                    "Test Story",
                    "A test story content.",
                    num_images=1
                )
                # If it doesn't raise an exception, it should return None or empty list
                if images is not None:
                    self.assertEqual(len(images), 0, "Should return empty list without API key")
            except Exception as e:
                # Should raise a clear exception about missing API key
                self.assertIn("API", str(e).upper(), "Exception should mention API key issue")
                
        self.logger.info("Graceful handling of missing API key test passed")
class TestVideoGenerationStandalone:
    """Standalone test functions for manual execution and debugging."""
    
    @staticmethod
    def setup_logging():
        """Set up logging for standalone test execution."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    @staticmethod
    def run_video_creation_test():
        """Standalone test for video creation with dummy images."""
        TestVideoGenerationStandalone.setup_logging()
        logger = logging.getLogger(__name__)
        
        try:
            logger.info("Starting standalone video generation test...")
            
            # Initialize components
            config = ConfigManager()
            video_generator = VideoGenerator(config)
            
            # Find an audio file to test with
            audio_files = list(video_generator.audio_path.glob("*.mp3"))
            if not audio_files:
                logger.error("No audio files found in assets/output directory")
                return False
            
            test_audio = audio_files[0]
            logger.info(f"Using test audio file: {test_audio.name}")
            
            # Create test instance to use the image creation method
            test_instance = TestVideoGeneration()
            test_instance.logger = logger
            test_instance.test_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create dummy images
            logger.info("Creating dummy images for testing...")
            dummy_images = test_instance.create_test_images_for_video_generation()
            
            # Override the image generation method temporarily
            original_method = video_generator.generate_horror_images
            video_generator.generate_horror_images = lambda story_title, story_content, num_images=None: dummy_images
            
            try:
                # Create the test video
                results_dir = Path(__file__).parent / "results" / "videos"
                results_dir.mkdir(parents=True, exist_ok=True)
                
                video_path = video_generator.create_video(
                    str(test_audio),
                    story_title="Standalone Test Horror Story",
                    story_content="A spooky test story for standalone video generation testing.",
                    output_dir=str(results_dir)
                )
                
                if video_path:
                    logger.info(f"Standalone test video created successfully: {video_path}")
                    
                    # Check if the video file exists and has reasonable size
                    video_file = Path(video_path)
                    if video_file.exists() and video_file.stat().st_size > 1000:
                        logger.info(f"Video file exists and has size: {video_file.stat().st_size} bytes")
                        return True
                    else:
                        logger.error("FAILED: Video file is missing or too small")
                        return False
                else:
                    logger.error("FAILED: Video creation failed")
                    return False
                    
            finally:
                # Restore the original method
                video_generator.generate_horror_images = original_method
                
        except Exception as e:
            logger.error(f"FAILED: Standalone test failed with error: {e}")
            return False
    
    @staticmethod 
    def run_openai_image_test():
        """Standalone test for OpenAI image generation if API key is available."""
        TestVideoGenerationStandalone.setup_logging()
        logger = logging.getLogger(__name__)
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.info("⚠️ OPENAI_API_KEY not set. Skipping OpenAI image generation test.")
            return True  # Not an error, just skipped
        
        try:
            logger.info("Testing OpenAI image generation...")
            
            # Initialize components
            config = ConfigManager()
            video_generator = VideoGenerator(config)
            
            # Test image generation
            images = video_generator.generate_horror_images(
                "Standalone Test Story",
                "A mysterious house with strange shadows and eerie sounds.",
                num_images=2
            )
            
            if images:
                logger.info(f"Generated {len(images)} images successfully")
                for img in images:
                    logger.info(f"  - {img}")
                return True
            else:
                logger.error("❌ Image generation failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ OpenAI image generation test failed: {e}")
            return False


def run_standalone_tests():
    """Run standalone tests for manual execution and debugging."""
    print("🎬 CreepyPasta AI Video Generation Test Suite (Standalone)")
    print("=" * 60)
    
    # Test 1: Video creation without OpenAI (using dummy images)
    print("\n📹 Test 1: Video Creation with Dummy Images")
    test1_result = TestVideoGenerationStandalone.run_video_creation_test()
    
    # Test 2: OpenAI image generation (if API key available)
    print("\n🎨 Test 2: OpenAI Image Generation")
    test2_result = TestVideoGenerationStandalone.run_openai_image_test()
    
    # Results summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"  Video Creation Test: {'PASSED' if test1_result else 'FAILED'}")
    print(f"  OpenAI Image Test:   {'PASSED' if test2_result else 'FAILED'}")
    
    if test1_result:
        print("\n🎉 Video generation system is working!")
        print("💡 To use OpenAI image generation, set your OPENAI_API_KEY environment variable.")
    else:
        print("\n⚠️ Video generation system has issues. Check the logs above.")
    
    return test1_result and test2_result


if __name__ == "__main__":
    # Run as standalone test script
    success = run_standalone_tests()
    sys.exit(0 if success else 1)
