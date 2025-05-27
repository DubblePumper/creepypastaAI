"""
OpenAI Image Generator Module

Enhanced image generation system for CreepyPasta AI that:
- Creates kid-friendly horror images using DALL-E 3
- Implements smart caching to avoid regenerating identical images
- Provides fallback generation when existing images are insufficient
- Maintains consistency with story themes and atmosphere
"""

import os
import logging
import hashlib
import requests
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

import openai
from PIL import Image


class OpenAIImageGenerator:
    """
    Enhanced OpenAI image generator for horror-themed video content.
    """
    
    def __init__(self, config_manager, images_path: Path):
        """
        Initialize the OpenAI image generator.
        
        Args:
            config_manager: Configuration manager instance
            images_path: Path to store generated images
        """
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
        self.images_path = images_path
        self.images_path.mkdir(parents=True, exist_ok=True)
        
        # Set up OpenAI client
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            self.logger.warning("OPENAI_API_KEY not found. Image generation will be disabled.")
            self.openai_client = None
        else:
            self.openai_client = openai.OpenAI(api_key=openai_api_key)
            self.logger.info("OpenAI image generator initialized successfully")
        
        # Image generation settings
        self.image_style = self.config.get("video.images.style", "kid_friendly_horror")
        self.image_quality = self.config.get("video.images.quality", "standard")
        self.image_size = self.config.get("video.images.size", "1792x1024")
        self.cache_enabled = self.config.get("video.images.cache_enabled", True)
        
        # Cache file for generated images metadata
        self.cache_file = self.images_path / "generated_images_cache.json"
        self.cache_data = self._load_cache()
    
    def _load_cache(self) -> Dict[str, Any]:
        """Load image generation cache."""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"Could not load image cache: {e}")
        
        return {
            "generated_images": {},
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_images": 0
            }
        }
    
    def _save_cache(self):
        """Save image generation cache."""
        try:
            self.cache_data["metadata"]["last_updated"] = datetime.now().isoformat()
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.warning(f"Could not save image cache: {e}")
    
    def _extract_story_themes(self, title: str, content: str) -> Dict[str, Any]:
        """
        Extract key themes and elements from story for image generation.
        
        Args:
            title: Story title
            content: Story content
            
        Returns:
            Dictionary of extracted themes
        """
        text = (title + " " + content).lower()
        
        # Common horror settings
        settings = ["house", "forest", "school", "hospital", "church", "library", 
                   "attic", "basement", "mansion", "cabin", "apartment", "graveyard"]
        setting = next((s for s in settings if s in text), "mysterious house")
        
        # Common locations within settings
        locations = ["room", "hallway", "corridor", "staircase", "doorway", 
                    "window", "garden", "pathway", "entrance"]
        location = next((l for l in locations if l in text), "room")
        
        # Common horror objects
        objects = ["mirror", "doll", "book", "phone", "computer", "music box", 
                  "painting", "door", "window", "clock", "lamp", "chest"]
        obj = next((o for o in objects if o in text), "mirror")
        
        # Atmospheric elements
        atmospheres = ["fog", "mist", "shadows", "darkness", "twilight", 
                      "moonlight", "candlelight", "storm", "rain"]
        atmosphere = next((a for a in atmospheres if a in text), "shadows")
        
        return {
            "setting": setting,
            "location": location,
            "object": obj,
            "atmosphere": atmosphere,
            "title_keywords": title.lower().split()[:3]  # First 3 words of title
        }
    
    def _create_advanced_prompts(self, title: str, content: str, num_images: int) -> List[str]:
        """
        Create sophisticated image prompts based on story analysis.
        
        Args:
            title: Story title
            content: Story content
            num_images: Number of prompts to create
            
        Returns:
            List of detailed image generation prompts
        """
        # Extract story themes
        themes = self._extract_story_themes(title, content)
        
        # Base style for all images
        base_style = (
            "Digital art, atmospheric horror scene, dark and mysterious but suitable for teens, "
            "no blood, no gore, no disturbing imagery, cinematic lighting, moody atmosphere, "
            "professional digital artwork, high quality, detailed"
        )
        
        # Advanced prompt templates with thematic variations
        prompt_templates = [
            # Setting-based prompts
            f"A mysterious {themes['setting']} at {themes['atmosphere']}, "
            f"empty and atmospheric, {base_style}",
            
            f"The interior of an old {themes['setting']}, dim lighting with {themes['atmosphere']}, "
            f"vintage furniture, {base_style}",
            
            # Object-focused prompts
            f"An antique {themes['object']} in a dark {themes['location']}, "
            f"surrounded by {themes['atmosphere']}, mysterious and eerie, {base_style}",
            
            f"A close-up of an old {themes['object']}, weathered and mysterious, "
            f"dramatic lighting, {base_style}",
            
            # Atmospheric scenes
            f"A long {themes['location']} with {themes['atmosphere']}, "
            f"old-fashioned lighting, perspective view, {base_style}",
            
            f"A {themes['setting']} exterior at night, {themes['atmosphere']} surrounding it, "
            f"moonlight casting shadows, {base_style}",
            
            # Story-specific prompts (using title keywords)
            f"A scene inspired by '{' '.join(themes['title_keywords'])}', "
            f"mysterious {themes['setting']}, {themes['atmosphere']}, {base_style}",
            
            # Generic atmospheric scenes
            f"A spooky but elegant staircase with ornate railings, "
            f"{themes['atmosphere']} and dramatic lighting, {base_style}",
            
            f"An abandoned library with floating dust particles in sunbeams, "
            f"old books and {themes['atmosphere']}, {base_style}",
            
            f"A vintage window with {themes['atmosphere']} outside, "
            f"curtains slightly moving, moody lighting, {base_style}",
            
            f"A misty forest path with ancient trees, "
            f"mysterious lights in the distance, {base_style}",
            
            f"An old-fashioned street with vintage lampposts, "
            f"{themes['atmosphere']} creating long shadows, {base_style}"
        ]
        
        # Select and customize prompts
        selected_prompts = []
        for i in range(num_images):
            template_index = i % len(prompt_templates)
            prompt = prompt_templates[template_index]
            
            # Add variation to avoid identical images
            variations = [
                f", viewed from a different angle",
                f", with enhanced {themes['atmosphere']}",
                f", in a different time of day",
                f", with subtle color variations",
                f", with additional atmospheric details"
            ]
            
            if i > 0:  # Add variation to non-first images
                variation = variations[i % len(variations)]
                prompt += variation
            
            selected_prompts.append(prompt)
        
        return selected_prompts
    
    def generate_images(self, story_title: str, story_content: str, num_images: int) -> List[str]:
        """
        Generate horror images for the story using OpenAI DALL-E.
        
        Args:
            story_title: Title of the story for context
            story_content: Story content to extract themes
            num_images: Number of images to generate
            
        Returns:
            List of paths to generated image files
        """
        if not self.openai_client:
            self.logger.error("OpenAI client not available. Cannot generate images.")
            return []
        
        self.logger.info(f"Generating {num_images} images for story: {story_title[:50]}...")
        
        # Create sophisticated prompts
        prompts = self._create_advanced_prompts(story_title, story_content, num_images)
        generated_images = []
        
        for i, prompt in enumerate(prompts, 1):
            self.logger.info(f"Generating image {i}/{num_images}...")
            self.logger.debug(f"Prompt: {prompt[:150]}...")
            
            # Check cache first
            prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
            cache_key = f"{prompt_hash}_{self.image_size}_{self.image_quality}"
            
            if self.cache_enabled and cache_key in self.cache_data["generated_images"]:
                cached_path = self.cache_data["generated_images"][cache_key]["file_path"]
                if Path(cached_path).exists():
                    self.logger.info(f"Using cached image: {Path(cached_path).name}")
                    generated_images.append(cached_path)
                    continue
            
            try:
                # Generate image with OpenAI DALL-E 3
                response = self.openai_client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size=self.image_size,
                    quality=self.image_quality,
                    n=1
                )
                
                if response and response.data and len(response.data) > 0:
                    image_url = response.data[0].url
                    if image_url:
                        # Download and save the image
                        image_filename = f"horror_generated_{prompt_hash}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        image_path = self.images_path / image_filename
                        
                        image_response = requests.get(image_url, timeout=30)
                        if image_response.status_code == 200:
                            with open(image_path, 'wb') as f:
                                f.write(image_response.content)
                            
                            # Verify image was saved correctly
                            if image_path.exists() and image_path.stat().st_size > 1000:
                                generated_images.append(str(image_path))
                                self.logger.info(f"Successfully generated: {image_filename}")
                                
                                # Update cache
                                if self.cache_enabled:
                                    self.cache_data["generated_images"][cache_key] = {
                                        "file_path": str(image_path),
                                        "prompt": prompt,
                                        "generated_at": datetime.now().isoformat(),
                                        "story_title": story_title
                                    }
                                    self.cache_data["metadata"]["total_images"] = len(self.cache_data["generated_images"])
                                    self._save_cache()
                            else:
                                self.logger.error(f"Generated image file is invalid: {image_filename}")
                        else:
                            self.logger.error(f"Failed to download image {i}: HTTP {image_response.status_code}")
                    else:
                        self.logger.error(f"No image URL returned for image {i}")
                else:
                    self.logger.error(f"No image data returned for image {i}")
                    
            except Exception as e:
                self.logger.error(f"Error generating image {i}: {e}")
                continue
        
        self.logger.info(f"Generated {len(generated_images)} new images successfully")
        return generated_images
    
    def get_existing_images(self) -> List[str]:
        """
        Get list of all existing horror images.
        
        Returns:
            List of paths to existing images
        """
        existing_images = []
        if self.images_path.exists():
            # Get both original and generated images
            for pattern in ["horror_*.png", "horror_generated_*.png"]:
                existing_images.extend(list(self.images_path.glob(pattern)))
        
        return [str(img) for img in existing_images]
    
    def ensure_sufficient_images(self, story_title: str, story_content: str, required_count: int) -> List[str]:
        """
        Ensure there are enough images for video creation, generating if necessary.
        
        Args:
            story_title: Story title for context
            story_content: Story content for theme extraction
            required_count: Number of images needed
            
        Returns:
            List of image paths (existing + newly generated as needed)
        """
        self.logger.info(f"Ensuring {required_count} images are available...")
        
        # Get existing images
        existing_images = self.get_existing_images()
        self.logger.info(f"Found {len(existing_images)} existing images")
        
        if len(existing_images) >= required_count:
            # We have enough existing images
            import random
            selected_images = random.sample(existing_images, required_count)
            random.shuffle(selected_images)
            self.logger.info(f"Using {required_count} existing images")
            return selected_images
        
        # We need to generate additional images
        images_needed = required_count - len(existing_images)
        self.logger.info(f"Need to generate {images_needed} additional images")
        
        if not self.openai_client:
            self.logger.warning(f"Cannot generate images - OpenAI client not available")
            if existing_images:
                self.logger.info(f"Using all {len(existing_images)} existing images")
                return existing_images
            return []
        
        # Generate additional images
        new_images = self.generate_images(story_title, story_content, images_needed)
        
        # Combine existing and new images
        all_images = existing_images + new_images
        
        # Shuffle for random order
        import random
        random.shuffle(all_images)
        
        self.logger.info(f"Total images available: {len(all_images)} ({len(existing_images)} existing + {len(new_images)} generated)")
        return all_images[:required_count] if len(all_images) >= required_count else all_images
    
    def cleanup_cache(self, max_age_days: int = 30):
        """
        Clean up old cached images and cache entries.
        
        Args:
            max_age_days: Maximum age for cached images in days
        """
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=max_age_days)
            
            removed_count = 0
            for cache_key, cache_entry in list(self.cache_data["generated_images"].items()):
                try:
                    generated_at = datetime.fromisoformat(cache_entry["generated_at"])
                    if generated_at < cutoff_date:
                        # Remove file if it exists
                        file_path = Path(cache_entry["file_path"])
                        if file_path.exists():
                            file_path.unlink()
                        
                        # Remove from cache
                        del self.cache_data["generated_images"][cache_key]
                        removed_count += 1
                        
                except Exception as e:
                    self.logger.warning(f"Error cleaning cache entry {cache_key}: {e}")
            
            if removed_count > 0:
                self.cache_data["metadata"]["total_images"] = len(self.cache_data["generated_images"])
                self._save_cache()
                self.logger.info(f"Cleaned up {removed_count} old cached images")
                
        except Exception as e:
            self.logger.error(f"Error during cache cleanup: {e}")
