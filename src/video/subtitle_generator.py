"""
Subtitle Generator Module

Generates synchronized subtitle files (SRT format) for video content based on
story text and audio duration. Creates properly timed subtitle segments for
better accessibility and viewer engagement.
"""

import logging
import re
from pathlib import Path
from typing import List, Optional, Tuple
from datetime import timedelta


class SubtitleGenerator:
    """
    Generates subtitle files synchronized with audio narration.
    
    Creates SRT format subtitle files with proper timing based on
    audio duration and text content segmentation.
    """
    
    def __init__(self, config=None):
        """
        Initialize the subtitle generator.
        
        Args:
            config: Configuration manager instance (optional)
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        
        # Default subtitle settings
        self.words_per_subtitle = 8
        self.max_chars_per_line = 50
        
        if config:
            self.words_per_subtitle = config.get("video.subtitles.words_per_subtitle", 8)
            self.max_chars_per_line = config.get("video.subtitles.max_chars_per_line", 50)
    
    def generate_subtitle_file(
        self, 
        text: str, 
        audio_duration: float, 
        output_path: str
    ) -> Optional[str]:
        """
        Generate an SRT subtitle file for the given text and audio duration.
        
        Args:
            text: The story text content
            audio_duration: Duration of the audio in seconds
            output_path: Path where the SRT file should be saved
            
        Returns:
            Path to the generated SRT file, or None if failed
        """
        try:
            # Clean and prepare text
            cleaned_text = self._clean_text(text)
            
            # Split text into subtitle segments
            subtitle_segments = self._split_text_into_segments(cleaned_text)
            
            if not subtitle_segments:
                self.logger.warning("No subtitle segments generated from text")
                return None
            
            # Calculate timing for each segment
            timed_segments = self._calculate_timing(subtitle_segments, audio_duration)
            
            # Generate SRT content
            srt_content = self._generate_srt_content(timed_segments)
            
            # Save to file
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            self.logger.info(f"Generated subtitle file: {output_file}")
            self.logger.info(f"Created {len(timed_segments)} subtitle segments")
            
            return str(output_file)
            
        except Exception as e:
            self.logger.error(f"Failed to generate subtitle file: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """
        Clean text content for subtitle generation.
        
        Args:
            text: Raw text content
            
        Returns:
            Cleaned text suitable for subtitles
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove formatting markers
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Italic
        text = re.sub(r'_([^_]+)_', r'\1', text)        # Underscore
        
        # Fix common issues
        text = re.sub(r'\[.*?\]', '', text)  # Remove brackets
        text = re.sub(r'\(.*?\)', '', text)  # Remove parentheses
        
        # Clean up spacing
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _split_text_into_segments(self, text: str) -> List[str]:
        """
        Split text into subtitle segments.
        
        Args:
            text: Cleaned text content
            
        Returns:
            List of subtitle segments
        """
        # Split by sentences first
        sentences = re.split(r'[.!?]+', text)
        segments = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Split long sentences into smaller segments
            words = sentence.split()
            
            # Create segments with appropriate word count
            for i in range(0, len(words), self.words_per_subtitle):
                segment_words = words[i:i + self.words_per_subtitle]
                segment_text = ' '.join(segment_words)
                
                # Break into lines if too long
                if len(segment_text) > self.max_chars_per_line:
                    lines = self._break_into_lines(segment_text)
                    segments.append('\n'.join(lines))
                else:
                    segments.append(segment_text)
        
        return [seg for seg in segments if seg.strip()]
    
    def _break_into_lines(self, text: str) -> List[str]:
        """
        Break long text into multiple lines for better readability.
        
        Args:
            text: Text to break into lines
            
        Returns:
            List of lines
        """
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= self.max_chars_per_line:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = len(word)
                else:
                    # Single word is too long, just add it
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _calculate_timing(
        self, 
        segments: List[str], 
        total_duration: float
    ) -> List[Tuple[float, float, str]]:
        """
        Calculate timing for each subtitle segment.
        
        Args:
            segments: List of subtitle text segments
            total_duration: Total audio duration in seconds
            
        Returns:
            List of tuples (start_time, end_time, text)
        """
        if not segments:
            return []
        
        # Calculate duration per segment based on text length
        total_chars = sum(len(seg) for seg in segments)
        
        timed_segments = []
        current_time = 0.0
        
        for segment in segments:
            # Calculate duration based on character count
            char_ratio = len(segment) / total_chars if total_chars > 0 else 1.0 / len(segments)
            segment_duration = total_duration * char_ratio
            
            # Ensure minimum duration of 1 second per segment
            segment_duration = max(1.0, segment_duration)
            
            start_time = current_time
            end_time = min(current_time + segment_duration, total_duration)
            
            timed_segments.append((start_time, end_time, segment))
            current_time = end_time
            
            # Stop if we've reached the total duration
            if current_time >= total_duration:
                break
        
        return timed_segments
    
    def _generate_srt_content(self, timed_segments: List[Tuple[float, float, str]]) -> str:
        """
        Generate SRT format content from timed segments.
        
        Args:
            timed_segments: List of (start_time, end_time, text) tuples
            
        Returns:
            SRT format content as string
        """
        srt_content = []
        
        for i, (start_time, end_time, text) in enumerate(timed_segments, 1):
            # Format times as SRT timestamp (HH:MM:SS,mmm)
            start_timestamp = self._seconds_to_srt_timestamp(start_time)
            end_timestamp = self._seconds_to_srt_timestamp(end_time)
            
            # Add subtitle entry
            srt_content.append(f"{i}")
            srt_content.append(f"{start_timestamp} --> {end_timestamp}")
            srt_content.append(text)
            srt_content.append("")  # Empty line between entries
        
        return '\n'.join(srt_content)
    
    def _seconds_to_srt_timestamp(self, seconds: float) -> str:
        """
        Convert seconds to SRT timestamp format.
        
        Args:
            seconds: Time in seconds
            
        Returns:
            SRT timestamp string (HH:MM:SS,mmm)
        """
        td = timedelta(seconds=seconds)
        hours, remainder = divmod(td.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds % 1) * 1000)
        
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"
    
    def get_subtitle_style_options(self) -> dict:
        """
        Get subtitle style options for FFmpeg.
        
        Returns:
            Dictionary of FFmpeg subtitle style options
        """
        if not self.config:
            return self._get_default_style_options()
        
        return {
            'FontSize': self.config.get("video.subtitles.font_size", 24),
            'PrimaryColour': self._color_to_hex(
                self.config.get("video.subtitles.font_color", "white")
            ),
            'OutlineColour': self._color_to_hex(
                self.config.get("video.subtitles.outline_color", "black")
            ),
            'Outline': self.config.get("video.subtitles.outline_width", 2),
            'Alignment': self._get_alignment_value(
                self.config.get("video.subtitles.position", "bottom")
            )
        }
    
    def _get_default_style_options(self) -> dict:
        """Get default subtitle style options."""
        return {
            'FontSize': 24,
            'PrimaryColour': '&Hffffff',  # White
            'OutlineColour': '&H000000',  # Black
            'Outline': 2,
            'Alignment': 2  # Bottom center
        }
    
    def _color_to_hex(self, color: str) -> str:
        """
        Convert color name to hex format for FFmpeg.
        
        Args:
            color: Color name (white, black, yellow, etc.)
            
        Returns:
            Hex color string for FFmpeg
        """
        color_map = {
            'white': '&Hffffff',
            'black': '&H000000',
            'red': '&H0000ff',
            'green': '&H00ff00',
            'blue': '&Hff0000',
            'yellow': '&H00ffff',
            'cyan': '&Hffff00',
            'magenta': '&Hff00ff'
        }
        
        return color_map.get(color.lower(), '&Hffffff')  # Default to white
    
    def _get_alignment_value(self, position: str) -> int:
        """
        Get FFmpeg alignment value for subtitle position.
        
        Args:
            position: Position string (bottom, top, center)
            
        Returns:
            FFmpeg alignment value
        """
        alignment_map = {
            'bottom': 2,  # Bottom center
            'top': 8,     # Top center
            'center': 5   # Middle center
        }
        
        return alignment_map.get(position.lower(), 2)  # Default to bottom
