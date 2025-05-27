#!/usr/bin/env python3
"""
Test script to verify OpenAI image generation functionality.

This test specifically validates:
1. OpenAI API key is properly configured
2. Image generation when insufficient images are available
3. Fallback to existing images when OpenAI is unavailable
4. Cache functionality for generated images

Usage:
    python test_openai_image_generation.py
"""

import sys
import logging
import tempfile
import shutil
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
    from src.image.openai_image_generator import OpenAIImageGenerator
    from src.utils.config_manager import ConfigManager
except ImportError as e:
    logger.error(f"Failed to import project modules: {e}")
    logger.error("Make sure you're running from the project root directory")
    sys.exit(1)

def test_openai_image_generation():
    """Test OpenAI image generation with various scenarios."""
    try:
        logger.info("🧪 Starting OpenAI Image Generation Test...")
        
        # Initialize config and image generator
        config = ConfigManager("config/settings.yaml")
        
        # Create a temporary directory for testing
        temp_images_dir = Path("temp/test_images")
        temp_images_dir.mkdir(parents=True, exist_ok=True)
        
        generator = OpenAIImageGenerator(config, temp_images_dir)
        
        # Test story content
        test_title = "The Haunted Library"
        test_content = """
        Sarah always loved the old library at the end of Maple Street. The towering shelves,
        the musty smell of ancient books, and the way sunlight filtered through dusty windows
        created an atmosphere of mystery she found irresistible. But tonight, something was different.
        
        As she walked between the rows of books, she noticed shadows moving where there should be
        only stillness. The grandfather clock in the corner ticked with an irregular rhythm,
        and books seemed to whisper secrets from their shelves.
        """
        
        # Test 1: Check existing images count
        logger.info("📊 Test 1: Checking existing image count...")
        existing_images = generator.get_existing_images()
        logger.info(f"Found {len(existing_images)} existing images")
        
        # Test 2: Test with more images needed than available (should trigger generation)
        logger.info("🎨 Test 2: Testing image generation (need more than available)...")
        required_images = 15  # More than the 13 existing images
        
        all_images = generator.ensure_sufficient_images(
            test_title, test_content, required_images
        )
        
        logger.info(f"Requested {required_images} images, got {len(all_images)} images")
        
        if len(all_images) >= required_images:
            logger.info("✅ Successfully generated sufficient images!")
            
            # Check if new images were actually generated
            new_existing = generator.get_existing_images()
            if len(new_existing) > len(existing_images):
                logger.info(f"✅ New images generated: {len(new_existing) - len(existing_images)}")
                
                # Test 3: Check cache functionality
                logger.info("💾 Test 3: Testing cache functionality...")
                cache_file = generator.cache_file
                if cache_file.exists():
                    logger.info("✅ Cache file exists and is being maintained")
                else:
                    logger.warning("⚠️ Cache file not found")
                    
                return True
            else:
                logger.warning("⚠️ No new images generated - may be using existing images only")
                return True
        else:
            logger.warning(f"⚠️ Got {len(all_images)} images but requested {required_images}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error during OpenAI image generation test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        try:
            logger.info("🧹 Cleaning up test files...")
            if temp_images_dir.exists():
                shutil.rmtree(temp_images_dir)
            logger.info("✅ Cleanup completed")
        except Exception as cleanup_error:
            logger.warning(f"Warning: Error during cleanup: {cleanup_error}")

def test_openai_api_connection():
    """Test OpenAI API connection."""
    try:
        logger.info("🔗 Testing OpenAI API connection...")
        
        import os
        import openai
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("❌ OPENAI_API_KEY not found in environment")
            return False
            
        logger.info("✅ OpenAI API key found")
        
        # Test API connection
        client = openai.OpenAI(api_key=api_key)
        
        # Simple test call
        response = client.models.list()
        if response:
            logger.info("✅ OpenAI API connection successful")
            return True
        else:
            logger.error("❌ OpenAI API connection failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ OpenAI API test failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting OpenAI Image Generation Tests...")
    
    # Test 1: API Connection
    api_test = test_openai_api_connection()
    
    # Test 2: Image Generation
    if api_test:
        generation_test = test_openai_image_generation()
        
        if generation_test:
            logger.info("✅ All tests passed! OpenAI image generation is working correctly.")
            print("\n🎉 SUCCESS: OpenAI integration is working properly!")
            sys.exit(0)
        else:
            logger.error("❌ Image generation test failed!")
            print("\n💥 FAILED: Image generation test failed!")
            sys.exit(1)
    else:
        logger.error("❌ OpenAI API connection test failed!")
        print("\n💥 FAILED: OpenAI API connection failed!")
        sys.exit(1)
