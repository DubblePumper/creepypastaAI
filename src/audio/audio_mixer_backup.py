"""
Audio Mixer Module

This module handles mixing narration with background music and atmospheric effects
to create immersive creepypasta audio experiences.
"""

import logging
import os
import random
from pathlib import Path
from typing import Optional, List
import pygame
from pydub import AudioSegment
from pydub.effects import normalize, low_pass_filter
from pydub.playback import play

from ..utils.config_manager import ConfigManager


class AudioMixer:
    """
    Handles audio mixing, effects, and atmospheric enhancements.
    
    Combines narration with background music, applies effects,
    and creates immersive audio experiences.
    """
    
    def __init__(self, config: ConfigManager):
        """
        Initialize the audio mixer.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        self.output_dir = Path(config.get("output.directory", "assets/output"))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.music_dir = Path("assets/music")
        self.music_dir.mkdir(parents=True, exist_ok=True)
        
        # Audio settings
        self.narration_volume = config.get("audio.volume.narration", 0.8)
        self.music_volume = config.get("audio.volume.background_music", 0.3)
        self.fade_in_duration = config.get("audio.background_music.fade_in_duration", 2.0)
        self.fade_out_duration = config.get("audio.background_music.fade_out_duration", 2.0)
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
        self.logger.info("Audio mixer initialized")
    
    def create_atmospheric_mix(self, narration_file: str, title: str, 
                             story_metadata: Optional[dict] = None) -> Optional[str]:
        """
        Create an atmospheric audio mix with narration and background music.
        
        Args:
            narration_file: Path to the narration audio file
            title: Story title for output filename
            story_metadata: Optional story metadata for effect selection
            
        Returns:
            Path to the mixed audio file, or None if failed
        """
        try:
            self.logger.info(f"Creating atmospheric mix for: {title}")
            
            # Load narration audio
            narration = AudioSegment.from_file(narration_file)
            
            # Apply narration effects
            narration = self._apply_narration_effects(narration)
            
            # Create or load background music
            background_music = self._get_background_music(narration.duration_seconds)
            
            if background_music and self.config.get("audio.background_music.enabled", True):
                # Mix narration with background music
                mixed_audio = self._mix_audio(narration, background_music)
            else:
                mixed_audio = narration
            
            # Apply final effects
            mixed_audio = self._apply_final_effects(mixed_audio)
            
            # Generate output filename
            output_filename = self._generate_output_filename(title)
            output_path = self.output_dir / output_filename
            
            # Export the final mix
            mixed_audio.export(
                str(output_path),
                format="mp3",
                bitrate="192k",
                tags={
                    "title": title,
                    "artist": "CreepyPasta AI",
                    "album": "AI Generated Creepypasta",
                    "genre": "Horror"
                }
            )
            
            self.logger.info(f"Mixed audio saved: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Error creating atmospheric mix: {e}")
            return None
    
    def _apply_narration_effects(self, narration: AudioSegment) -> AudioSegment:
        """
        Apply effects to enhance the narration.
        
        Args:
            narration: Original narration audio
            
        Returns:
            Processed narration audio
        """
        try:
            # Normalize audio levels
            narration = normalize(narration)
            
            # Adjust volume
            narration = narration + (20 * (self.narration_volume - 1))  # Convert to dB
            
            # Optional: Add slight reverb effect (using echo)
            if self.config.get("audio.effects.reverb", False):
                echo = narration - 20  # Quieter echo
                delayed_echo = AudioSegment.silent(duration=200) + echo  # 200ms delay
                narration = narration.overlay(delayed_echo)
            
            # Optional: Add low-pass filter for warmth
            if self.config.get("audio.effects.warm_filter", True):
                narration = low_pass_filter(narration, 8000)
            
            return narration
            
        except Exception as e:
            self.logger.error(f"Error applying narration effects: {e}")
            return narration
    
    def _get_background_music(self, duration_seconds: float) -> Optional[AudioSegment]:
        """
        Get or generate background music for the given duration.
        
        Args:
            duration_seconds: Required duration in seconds
            
        Returns:
            Background music audio segment, or None if not available
        """
        try:
            # Look for existing music files
            music_files = list(self.music_dir.glob("*.mp3")) + list(self.music_dir.glob("*.wav"))
            
            if not music_files:
                self.logger.info("No background music files found, creating default ambient track")
                return self._generate_ambient_background(duration_seconds)
            
            # Select a random music file
            selected_music = random.choice(music_files)
            self.logger.info(f"Using background music: {selected_music.name}")
            
            music = AudioSegment.from_file(str(selected_music))
            
            # Adjust music to match narration duration
            music = self._adjust_music_duration(music, duration_seconds)
            
            # Apply music effects
            music = self._apply_music_effects(music)
            
            return music
            
        except Exception as e:
            self.logger.error(f"Error loading background music: {e}")
            return None
    
    def _generate_ambient_background(self, duration_seconds: float) -> AudioSegment:
        """
        Generate a simple ambient background track.
        
        Args:
            duration_seconds: Required duration
            
        Returns:
            Generated ambient audio
        """
        try:
            # Create a very simple ambient track using sine waves
            # This is a basic implementation - you might want to use more sophisticated generation
            
            duration_ms = int(duration_seconds * 1000)
            
            # Generate low-frequency ambient sound
            from pydub.generators import Sine
            
            ambient = AudioSegment.silent(duration=duration_ms)
            
            # Add multiple low-frequency tones for depth
            frequencies = [40, 55, 80, 110]  # Low frequencies for ambiance
            
            for freq in frequencies:
                tone = Sine(freq).to_audio_segment(duration=duration_ms)
                tone = tone - 30  # Make it very quiet
                ambient = ambient.overlay(tone)
            
            # Add some variation with volume modulation
            ambient = self._add_volume_modulation(ambient)
            self.logger.info("Generated ambient background track")
            return ambient
            
        except Exception as e:
            self.logger.error(f"Error generating ambient background: {e}")
            return AudioSegment.silent(duration=int(duration_seconds * 1000))
    
    def _adjust_music_duration(self, music: AudioSegment, target_duration: float) -> AudioSegment:
        """
        Adjust music duration to match the target duration.

        Args:
            music: Original music audio
            target_duration: Target duration in seconds

        Returns:
            Adjusted music audio
        """
        target_ms = int(target_duration * 1000)
        current_ms = len(music)
        if current_ms < target_ms:
            # Loop the music if it's shorter than needed
            loops_needed = (target_ms // current_ms) + 1
            music = music * loops_needed
        
        # Trim to exact duration
        if len(music) > target_ms:
            music = music[:target_ms]
        
        # Add fade in/out
        fade_in_ms = int(self.fade_in_duration * 1000)
        fade_out_ms = int(self.fade_out_duration * 1000)
        
        music = music.fade_in(fade_in_ms).fade_out(fade_out_ms)
        
        return music
    
    def _apply_music_effects(self, music: AudioSegment) -> AudioSegment:
        """
        Apply effects to background music.
        
        Args:
            music: Original music audio
            
        Returns:
            Processed music audio
        """
        try:
            # Adjust volume
            music = music + (20 * (self.music_volume - 1))  # Convert to dB
            
            # Apply low-pass filter to make music less intrusive
            music = low_pass_filter(music, 4000)
            
            # Optional: Add stereo width effect
            if len(music.get_array_of_samples()) > 1:  # Stereo
                # Simple stereo width adjustment could be added here
                pass
            
            except Exception as e:
            self.logger.error(f"Error applying music effects: {e}")
            return music
    
    def _add_volume_modulation(self, audio: AudioSegment) -> AudioSegment:
        """
        Add subtle volume modulation to create movement in ambient sounds.
        
        Args:
            audio: Original audio
            
        Returns:
            Modulated audio
        """
        try:
            # This is a simplified implementation
            # In a real application, you might use more sophisticated modulation
            
            # Split audio into chunks and apply slight volume variations
            chunk_size = 5000  # 5 seconds
            modulated = AudioSegment.empty()
            
            for i in range(0, len(audio), chunk_size):
                chunk = audio[i:i + chunk_size]
                # Random volume variation between -3dB and +1dB
                volume_change = random.uniform(-3, 1)
                if len(chunk) > 0:  # Only process non-empty chunks
                    chunk = chunk + volume_change
                    modulated += chunk
            
            return modulated
            
        except Exception as e:
            self.logger.error(f"Error adding volume modulation: {e}")
            return audio
    
    def _mix_audio(self, narration: AudioSegment, background: AudioSegment) -> AudioSegment:
        """
        Mix narration with background music.
        
        Args:
            narration: Narration audio
            background: Background music audio
            
        Returns:
            Mixed audio
        """
        try:
            # Ensure both audio segments are the same length
            max_length = max(len(narration), len(background))
            
            if len(narration) < max_length:
                narration = narration + AudioSegment.silent(duration=max_length - len(narration))
            
            if len(background) < max_length:
                background = background + AudioSegment.silent(duration=max_length - len(background))
            
            # Mix the audio
            mixed = narration.overlay(background)
            
            return mixed
            
        except Exception as e:
            self.logger.error(f"Error mixing audio: {e}")
            return narration
    
    def _apply_final_effects(self, audio: AudioSegment) -> AudioSegment:
        """
        Apply final effects to the mixed audio.
        
        Args:
            audio: Mixed audio
            
        Returns:
            Final processed audio
        """
        try:
            # Normalize the final mix
            audio = normalize(audio)
            
            # Optional: Apply compression (simplified)
            # This could be enhanced with proper audio compression algorithms
            
            # Optional: Apply final EQ
            if self.config.get("audio.effects.final_eq", False):
                # Simple high-frequency rolloff for vintage feel
                audio = low_pass_filter(audio, 12000)
            
            return audio
            
        except Exception as e:
            self.logger.error(f"Error applying final effects: {e}")
            return audio
    
    def _generate_output_filename(self, title: str) -> str:
        """
        Generate output filename for the mixed audio.
        
        Args:
            title: Story title
            
        Returns:
            Generated filename
        """
        # Clean title for filename
        clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_title = clean_title.replace(' ', '_')[:50]  # Limit length
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return f"creepypasta_{clean_title}_{timestamp}.mp3"
    
    def play_audio(self, audio_file: str) -> bool:
        """
        Play an audio file using pygame.
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            True if playback started successfully
        """
        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            self.logger.info(f"Playing audio: {audio_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error playing audio: {e}")
            return False
    
    def stop_audio(self):
        """Stop audio playback."""
        try:
            pygame.mixer.music.stop()
            self.logger.info("Audio playback stopped")
        except Exception as e:
            self.logger.error(f"Error stopping audio: {e}")
