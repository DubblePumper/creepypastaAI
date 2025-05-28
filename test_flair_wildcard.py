#!/usr/bin/env python3
"""
Test script to verify that the '*' wildcard in allowed_flairs works correctly.
This script tests the flair filtering logic without actually connecting to Reddit.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.config_manager import ConfigManager


class MockSubmission:
    """Mock submission object for testing."""
    
    def __init__(self, flair_text, is_self=True, selftext="A good story content"):
        self.link_flair_text = flair_text
        self.is_self = is_self
        self.selftext = selftext


class MockRedditScraper:
    """Mock Reddit scraper for testing flair logic."""
    
    def __init__(self, allowed_flairs):
        self.allowed_flairs = allowed_flairs
    
    def _is_valid_story_flair_check(self, submission) -> bool:
        """Test the flair checking logic only."""
        # Check flair (allow all flairs if '*' is in allowed_flairs)
        if "*" not in self.allowed_flairs:
            # Handle posts with no flair (None) vs posts with specific flairs
            post_flair = submission.link_flair_text
            if post_flair not in self.allowed_flairs:
                return False
        return True


def test_flair_wildcard():
    """Test the wildcard flair functionality."""
    
    print("Testing flair wildcard functionality...")
    print("=" * 50)
    
    # Test cases: different flair configurations
    test_cases = [
        {
            "name": "Wildcard - Accept All",
            "config": ["*"],
            "test_flairs": ["Text Story", "Very Short Story", None, "Random Flair", ""],
            "expected_results": [True, True, True, True, True]
        },
        {
            "name": "Specific Flairs Only",
            "config": ["Text Story", "Very Short Story"],
            "test_flairs": ["Text Story", "Very Short Story", None, "Random Flair", ""],
            "expected_results": [True, True, False, False, False]
        },
        {
            "name": "Include None in specific list",
            "config": ["Text Story", None],
            "test_flairs": ["Text Story", "Very Short Story", None, "Random Flair", ""],
            "expected_results": [True, False, True, False, False]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n--- {test_case['name']} ---")
        print(f"Allowed flairs: {test_case['config']}")
        
        scraper = MockRedditScraper(test_case['config'])
        
        for i, flair in enumerate(test_case['test_flairs']):
            submission = MockSubmission(flair)
            result = scraper._is_valid_story_flair_check(submission)
            expected = test_case['expected_results'][i]
            
            status = "✓" if result == expected else "✗"
            flair_display = f"'{flair}'" if flair is not None else "None"
            print(f"  {status} Flair {flair_display}: {result} (expected {expected})")
            
            if result != expected:
                print(f"    ERROR: Expected {expected}, got {result}")


def test_current_config():
    """Test with the current settings.yaml configuration."""
    print("\n" + "=" * 50)
    print("Testing with current settings.yaml configuration...")
    
    try:
        config = ConfigManager()
        allowed_flairs = config.get("reddit.allowed_flairs", ["Text Story", "Very Short Story"])
        print(f"Current allowed_flairs from config: {allowed_flairs}")
        
        scraper = MockRedditScraper(allowed_flairs)
        
        # Test common scenarios
        test_flairs = [
            "Text Story", 
            "Very Short Story", 
            None, 
            "Random Flair",
            "",
            "Long Story",
            "Horror"
        ]
        
        print("\nTesting with current configuration:")
        for flair in test_flairs:
            submission = MockSubmission(flair)
            result = scraper._is_valid_story_flair_check(submission)
            flair_display = f"'{flair}'" if flair is not None else "None"
            status = "ACCEPTED" if result else "REJECTED"
            print(f"  Flair {flair_display}: {status}")
    
    except Exception as e:
        print(f"Error loading config: {e}")


if __name__ == "__main__":
    test_flair_wildcard()
    test_current_config()
    print("\n" + "=" * 50)
    print("Flair wildcard testing completed!")
