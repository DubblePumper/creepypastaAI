# filepath: c:\Users\sande\Documents\GitHub\creepypastaAI\src\audio\tts_manager.py
"""
Text-to-Speech Manager

This module handles converting text to speech using various TTS providers
including Google TTS, OpenAI TTS, Azure Speech Services, and ElevenLabs TTS.
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

try:
    from elevenlabs import ElevenLabs, Voice, VoiceSettings
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ElevenLabs = None
    Voice = None
    VoiceSettings = None
    ELEVENLABS_AVAILABLE = False

from ..utils.config_manager import ConfigManager


class TTSManager:
    """
    Manages text-to-speech conversion using multiple providers.
    
    Supports Google TTS (free), OpenAI TTS (paid), Azure Speech Services (paid),
    and ElevenLabs TTS (paid).
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
        
        if self.provider == "elevenlabs" and not ELEVENLABS_AVAILABLE:
            self.logger.warning("ElevenLabs not available, falling back to gTTS")
            self.provider = "gtts"
        
        # Initialize provider-specific clients
        if self.provider == "openai" and OPENAI_AVAILABLE:
            self._initialize_openai()
        elif self.provider == "azure" and AZURE_AVAILABLE:
            self._initialize_azure()
        elif self.provider == "elevenlabs" and ELEVENLABS_AVAILABLE:
            self._initialize_elevenlabs()
    
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
    
    def _initialize_elevenlabs(self):
        """Initialize ElevenLabs TTS client."""
        if not ELEVENLABS_AVAILABLE or ElevenLabs is None:
            self.logger.error("ElevenLabs library not available")
            self.provider = "gtts"
            return
            
        try:
            api_key = self.config.get_env("ELEVENLABS_API_KEY")
            if not api_key or api_key == "your_elevenlabs_api_key_here":
                self.logger.error("ElevenLabs API key not configured")
                self.provider = "gtts"
                return
                
            # Initialize ElevenLabs client
            self.elevenlabs_client = ElevenLabs(api_key=api_key)
            
            # Get configuration settings
            self.elevenlabs_model = self.config.get("tts.elevenlabs.model", "eleven_monolingual_v1")
            self.elevenlabs_voice_id = self.config.get("tts.elevenlabs.voice", "21m00Tcm4TlvDq8ikWAM")
            self.elevenlabs_stability = self.config.get("tts.elevenlabs.stability", 0.75)
            self.elevenlabs_similarity_boost = self.config.get("tts.elevenlabs.similarity_boost", 0.5)
            self.elevenlabs_style = self.config.get("tts.elevenlabs.style", 0.0)
            self.elevenlabs_use_speaker_boost = self.config.get("tts.elevenlabs.use_speaker_boost", True)
            
            self.logger.info(f"ElevenLabs TTS client initialized with voice: {self.elevenlabs_voice_id}")
        except Exception as e:
            self.logger.error(f"Failed to initialize ElevenLabs TTS: {e}")
            self.provider = "gtts"
    
    def text_to_speech(self, text: str, title: Optional[str] = None) -> Optional[str]:
        """
        Convert text to speech using the configured provider with automatic fallback.
        
        Args:
            text: Text content to convert
            title: Optional title for filename generation
            
        Returns:
            Path to generated audio file, or None if failed
        """
        # Generate filename and output_path before try block to ensure it is always defined
        filename = self._generate_filename(text, title)
        output_path = self.output_dir / f"{filename}.mp3"
        try:
            # Check if file already exists (caching)
            if output_path.exists():
                self.logger.info(f"Using cached TTS file: {output_path}")
                return str(output_path)
            
            # Try primary provider first
            result = None
            if self.provider == "gtts":
                result = self._gtts_generate(text, output_path)
            elif self.provider == "openai":
                result = self._openai_generate(text, output_path)
                # If OpenAI fails, automatically fallback to gTTS
                if result is None:
                    self.logger.warning("OpenAI TTS failed, falling back to gTTS")
                    result = self._gtts_generate(text, output_path)
            elif self.provider == "azure":
                result = self._azure_generate(text, output_path)
                # If Azure fails, automatically fallback to gTTS
                if result is None:
                    self.logger.warning("Azure TTS failed, falling back to gTTS")
                    result = self._gtts_generate(text, output_path)
            elif self.provider == "elevenlabs":
                result = self._elevenlabs_generate(text, output_path)
                # If ElevenLabs fails, automatically fallback to gTTS
                if result is None:
                    self.logger.warning("ElevenLabs TTS failed, falling back to gTTS")
                    result = self._gtts_generate(text, output_path)
            else:
                self.logger.error(f"Unknown TTS provider: {self.provider}, using gTTS")
                result = self._gtts_generate(text, output_path)
            
            return result
                
        except Exception as e:
            self.logger.error(f"Error in text_to_speech: {e}")
            # Last resort: try gTTS if not already tried
            if self.provider != "gtts":
                try:
                    self.logger.warning("Attempting final fallback to gTTS")
                    return self._gtts_generate(text, output_path)
                except Exception as fallback_error:
                    self.logger.error(f"Fallback to gTTS also failed: {fallback_error}")
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
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
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
    
    def _elevenlabs_generate(self, text: str, output_path: Path) -> Optional[str]:
        """
        Generate speech using ElevenLabs TTS.
        
        Args:
            text: Text to convert
            output_path: Output file path
            
        Returns:
            Path to generated file or None if failed
        """
        if not ELEVENLABS_AVAILABLE or not hasattr(self, 'elevenlabs_client') or Voice is None or VoiceSettings is None:
            self.logger.warning("ElevenLabs client not available")
            return None
            
        try:
            # Create voice settings
            voice_settings = VoiceSettings(
                stability=self.elevenlabs_stability,
                similarity_boost=self.elevenlabs_similarity_boost,
                style=self.elevenlabs_style,
                use_speaker_boost=self.elevenlabs_use_speaker_boost            )            # Try to use a simple approach that should work with most ElevenLabs versions
            # Note: The exact API may vary depending on elevenlabs package version
            audio = None
            
            # Try common API patterns
            try:
                # Try newer SDK pattern first
                if hasattr(self.elevenlabs_client, 'text_to_speech'):
                    audio = self.elevenlabs_client.text_to_speech.convert(
                        text=text,
                        voice_id=self.elevenlabs_voice_id,
                        voice_settings=voice_settings
                    )
                elif hasattr(self.elevenlabs_client, 'generate'):
                    # Use getattr to avoid linter complaints about unknown method
                    generate_method = getattr(self.elevenlabs_client, 'generate')
                    audio = generate_method(
                        text=text,
                        voice=self.elevenlabs_voice_id
                    )
                else:
                    raise AttributeError("No suitable ElevenLabs API method found")
                    
            except Exception as api_error:
                # For now, log the error and fall back to other TTS providers
                self.logger.error(f"ElevenLabs API call failed: {api_error}")
                self.logger.info("ElevenLabs TTS not working - check API version compatibility")
                return None
            
            if not audio:
                self.logger.error("ElevenLabs returned no audio data")
                return None
            
            # Save audio to file
            with open(output_path, 'wb') as f:
                for chunk in audio:
                    f.write(chunk)
            
            self.logger.info(f"Generated ElevenLabs TTS audio: {output_path}")
            return str(output_path)
            
        except Exception as e:
            error_msg = str(e).lower()
            if "quota" in error_msg or "limit" in error_msg:
                self.logger.warning(f"ElevenLabs TTS quota/limit exceeded: {e}")
            elif "unauthorized" in error_msg or "401" in error_msg:
                self.logger.error(f"ElevenLabs TTS authentication failed: {e}")
            elif "payment" in error_msg or "402" in error_msg:
                self.logger.error(f"ElevenLabs TTS payment required: {e}")
            else:
                self.logger.error(f"ElevenLabs TTS generation failed: {e}")
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
            
        if ELEVENLABS_AVAILABLE and ElevenLabs is not None and self.config.get_env("ELEVENLABS_API_KEY"):
            providers.append("elevenlabs")
        
        return providers
