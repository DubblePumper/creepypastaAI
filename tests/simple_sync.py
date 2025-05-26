#!/usr/bin/env python3
"""
Simple Audio Database Sync Script
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime

def main():
    print("🔄 Audio Database Sync Tool")
    print("=" * 50)
    
    # Check current directory
    print(f"Working directory: {os.getcwd()}")
    
    # Paths
    audio_dir = Path("assets/output")
    database_file = Path("data/generated_stories.json")
    
    print(f"Audio dir exists: {audio_dir.exists()}")
    print(f"Database file exists: {database_file.exists()}")
    
    if not audio_dir.exists():
        print(f"❌ Audio directory not found: {audio_dir}")
        return
    
    if not database_file.exists():
        print(f"❌ Database file not found: {database_file}")
        return
    
    # Load database
    print("📖 Loading database...")
    with open(database_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    stories = data.get('stories', [])
    print(f"📚 Found {len(stories)} stories in database")
    
    # Get all audio files
    audio_files = list(audio_dir.glob("*.mp3"))
    print(f"🎵 Found {len(audio_files)} audio files:")
    
    for audio_file in audio_files:
        print(f"  📄 {audio_file.name}")
    
    if not audio_files:
        print("❌ No audio files found to sync")
        return
    
    # Extract titles and try to match
    def extract_title_from_filename(filename):
        name = Path(filename).stem
        # Remove timestamp pattern (8 digits + underscore + 6 digits)
        name = re.sub(r'_\d{8}_\d{6}$', '', name)
        # Remove "creepypasta_" prefix if present
        if name.startswith('creepypasta_'):
            name = name[12:]
        # Replace underscores with spaces
        title = name.replace('_', ' ')
        return title.strip()
    
    # Create lookup dict of story titles
    story_lookup = {story['title']: story for story in stories}
    story_titles = list(story_lookup.keys())
    
    print("\n🔄 Processing audio files...")
    matched_count = 0
    
    for audio_file in audio_files:
        filename = audio_file.name
        extracted_title = extract_title_from_filename(filename)
        
        print(f"  📄 {filename}")
        print(f"     📝 Extracted title: '{extracted_title}'")
        
        # Try exact match first
        if extracted_title in story_lookup:
            story = story_lookup[extracted_title]
            story['generation_info']['audio_file_path'] = str(audio_file)
            matched_count += 1
            print(f"     ✅ Exact match found with story: '{story['title']}'")
        else:
            # Try case-insensitive match
            for story_title in story_titles:
                if story_title.lower() == extracted_title.lower():
                    story = story_lookup[story_title]
                    story['generation_info']['audio_file_path'] = str(audio_file)
                    matched_count += 1
                    print(f"     ✅ Case-insensitive match found with story: '{story_title}'")
                    break
            else:
                print(f"     ❌ No match found")
                # Show similar titles for debugging
                similar_titles = [t for t in story_titles if extracted_title.lower() in t.lower() or t.lower() in extracted_title.lower()]
                if similar_titles:
                    print(f"     💡 Similar titles found: {similar_titles[:3]}")
    
    # Save updated database
    if matched_count > 0:
        print(f"\n💾 Saving database with {matched_count} updated audio paths...")
        
        # Update metadata
        data['metadata']['last_updated'] = datetime.now().isoformat()
        
        # Write back to file
        with open(database_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Database updated successfully!")
    else:
        print("⚠️ No matches found, database not modified")
    
    # Summary
    print(f"\n📊 Sync Summary:")
    print(f"   🎵 Audio files processed: {len(audio_files)}")
    print(f"   ✅ Successfully matched: {matched_count}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error during sync: {e}")
        import traceback
        traceback.print_exc()
