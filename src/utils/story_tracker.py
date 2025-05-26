"""
Story Tracker Module

This module handles tracking and storage of generated CreepyPasta stories
in JSON format with complete metadata including title, content, Reddit URL,
generation timestamps, and audio file paths.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import uuid

from .config_manager import ConfigManager


class StoryTracker:
    """
    Tracks and stores generated CreepyPasta stories with metadata in JSON format.
    
    Maintains a persistent JSON database of all generated stories including:
    - Story metadata (title, content, Reddit URL)
    - Generation information (timestamp, TTS provider, audio file path)
    - Processing statistics and configuration used
    """
    
    def __init__(self, config: ConfigManager, json_file_path: str = "data/generated_stories.json"):
        """
        Initialize the story tracker.
        
        Args:
            config: Configuration manager instance
            json_file_path: Path to the JSON storage file
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.json_file_path = Path(json_file_path)
        
        # Ensure data directory exists
        self.json_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize or load existing stories
        self.stories = self._load_stories()
        
        self.logger.info(f"Story tracker initialized with {len(self.stories)} existing stories")
    
    def _load_stories(self) -> List[Dict[str, Any]]:
        """
        Load existing stories from JSON file.
        
        Returns:
            List of existing story dictionaries
        """
        try:
            if self.json_file_path.exists():
                with open(self.json_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    # Ensure we have a list structure
                    if isinstance(data, dict) and "stories" in data:
                        return data["stories"]
                    elif isinstance(data, list):
                        return data
                    else:
                        self.logger.warning("Invalid JSON structure, starting with empty list")
                        return []
            else:
                self.logger.info("No existing stories file found, starting fresh")
                return []
        except Exception as e:
            self.logger.error(f"Error loading stories from {self.json_file_path}: {e}")
            return []
    
    def _save_stories(self) -> bool:
        """
        Save stories to JSON file with metadata.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create comprehensive data structure
            data = {
                "metadata": {
                    "total_stories": len(self.stories),
                    "last_updated": datetime.now().isoformat(),
                    "format_version": "1.0",
                    "generated_by": "CreepyPasta AI"
                },
                "stories": self.stories
            }
            
            # Write to temporary file first, then rename (atomic operation)
            temp_file = self.json_file_path.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            
            # Rename temp file to actual file
            temp_file.rename(self.json_file_path)
            
            self.logger.debug(f"Successfully saved {len(self.stories)} stories to {self.json_file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving stories to {self.json_file_path}: {e}")
            return False
    
    def add_story(self, 
                  title: str,
                  content: str,
                  reddit_url: str,
                  audio_file_path: Optional[str] = None,
                  tts_provider: Optional[str] = None,
                  processing_stats: Optional[Dict] = None) -> str:
        """
        Add a new generated story to the tracking system.
        
        Args:
            title: Story title
            content: Full story content
            reddit_url: Original Reddit URL
            audio_file_path: Path to generated audio file
            tts_provider: TTS provider used for generation
            processing_stats: Additional processing statistics
            
        Returns:
            Unique story ID
        """
        try:
            # Generate unique ID for this story
            story_id = str(uuid.uuid4())
            
            # Create story entry
            story_entry = {
                "id": story_id,
                "title": title,
                "content": content,
                "reddit_url": reddit_url,
                "generation_info": {
                    "timestamp": datetime.now().isoformat(),
                    "tts_provider": tts_provider or self.config.get("tts.provider", "unknown"),
                    "audio_file_path": audio_file_path,
                    "content_length": len(content),
                    "word_count": len(content.split()) if content else 0
                },
                "processing_stats": processing_stats or {},
                "config_snapshot": {
                    "min_length": self.config.get("story.min_length", 100),
                    "max_length": self.config.get("story.max_length", 5000),
                    "tts_provider": self.config.get("tts.provider", "gtts"),
                    "audio_format": self.config.get("audio.format", "mp3")
                }
            }
            
            # Add to stories list
            self.stories.append(story_entry)
            
            # Save to file
            if self._save_stories():
                self.logger.info(f"Successfully tracked story: '{title[:50]}...' (ID: {story_id})")
                return story_id
            else:
                self.logger.error(f"Failed to save story: '{title[:50]}...'")
                # Remove from memory if save failed
                self.stories.pop()
                return ""
                
        except Exception as e:
            self.logger.error(f"Error adding story '{title[:50]}...': {e}")
            return ""
    
    def update_story_audio(self, story_id: str, audio_file_path: str) -> bool:
        """
        Update an existing story with audio file path.
        
        Args:
            story_id: Unique story ID
            audio_file_path: Path to generated audio file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            for story in self.stories:
                if story["id"] == story_id:
                    story["generation_info"]["audio_file_path"] = audio_file_path
                    story["generation_info"]["audio_generated_at"] = datetime.now().isoformat()
                    
                    if self._save_stories():
                        self.logger.info(f"Updated story {story_id} with audio path: {audio_file_path}")
                        return True
                    return False
            
            self.logger.warning(f"Story ID {story_id} not found for audio update")
            return False
            
        except Exception as e:
            self.logger.error(f"Error updating story {story_id} with audio: {e}")
            return False
    
    def get_story_by_id(self, story_id: str) -> Optional[Dict]:
        """
        Retrieve a story by its ID.
        
        Args:
            story_id: Unique story ID
            
        Returns:
            Story dictionary or None if not found
        """
        for story in self.stories:
            if story["id"] == story_id:
                return story
        return None
    
    def get_stories_by_date(self, date_str: str) -> List[Dict]:
        """
        Get all stories generated on a specific date.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
            
        Returns:
            List of story dictionaries
        """
        matching_stories = []
        for story in self.stories:
            story_date = story["generation_info"]["timestamp"][:10]  # Extract YYYY-MM-DD
            if story_date == date_str:
                matching_stories.append(story)
        return matching_stories
    
    def get_recent_stories(self, limit: int = 10) -> List[Dict]:
        """
        Get the most recently generated stories.
        
        Args:
            limit: Maximum number of stories to return
            
        Returns:
            List of recent story dictionaries
        """
        # Sort by timestamp (most recent first)
        sorted_stories = sorted(
            self.stories,
            key=lambda x: x["generation_info"]["timestamp"],
            reverse=True
        )
        return sorted_stories[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about tracked stories.
        
        Returns:
            Dictionary containing various statistics
        """
        if not self.stories:
            return {"total_stories": 0}
        
        stats = {
            "total_stories": len(self.stories),
            "total_content_length": sum(story["generation_info"]["content_length"] for story in self.stories),
            "total_word_count": sum(story["generation_info"]["word_count"] for story in self.stories),
            "stories_with_audio": sum(1 for story in self.stories if story["generation_info"].get("audio_file_path")),
            "tts_providers_used": list(set(story["generation_info"]["tts_provider"] for story in self.stories)),
            "date_range": {
                "earliest": min(story["generation_info"]["timestamp"] for story in self.stories),
                "latest": max(story["generation_info"]["timestamp"] for story in self.stories)
            },
            "average_content_length": sum(story["generation_info"]["content_length"] for story in self.stories) / len(self.stories),
            "average_word_count": sum(story["generation_info"]["word_count"] for story in self.stories) / len(self.stories)
        }
        
        return stats
    
    def export_stories(self, export_path: str, include_content: bool = True) -> bool:
        """
        Export stories to a separate JSON file.
        
        Args:
            export_path: Path for the export file
            include_content: Whether to include full story content
            
        Returns:
            True if successful, False otherwise
        """
        try:
            export_data = []
            for story in self.stories:
                export_entry = {
                    "id": story["id"],
                    "title": story["title"],
                    "reddit_url": story["reddit_url"],
                    "generation_info": story["generation_info"],
                    "processing_stats": story["processing_stats"]
                }
                
                if include_content:
                    export_entry["content"] = story["content"]
                
                export_data.append(export_entry)
            
            export_structure = {
                "export_metadata": {
                    "exported_at": datetime.now().isoformat(),
                    "total_stories": len(export_data),
                    "content_included": include_content,
                    "source_file": str(self.json_file_path)
                },
                "stories": export_data
            }
            
            with open(export_path, 'w', encoding='utf-8') as file:
                json.dump(export_structure, file, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Successfully exported {len(export_data)} stories to {export_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting stories to {export_path}: {e}")
            return False
        
    def story_exists(self, reddit_url: Optional[str] = None, reddit_id: Optional[str] = None, title: Optional[str] = None) -> bool:
        """
        Check if a story already exists in the database.
        
        Args:
            reddit_url: Reddit URL to check for duplicates
            reddit_id: Reddit ID to check for duplicates  
            title: Story title to check for duplicates
            
        Returns:
            True if story exists, False otherwise
        """
        try:
            for story in self.stories:
                # Check by Reddit URL (primary method)
                if reddit_url and story.get("reddit_url") == reddit_url:
                    return True
                
                # Check by Reddit ID (if available in processing_stats)
                if reddit_id:
                    story_reddit_id = story.get("processing_stats", {}).get("reddit_id")
                    if story_reddit_id == reddit_id:
                        return True
                
                # Check by title as fallback (less reliable)
                if title and story.get("title") == title:
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking if story exists: {e}")
            return False
    
    def get_duplicate_info(self, reddit_url: Optional[str] = None, reddit_id: Optional[str] = None, title: Optional[str] = None) -> Optional[Dict]:
        """
        Get information about a duplicate story if it exists.
        
        Args:
            reddit_url: Reddit URL to check for duplicates
            reddit_id: Reddit ID to check for duplicates  
            title: Story title to check for duplicates
            
        Returns:
            Story dictionary if duplicate found, None otherwise
        """
        try:
            for story in self.stories:
                # Check by Reddit URL (primary method)
                if reddit_url and story.get("reddit_url") == reddit_url:
                    return story
                
                # Check by Reddit ID (if available in processing_stats)
                if reddit_id:
                    story_reddit_id = story.get("processing_stats", {}).get("reddit_id")
                    if story_reddit_id == reddit_id:
                        return story
                
                # Check by title as fallback (less reliable)
                if title and story.get("title") == title:
                    return story
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting duplicate info: {e}")
            return None
