"""
CreepyPasta AI - Main Application Entry Point

This module serves as the main entry point for the CreepyPasta AI application.
It orchestrates the scraping of stories from Reddit, converts them to speech,
and creates atmospheric audio experiences with background music and effects.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from src.scrapers.reddit_scraper import RedditScraper
from src.audio.tts_manager import TTSManager
from src.audio.audio_mixer import AudioMixer
from src.video.video_generator import VideoGenerator
from src.utils.config_manager import ConfigManager
from src.utils.story_processor import StoryProcessor
from src.utils.story_tracker import StoryTracker
from src.utils.logger import setup_logger
from src.utils.translation import TranslationManager
from src.utils.language_manager import LanguageManager
from src.cli.cli_handler import CLIHandler
from src.cli.execution_modes import ScrapeOnlyMode, AudioOnlyMode, VideoOnlyMode


class CreepyPastaAI:
    """
    Main application class for CreepyPasta AI.
    
    Handles the complete workflow from story scraping to audio generation.
    """
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        """
        Initialize the CreepyPasta AI application.
        
        Args:
            config_path: Path to the configuration file
        """        
        self.config = ConfigManager(config_path)
        self.logger = setup_logger("CreepyPastaAI", self.config.get("logging.level", "INFO"))
        
        # Initialize components
        self.reddit_scraper = RedditScraper(self.config)
        self.tts_manager = TTSManager(self.config)
        self.audio_mixer = AudioMixer(self.config)
        self.video_generator = VideoGenerator(self.config)
        self.story_processor = StoryProcessor(self.config)
        self.story_tracker = StoryTracker(self.config)
        self.translation_manager = TranslationManager(self.config.config)
        self.language_manager = LanguageManager(self.config)
        
        self.logger.info("CreepyPasta AI initialized successfully")
    
    def run(self, num_stories: Optional[int] = None) -> List[str]:
        """
        Run the complete CreepyPasta AI workflow.
        
        Args:
            num_stories: Number of stories to process (uses config default if None)
            
        Returns:
            List of generated audio file paths
        """
        try:
            # Get number of stories from config if not specified
            if num_stories is None:
                num_stories = self.config.get("reddit.limit", 10)
            if num_stories is None:
                num_stories = 10  # Fallback to default if config returns None
            
            self.logger.info(f"Starting CreepyPasta AI workflow for {num_stories} stories")
            
            # Step 1: Scrape and store stories from Reddit
            new_stories_count = self._scrape_and_store_stories(int(num_stories))
            
            if new_stories_count == 0:
                self.logger.info("No new stories to process.")
            else:
                self.logger.info(f"Added {new_stories_count} new stories to database")
            
            # Step 2: Generate audio for stories without audio files
            generated_files = self._generate_audio_for_pending_stories()
            
            self.logger.info(f"Workflow completed. Generated {len(generated_files)} audio files")
              # Display tracking statistics
            self._display_tracking_statistics()
            
            return generated_files
            
        except Exception as e:
            self.logger.error(f"Error in main workflow: {e}")
            raise
    
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
        
    def display_system_info(self):
        """Display system information and available TTS providers."""
        self.logger.info("=" * 50)
        self.logger.info("CreepyPasta AI System Information")
        self.logger.info("=" * 50)
        
        # Display available TTS providers
        providers = self.tts_manager.get_available_providers()
        current_provider = self.config.get("tts.provider", "gtts")
        
        self.logger.info(f"Current TTS Provider: {current_provider}")
        self.logger.info(f"Available TTS Providers: {', '.join(providers)}")
        if "openai" in providers and current_provider == "openai":
            self.logger.info("✅ OpenAI TTS configured with automatic fallback to Google TTS")
        elif "gtts" in providers:
            self.logger.info("✅ Google TTS available as fallback option")
        
        self.logger.info("=" * 50)
    
    def _display_tracking_statistics(self):
        """Display story tracking statistics."""
        try:
            stats = self.story_tracker.get_statistics()
            
            self.logger.info("=" * 50)
            self.logger.info("Story Tracking Statistics")
            self.logger.info("=" * 50)
            
            self.logger.info(f"📚 Total Stories Tracked: {stats.get('total_stories', 0)}")
            self.logger.info(f"🎵 Stories with Audio: {stats.get('stories_with_audio', 0)}")
            self.logger.info(f"📊 Average Content Length: {stats.get('average_content_length', 0):.0f} characters")
            self.logger.info(f"📝 Average Word Count: {stats.get('average_word_count', 0):.0f} words")
            
            tts_providers = stats.get('tts_providers_used', [])
            if tts_providers:
                self.logger.info(f"🗣️ TTS Providers Used: {', '.join(tts_providers)}")
            
            date_range = stats.get('date_range', {})
            if date_range:
                self.logger.info(f"📅 Date Range: {date_range.get('earliest', 'N/A')[:10]} to {date_range.get('latest', 'N/A')[:10]}")
            
            self.logger.info(f"💾 Stories saved to: data/generated_stories.json")
            self.logger.info("=" * 50)
            
        except Exception as e:
            self.logger.error(f"Error displaying tracking statistics: {e}")
    
    def _scrape_and_store_stories(self, num_stories: int) -> int:
        """
        Scrape stories from Reddit and store new ones in JSON database.
        
        Args:
            num_stories: Number of stories to scrape
            
        Returns:
            Number of new stories added to database
        """
        try:
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
                        }                    )
                    
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
            
            self.logger.info(f"Successfully added {new_stories_count} new stories to database")
            return new_stories_count
            
        except Exception as e:
            self.logger.error(f"Error in scraping and storing stories: {e}")
            return 0
    
    def _generate_audio_for_pending_stories(self) -> List[str]:
        """
        Generate audio for all stories in database that don't have audio files yet.
        
        Returns:
            List of generated audio file paths
        """
        try:
            self.logger.info("Generating audio for stories without audio files...")
            
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
            self.logger.error(f"Error generating audio for pending stories: {e}")
            return []
    
    def generate_videos(self, generate_for_all: bool = True) -> List[str]:
        """
        Generate videos for audio files.
        
        Args:
            generate_for_all: If True, generate videos for all audio files
            
        Returns:
            List of generated video file paths
        """
        try:
            self.logger.info("Starting video generation workflow...")
            
            if generate_for_all:
                # Generate videos for all existing audio files
                generated_videos = self.video_generator.generate_videos_for_all_audio()
            else:
                # Generate videos only for stories without videos
                generated_videos = self._generate_videos_for_pending_stories()
            
            self.logger.info(f"Video generation completed. Generated {len(generated_videos)} videos")
            return generated_videos
            
        except Exception as e:
            self.logger.error(f"Error in video generation workflow: {e}")
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
        

def main():
    """Main entry point for the application."""
    try:
        # Create logs directory if it doesn't exist
        Path("logs").mkdir(exist_ok=True)
        
        # Initialize CLI handler
        cli = CLIHandler()
        
        # Parse command line arguments
        args = cli.parse_args()
        
        # Validate arguments
        if not cli.validate_args(args):
            sys.exit(1)
          # Display banner unless we're just showing info/stats/language commands
        if not (args.info or args.stats or 
                (hasattr(args, 'list_languages') and args.list_languages) or
                (hasattr(args, 'enable_language') and args.enable_language) or
                (hasattr(args, 'disable_language') and args.disable_language) or
                (hasattr(args, 'list_enabled') and args.list_enabled) or
                (hasattr(args, 'language_status') and args.language_status)):
            cli.display_banner()
        
        # Initialize the application
        app = CreepyPastaAI(args.config)
        
        # Handle language management commands first
        if cli.handle_language_management_commands(args, app.language_manager):
            return
        
        # Handle info and stats modes
        if args.info:
            app.display_system_info()
            return
        
        if args.stats:
            app._display_tracking_statistics()
            return
        
        # Set up multilingual support
        if hasattr(args, 'language') and args.language:
            app.logger.info(f"Setting target language to: {args.language}")
            app.tts_manager.set_language(args.language)
            
            # Override translation provider if specified
            if hasattr(args, 'translation_provider') and args.translation_provider:
                # Check if set_provider method exists before calling it
                if hasattr(app.translation_manager, 'set_provider'):
                    app.translation_manager.set_provider(args.translation_provider)
                    app.logger.info(f"Using translation provider: {args.translation_provider}")
                else:
                    app.logger.warning(f"Translation provider setting not supported by current TranslationManager implementation")
        
        # Enable translation if requested
        translation_enabled = hasattr(args, 'translate') and args.translate
        if translation_enabled:
            app.logger.info("Translation enabled for stories")
        
        # Set up logging level based on verbose flag
        if args.verbose:
            app.logger.setLevel(logging.DEBUG)
        
        # Execute based on mode
        if args.mode == "complete":
            # Run complete workflow
            app.logger.info("Running complete workflow...")
            app.display_system_info()
            
            generated_files = app.run(args.stories)
            
            if generated_files:
                print(f"\n✅ Successfully generated {len(generated_files)} creepypasta audio files:")
                for file_path in generated_files:
                    print(f"  📁 {file_path}")
            else:
                print("\n❌ No audio files were generated.")
        
        elif args.mode == "scrape":
            # Scraping only mode
            app.logger.info("Running scraping-only mode...")
            scrape_handler = ScrapeOnlyMode(app.config, app.logger)
            new_stories_count = scrape_handler.execute(args.stories)
            
            if new_stories_count > 0:
                print(f"\n✅ Successfully scraped and stored {new_stories_count} new stories")
                print("  💡 Use 'python main.py --mode audio' to generate audio files")
            else:
                print("\n❌ No new stories were scraped.")
        
        elif args.mode == "audio":
            # Audio only mode
            app.logger.info("Running audio-only mode...")
            audio_handler = AudioOnlyMode(app.config, app.logger)
            generated_files = audio_handler.execute()
            
            if generated_files:
                print(f"\n✅ Successfully generated {len(generated_files)} audio files:")
                for file_path in generated_files:
                    print(f"  📁 {file_path}")
                print("  💡 Use 'python main.py --mode video' to generate video files")
            else:
                print("\n❌ No audio files were generated.")
        
        elif args.mode == "video":
            # Video only mode
            app.logger.info("Running video-only mode...")
            video_handler = VideoOnlyMode(app.config, app.logger)
            generated_videos = video_handler.execute(args.video_all)
            
            if generated_videos:
                print(f"\n✅ Successfully generated {len(generated_videos)} video files:")
                for file_path in generated_videos:
                    print(f"  📁 {file_path}")
            else:
                print("\n❌ No video files were generated.")
        
        # Display final statistics unless we're in quiet mode
        if not args.info and not args.stats:
            app._display_tracking_statistics()
            
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
