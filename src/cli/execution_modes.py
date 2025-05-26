# filepath: src/cli/execution_modes.py
"""
Execution Mode Handlers for CreepyPasta AI

This module contains handlers for different execution modes:
- Scraping only
- Audio generation only
- Video generation only
- Complete workflow
"""

import logging
from pathlib import Path
from typing import List, Optional

from src.scrapers.reddit_scraper import RedditScraper
from src.audio.tts_manager import TTSManager
from src.audio.audio_mixer import AudioMixer
from src.video.video_generator import VideoGenerator
from src.utils.config_manager import ConfigManager
from src.utils.story_processor import StoryProcessor
from src.utils.story_tracker import StoryTracker


class ExecutionModeHandler:
    """
    Base class for execution mode handlers.
    """
    
    def __init__(self, config: ConfigManager, logger: logging.Logger):
        """
        Initialize the execution mode handler.
        
        Args:
            config: Configuration manager instance
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.story_tracker = StoryTracker(config)


class ScrapeOnlyMode(ExecutionModeHandler):
    """
    Handler for scraping-only execution mode.
    """
    
    def __init__(self, config: ConfigManager, logger: logging.Logger):
        """Initialize scraping-only mode handler."""
        super().__init__(config, logger)
        self.reddit_scraper = RedditScraper(config)
        self.story_processor = StoryProcessor(config)
    
    def execute(self, num_stories: Optional[int] = None) -> int:
        """
        Execute scraping-only workflow.
        
        Args:
            num_stories: Number of stories to scrape
            
        Returns:
            Number of new stories added to database
        """
        try:
            # Get number of stories from config if not specified
            if num_stories is None:
                num_stories = self.config.get("reddit.limit", 10)
            if num_stories is None:
                num_stories = 10  # Fallback to default
            
            self.logger.info(f"Starting scraping-only mode for {num_stories} stories")
            
            # Scrape stories from Reddit
            self.logger.info("Scraping stories from Reddit...")
            raw_stories = self.reddit_scraper.scrape_stories(limit=num_stories)
            
            if not raw_stories:
                self.logger.warning("No stories found.")
                return 0
            
            self.logger.info(f"Found {len(raw_stories)} stories from Reddit")
            
            # Process and store each story
            new_stories_count = 0
            for i, story in enumerate(raw_stories, 1):
                self.logger.info(f"Processing story {i}/{len(raw_stories)}: {story.get('title', 'Unknown')[:50]}...")
                
                try:
                    # Process the story
                    processed_story = self.story_processor.process_story(story)
                    if not processed_story:
                        self.logger.warning(f"Story processing failed for: {story.get('title', 'Unknown')[:50]}")
                        continue
                    
                    # Check if story already exists in database
                    reddit_url = processed_story.get('url')
                    reddit_id = processed_story.get('id')
                    title = processed_story.get('title')
                    
                    if self.story_tracker.story_exists(reddit_url=reddit_url, reddit_id=reddit_id, title=title):
                        safe_title = title[:50] if title else "Unknown"
                        self.logger.info(f"Story already exists in database, skipping: {safe_title}...")
                        continue
                    
                    # Add new story to database
                    story_id = self.story_tracker.add_story(
                        title=processed_story['title'],
                        content=processed_story['content'],
                        reddit_url=reddit_url or 'unknown',
                        tts_provider=None,  # Will be set when audio is generated
                        processing_stats={
                            "reddit_id": reddit_id,
                            "original_length": len(story.get('raw_content', '')),
                            "processed_length": len(processed_story['content']),
                            "word_count": len(processed_story['content'].split()),
                            "scraping_timestamp": processed_story.get('timestamp', 'unknown'),
                            "author": processed_story.get('author', 'unknown'),
                            "score": processed_story.get('score', 0),
                            "num_comments": processed_story.get('num_comments', 0)
                        }
                    )
                    
                    if story_id:
                        new_stories_count += 1
                        safe_title = title[:50] if title else "Unknown"
                        self.logger.info(f"Added new story to database: {safe_title}... (ID: {story_id})")
                    else:
                        safe_title = title[:50] if title else "Unknown"
                        self.logger.error(f"Failed to add story to database: {safe_title}...")
                        
                except Exception as e:
                    self.logger.error(f"Error processing story '{story.get('title', 'Unknown')[:50]}': {e}")
                    continue
            
            self.logger.info(f"Scraping completed. Added {new_stories_count} new stories to database")
            return new_stories_count
            
        except Exception as e:
            self.logger.error(f"Error in scraping-only mode: {e}")
            return 0


class AudioOnlyMode(ExecutionModeHandler):
    """
    Handler for audio-only execution mode.
    """
    
    def __init__(self, config: ConfigManager, logger: logging.Logger):
        """Initialize audio-only mode handler."""
        super().__init__(config, logger)
        self.tts_manager = TTSManager(config)
        self.audio_mixer = AudioMixer(config)
    
    def execute(self) -> List[str]:
        """
        Execute audio-only workflow.
        
        Returns:
            List of generated audio file paths
        """
        try:
            self.logger.info("Starting audio-only mode")
            
            # Get all stories that need audio generation
            pending_stories = []
            for story in self.story_tracker.stories:
                audio_path = story.get("generation_info", {}).get("audio_file_path")
                if not audio_path:
                    pending_stories.append(story)
            
            if not pending_stories:
                self.logger.info("No pending stories found for audio generation")
                return []
            
            self.logger.info(f"Found {len(pending_stories)} stories pending audio generation")
            
            # Generate audio for each pending story
            generated_files = []
            for i, story in enumerate(pending_stories, 1):
                self.logger.info(f"Generating audio {i}/{len(pending_stories)}: {story['title'][:50]}...")
                
                try:
                    # Prepare story data for audio generation
                    story_data = {
                        'title': story['title'],
                        'content': story['content'],
                        'url': story['reddit_url'],
                        'timestamp': story.get('generation_info', {}).get('timestamp', 'unknown')
                    }
                    
                    # Generate audio for the story
                    audio_file = self._generate_story_audio(story_data)
                    if audio_file:
                        generated_files.append(audio_file)
                        self.logger.info(f"Successfully generated: {audio_file}")
                        
                        # Update story record with audio file path and TTS provider
                        self.story_tracker.update_story_audio(story['id'], audio_file)
                        
                        # Update TTS provider info
                        if "generation_info" not in story:
                            story["generation_info"] = {}
                        story['generation_info']['tts_provider'] = self.config.get("tts.provider", "gtts")
                        self.story_tracker._save_stories()
                        
                    else:
                        self.logger.warning(f"Audio generation failed for story: {story['title'][:50]}...")
                        
                except Exception as e:
                    self.logger.error(f"Failed to generate audio for story '{story['title']}': {e}")
                    continue
            
            self.logger.info(f"Audio generation completed. Generated {len(generated_files)} files")
            return generated_files
            
        except Exception as e:
            self.logger.error(f"Error in audio-only mode: {e}")
            return []
    
    def _generate_story_audio(self, story: dict) -> Optional[str]:
        """
        Generate complete audio experience for a single story.
        
        Args:
            story: Processed story dictionary
            
        Returns:
            Path to generated audio file, or None if failed
        """
        try:
            # Generate TTS audio
            tts_file = self.tts_manager.text_to_speech(
                text=story["content"],
                title=story["title"]
            )
            
            if not tts_file:
                self.logger.error(f"Failed to generate TTS for story: {story['title']}")
                return None
            
            # Mix with background music and effects
            final_audio = self.audio_mixer.create_atmospheric_mix(
                narration_file=tts_file,
                title=story["title"],
                story_metadata=story
            )
            
            return final_audio
            
        except Exception as e:
            self.logger.error(f"Error generating audio for story '{story['title']}': {e}")
            return None


class VideoOnlyMode(ExecutionModeHandler):
    """
    Handler for video-only execution mode.
    """
    
    def __init__(self, config: ConfigManager, logger: logging.Logger):
        """Initialize video-only mode handler."""
        super().__init__(config, logger)
        self.video_generator = VideoGenerator(config)
    
    def execute(self, generate_for_all: bool = False) -> List[str]:
        """
        Execute video-only workflow.
        
        Args:
            generate_for_all: If True, generate videos for all audio files
            
        Returns:
            List of generated video file paths
        """
        try:
            self.logger.info("Starting video-only mode")
            
            if generate_for_all:
                # Generate videos for all existing audio files
                self.logger.info("Generating videos for all existing audio files...")
                generated_videos = self.video_generator.generate_videos_for_all_audio()
            else:
                # Generate videos only for stories without videos
                generated_videos = self._generate_videos_for_pending_stories()
            
            self.logger.info(f"Video generation completed. Generated {len(generated_videos)} videos")
            return generated_videos
            
        except Exception as e:
            self.logger.error(f"Error in video-only mode: {e}")
            return []
    
    def _generate_videos_for_pending_stories(self) -> List[str]:
        """
        Generate videos for stories that have audio but no video yet.
        
        Returns:
            List of generated video file paths
        """
        try:
            self.logger.info("Generating videos for stories without videos...")
            
            # Get all stories with audio files
            stories_with_audio = []
            for story in self.story_tracker.stories:
                audio_path = story.get("generation_info", {}).get("audio_file_path")
                if audio_path and Path(audio_path).exists():
                    stories_with_audio.append(story)
            
            if not stories_with_audio:
                self.logger.info("No stories with audio files found")
                return []
            
            self.logger.info(f"Found {len(stories_with_audio)} stories with audio files")
            
            # Generate videos for each story
            generated_videos = []
            for i, story in enumerate(stories_with_audio, 1):
                self.logger.info(f"Generating video {i}/{len(stories_with_audio)}: {story['title'][:50]}...")
                
                try:
                    audio_path = story["generation_info"]["audio_file_path"]
                    
                    # Check if video already exists
                    video_exists = self._check_if_video_exists(story['title'])
                    if video_exists:
                        self.logger.info(f"Video already exists for: {story['title'][:50]}...")
                        continue
                    
                    # Generate video
                    video_path = self.video_generator.create_video(
                        audio_file=audio_path,
                        story_title=story['title'],
                        story_content=story['content']
                    )
                    
                    if video_path:
                        generated_videos.append(video_path)
                        self.logger.info(f"Successfully generated video: {video_path}")
                        
                        # Update story record with video file path
                        self._update_story_with_video_path(story['id'], video_path)
                    else:
                        self.logger.warning(f"Video generation failed for story: {story['title'][:50]}...")
                        
                except Exception as e:
                    self.logger.error(f"Failed to generate video for story '{story['title']}': {e}")
                    continue
            
            self.logger.info(f"Video generation completed. Generated {len(generated_videos)} files")
            return generated_videos
            
        except Exception as e:
            self.logger.error(f"Error generating videos for pending stories: {e}")
            return []
    
    def _check_if_video_exists(self, title: str) -> bool:
        """
        Check if a video already exists for the given title.
        
        Args:
            title: Story title
            
        Returns:
            True if video exists, False otherwise
        """
        try:
            videos_path = Path("assets/videos")
            if not videos_path.exists():
                return False
            
            # Create safe filename pattern
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:50]
            
            # Check for existing videos with similar names
            existing_videos = list(videos_path.glob(f"*{safe_title}*.mp4"))
            return len(existing_videos) > 0
            
        except Exception as e:
            self.logger.error(f"Error checking if video exists: {e}")
            return False
    
    def _update_story_with_video_path(self, story_id: str, video_path: str) -> bool:
        """
        Update story record with video file path.
        
        Args:
            story_id: Unique story ID
            video_path: Path to generated video file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from datetime import datetime
            
            for story in self.story_tracker.stories:
                if story["id"] == story_id:
                    if "generation_info" not in story:
                        story["generation_info"] = {}
                    
                    story["generation_info"]["video_file_path"] = video_path
                    story["generation_info"]["video_generated_at"] = datetime.now().isoformat()
                    
                    if self.story_tracker._save_stories():
                        self.logger.info(f"Updated story {story_id} with video path: {video_path}")
                        return True
                    return False
            
            self.logger.warning(f"Story ID {story_id} not found for video update")
            return False
            
        except Exception as e:
            self.logger.error(f"Error updating story {story_id} with video: {e}")
            return False
