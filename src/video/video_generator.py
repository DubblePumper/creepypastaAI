"""
Video Generator Module

Creates atmospheric horror videos by combining:
- Audio narration (from assets/output)
- Background music (from assets/music)
- AI-generated horror images (stored in assets/images)

Uses FFmpeg-Python and OpenCV for robust, high-performance video generation.
"""

import os
import logging
import hashlib
import random
import tempfile
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

import openai
from PIL import Image
import requests

from ..utils.config_manager import ConfigManager
from .ffmpeg_video_processor import FFmpegVideoProcessor
from .subtitle_generator import SubtitleGenerator
from ..image.openai_image_generator import OpenAIImageGenerator


class VideoGenerator:
    """
    Generates atmospheric horror videos by combining audio narration,
    background music, and AI-generated horror images.
    """
    
    def __init__(self, config: ConfigManager):
        """
        Initialize the video generator.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Paths
        self.audio_path = Path("assets/output")
        self.music_path = Path("assets/music")
        self.images_path = Path("assets/images")
        self.videos_path = Path("assets/videos")
        self.temp_video_dir = Path("temp/video")
        
        # Ensure directories exist
        self.images_path.mkdir(parents=True, exist_ok=True)
        self.videos_path.mkdir(parents=True, exist_ok=True)
        self.temp_video_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up OpenAI API
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            self.logger.warning("OPENAI_API_KEY not found in environment variables. Image generation will be disabled.")
            self.openai_client = None
        else:
            self.openai_client = openai.OpenAI(api_key=openai_api_key)
          # Initialize OpenAI Image Generator
        self.openai_image_generator = OpenAIImageGenerator(config, self.images_path)
        
        # Initialize subtitle generator
        self.subtitle_generator = SubtitleGenerator(config)
        
        # Subtitle output directory
        self.subtitles_path = Path("temp/subtitles")
        self.subtitles_path.mkdir(parents=True, exist_ok=True)
        
        # Video settings
        self.image_duration = 10  # seconds per image
        self.fade_duration = 1.0  # seconds for smooth transitions
        self.video_resolution = (1920, 1080)  # Full HD
        
        # Check FFmpeg availability
        self._check_ffmpeg_config()        
        self.logger.info("Video generator initialized successfully")
    
    def _check_ffmpeg_config(self):
        """Check FFmpeg availability for video processing."""
        try:
            import subprocess
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version_info = result.stdout.split('\n')[0]
                self.logger.info(f"FFmpeg available: {version_info}")
            else:
                self.logger.warning("FFmpeg not available or not working properly")
        except Exception as e:
            self.logger.warning(f"Could not check FFmpeg configuration: {e}")
            
        # Test librosa for audio duration
        try:
            import librosa
            self.logger.info("Librosa audio processing: Available")
        except ImportError:
            self.logger.warning("Librosa not available, using fallback for audio duration")
    
    def generate_horror_images(self, story_title: str, story_content: str, num_images: Optional[int] = None) -> List[str]:
        """
        Generate atmospheric horror images for the story using existing images first,
        then generating only what's needed in random order.
        
        Args:
            story_title: Title of the story for context
            story_content: Story content to extract themes
            num_images: Number of images needed (auto-calculated if None)
            
        Returns:
            List of paths to image files in random order
        """
        try:
            # Calculate number of images needed based on audio duration
            if num_images is None:
                # Estimate audio duration (rough calculation: ~150 words per minute)
                word_count = len(story_content.split())
                estimated_duration = (word_count / 150) * 60  # seconds
                num_images = max(3, int(estimated_duration / self.image_duration))
            
            self.logger.info(f"Need {num_images} horror images for story: {story_title[:50]}...")
            
            # First, collect existing horror images
            existing_images = []
            if self.images_path.exists():
                existing_images = list(self.images_path.glob("horror_*.png"))
            
            self.logger.info(f"Found {len(existing_images)} existing horror images")
            
            # If we have enough existing images, use them in random order
            if len(existing_images) >= num_images:
                selected_images = random.sample(existing_images, num_images)
                random.shuffle(selected_images)  # Additional shuffle for good measure
                self.logger.info(f"Using {num_images} existing images in random order")
                return [str(img) for img in selected_images]
            
            # If we need more images, use all existing ones plus generate additional ones
            final_images = [str(img) for img in existing_images]
            images_needed = num_images - len(existing_images)
            
            self.logger.info(f"Using {len(existing_images)} existing images, generating {images_needed} new images")
            
            if images_needed > 0:
                if not self.openai_client:
                    self.logger.error("OpenAI client not available. Please set OPENAI_API_KEY environment variable.")
                    # Return existing images shuffled if we can't generate new ones
                    if existing_images:
                        random.shuffle(final_images)
                        return final_images
                    return []
                
                # Create prompts for new images
                prompts = self._create_image_prompts(story_title, story_content, images_needed)
                
                for i, prompt in enumerate(prompts, 1):
                    self.logger.info(f"Generating new image {i}/{len(prompts)}: {prompt[:100]}...")
                    
                    # Check if image already exists (cache)
                    image_hash = hashlib.md5(prompt.encode()).hexdigest()
                    image_filename = f"horror_{image_hash}.png"
                    image_path = self.images_path / image_filename
                    
                    if image_path.exists():
                        self.logger.info(f"Using cached image: {image_filename}")
                        final_images.append(str(image_path))
                        continue
                    
                    try:
                        # Generate image with OpenAI DALL-E
                        response = self.openai_client.images.generate(
                            model="dall-e-3",
                            prompt=prompt,
                            size="1792x1024",  # Landscape format
                            quality="standard",
                            n=1
                        )
                        
                        # Download and save the image
                        if response and response.data and len(response.data) > 0:
                            image_url = response.data[0].url
                            if image_url:
                                image_response = requests.get(image_url)
                                
                                if image_response.status_code == 200:
                                    with open(image_path, 'wb') as f:
                                        f.write(image_response.content)
                                    
                                    final_images.append(str(image_path))
                                    self.logger.info(f"Successfully generated and saved: {image_filename}")
                                else:
                                    self.logger.error(f"Failed to download image {i}")
                            else:
                                self.logger.error(f"No image URL returned for image {i}")
                        else:
                            self.logger.error(f"No image data returned for image {i}")
                            
                    except Exception as e:
                        self.logger.error(f"Error generating image {i}: {e}")
                        continue
              # Shuffle final image list for random order
            random.shuffle(final_images)
            
            self.logger.info(f"Final image set: {len(final_images)} images in random order")
            return final_images
            
        except Exception as e:
            self.logger.error(f"Error in image generation: {e}")
            return []
    
    def _create_image_prompts(self, title: str, content: str, num_images: int) -> List[str]:
        """
        Create kid-friendly horror image prompts based on story content.
        
        Args:
            title: Story title
            content: Story content
            num_images: Number of prompts to create
            
        Returns:
            List of image generation prompts
        """
        # Base prompt template for kid-friendly horror
        base_style = ("Digital art, atmospheric horror scene, dark and mysterious but suitable for teens, "
                     "no blood, no gore, no disturbing imagery, cinematic lighting, moody atmosphere, "
                     "professional digital artwork")
        
        # Extract key themes and concepts from the story
        story_themes = self._extract_story_themes(title, content)
        
        # Template prompts that work well for horror stories
        prompt_templates = [
            f"A mysterious {story_themes['setting']} at twilight, {base_style}",
            f"An abandoned {story_themes['location']} with shadows and fog, {base_style}",
            f"A dark forest path with mysterious lights in the distance, {base_style}",
            f"An old vintage {story_themes['object']} in a dimly lit room, {base_style}",
            f"A misty graveyard with ancient headstones under moonlight, {base_style}",
            f"A spooky but elegant mansion silhouette against storm clouds, {base_style}",
            f"A mysterious library with floating books and ethereal light, {base_style}",
            f"An antique mirror in a dusty attic with strange reflections, {base_style}",
            f"A foggy street with old-fashioned lampposts creating long shadows, {base_style}",
            f"A mystical portal or doorway glowing with otherworldly light, {base_style}"
        ]
        
        # Select and customize prompts
        selected_prompts = []
        for i in range(num_images):
            template_index = i % len(prompt_templates)
            prompt = prompt_templates[template_index]
            
            # Add story-specific elements
            if story_themes['main_element']:
                prompt = prompt.replace("mysterious", f"mysterious {story_themes['main_element']}")
            
            selected_prompts.append(prompt)
        
        return selected_prompts
    
    def _extract_story_themes(self, title: str, content: str) -> Dict[str, str]:
        """
        Extract key themes and elements from story for image generation.
        
        Args:
            title: Story title
            content: Story content
            
        Returns:
            Dictionary of extracted themes
        """
        # Simple keyword extraction for themes
        text = (title + " " + content).lower()
        
        # Common settings
        settings = ["house", "forest", "school", "hospital", "church", "library", "attic", "basement"]
        setting = next((s for s in settings if s in text), "house")
          # Common locations
        locations = ["room", "hallway", "garden", "building", "cabin", "mansion", "apartment"]
        location = next((l for l in locations if l in text), "room")
        
        # Common objects
        objects = ["mirror", "doll", "book", "phone", "computer", "music box", "painting", "door"]
        obj = next((o for o in objects if o in text), "mirror")
        
        # Main element
        main_elements = ["shadow", "whisper", "footstep", "voice", "presence", "figure"]
        main_element = next((e for e in main_elements if e in text), "")
        
        return {
            "setting": setting,
            "location": location,
            "object": obj,
            "main_element": main_element
        }
    
    def create_video(self, audio_file: str, story_title: Optional[str] = None, story_content: Optional[str] = None, output_dir: Optional[str] = None) -> Optional[str]:
        """
        Create a complete video following the structured workflow:
        1. Calculate needed images based on audio duration
        2. Check available images in assets/images  
        3. Generate additional images if needed
        4. Create video with images (10 sec per image, smooth transitions)
        5. Add storyline audio from assets/output
        6. Add background music (creepy-music.mp3)
        7. Combine everything into 1 final video
        
        Args:
            audio_file: Path to the audio narration file
            story_title: Title of the story (extracted from filename if None)
            story_content: Story content for image generation context
            output_dir: Optional output directory (uses default if None)
              
        Returns:
            Path to generated video file, or None if failed
        """
        try:
            audio_path = Path(audio_file)
            if not audio_path.exists():
                self.logger.error(f"Audio file not found: {audio_file}")
                return None
            
            # Extract story title from filename if not provided
            if not story_title:
                story_title = self._extract_title_from_filename(audio_path.name)
            
            self.logger.info(f"🎬 Starting video creation workflow for: {story_title}")
            self.logger.info("=" * 60)
            self.logger.info(f"📹 VIDEO GENERATION PROCESS STARTED")
            self.logger.info(f"🎯 Target: {story_title}")
            self.logger.info(f"📁 Input: {audio_path.name}")
            self.logger.info("=" * 60)
              # Step 1: Load audio to get duration
            self.logger.info("📊 Step 1: Loading audio file and calculating duration...")
            import librosa
            try:
                # Use librosa to get audio duration (more reliable than MoviePy)
                audio_duration = librosa.get_duration(path=str(audio_path))
                self.logger.info(f"   Audio duration: {audio_duration:.2f} seconds")
            except Exception as e:
                self.logger.error(f"Error loading audio duration: {e}")
                # Fallback: estimate based on file size (very rough)
                audio_duration = max(30, audio_path.stat().st_size / 16000)  # Rough estimate
                self.logger.warning(f"   Using estimated duration: {audio_duration:.2f} seconds")
            
            # Step 2: Calculate number of images needed
            images_needed = max(3, int(audio_duration / self.image_duration))
            self.logger.info(f"🖼️  Step 2: Calculating images needed...")
            self.logger.info(f"   Images needed: {images_needed} (based on {self.image_duration}s per image)")
            
            # Step 3-4: Ensure sufficient images using OpenAI Image Generator
            self.logger.info("🎨 Step 3-4: Ensuring sufficient images for video...")
              # Get story content for image generation context if not provided
            if not story_content:
                retrieved_content = self._get_story_content(story_title)
                story_content = retrieved_content or ""
            
            all_image_paths = self.openai_image_generator.ensure_sufficient_images(
                story_title or "unknown_story", story_content, images_needed
            )
            
            if not all_image_paths:
                self.logger.error("❌ No images available, cannot create video")
                return None
            
            self.logger.info(f"   Using {len(all_image_paths)} images for video")
            self.logger.info(f"   Total video duration will be: {audio_duration:.2f} seconds")
            self.logger.info(f"   Each image will display for: {audio_duration/len(all_image_paths):.2f} seconds")
              # Generate output filename and path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            story_title = story_title or "unknown_story"  # Ensure story_title is not None
            safe_title = "".join(c for c in story_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:50]
            output_filename = f"creepypasta_video_{safe_title}_{timestamp}.mp4"
            
            # Use custom output directory if provided, otherwise use default
            if output_dir:
                output_path_base = Path(output_dir)
                output_path_base.mkdir(parents=True, exist_ok=True)
            else:
                output_path_base = self.videos_path
            
            output_path = output_path_base / output_filename
            
            # Step 5: Find background music
            background_music_path = None
            music_file = self.music_path / "creepy-music.mp3"
            if music_file.exists():
                background_music_path = str(music_file)
                self.logger.info(f"🎵 Found background music: {music_file}")
            else:
                self.logger.warning(f"Background music not found at {music_file}, proceeding without music")
              # Get audio volume settings
            music_volume = (
                self.config.get("video.background_music.volume", None) or
                self.config.get("audio.volume.background_music", None) or
                self.config.get("audio.background_music.volume", None) or
                self.config.get("video.background_music_volume", None) or
                0.12  # Default to 12% volume for subtle background
            )
            narration_volume = self.config.get("audio.volume.narration", 0.8)
            
            # Step 6: Generate subtitles if enabled
            subtitle_path = None
            if self.config.get("video.subtitles.enabled", False):
                self.logger.info("📝 Step 6: Generating subtitles...")
                if story_content:
                    try:
                        subtitle_filename = f"subtitle_{safe_title}_{timestamp}.srt"
                        subtitle_output_path = self.subtitles_path / subtitle_filename
                        
                        subtitle_path = self.subtitle_generator.generate_subtitle_file(
                            text=story_content,
                            audio_duration=audio_duration,
                            output_path=str(subtitle_output_path)
                        )
                        
                        if subtitle_path:
                            self.logger.info(f"   ✅ Subtitles generated: {subtitle_filename}")
                        else:
                            self.logger.warning("   ⚠️ Subtitle generation failed")
                    except Exception as e:
                        self.logger.error(f"   ❌ Error generating subtitles: {e}")
                        subtitle_path = None
                else:
                    self.logger.warning("   ⚠️ No story content available for subtitle generation")
            else:
                self.logger.info("📝 Step 6: Subtitles disabled in configuration")
            
            # Step 7: Create video using FFmpeg processor
            self.logger.info("🎞️ Step 7-10: Creating video with FFmpeg processor...")
            processor = FFmpegVideoProcessor(temp_dir=self.temp_video_dir)
            
            # Calculate duration for each image (equal distribution)
            image_durations = [audio_duration / len(all_image_paths)] * len(all_image_paths)
              # Create video with all components
            success = processor.create_video_from_images(
                image_paths=all_image_paths,
                durations=image_durations,
                audio_path=str(audio_path),
                output_path=str(output_path),
                background_music_path=background_music_path,
                music_volume=music_volume,
                crossfade_duration=self.fade_duration,
                resolution=self.video_resolution,
                fps=24,
                subtitle_path=subtitle_path
            )
            
            if success:
                self.logger.info("=" * 60)
                self.logger.info("🎉 VIDEO GENERATION COMPLETED SUCCESSFULLY!")
                self.logger.info(f"📁 Output file: {output_path.name}")
                self.logger.info(f"📍 Full path: {output_path}")
                if output_path.exists():
                    self.logger.info(f"📏 File size: {output_path.stat().st_size / (1024*1024):.1f} MB")
                self.logger.info("=" * 60)
                return str(output_path)
            else:
                self.logger.error("=" * 60)
                self.logger.error("❌ VIDEO GENERATION FAILED")
                self.logger.error("FFmpeg video processor failed to create video")
                self.logger.error("=" * 60)
                return None
            
        except Exception as e:
            self.logger.error(f"Error creating video: {e}")
            return None
    
    def cleanup_temp_files(self):
        """Clean up temporary files created during video generation."""
        try:
            # Clean up temp video directory
            if self.temp_video_dir.exists():
                for temp_file in self.temp_video_dir.glob("*TEMP_MPY*"):
                    try:
                        temp_file.unlink()
                        self.logger.debug(f"Cleaned up temp file: {temp_file.name}")
                    except Exception as e:
                        self.logger.warning(f"Could not remove temp file {temp_file}: {e}")
                
                # Also clean up any FFmpeg temp files
                for temp_file in self.temp_video_dir.glob("temp_*"):
                    try:
                        temp_file.unlink()
                        self.logger.debug(f"Cleaned up temp file: {temp_file.name}")
                    except Exception as e:
                        self.logger.warning(f"Could not remove temp file {temp_file}: {e}")
            
            # Clean up subtitle temp files
            if self.subtitles_path.exists():
                for subtitle_file in self.subtitles_path.glob("subtitle_*.srt"):
                    try:
                        subtitle_file.unlink()
                        self.logger.debug(f"Cleaned up subtitle file: {subtitle_file.name}")
                    except Exception as e:
                        self.logger.warning(f"Could not remove subtitle file {subtitle_file}: {e}")
            
            # Clean up any temp files in root directory (fallback)
            root_dir = Path(".")
            for temp_file in root_dir.glob("*TEMP_MPY*"):
                try:
                    temp_file.unlink()
                    self.logger.info(f"Cleaned up stray temp file: {temp_file.name}")
                except Exception as e:
                    self.logger.warning(f"Could not remove stray temp file {temp_file}: {e}")
                    
        except Exception as e:
            self.logger.error(f"Error during temp file cleanup: {e}")
    
    def _extract_title_from_filename(self, filename: str) -> str:
        """
        Extract story title from audio filename.
        
        Args:
            filename: Audio filename
            
        Returns:
            Extracted title
        """
        # Remove file extension
        name = Path(filename).stem
        
        # Remove common prefixes
        prefixes = ["creepypasta_", "creepypasta-", "story_", "story-"]
        for prefix in prefixes:
            if name.startswith(prefix):
                name = name[len(prefix):]
                break
        
        # Remove timestamp pattern (YYYYMMDD_HHMMSS)
        import re
        name = re.sub(r'_\d{8}_\d{6}$', '', name)
        
        # Replace underscores with spaces
        title = name.replace('_', ' ').strip()
        
        return title if title else filename
    
    def _get_story_content(self, title: str) -> Optional[str]:
        """
        Get story content from the story database.
        
        Args:
            title: Story title
            
        Returns:
            Story content if found, None otherwise
        """
        try:
            # Load stories from JSON database
            stories_file = Path("data/generated_stories.json")
            if not stories_file.exists():
                return None
            
            with open(stories_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Get stories list
            stories = data.get("stories", []) if isinstance(data, dict) else data
            
            # Find story by title (fuzzy match)
            for story in stories:
                story_title = story.get("title", "")
                if title.lower() in story_title.lower() or story_title.lower() in title.lower():
                    return story.get("content", "")
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error loading story content: {e}")
            return None
    
    def generate_videos_for_all_audio(self) -> List[str]:
        """
        Generate videos for all audio files in the output directory.
        
        Returns:
            List of generated video file paths
        """
        try:
            self.logger.info("Generating videos for all audio files...")
            
            # Find all audio files
            audio_files = list(self.audio_path.glob("*.mp3"))
            
            if not audio_files:
                self.logger.warning("No audio files found in output directory")
                return []
            
            generated_videos = []
            for i, audio_file in enumerate(audio_files, 1):
                self.logger.info(f"Processing audio file {i}/{len(audio_files)}: {audio_file.name}")
                
                # Check if video already exists
                title = self._extract_title_from_filename(audio_file.name)
                existing_videos = list(self.videos_path.glob(f"*{title.replace(' ', '_')}*.mp4"))
                
                if existing_videos:
                    self.logger.info(f"Video already exists for: {title}")
                    generated_videos.extend([str(v) for v in existing_videos])
                    continue
                
                # Generate video
                video_path = self.create_video(str(audio_file))
                if video_path:
                    generated_videos.append(video_path)
            
            # Clean up any temp files
            self.cleanup_temp_files()
            
            self.logger.info(f"Generated {len(generated_videos)} videos successfully")
            return generated_videos
            
        except Exception as e:
            # Clean up temp files even on error
            self.cleanup_temp_files()
            self.logger.error(f"Error generating videos for all audio: {e}")
            return []
