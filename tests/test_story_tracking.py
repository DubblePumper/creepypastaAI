#!/usr/bin/env python3
"""
Test script for the JSON Story Tracking System

This script tests the story tracker functionality without running
the full CreepyPasta AI workflow.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.config_manager import ConfigManager
from src.utils.story_tracker import StoryTracker


def test_story_tracking():
    """Test the story tracking system with sample data."""
    print("🧪 Testing CreepyPasta AI Story Tracking System")
    print("=" * 50)
    
    try:
        print("📦 Importing modules...")
        # Initialize components
        config = ConfigManager("config/settings.yaml")
        print("✅ ConfigManager loaded")
        
        tracker = StoryTracker(config, "data/test_stories.json")
        print("✅ Story tracker initialized successfully")
        
        # Test data
        test_stories = [
            {
                "title": "The Midnight Visitor",
                "content": "It was a dark and stormy night when I heard the first knock at my door. Three soft taps, then silence. I waited, but nothing came. Then, just as I was about to return to bed, I heard it again. Three taps, deliberate and precise. This time, I decided to investigate...",
                "reddit_url": "https://reddit.com/r/nosleep/test1",
                "tts_provider": "elevenlabs",
                "processing_stats": {
                    "original_length": 250,
                    "processed_length": 235,
                    "word_count": 45,
                    "processing_timestamp": datetime.now().isoformat()
                }
            },
            {
                "title": "The Empty Room",
                "content": "My grandmother's house had always felt wrong to me. There was something about the way the shadows moved in the corners, the way the floorboards creaked when no one was walking on them. But it wasn't until I found the empty room that I understood why...",
                "reddit_url": "https://reddit.com/r/nosleep/test2",
                "tts_provider": "gtts",
                "processing_stats": {
                    "original_length": 280,
                    "processed_length": 275,
                    "word_count": 52,
                    "processing_timestamp": datetime.now().isoformat()
                }
            },
            {
                "title": "Digital Whispers",
                "content": "The notification sound started at 3:33 AM, exactly. My phone would buzz once, then go silent. When I checked, there were no messages, no missed calls, nothing in my notification history. But every night, at exactly 3:33 AM, it happened again...",
                "reddit_url": "https://reddit.com/r/nosleep/test3",
                "tts_provider": "openai",
                "processing_stats": {
                    "original_length": 300,
                    "processed_length": 295,
                    "word_count": 55,
                    "processing_timestamp": datetime.now().isoformat()
                }
            }
        ]
        
        # Add stories to tracker
        story_ids = []
        for i, story in enumerate(test_stories, 1):
            print(f"\n📖 Adding test story {i}: '{story['title']}'")
            
            story_id = tracker.add_story(
                title=story["title"],
                content=story["content"],
                reddit_url=story["reddit_url"],
                tts_provider=story["tts_provider"],
                processing_stats=story["processing_stats"]
            )
            
            if story_id:
                story_ids.append(story_id)
                print(f"   ✅ Added with ID: {story_id}")
                
                # Simulate audio generation
                fake_audio_path = f"output/audio/{story['title'].lower().replace(' ', '_')}.mp3"
                if tracker.update_story_audio(story_id, fake_audio_path):
                    print(f"   🎵 Updated with audio path: {fake_audio_path}")
                else:
                    print(f"   ❌ Failed to update audio path")
            else:
                print(f"   ❌ Failed to add story")
        
        # Test statistics
        print(f"\n📊 Testing statistics...")
        stats = tracker.get_statistics()
        
        print(f"   📚 Total stories: {stats.get('total_stories', 0)}")
        print(f"   🎵 Stories with audio: {stats.get('stories_with_audio', 0)}")
        print(f"   📏 Average content length: {stats.get('average_content_length', 0):.0f} characters")
        print(f"   🗣️ TTS providers used: {', '.join(stats.get('tts_providers_used', []))}")
        
        # Test retrieval
        print(f"\n🔍 Testing story retrieval...")
        if story_ids:
            test_id = story_ids[0]
            retrieved_story = tracker.get_story_by_id(test_id)
            if retrieved_story:
                print(f"   ✅ Successfully retrieved story: '{retrieved_story['title']}'")
            else:
                print(f"   ❌ Failed to retrieve story with ID: {test_id}")
        
        # Test recent stories
        recent_stories = tracker.get_recent_stories(2)
        print(f"   📖 Recent stories: {len(recent_stories)} found")
        
        # Test export
        print(f"\n💾 Testing export functionality...")
        export_path = "data/test_export.json"
        if tracker.export_stories(export_path, include_content=True):
            print(f"   ✅ Successfully exported to: {export_path}")
        else:
            print(f"   ❌ Failed to export stories")
        
        print(f"\n🎉 All tests completed successfully!")
        print(f"📁 Test database saved to: data/test_stories.json")
        print(f"📁 Export saved to: {export_path}")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_story_tracking()
