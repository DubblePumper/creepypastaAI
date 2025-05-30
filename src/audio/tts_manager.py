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
        
        # Multilingual support
        self.current_language = config.get("tts.language", "en")
        self.multilingual_enabled = config.get("multilingual.enabled", False)
        
        # Initialize provider-specific settings
        self._initialize_provider()
        
        self.logger.info(f"TTS Manager initialized with provider: {self.provider}")
        if self.multilingual_enabled:
            self.logger.info(f"Multilingual support enabled, current language: {self.current_language}")
    
    def set_language(self, language_code: str):
        """
        Set the current language for TTS generation.
        
        Args:
            language_code: Language code (e.g., 'en', 'es', 'fr')
        """
        if not self.multilingual_enabled:
            self.logger.warning("Multilingual support is disabled")
            return
        
        # Check if language is supported
        languages = self.config.get("multilingual.languages", {})
        if language_code not in languages:
            self.logger.error(f"Language {language_code} is not supported")
            return
        
        self.current_language = language_code
        self.logger.info(f"Language set to: {language_code}")
    
    def _get_language_voice_config(self, language_code: Optional[str] = None) -> dict:
        """
        Get voice configuration for a specific language.
        
        Args:
            language_code: Language code (uses current language if None)
            
        Returns:
            Voice configuration dictionary
        """
        if language_code is None:
            language_code = self.current_language
        
        if not self.multilingual_enabled:
            # Return default voice configuration
            return {
                "gtts_lang": self.config.get("tts.language", "en"),
                "openai_voice": self.config.get("tts.openai.voice", "onyx"),
                "azure_voice": self.config.get("tts.azure.voice", "en-US-AriaNeural"),
                "elevenlabs_voice": self.config.get("tts.elevenlabs.voice", "3SF4rB1fGBMXU9xRM7pz")
            }
        
        # Get language-specific configuration
        languages = self.config.get("multilingual.languages", {})
        lang_config = languages.get(language_code, {})
        
        if not lang_config:
            self.logger.warning(f"No configuration found for language {language_code}, using defaults")
            lang_config = languages.get("en", {})
        
        return {
            "gtts_lang": lang_config.get("gtts_lang", "en"),
            "openai_voice": lang_config.get("openai_voice", "onyx"),
            "azure_voice": lang_config.get("azure_voice", "en-US-AriaNeural"),
            "elevenlabs_voice": lang_config.get("elevenlabs_voice", "3SF4rB1fGBMXU9xRM7pz")
        }
    
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
            openai_key = self.config.get_env("OPENAI_API_KEY")
            if not openai_key:
                self.logger.error("OpenAI API key not found in environment variables")
                self.provider = "gtts"
                return
                
            import openai
            self.openai_client = openai.OpenAI(api_key=openai_key)
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
            speech_key = self.config.get_env("AZURE_SPEECH_KEY")
            speech_region = self.config.get_env("AZURE_SPEECH_REGION")
            
            if not speech_key or not speech_region:
                self.logger.error("Azure Speech key or region not found in environment variables")
                self.provider = "gtts"
                return
            
            import azure.cognitiveservices.speech as speechsdk
            self.azure_config = speechsdk.SpeechConfig(
                subscription=speech_key,
                region=speech_region
            )
            
            self.azure_voice = self.config.get("tts.azure.voice", "en-US-AriaNeural")
            self.azure_config.speech_synthesis_voice_name = self.azure_voice
            self.speechsdk = speechsdk
            
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
    
    def text_to_speech(self, text: str, title: Optional[str] = None, language: Optional[str] = None) -> Optional[str]:
        """
        Convert text to speech using the configured provider with automatic fallback.
        
        Args:
            text: Text content to convert
            title: Optional title for filename generation
            language: Language code for TTS (uses current language if None)
            
        Returns:
            Path to generated audio file, or None if failed
        """
        # Use provided language or current language
        if language:
            voice_config = self._get_language_voice_config(language)
        else:
            voice_config = self._get_language_voice_config()
            language = self.current_language
        
        # Generate filename and output_path before try block to ensure it is always defined
        safe_language = language if language is not None else self.current_language
        filename = self._generate_filename(text, title, safe_language)
        output_path = self.output_dir / f"{filename}.mp3"
        try:
            # Check if file already exists (caching)
            if output_path.exists():
                self.logger.info(f"Using cached TTS file: {output_path}")
                return str(output_path)
            
            # Try primary provider first
            result = None
            if self.provider == "gtts":
                result = self._gtts_generate(text, output_path, voice_config)
            elif self.provider == "openai":
                result = self._openai_generate(text, output_path, voice_config)
                # If OpenAI fails, automatically fallback to gTTS
                if result is None:
                    self.logger.warning("OpenAI TTS failed, falling back to gTTS")
                    result = self._gtts_generate(text, output_path, voice_config)
            elif self.provider == "azure":
                result = self._azure_generate(text, output_path, voice_config)
                # If Azure fails, automatically fallback to gTTS
                if result is None:
                    self.logger.warning("Azure TTS failed, falling back to gTTS")
                    result = self._gtts_generate(text, output_path, voice_config)
            elif self.provider == "elevenlabs":
                result = self._elevenlabs_generate(text, output_path, voice_config)
                # If ElevenLabs fails, automatically fallback to gTTS
                if result is None:
                    self.logger.warning("ElevenLabs TTS failed, falling back to gTTS")
                    result = self._gtts_generate(text, output_path, voice_config)
            else:
                self.logger.error(f"Unknown TTS provider: {self.provider}, using gTTS")
                result = self._gtts_generate(text, output_path, voice_config)
            
            return result
                
        except Exception as e:
            self.logger.error(f"Error in text_to_speech: {e}")
            # Last resort: try gTTS if not already tried
            if self.provider != "gtts":
                try:
                    self.logger.warning("Attempting final fallback to gTTS")
                    return self._gtts_generate(text, output_path, voice_config)
                except Exception as fallback_error:
                    self.logger.error(f"Fallback to gTTS also failed: {fallback_error}")
            return None
    def _gtts_generate(self, text: str, output_path: Path, voice_config: Optional[dict] = None) -> Optional[str]:
        """
        Generate speech using Google TTS.
        
        Args:
            text: Text to convert
            output_path: Output file path
            voice_config: Language-specific voice configuration
            
        Returns:
            Path to generated file or None if failed
        """
        try:
            if voice_config:
                language = voice_config.get("gtts_lang", "en")
            else:
                language = self.config.get("tts.language", "en")
            
            slow = self.config.get("tts.slow", False)
            
            tts = gTTS(text=text, lang=language, slow=slow)
            tts.save(str(output_path))
            
            self.logger.info(f"Generated gTTS audio: {output_path} (language: {language})")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"gTTS generation failed: {e}")
            return None
    def _openai_generate(self, text: str, output_path: Path, voice_config: dict = {}) -> Optional[str]:
        """
        Generate speech using OpenAI TTS.
        
        Args:
            text: Text to convert
            output_path: Output file path
            voice_config: Language-specific voice configuration
            
        Returns:
            Path to generated file or None if failed
        """
        if not OPENAI_AVAILABLE or not hasattr(self, 'openai_client'):
            return None
            
        try:
            # Use voice from config or fallback to default
            voice = voice_config.get("openai_voice", self.openai_voice) if voice_config else self.openai_voice
            
            response = self.openai_client.audio.speech.create(
                model=self.openai_model,
                voice=voice,
                input=text
            )
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            self.logger.info(f"Generated OpenAI TTS audio: {output_path} (voice: {voice})")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"OpenAI TTS generation failed: {e}")           
            return None
    
    def _azure_generate(self, text: str, output_path: Path, voice_config: dict = {}) -> Optional[str]:
        """
        Generate speech using Azure Speech Services.
        
        Args:
            text: Text to convert
            output_path: Output file path
            voice_config: Language-specific voice configuration
            
        Returns:
            Path to generated file or None if failed
        """
        if not AZURE_AVAILABLE or not hasattr(self, 'speechsdk'):
            return None
            
        try:
            # Use voice from config or fallback to default
            voice = voice_config.get("azure_voice", self.azure_voice) if voice_config else self.azure_voice
            
            # Create a new config with the appropriate voice
            azure_config = self.speechsdk.SpeechConfig(
                subscription=self.config.get_env("AZURE_SPEECH_KEY"),
                region=self.config.get_env("AZURE_SPEECH_REGION")
            )
            azure_config.speech_synthesis_voice_name = voice
            
            audio_config = self.speechsdk.audio.AudioOutputConfig(filename=str(output_path))
            synthesizer = self.speechsdk.SpeechSynthesizer(
                speech_config=azure_config,
                audio_config=audio_config
            )
            
            result = synthesizer.speak_text_async(text).get()
            
            if result and hasattr(result, 'reason') and result.reason == self.speechsdk.ResultReason.SynthesizingAudioCompleted:
                self.logger.info(f"Generated Azure TTS audio: {output_path} (voice: {voice})")
                return str(output_path)
            else:
                reason = result.reason if result and hasattr(result, 'reason') else "Unknown error"
                self.logger.error(f"Azure TTS failed: {reason}")
                return None
                
        except Exception as e:
            self.logger.error(f"Azure TTS generation failed: {e}")
            return None
    def _elevenlabs_generate(self, text: str, output_path: Path, voice_config: dict = {}) -> Optional[str]:
        """
        Generate speech using ElevenLabs TTS.
        
        Args:
            text: Text to convert
            output_path: Output file path
            voice_config: Language-specific voice configuration
            
        Returns:
            Path to generated file or None if failed
        """
        if not ELEVENLABS_AVAILABLE or not hasattr(self, 'elevenlabs_client') or Voice is None or VoiceSettings is None:
            self.logger.warning("ElevenLabs client not available")
            return None
            
        try:
            # Check if text exceeds ElevenLabs character limit (10,000 characters)
            max_chunk_size = 9500  # Leave some buffer for safety
            if len(text) > max_chunk_size:
                self.logger.info(f"Text length ({len(text)} chars) exceeds ElevenLabs limit. Splitting into chunks...")
                return self._elevenlabs_generate_chunked(text, output_path, voice_config)
            
            # Use voice from config or fallback to default
            voice_id = voice_config.get("elevenlabs_voice", self.elevenlabs_voice_id) if voice_config else self.elevenlabs_voice_id
            
            # Create voice settings (only if VoiceSettings is available)
            voice_settings = None
            if VoiceSettings is not None:
                voice_settings = VoiceSettings(
                    stability=self.elevenlabs_stability,
                    similarity_boost=self.elevenlabs_similarity_boost,
                    style=self.elevenlabs_style,
                    use_speaker_boost=self.elevenlabs_use_speaker_boost
                )
              # Try to use a simple approach that should work with most ElevenLabs versions
            # Note: The exact API may vary depending on elevenlabs package version
            audio = None
              # Try common API patterns
            try:
                # Try newer SDK pattern first
                if hasattr(self.elevenlabs_client, 'text_to_speech'):
                    # Call with explicit parameters to avoid type issues
                    if voice_settings is not None:
                        audio = self.elevenlabs_client.text_to_speech.convert(
                            text=text,
                            voice_id=voice_id,
                            voice_settings=voice_settings
                        )
                    else:
                        audio = self.elevenlabs_client.text_to_speech.convert(
                            text=text,
                            voice_id=voice_id
                        )
                elif hasattr(self.elevenlabs_client, 'generate'):
                    # Use getattr to avoid linter complaints about unknown method
                    generate_method = getattr(self.elevenlabs_client, 'generate')
                    if generate_method is not None:
                        audio = generate_method(
                            text=text,
                            voice=voice_id
                        )
                    else:
                        raise AttributeError("Generate method is None")
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
            
            self.logger.info(f"Generated ElevenLabs TTS audio: {output_path} (voice: {voice_id})")
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
    
    def _generate_filename(self, text: str, title: Optional[str] = None, language: Optional[str] = None) -> str:
        """
        Generate a filename for the audio file.
        
        Args:
            text: Text content (used for hashing)
            title: Optional title
            language: Language code for the audio
            
        Returns:
            Generated filename (without extension)
        """
        # Language prefix
        lang_prefix = f"{language}_" if language and language != "en" else ""
        
        # Use title if provided, otherwise use text hash
        if title:
            # Clean title for filename
            clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            clean_title = clean_title.replace(' ', '_')[:50]  # Limit length
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"{lang_prefix}{clean_title}_{timestamp}"
        else:
            # Use hash of text content
            text_hash = hashlib.md5(text.encode()).hexdigest()[:12]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"{lang_prefix}story_{text_hash}_{timestamp}"
    
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
    
    def _elevenlabs_generate_chunked(self, text: str, output_path: Path, voice_config: dict = {}) -> Optional[str]:
        """
        Generate speech for long text by splitting into chunks and combining the audio.
        """
        try:
            # Split text into chunks
            chunks = self._split_text_into_chunks(text, max_size=9500)
            self.logger.info(f"Split text into {len(chunks)} chunks for ElevenLabs processing")
              # Use voice from config or fallback to default
            voice_id = voice_config.get("elevenlabs_voice", self.elevenlabs_voice_id) if voice_config else self.elevenlabs_voice_id
            
            # Create voice settings (only if VoiceSettings is available)
            voice_settings = None
            if VoiceSettings is not None:
                voice_settings = VoiceSettings(
                    stability=self.elevenlabs_stability,
                    similarity_boost=self.elevenlabs_similarity_boost,
                    style=self.elevenlabs_style,
                    use_speaker_boost=self.elevenlabs_use_speaker_boost
                )
              # Generate audio for each chunk
            chunk_files = []
            for i, chunk in enumerate(chunks):
                # Create chunk file path by modifying the filename before the extension
                chunk_filename = f"{output_path.stem}_chunk_{i}.mp3"
                chunk_path = output_path.parent / chunk_filename
                result = self._elevenlabs_generate_single_chunk(chunk, chunk_path, voice_id, voice_settings)
                if result:
                    chunk_files.append(result)
                else:
                    # If any chunk fails, clean up and return None
                    self._cleanup_temp_files(chunk_files)
                    return None
            
            # Combine all chunk files into final audio
            final_result = self._combine_audio_files(chunk_files, output_path)
            
            # Clean up temporary chunk files
            self._cleanup_temp_files(chunk_files)
            
            return final_result
            
        except Exception as e:
            self.logger.error(f"ElevenLabs chunked generation failed: {e}")
            return None
    
    def _elevenlabs_generate_single_chunk(self, text: str, output_path: Path, voice_id: str, voice_settings) -> Optional[str]:
        """
        Generate speech for a single text chunk using ElevenLabs TTS.
        """
        try:            # Try to use a simple approach that should work with most ElevenLabs versions
            audio = None
            
            # Try common API patterns
            try:                # Try newer SDK pattern first
                if hasattr(self.elevenlabs_client, 'text_to_speech'):
                    # Call with explicit parameters to avoid type issues
                    if voice_settings is not None:
                        audio = self.elevenlabs_client.text_to_speech.convert(
                            text=text,
                            voice_id=voice_id,
                            voice_settings=voice_settings
                        )
                    else:
                        audio = self.elevenlabs_client.text_to_speech.convert(
                            text=text,
                            voice_id=voice_id
                        )
                elif hasattr(self.elevenlabs_client, 'generate'):
                    # Use getattr to avoid linter complaints about unknown method
                    generate_method = getattr(self.elevenlabs_client, 'generate')
                    audio = generate_method(
                        text=text,
                        voice=voice_id
                    )
                else:
                    raise AttributeError("No suitable ElevenLabs API method found")
                    
            except Exception as api_error:
                self.logger.error(f"ElevenLabs API call failed: {api_error}")
                return None
            
            if not audio:
                self.logger.error("ElevenLabs returned no audio data")
                return None
            
            # Save audio to file
            with open(output_path, 'wb') as f:
                for chunk in audio:
                    f.write(chunk)
            
            self.logger.debug(f"Generated ElevenLabs chunk: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"ElevenLabs single chunk generation failed: {e}")
            return None
    
    def _split_text_into_chunks(self, text: str, max_size: int = 9500) -> list:
        """
        Split text into chunks at sentence boundaries to stay under character limit.
        """
        import re
        
        # Split by sentences (periods, exclamation marks, question marks)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Check if adding this sentence would exceed the limit
            if len(current_chunk) + len(sentence) + 1 > max_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    # Single sentence is too long, split by words
                    words = sentence.split()
                    word_chunk = ""
                    for word in words:
                        if len(word_chunk) + len(word) + 1 > max_size:
                            if word_chunk:
                                chunks.append(word_chunk.strip())
                                word_chunk = word
                            else:
                                # Single word is too long, just add it
                                chunks.append(word)
                        else:
                            word_chunk += " " + word if word_chunk else word
                    if word_chunk:
                        current_chunk = word_chunk
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _combine_audio_files(self, audio_files: list, output_path: Path) -> Optional[str]:
        """
        Combine multiple audio files into a single file using pydub.
        """
        try:
            from pydub import AudioSegment
            
            combined = AudioSegment.empty()
            
            for audio_file in audio_files:
                segment = AudioSegment.from_mp3(audio_file)
                combined += segment
            
            # Export combined audio
            combined.export(str(output_path), format="mp3")
            self.logger.info(f"Combined {len(audio_files)} audio chunks into: {output_path}")
            
            return str(output_path)
            
        except ImportError:
            self.logger.error("pydub not available for audio combining. Install with: pip install pydub")
            return None
        except Exception as e:
            self.logger.error(f"Failed to combine audio files: {e}")
            return None
    
    def _cleanup_temp_files(self, file_paths: list):
        """
        Clean up temporary audio chunk files.
        """
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except Exception as e:
                self.logger.warning(f"Failed to clean up temp file {file_path}: {e}")
