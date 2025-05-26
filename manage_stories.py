#!/usr/bin/env python3
"""
Story Management CLI Tool

Command-line interface for managing the CreepyPasta AI story database.
Provides functionality to view, search, export, and analyze tracked stories.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.config_manager import ConfigManager
from src.utils.story_tracker import StoryTracker


def display_story_summary(story: dict, show_content: bool = False):
    """Display a formatted summary of a story."""
    print(f"\n{'='*60}")
    print(f"📖 Title: {story['title']}")
    print(f"🆔 ID: {story['id']}")
    print(f"🔗 Reddit URL: {story['reddit_url']}")
    print(f"📅 Generated: {story['generation_info']['timestamp'][:19]}")
    print(f"🗣️ TTS Provider: {story['generation_info']['tts_provider']}")
    print(f"📏 Content Length: {story['generation_info']['content_length']:,} characters")
    print(f"📝 Word Count: {story['generation_info']['word_count']:,} words")
    
    audio_path = story['generation_info'].get('audio_file_path')
    if audio_path:
        print(f"🎵 Audio File: {audio_path}")
    else:
        print("🎵 Audio File: Not generated")
    
    if show_content:
        print(f"\n📄 Content:")
        print("-" * 40)
        content = story['content']
        if len(content) > 500:
            print(f"{content[:500]}...")
            print(f"\n[Content truncated - showing first 500 of {len(content)} characters]")
        else:
            print(content)
    
    print(f"{'='*60}")


def list_stories(tracker: StoryTracker, limit: int = 10, show_content: bool = False):
    """List recent stories."""
    stories = tracker.get_recent_stories(limit)
    
    if not stories:
        print("📭 No stories found in the database.")
        return
    
    print(f"\n📚 Showing {len(stories)} most recent stories:")
    
    for story in stories:
        display_story_summary(story, show_content)


def search_stories(tracker: StoryTracker, search_term: str, show_content: bool = False):
    """Search stories by title or content."""
    matching_stories = []
    
    for story in tracker.stories:
        if (search_term.lower() in story['title'].lower() or 
            search_term.lower() in story['content'].lower()):
            matching_stories.append(story)
    
    if not matching_stories:
        print(f"🔍 No stories found matching '{search_term}'")
        return
    
    print(f"\n🔍 Found {len(matching_stories)} stories matching '{search_term}':")
    
    for story in matching_stories:
        display_story_summary(story, show_content)


def show_statistics(tracker: StoryTracker):
    """Display comprehensive statistics."""
    stats = tracker.get_statistics()
    
    print("\n📊 CreepyPasta AI Database Statistics")
    print("=" * 50)
    
    print(f"📚 Total Stories: {stats.get('total_stories', 0)}")
    print(f"🎵 Stories with Audio: {stats.get('stories_with_audio', 0)}")
    print(f"📏 Total Content: {stats.get('total_content_length', 0):,} characters")
    print(f"📝 Total Words: {stats.get('total_word_count', 0):,} words")
    
    if stats.get('total_stories', 0) > 0:
        print(f"📊 Average Content Length: {stats.get('average_content_length', 0):.0f} characters")
        print(f"📝 Average Word Count: {stats.get('average_word_count', 0):.0f} words")
    
    tts_providers = stats.get('tts_providers_used', [])
    if tts_providers:
        print(f"🗣️ TTS Providers Used: {', '.join(tts_providers)}")
    
    date_range = stats.get('date_range', {})
    if date_range:
        earliest = date_range.get('earliest', 'N/A')[:10]
        latest = date_range.get('latest', 'N/A')[:10]
        print(f"📅 Date Range: {earliest} to {latest}")
    
    print("=" * 50)


def export_stories(tracker: StoryTracker, export_path: str, include_content: bool = True):
    """Export stories to a file."""
    success = tracker.export_stories(export_path, include_content)
    
    if success:
        print(f"✅ Successfully exported {len(tracker.stories)} stories to {export_path}")
        if not include_content:
            print("ℹ️ Content was excluded from export (metadata only)")
    else:
        print(f"❌ Failed to export stories to {export_path}")


def show_story_by_id(tracker: StoryTracker, story_id: str, show_content: bool = True):
    """Show details for a specific story ID."""
    story = tracker.get_story_by_id(story_id)
    
    if not story:
        print(f"❌ Story with ID '{story_id}' not found")
        return
    
    display_story_summary(story, show_content)


def stories_by_date(tracker: StoryTracker, date_str: str, show_content: bool = False):
    """Show stories generated on a specific date."""
    try:
        # Validate date format
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print("❌ Invalid date format. Please use YYYY-MM-DD")
        return
    
    stories = tracker.get_stories_by_date(date_str)
    
    if not stories:
        print(f"📭 No stories found for date {date_str}")
        return
    
    print(f"\n📅 Stories generated on {date_str}:")
    
    for story in stories:
        display_story_summary(story, show_content)


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="CreepyPasta AI Story Database Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_stories.py stats                    # Show database statistics
  python manage_stories.py list                     # List 10 most recent stories
  python manage_stories.py list --limit 20          # List 20 most recent stories
  python manage_stories.py search "horror"          # Search for stories containing "horror"
  python manage_stories.py show <story-id>          # Show specific story by ID
  python manage_stories.py date 2024-01-15          # Show stories from specific date
  python manage_stories.py export output.json       # Export all stories
  python manage_stories.py export output.json --no-content  # Export metadata only
        """
    )
    
    parser.add_argument(
        'command',
        choices=['stats', 'list', 'search', 'show', 'date', 'export'],
        help='Command to execute'
    )
    
    parser.add_argument(
        'value',
        nargs='?',
        help='Value for the command (search term, story ID, date, or export path)'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Limit number of results (default: 10)'
    )
    
    parser.add_argument(
        '--content',
        action='store_true',
        help='Show full content in listings'
    )
    
    parser.add_argument(
        '--no-content',
        action='store_true',
        help='Exclude content from export'
    )
    
    parser.add_argument(
        '--config',
        default='config/settings.yaml',
        help='Path to config file (default: config/settings.yaml)'
    )
    
    parser.add_argument(
        '--database',
        default='data/generated_stories.json',
        help='Path to story database (default: data/generated_stories.json)'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize configuration and tracker
        config = ConfigManager(args.config)
        tracker = StoryTracker(config, args.database)
        
        # Execute commands
        if args.command == 'stats':
            show_statistics(tracker)
            
        elif args.command == 'list':
            list_stories(tracker, args.limit, args.content)
            
        elif args.command == 'search':
            if not args.value:
                print("❌ Search command requires a search term")
                sys.exit(1)
            search_stories(tracker, args.value, args.content)
            
        elif args.command == 'show':
            if not args.value:
                print("❌ Show command requires a story ID")
                sys.exit(1)
            show_story_by_id(tracker, args.value, True)
            
        elif args.command == 'date':
            if not args.value:
                print("❌ Date command requires a date (YYYY-MM-DD)")
                sys.exit(1)
            stories_by_date(tracker, args.value, args.content)
            
        elif args.command == 'export':
            if not args.value:
                print("❌ Export command requires an output file path")
                sys.exit(1)
            export_stories(tracker, args.value, not args.no_content)
    
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
