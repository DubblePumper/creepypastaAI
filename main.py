"""
CreepyPasta AI - Main Application Entry Point

This module serves as the main entry point for the CreepyPasta AI application.
It orchestrates the scraping of stories from Reddit, converts them to speech,
and creates atmospheric audio experiences with background music and effects.
"""

import logging
import sys
from pathlib import Path
from typing import List, Optional

from src.scrapers.reddit_scraper import RedditScraper
from src.audio.tts_manager import TTSManager
from src.audio.audio_mixer import AudioMixer
from src.utils.config_manager import ConfigManager
from src.utils.story_processor import StoryProcessor
from src.utils.logger import setup_logger


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
        self.story_processor = StoryProcessor(self.config)
        
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
            
            # Step 1: Scrape stories from Reddit
            self.logger.info("Scraping stories from Reddit...")
            raw_stories = self.reddit_scraper.scrape_stories(limit=int(num_stories))
            
            if not raw_stories:
                self.logger.warning("No stories found. Exiting.")
                return []
            
            self.logger.info(f"Found {len(raw_stories)} stories")
            
            # Step 2: Process and filter stories
            self.logger.info("Processing stories...")
            processed_stories = []
            for story in raw_stories:
                processed_story = self.story_processor.process_story(story)
                if processed_story:
                    processed_stories.append(processed_story)
            
            self.logger.info(f"Processed {len(processed_stories)} valid stories")
            
            # Step 3: Generate audio for each story
            generated_files = []
            for i, story in enumerate(processed_stories, 1):
                self.logger.info(f"Generating audio for story {i}/{len(processed_stories)}: {story['title'][:50]}...")
                
                try:
                    audio_file = self._generate_story_audio(story)
                    if audio_file:
                        generated_files.append(audio_file)
                        self.logger.info(f"Successfully generated: {audio_file}")
                    
                except Exception as e:
                    self.logger.error(f"Failed to generate audio for story '{story['title']}': {e}")
                    continue
            
            self.logger.info(f"Workflow completed. Generated {len(generated_files)} audio files")
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


def main():
    """Main entry point for the application."""
    try:
        # Create logs directory if it doesn't exist
        Path("logs").mkdir(exist_ok=True)
        
        # Initialize and run the application
        app = CreepyPastaAI()
        
        # Check command line arguments
        num_stories = None
        if len(sys.argv) > 1:
            try:
                num_stories = int(sys.argv[1])
            except ValueError:
                print("Usage: python main.py [number_of_stories]")
                sys.exit(1)
        
        # Run the application
        generated_files = app.run(num_stories)
        
        if generated_files:
            print(f"\n✅ Successfully generated {len(generated_files)} creepypasta audio files:")
            for file_path in generated_files:
                print(f"  📁 {file_path}")
        else:
            print("\n❌ No audio files were generated.")
            
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
