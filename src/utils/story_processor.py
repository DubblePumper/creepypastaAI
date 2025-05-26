"""
Story Processor Module

This module handles processing and cleaning of scraped stories before TTS conversion.
"""

import logging
import re
from typing import Dict, Optional
import html
from datetime import datetime

from .config_manager import ConfigManager


class StoryProcessor:
    """
    Processes and cleans scraped stories for TTS conversion.
    
    Handles text cleaning, formatting, length validation, and content filtering.
    """
    
    def __init__(self, config: ConfigManager):
        """
        Initialize the story processor.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Get processing settings
        self.min_length = config.get("story.min_length", 100)
        self.max_length = config.get("story.max_length", 5000)
        self.clean_text = config.get("story.clean_text", True)
        self.remove_markdown = config.get("story.remove_markdown", True)
        
        self.logger.info("Story processor initialized")
    
    def process_story(self, raw_story: Dict) -> Optional[Dict]:
        """
        Process a raw story from Reddit scraper.
        
        Args:
            raw_story: Raw story dictionary from Reddit scraper
            
        Returns:
            Processed story dictionary, or None if story doesn't meet criteria
        """
        try:
            # Create processed story dict
            processed_story = raw_story.copy()
            
            # Clean and process the content
            content = self._clean_content(raw_story["content"])
            
            if not content:
                self.logger.debug(f"Story '{raw_story['title']}' has no valid content after cleaning")
                return None
            
            # Validate length
            if not self._validate_length(content):
                self.logger.debug(f"Story '{raw_story['title']}' doesn't meet length requirements")
                return None
            
            # Update processed story
            processed_story["content"] = content
            processed_story["original_content"] = raw_story["content"]
            processed_story["word_count"] = len(content.split())
            processed_story["character_count"] = len(content)
            processed_story["estimated_duration"] = self._estimate_duration(content)
            processed_story["processed_at"] = datetime.now().isoformat()
            
            # Clean title
            processed_story["title"] = self._clean_title(raw_story["title"])
            
            self.logger.debug(f"Successfully processed story: {processed_story['title']}")
            return processed_story
            
        except Exception as e:
            self.logger.error(f"Error processing story '{raw_story.get('title', 'Unknown')}': {e}")
            return None
    
    def _clean_content(self, content: str) -> str:
        """
        Clean and format story content for TTS.
        
        Args:
            content: Raw story content
            
        Returns:
            Cleaned content
        """
        if not content:
            return ""
        
        # Decode HTML entities
        content = html.unescape(content)
        
        # Remove markdown formatting if enabled
        if self.remove_markdown:
            content = self._remove_markdown(content)
        
        # Clean text if enabled
        if self.clean_text:
            content = self._clean_text_content(content)
        
        # Final cleanup
        content = self._final_cleanup(content)
        
        return content.strip()
    
    def _remove_markdown(self, text: str) -> str:
        """
        Remove common markdown formatting.
        
        Args:
            text: Text with markdown
            
        Returns:
            Text without markdown
        """
        # Remove headers
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        
        # Remove bold and italic
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Italic
        text = re.sub(r'__([^_]+)__', r'\1', text)      # Bold alt
        text = re.sub(r'_([^_]+)_', r'\1', text)        # Italic alt
        
        # Remove strikethrough
        text = re.sub(r'~~([^~]+)~~', r'\1', text)
        
        # Remove code blocks and inline code
        text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        
        # Remove links but keep text
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove quotes
        text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)
        
        # Remove horizontal rules
        text = re.sub(r'^-{3,}$', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\*{3,}$', '', text, flags=re.MULTILINE)
        
        return text
    
    def _clean_text_content(self, text: str) -> str:
        """
        Clean text content for better TTS pronunciation.
        
        Args:
            text: Raw text content
            
        Returns:
            Cleaned text
        """
        # Fix common Reddit artifacts
        text = re.sub(r'\[removed\]', '', text)
        text = re.sub(r'\[deleted\]', '', text)
        text = re.sub(r'EDIT:', 'Edit:', text)
        text = re.sub(r'UPDATE:', 'Update:', text)
        
        # Fix spacing around punctuation
        text = re.sub(r'\s+([.!?])', r'\1', text)
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        
        # Fix multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Fix line breaks
        text = re.sub(r'\n+', '\n\n', text)
        
        # Remove excessive punctuation
        text = re.sub(r'[!]{3,}', '!', text)
        text = re.sub(r'[?]{3,}', '?', text)
        text = re.sub(r'[.]{4,}', '...', text)
        
        # Fix common abbreviations for TTS
        abbreviations = {
            r'\bdr\b': 'doctor',
            r'\bmr\b': 'mister',
            r'\bmrs\b': 'missus',
            r'\bms\b': 'miss',
            r'\bst\b': 'saint',
            r'\betc\b': 'etcetera',
            r'\bi\.e\b': 'that is',
            r'\be\.g\b': 'for example',
            r'\bvs\b': 'versus',
            r'\bw\/': 'with',
            r'\bw\/o': 'without',
            r'\bu\b': 'you',
            r'\bur\b': 'your',
            r'\btho\b': 'though',
            r'\bthru\b': 'through'
        }
        
        for abbr, expansion in abbreviations.items():
            text = re.sub(abbr, expansion, text, flags=re.IGNORECASE)
        
        return text
    
    def _final_cleanup(self, text: str) -> str:
        """
        Perform final cleanup on the text.
        
        Args:
            text: Text to clean up
            
        Returns:
            Final cleaned text
        """
        # Remove empty lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n\n'.join(lines)
        
        # Ensure sentences end with proper punctuation for TTS pauses
        text = re.sub(r'([a-zA-Z0-9])\s*\n\n', r'\1. ', text)
        
        # Fix sentence spacing
        text = re.sub(r'([.!?])\s*\n\n', r'\1 ', text)
        
        # Remove any remaining multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def _clean_title(self, title: str) -> str:
        """
        Clean story title.
        
        Args:
            title: Raw title
            
        Returns:
            Cleaned title
        """
        # Remove common prefixes/suffixes
        title = re.sub(r'^\[.*?\]\s*', '', title)  # Remove tags like [Short Story]
        title = re.sub(r'\s*\(.*?\)$', '', title)  # Remove ending parentheses
        
        # Remove markdown
        title = re.sub(r'\*\*([^*]+)\*\*', r'\1', title)
        title = re.sub(r'\*([^*]+)\*', r'\1', title)
        
        # Clean up spacing
        title = re.sub(r'\s+', ' ', title).strip()
        
        return title
    
    def _validate_length(self, content: str) -> bool:
        """
        Validate story length.
        
        Args:
            content: Story content
            
        Returns:
            True if length is within acceptable range
        """
        char_count = len(content)
        return self.min_length <= char_count <= self.max_length
    
    def _estimate_duration(self, content: str) -> float:
        """
        Estimate reading duration in seconds.
        
        Args:
            content: Story content
            
        Returns:
            Estimated duration in seconds
        """
        # Average reading speed: 200 words per minute
        # Average speaking speed: 150 words per minute for TTS
        word_count = len(content.split())
        words_per_second = 150 / 60  # 2.5 words per second
        
        return word_count / words_per_second
    
    def get_content_stats(self, content: str) -> Dict:
        """
        Get statistics about the content.
        
        Args:
            content: Story content
            
        Returns:
            Dictionary with content statistics
        """
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        return {
            "character_count": len(content),
            "word_count": len(words),
            "sentence_count": len([s for s in sentences if s.strip()]),
            "paragraph_count": len(paragraphs),
            "estimated_duration": self._estimate_duration(content),
            "average_word_length": sum(len(word) for word in words) / len(words) if words else 0,
            "reading_level": self._estimate_reading_level(content)
        }
    
    def _estimate_reading_level(self, content: str) -> str:
        """
        Estimate reading difficulty level.
        
        Args:
            content: Story content
            
        Returns:
            Reading level estimate
        """
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not words or not sentences:
            return "Unknown"
        
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Simple heuristic
        if avg_sentence_length < 15 and avg_word_length < 5:
            return "Easy"
        elif avg_sentence_length < 25 and avg_word_length < 6:
            return "Medium"
        else:
            return "Advanced"
