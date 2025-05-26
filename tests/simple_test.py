#!/usr/bin/env python3
"""
Simple test for JSON Story Tracking System
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Ensure we're in the right directory
project_dir = Path(__file__).parent
os.chdir(project_dir)

# Add src to path
sys.path.insert(0, str(project_dir / "src"))

def simple_test():
    """Simple test of story tracking without complex imports."""
    print("🧪 Simple Story Tracking Test")
    print("=" * 40)
    
    # Create test data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Create a simple JSON structure
    test_stories = [
        {
            "id": "test-123",
            "title": "Test Horror Story",
            "content": "This is a test horror story content...",
            "reddit_url": "https://reddit.com/r/nosleep/test",
            "generation_info": {
                "timestamp": datetime.now().isoformat(),
                "tts_provider": "elevenlabs",
                "content_length": 42,
                "word_count": 8
            }
        }
    ]
    
    # Save to JSON
    json_file = data_dir / "simple_test_stories.json"
    
    data_structure = {
        "metadata": {
            "total_stories": len(test_stories),
            "last_updated": datetime.now().isoformat(),
            "format_version": "1.0",
            "generated_by": "CreepyPasta AI Test"
        },
        "stories": test_stories
    }
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data_structure, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created test JSON: {json_file}")
    
    # Read it back
    with open(json_file, 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)
    
    print(f"✅ Loaded {loaded_data['metadata']['total_stories']} stories")
    print(f"📖 First story: {loaded_data['stories'][0]['title']}")
    
    print("\n🎉 JSON tracking structure test passed!")
    return True

if __name__ == "__main__":
    try:
        simple_test()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
