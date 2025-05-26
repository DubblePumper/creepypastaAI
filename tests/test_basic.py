"""
Basic tests for CreepyPasta AI components
"""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path for imports
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.utils.config_manager import ConfigManager
from src.utils.story_processor import StoryProcessor


class TestConfigManager:
    """Test the configuration manager."""
    
    def test_init_with_missing_file(self):
        """Test initialization with missing config file."""
        config = ConfigManager("nonexistent.yaml")
        assert config.config == {}
    
    def test_get_with_dot_notation(self):
        """Test getting values with dot notation."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
reddit:
  subreddit: "test"
  limit: 10
""")
            f.flush()
            
            config = ConfigManager(f.name)
            assert config.get("reddit.subreddit") == "test"
            assert config.get("reddit.limit") == 10
            assert config.get("nonexistent.key", "default") == "default"
            
            os.unlink(f.name)
    
    def test_env_variables(self):
        """Test environment variable access."""
        config = ConfigManager()
        
        # Test with mock environment variable
        with patch.dict(os.environ, {'TEST_VAR': 'test_value'}):
            assert config.get_env('TEST_VAR') == 'test_value'
            assert config.get_env('MISSING_VAR', 'default') == 'default'


class TestStoryProcessor:
    """Test the story processor."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = ConfigManager()
        self.processor = StoryProcessor(self.config)
    
    def test_clean_markdown(self):
        """Test markdown removal."""
        text = "# Header\n**Bold text** and *italic text*\n`code` and [link](url)"
        cleaned = self.processor._remove_markdown(text)
        
        assert "Header" in cleaned
        assert "Bold text" in cleaned
        assert "italic text" in cleaned
        assert "**" not in cleaned
        assert "*" not in cleaned
        assert "`" not in cleaned
        assert "[" not in cleaned
        assert "]" not in cleaned
    
    def test_content_length_validation(self):
        """Test content length validation."""
        short_text = "Too short"
        long_text = "Valid length content " * 10
        very_long_text = "X" * 10000
        
        assert not self.processor._validate_length(short_text)
        assert self.processor._validate_length(long_text)
        assert not self.processor._validate_length(very_long_text)
    
    def test_story_processing(self):
        """Test complete story processing."""
        raw_story = {
            'title': '**Scary Story**',
            'content': '# The Horror\n\nThis is a **scary** story with `code` and [links](url).\n\nIt has multiple paragraphs and should be processed correctly.',
            'author': 'test_author'
        }
        
        processed = self.processor.process_story(raw_story)
        
        assert processed is not None
        assert 'word_count' in processed
        assert 'character_count' in processed
        assert 'estimated_duration' in processed
        assert processed['title'] == 'Scary Story'
        assert '**' not in processed['content']
        assert 'scary' in processed['content']
    
    def test_duration_estimation(self):
        """Test reading duration estimation."""
        text = "This is a test story. " * 50  # ~150 words
        duration = self.processor._estimate_duration(text)
        
        # Should be around 60 seconds (150 words / 2.5 words per second)
        assert 50 < duration < 80


if __name__ == "__main__":
    pytest.main([__file__])
