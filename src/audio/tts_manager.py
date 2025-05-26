"""
Text-to-Speech Manager

This module handles converting text to speech using various TTS providers
including Google TTS, OpenAI TTS, and Azure Speech Services.
"""

import logging
import os
from pathlib import Path
from typing import Optional
import hashlib
from datetime import datetime

# TTS providers
from gtts import gTTS
import pygame

# Optional advanced TTS (install separately if needed)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import azure.cognitiveservices.speech as speechsdk
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

from ..utils.config_manager import ConfigManager


class TTSManager:
    """
    Manages text-to-speech conversion using multiple providers.
    
    Supports Google TTS (free), OpenAI TTS (paid), and Azure Speech Services (paid).
    """
    
    def __init__(self, config: ConfigManager):
        """
        Initialize the TTS manager.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        self.provider = config.get("tts.provider", "gtts")
        self.output_dir = Path(config.get("output.directory", "assets/output"))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize provider-specific settings
        self._initialize_provider()
        
        self.logger.info(f"TTS Manager initialized with provider: {self.provider}")
    
    def _initialize_provider(self):
        """Initialize the selected TTS provider."""
        if self.provider == "openai" and not OPENAI_AVAILABLE:
            self.logger.warning("OpenAI not available, falling back to gTTS")
            self.provider = "gtts"
        
        if self.provider == "azure" and not AZURE_AVAILABLE:
            self.logger.warning("Azure Speech not available, falling back to gTTS")
            self.provider = "gtts"
        
        # Initialize provider-specific clients
        if self.provider == "openai" and OPENAI_AVAILABLE:
            self._initialize_openai()
        elif self.provider == "azure" and AZURE_AVAILABLE:
            self._initialize_azure()
    
    def _initialize_openai(self):
        """Initialize OpenAI TTS client."""
        if not OPENAI_AVAILABLE:
            self.logger.error("OpenAI library not available")
            self.provider = "gtts"
            return
            
        try:
            import openai as openai_client
            openai_client.api_key = self.config.get_env("OPENAI_API_KEY")
            self.openai_client = openai_client
            self.openai_model = self.config.get("tts.openai.model", "tts-1")
            self.openai_voice = self.config.get("tts.openai.voice", "onyx")
            self.logger.info("OpenAI TTS client initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize OpenAI TTS: {e}")
            self.provider = "gtts"
    
    def _initialize_azure(self):
        """Initialize Azure Speech Services client."""
        if not AZURE_AVAILABLE:
            self.logger.error("Azure Speech SDK not available")
            self.provider = "gtts"
            return
            
        try:
            import azure.cognitiveservices.speech as speechsdk_client
            speech_key = self.config.get_env("AZURE_SPEECH_KEY")
            speech_region = self.config.get_env("AZURE_SPEECH_REGION")
            
            self.azure_config = speechsdk_client.SpeechConfig(
                subscription=speech_key,
                region=speech_region
            )
            
            self.azure_voice = self.config.get("tts.azure.voice", "en-US-AriaNeural")
            self.azure_config.speech_synthesis_voice_name = self.azure_voice
            self.speechsdk_client = speechsdk_client
            
            self.logger.info("Azure Speech Services initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize Azure Speech: {e}")
            self.provider = "gtts"
    
    def text_to_speech(self, text: str, title: Optional[str] = None) -> Optional[str]:
        """
        Convert text to speech using the configured provider.
        
        Args:
            text: Text content to convert
            title: Optional title for filename generation
            
        Returns:
            Path to generated audio file, or None if failed
        """
        try:
            # Generate filename
            filename = self._generate_filename(text, title)
            output_path = self.output_dir / f"{filename}.mp3"
            
            # Check if file already exists (caching)
            if output_path.exists():
                self.logger.info(f"Using cached TTS file: {output_path}")
                return str(output_path)
            
            # Generate speech based on provider
            if self.provider == "gtts":
                return self._gtts_generate(text, output_path)
            elif self.provider == "openai":
                return self._openai_generate(text, output_path)
            elif self.provider == "azure":
                return self._azure_generate(text, output_path)
            else:
                self.logger.error(f"Unknown TTS provider: {self.provider}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error in text_to_speech: {e}")
            return None
    
    def _gtts_generate(self, text: str, output_path: Path) -> Optional[str]:
        """
        Generate speech using Google TTS.
        
        Args:
            text: Text to convert
            output_path: Output file path
            
        Returns:
            Path to generated file or None if failed
        """
        try:
            language = self.config.get("tts.language", "en")
            slow = self.config.get("tts.slow", False)
            
            tts = gTTS(text=text, lang=language, slow=slow)
            tts.save(str(output_path))
            
            self.logger.info(f"Generated gTTS audio: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"gTTS generation failed: {e}")
            return None
    
    def _openai_generate(self, text: str, output_path: Path) -> Optional[str]:
        """
        Generate speech using OpenAI TTS.
        
        Args:
            text: Text to convert
            output_path: Output file path
            
        Returns:
            Path to generated file or None if failed
        """
        if not OPENAI_AVAILABLE or not hasattr(self, 'openai_client'):
            return None
            
        try:
            response = self.openai_client.audio.speech.create(
                model=self.openai_model,
                voice=self.openai_voice,
                input=text
            )
            
            response.stream_to_file(str(output_path))
            
            self.logger.info(f"Generated OpenAI TTS audio: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"OpenAI TTS generation failed: {e}")
            return None
    
    def _azure_generate(self, text: str, output_path: Path) -> Optional[str]:
        """
        Generate speech using Azure Speech Services.
        
        Args:
            text: Text to convert
            output_path: Output file path
            
        Returns:
            Path to generated file or None if failed
        """
        if not AZURE_AVAILABLE or not hasattr(self, 'speechsdk_client'):
            return None
            
        try:
            audio_config = self.speechsdk_client.audio.AudioOutputConfig(filename=str(output_path))
            synthesizer = self.speechsdk_client.SpeechSynthesizer(
                speech_config=self.azure_config,
                audio_config=audio_config
            )
            
            result = synthesizer.speak_text_async(text).get()
            
            if result and hasattr(result, 'reason') and result.reason == self.speechsdk_client.ResultReason.SynthesizingAudioCompleted:
                self.logger.info(f"Generated Azure TTS audio: {output_path}")
                return str(output_path)
            else:
                reason = result.reason if result and hasattr(result, 'reason') else "Unknown error"
                self.logger.error(f"Azure TTS failed: {reason}")
                return None
                
        except Exception as e:
            self.logger.error(f"Azure TTS generation failed: {e}")
            return None
    
    def _generate_filename(self, text: str, title: Optional[str] = None) -> str:
        """
        Generate a filename for the audio file.
        
        Args:
            text: Text content (used for hashing)
            title: Optional title
            
        Returns:
            Generated filename (without extension)
        """
        # Use title if provided, otherwise use text hash
        if title:
            # Clean title for filename
            clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            clean_title = clean_title.replace(' ', '_')[:50]  # Limit length
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"{clean_title}_{timestamp}"
        else:
            # Use hash of text content
            text_hash = hashlib.md5(text.encode()).hexdigest()[:12]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"story_{text_hash}_{timestamp}"
    
    def get_available_providers(self) -> list:
        """
        Get list of available TTS providers.
        
        Returns:
            List of available provider names
        """
        providers = ["gtts"]
        
        if OPENAI_AVAILABLE and self.config.get_env("OPENAI_API_KEY"):
            providers.append("openai")
            
        if AZURE_AVAILABLE and self.config.get_env("AZURE_SPEECH_KEY"):
            providers.append("azure")
        
        return providers
