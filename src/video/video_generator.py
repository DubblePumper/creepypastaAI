"""
Video Generator Module

Creates atmospheric horror videos by combining:
- Audio narration (from assets/output)
- Background music (from assets/music)
- AI-generated horror images (stored in assets/images)
"""

import os
import logging
import hashlib
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

import openai
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, CompositeAudioClip, concatenate_audioclips
from moviepy.config import change_settings
from PIL import Image
import requests

from ..utils.config_manager import ConfigManager

# Configure moviepy to work better with FFmpeg on Windows
try:
    import moviepy.config as mp_config
    # Try to find FFmpeg automatically - let moviepy detect it
    # Don't force a specific path, let it use PATH
    pass
except Exception:
    pass  # Continue without specific configuration


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
          # Set up OpenAI API
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            self.logger.warning("OPENAI_API_KEY not found in environment variables. Image generation will be disabled.")
            self.openai_client = None
        else:
            self.openai_client = openai.OpenAI(api_key=openai_api_key)
        
        # Paths
        self.audio_path = Path("assets/output")
        self.music_path = Path("assets/music")
        self.images_path = Path("assets/images")
        self.videos_path = Path("assets/videos")
        
        # Ensure directories exist
        self.images_path.mkdir(parents=True, exist_ok=True)
        self.videos_path.mkdir(parents=True, exist_ok=True)
        
        # Video settings
        self.image_duration = 10  # seconds per image
        self.fade_duration = 1.0  # seconds for smooth transitions
        self.video_resolution = (1920, 1080)  # Full HD
          # Check moviepy/FFmpeg configuration
        self._check_ffmpeg_config()
        
        self.logger.info("Video generator initialized successfulsly")
    
    
    def generate_horror_images(self, story_title: str, story_content: str, num_images: Optional[int] = None) -> List[str]:
        """
        Generate kid-friendly horror images using OpenAI DALL-E.
        
        Args:
            story_title: Title of the story for context
            story_content: Story content to extract themes
            num_images: Number of images to generate (auto-calculated if None)
            
        Returns:
            List of generated image file paths
        """
        try:
            if not self.openai_client:
                self.logger.error("OpenAI client not available. Please set OPENAI_API_KEY environment variable.")
                return []
            # Calculate number of images needed based on audio duration
            if num_images is None:
                # Estimate audio duration (rough calculation: ~150 words per minute)
                word_count = len(story_content.split())
                estimated_duration = (word_count / 150) * 60  # seconds
                num_images = max(3, int(estimated_duration / self.image_duration))
            
            self.logger.info(f"Generating {num_images} horror images for story: {story_title[:50]}...")
            
            # Create prompts for different scenes
            prompts = self._create_image_prompts(story_title, story_content, num_images)
            
            generated_images = []
            for i, prompt in enumerate(prompts, 1):
                self.logger.info(f"Generating image {i}/{len(prompts)}: {prompt[:100]}...")
                
                # Check if image already exists (cache)
                image_hash = hashlib.md5(prompt.encode()).hexdigest()
                image_filename = f"horror_{image_hash}.png"
                image_path = self.images_path / image_filename
                
                if image_path.exists():
                    self.logger.info(f"Using cached image: {image_filename}")
                    generated_images.append(str(image_path))
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
                                
                                generated_images.append(str(image_path))
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
            
            self.logger.info(f"Generated {len(generated_images)} images successfully")
            return generated_images
            
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
            "setting": setting,            "location": location,
            "object": obj,
            "main_element": main_element
        }
    
    def create_video(self, audio_file: str, story_title: Optional[str] = None, story_content: Optional[str] = None, output_dir: Optional[str] = None) -> Optional[str]:
        """
        Create a complete video with audio, images, and background music.
        
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
            
            self.logger.info(f"Creating video for: {story_title}")
            
            # Load audio to get duration
            audio_clip = AudioFileClip(str(audio_path))
            audio_duration = audio_clip.duration
              # Get story content from database if not provided
            if not story_content:
                retrieved_content = self._get_story_content(story_title)
                story_content = retrieved_content or ""
            
            # Generate horror images
            image_paths = self.generate_horror_images(story_title, story_content or "")
            
            if not image_paths:
                self.logger.error("No images generated, cannot create video")
                audio_clip.close()
                return None
            
            # Create video clips from images
            video_clips = self._create_video_clips_from_images(image_paths, audio_duration)
            
            # Combine all video clips
            final_video = concatenate_videoclips(video_clips, method="compose")
            
            # Add background music
            final_video = self._add_background_music(final_video, audio_clip)
              # Generate output filename and path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c for c in story_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:50]
            output_filename = f"creepypasta_video_{safe_title}_{timestamp}.mp4"
            
            # Use custom output directory if provided, otherwise use default
            if output_dir:
                output_path_base = Path(output_dir)
                output_path_base.mkdir(parents=True, exist_ok=True)
            else:
                output_path_base = self.videos_path
                
            output_path = output_path_base / output_filename# Write the final video with robust FFmpeg settings
            self.logger.info(f"Rendering video: {output_filename}")
            
            # Ensure video has proper FPS
            final_video = final_video.set_fps(24)
            
            # Try multiple rendering approaches
            success = False
            
            # Method 1: Simple rendering
            try:
                self.logger.info("Attempting simple video rendering...")
                final_video.write_videofile(
                    str(output_path),
                    fps=24,
                    verbose=False,
                    logger=None,
                    audio=True
                )
                success = True
                
            except Exception as e1:
                self.logger.warning(f"Simple rendering failed: {e1}")
                
                # Method 2: Without audio codec specification
                try:
                    self.logger.info("Trying without codec specification...")
                    final_video.write_videofile(
                        str(output_path),
                        fps=24,
                        verbose=False,
                        logger=None
                    )
                    success = True
                    
                except Exception as e2:
                    self.logger.warning(f"Second method failed: {e2}")
                    
                    # Method 3: Most basic approach
                    try:
                        self.logger.info("Trying most basic rendering...")
                        final_video.write_videofile(str(output_path), fps=24)
                        success = True
                        
                    except Exception as e3:
                        self.logger.error(f"All rendering methods failed:")
                        self.logger.error(f"  Method 1: {e1}")
                        self.logger.error(f"  Method 2: {e2}")
                        self.logger.error(f"  Method 3: {e3}")
            
            if not success:
                # Cleanup and return None
                final_video.close()
                audio_clip.close()
                return None
            
            # Cleanup
            final_video.close()
            audio_clip.close()
            
            self.logger.info(f"Video created successfully: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Error creating video: {e}")
            return None
    
    def _create_video_clips_from_images(self, image_paths: List[str], total_duration: float) -> List[VideoFileClip]:
        """
        Create video clips from images with smooth transitions.
        
        Args:
            image_paths: List of image file paths
            total_duration: Total duration needed for the video
            
        Returns:
            List of video clips
        """
        clips = []
          # Calculate duration per image
        duration_per_image = total_duration / len(image_paths)
        
        for i, image_path in enumerate(image_paths):
            try:
                # Create image clip with FPS set
                img_clip = ImageClip(image_path, duration=duration_per_image)
                img_clip = img_clip.set_fps(24)  # Set FPS to avoid rendering issues
                
                # Resize to fit video resolution while maintaining aspect ratio
                img_clip = img_clip.resize(height=self.video_resolution[1])
                
                # Center the image if it doesn't match the width
                if img_clip.w < self.video_resolution[0]:
                    img_clip = img_clip.on_color(
                        size=self.video_resolution,
                        color=(0, 0, 0),  # Black background
                        pos='center'
                    )
                elif img_clip.w > self.video_resolution[0]:
                    img_clip = img_clip.crop(
                        x_center=img_clip.w/2,
                        width=self.video_resolution[0]
                    )
                
                # Add fade in/out for smooth transitions
                if i == 0:
                    # First image: fade in only
                    img_clip = img_clip.fadein(self.fade_duration)
                elif i == len(image_paths) - 1:
                    # Last image: fade out only
                    img_clip = img_clip.fadeout(self.fade_duration)
                else:
                    # Middle images: crossfade
                    img_clip = img_clip.crossfadein(self.fade_duration).crossfadeout(self.fade_duration)
                
                clips.append(img_clip)
                
            except Exception as e:
                self.logger.error(f"Error processing image {image_path}: {e}")
                continue
        
        return clips
    
    def _add_background_music(self, video_clip, narration_audio: AudioFileClip):
        """
        Add background music to the video.
        
        Args:
            video_clip: Main video clip
            narration_audio: Narration audio clip
            
        Returns:
            Video clip with background music added
        """
        try:
            # Find background music file
            music_file = self.music_path / "creepy-music.mp3"
            if not music_file.exists():
                self.logger.warning("Background music file not found, proceeding without music")
                return video_clip.set_audio(narration_audio)
            
            # Load background music
            background_music = AudioFileClip(str(music_file))            # Loop music if it's shorter than the video
            if background_music.duration < video_clip.duration:
                # Calculate how many loops we need
                loops_needed = int(video_clip.duration / background_music.duration) + 1
                background_music = concatenate_audioclips([background_music] * loops_needed)
            
            # Trim music to match video duration
            background_music = background_music.subclip(0, video_clip.duration)
            
            # Reduce background music volume
            music_volume = self.config.get("video.background_music_volume", 0.3)
            background_music = background_music.volumex(music_volume)
            
            # Combine narration and background music
            final_audio = CompositeAudioClip([narration_audio, background_music])
            
            # Set the combined audio to the video
            final_video = video_clip.set_audio(final_audio)
            
            # Cleanup
            background_music.close()
            
            return final_video
            
        except Exception as e:
            self.logger.error(f"Error adding background music: {e}")
            # Return video with just narration audio
            return video_clip.set_audio(narration_audio)
    
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
            
            self.logger.info(f"Generated {len(generated_videos)} videos successfully")
            return generated_videos
            
        except Exception as e:
            self.logger.error(f"Error generating videos for all audio: {e}")
            return []
    
    def _check_ffmpeg_config(self):
        """Check and log moviepy/FFmpeg configuration."""
        try:
            from moviepy.config import FFMPEG_BINARY
            self.logger.info(f"MoviePy FFmpeg binary: {FFMPEG_BINARY}")
        except Exception as e:
            self.logger.warning(f"Could not check FFmpeg configuration: {e}")
            
        # Test a simple moviepy operation
        try:
            from moviepy.editor import ColorClip
            test_clip = ColorClip(size=(100, 100), color=(0, 0, 0), duration=0.1)
            test_clip.close()
            self.logger.info("MoviePy basic functionality test: PASSED")
        except Exception as e:
            self.logger.warning(f"MoviePy basic test failed: {e}")
