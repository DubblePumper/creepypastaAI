"""
Demo/Test Script for CreepyPasta AI

This script demonstrates the basic functionality without requiring Reddit API credentials.
Perfect for testing the installation and core components.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.config_manager import ConfigManager
from src.utils.story_processor import StoryProcessor
from src.audio.tts_manager import TTSManager
from src.utils.logger import setup_logger


def test_story_processing():
    """Test story processing functionality."""
    print("🧪 Testing Story Processing...")
    
    config = ConfigManager()
    processor = StoryProcessor(config)
    
    # Sample creepypasta-style story
    test_story = {
        "title": "**The Midnight Visitor**",
        "content": """# The Horror Begins

I never believed in **supernatural** things until *that night*. 

I was alone in my apartment when I heard the `scratching` at my door. At first, I thought it was just my neighbor's cat, but then I realized... cats don't knock.

The scratching became more insistent, almost rhythmic. *Scratch, scratch, pause. Scratch, scratch, pause.*

When I finally worked up the courage to look through the peephole, there was nothing there. But the scratching continued.

That's when I noticed something that made my blood run cold: the scratches were coming from the **inside** of my door.

[Source: Original creepypasta for demo purposes]""",
        "author": "demo_user"
    }
    
    processed = processor.process_story(test_story)
    
    if processed:
        print("✅ Story processing successful!")
        print(f"   📝 Title: {processed['title']}")
        print(f"   📊 Word count: {processed['word_count']}")
        print(f"   ⏱️  Estimated duration: {processed['estimated_duration']:.1f}s")
        print(f"   📄 Content preview: {processed['content'][:100]}...")
        return processed
    else:
        print("❌ Story processing failed!")
        return None


def test_tts_generation(story):
    """Test TTS generation (basic only, no advanced APIs)."""
    print("\n🎤 Testing Text-to-Speech Generation...")
    
    try:
        config = ConfigManager()
        tts_manager = TTSManager(config)
        
        # Test with a short excerpt to avoid long generation times
        short_text = "This is a test of the text to speech system. Hello, creepypasta fans!"
        
        print("   🔄 Generating speech audio...")
        audio_file = tts_manager.text_to_speech(short_text, "demo_test")
        
        if audio_file and Path(audio_file).exists():
            print(f"✅ TTS generation successful!")
            print(f"   🎵 Audio file: {audio_file}")
            print(f"   📏 File size: {Path(audio_file).stat().st_size} bytes")
            return audio_file
        else:
            print("❌ TTS generation failed!")
            return None
            
    except Exception as e:
        print(f"❌ TTS test failed: {e}")
        print("   💡 Note: TTS requires internet connection for Google TTS")
        return None


def test_config_system():
    """Test configuration system."""
    print("\n⚙️  Testing Configuration System...")
    
    config = ConfigManager()
    
    # Test configuration access
    subreddit = config.get("reddit.subreddit", "creepypasta")
    tts_provider = config.get("tts.provider", "gtts")
    
    print(f"✅ Configuration loaded successfully!")
    print(f"   🎯 Target subreddit: {subreddit}")
    print(f"   🗣️  TTS provider: {tts_provider}")
    
    # Test environment variable access
    has_reddit_creds = bool(config.get_env("REDDIT_CLIENT_ID"))
    print(f"   🔑 Reddit credentials: {'✅ Configured' if has_reddit_creds else '❌ Missing'}")
    
    return True


def test_directory_structure():
    """Test that all required directories exist."""
    print("\n📁 Testing Directory Structure...")
    
    required_dirs = [
        "src",
        "assets/output",
        "assets/music", 
        "config",
        "logs"
    ]
    
    all_good = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"   ✅ {dir_path}/")
        else:
            print(f"   ❌ {dir_path}/ (missing)")
            all_good = False
    
    if all_good:
        print("✅ Directory structure is correct!")
    else:
        print("❌ Some directories are missing!")
    
    return all_good


def main():
    """Run the demo tests."""
    print("🎭 CreepyPasta AI - Demo & Test Script")
    print("=" * 50)
    
    # Set up logging
    logger = setup_logger("Demo", "INFO")
    
    # Create required directories
    Path("logs").mkdir(exist_ok=True)
    Path("assets/output").mkdir(parents=True, exist_ok=True)
    
    # Run tests
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Directory structure
    if test_directory_structure():
        tests_passed += 1
    
    # Test 2: Configuration system
    if test_config_system():
        tests_passed += 1
    
    # Test 3: Story processing
    story = test_story_processing()
    if story:
        tests_passed += 1
    
    # Test 4: TTS generation (optional, might fail without internet)
    if story:
        audio_file = test_tts_generation(story)
        if audio_file:
            tests_passed += 1
    
    # Results
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! CreepyPasta AI is ready to use.")
        print("\n📝 Next steps:")
        print("   1. Add your Reddit API credentials to .env file")
        print("   2. Add background music to assets/music/")
        print("   3. Run: python main.py")
    elif tests_passed >= 2:
        print("⚠️  Most tests passed. Check the failed tests above.")
        print("\n💡 Common issues:")
        print("   - Missing internet connection (for TTS)")
        print("   - Missing dependencies (run: pip install -r requirements.txt)")
    else:
        print("❌ Multiple tests failed. Check your installation.")
        print("\n🔧 Try:")
        print("   - pip install -r requirements.txt")
        print("   - Check that you're in the right directory")
    
    print("\n👻 Happy creepypasta generating!")


if __name__ == "__main__":
    main()
