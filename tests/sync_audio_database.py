#!/usr/bin/env python3
"""
Audio Database Sync Script

This script syncs existing audio files in assets/output/ with the database
by updating the audio_file_path field for matching stories.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional
from difflib import SequenceMatcher

def extract_title_from_filename(filename: str) -> str:
    """
    Extract story title from audio filename.
    
    Handles patterns like:
    - "creepypasta_A_Pulse_20250526_140726.mp3"
    - "The_Used_Snes_20250526_140559.mp3"
    - "Evil_20250526_140518.mp3"
    """
    # Remove file extension
    name = Path(filename).stem
    
    # Remove timestamp pattern (8 digits + underscore + 6 digits)
    name = re.sub(r'_\d{8}_\d{6}$', '', name)
    
    # Remove "creepypasta_" prefix if present
    if name.startswith('creepypasta_'):
        name = name[12:]  # len('creepypasta_') = 12
    
    # Replace underscores with spaces
    title = name.replace('_', ' ')
    
    return title.strip()

def normalize_title(title: str) -> str:
    """Normalize title for comparison."""
    return re.sub(r'[^\w\s]', '', title.lower().strip())

def find_best_match(target_title: str, story_titles: List[str]) -> Optional[str]:
    """Find the best matching story title using fuzzy matching."""
    target_normalized = normalize_title(target_title)
    
    best_match = None
    best_ratio = 0.0
    
    for story_title in story_titles:
        story_normalized = normalize_title(story_title)
        ratio = SequenceMatcher(None, target_normalized, story_normalized).ratio()
        
        if ratio > best_ratio and ratio > 0.7:  # 70% similarity threshold
            best_ratio = ratio
            best_match = story_title
    
    return best_match

def sync_audio_database():
    """Main function to sync audio files with database."""
    
    # Paths
    audio_dir = Path("assets/output")
    database_file = Path("data/generated_stories.json")
    
    print(f"Working directory: {os.getcwd()}")
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
    print(f"🎵 Found {len(audio_files)} audio files")
    
    if not audio_files:
        print("❌ No audio files found to sync")
        return
    
    # Create lookup dict of story titles
    story_lookup = {story['title']: story for story in stories}
    story_titles = list(story_lookup.keys())
    
    # Process each audio file
    matched_count = 0
    unmatched_files = []
    
    print("\n🔄 Processing audio files...")
    
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
            print(f"     ✅ Exact match found")
            continue
        
        # Try fuzzy matching
        best_match = find_best_match(extracted_title, story_titles)
        if best_match:
            story = story_lookup[best_match]
            story['generation_info']['audio_file_path'] = str(audio_file)
            matched_count += 1
            print(f"     ✅ Fuzzy match: '{best_match}'")
        else:
            unmatched_files.append((filename, extracted_title))
            print(f"     ❌ No match found")
    
    # Save updated database
    if matched_count > 0:
        print(f"\n💾 Saving database with {matched_count} updated audio paths...")
        
        # Update metadata
        data['metadata']['total_stories'] = len(stories)
        data['metadata']['last_updated'] = f"{datetime.now().isoformat()}"
        
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
    print(f"   ❌ Unmatched files: {len(unmatched_files)}")
    
    if unmatched_files:
        print(f"\n❌ Unmatched files:")
        for filename, extracted_title in unmatched_files:
            print(f"   📄 {filename} -> '{extracted_title}'")

if __name__ == "__main__":
    from datetime import datetime
    
    print("🔄 Audio Database Sync Tool")
    print("=" * 50)
    
    try:
        sync_audio_database()
    except Exception as e:
        print(f"❌ Error during sync: {e}")
        import traceback
        traceback.print_exc()
