"""
Reddit Scraper Module

This module handles scraping creepypasta stories from Reddit using the PRAW library.
It filters stories based on flair tags and processes them for the TTS pipeline.
"""

import logging
import time
from typing import List, Dict, Optional
import praw
from datetime import datetime

from ..utils.config_manager import ConfigManager


class RedditScraper:
    """
    Handles scraping creepypasta stories from Reddit.
    
    Uses PRAW (Python Reddit API Wrapper) to fetch stories from r/creepypasta
    with specific flair filters.
    """
    
    def __init__(self, config: ConfigManager):
        """
        Initialize the Reddit scraper.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize Reddit instance
        self.reddit = self._initialize_reddit()
        
        # Get configuration values
        self.subreddit_name = config.get("reddit.subreddit", "creepypasta")
        self.allowed_flairs = config.get("reddit.allowed_flairs", ["Text Story", "Very Short Story"])
        self.sort_by = config.get("reddit.sort_by", "hot")
        self.time_filter = config.get("reddit.time_filter", "week")
        
        self.logger.info(f"Reddit scraper initialized for r/{self.subreddit_name}")
    
    def _initialize_reddit(self) -> praw.Reddit:
        """
        Initialize the Reddit API connection.
        
        Returns:
            Configured Reddit instance
            
        Raises:
            Exception: If Reddit credentials are missing or invalid
        """
        try:
            reddit = praw.Reddit(
                client_id=self.config.get_env("REDDIT_CLIENT_ID"),
                client_secret=self.config.get_env("REDDIT_CLIENT_SECRET"),
                user_agent=self.config.get_env("REDDIT_USER_AGENT", "CreepyPastaAI/1.0")
            )
            
            # Test the connection
            reddit.user.me()
            self.logger.info("Reddit API connection established successfully")
            return reddit
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Reddit API: {e}")
            raise
    
    def scrape_stories(self, limit: int = 25) -> List[Dict]:
        """
        Scrape creepypasta stories from Reddit.
        
        Args:
            limit: Maximum number of stories to fetch
            
        Returns:
            List of story dictionaries containing metadata and content
        """
        try:
            subreddit = self.reddit.subreddit(self.subreddit_name)
            stories = []
            
            self.logger.info(f"Fetching stories from r/{self.subreddit_name} (limit: {limit})")
            
            # Get submissions based on sort method
            if self.sort_by == "hot":
                submissions = subreddit.hot(limit=limit * 3)  # Fetch more to account for filtering
            elif self.sort_by == "new":
                submissions = subreddit.new(limit=limit * 3)
            elif self.sort_by == "top":
                submissions = subreddit.top(time_filter=self.time_filter, limit=limit * 3)
            elif self.sort_by == "rising":
                submissions = subreddit.rising(limit=limit * 3)
            else:
                submissions = subreddit.hot(limit=limit * 3)
            
            processed_count = 0
            
            for submission in submissions:
                if processed_count >= limit:
                    break
                
                # Check if submission meets our criteria
                if self._is_valid_story(submission):
                    story = self._extract_story_data(submission)
                    if story:
                        stories.append(story)
                        processed_count += 1
                        self.logger.debug(f"Added story: {story['title'][:50]}...")
                
                # Add small delay to be respectful to Reddit's API
                time.sleep(0.1)
            
            self.logger.info(f"Successfully scraped {len(stories)} valid stories")
            return stories
            
        except Exception as e:
            self.logger.error(f"Error scraping stories: {e}")
            return []
    
    def _is_valid_story(self, submission) -> bool:
        """
        Check if a Reddit submission is a valid creepypasta story.
        
        Args:
            submission: Reddit submission object
            
        Returns:
            True if the submission meets our criteria
        """
        # Check if it's a text post
        if not submission.is_self:
            return False
        
        # Check flair
        if submission.link_flair_text not in self.allowed_flairs:
            return False
        
        # Check if it has content
        if not submission.selftext or len(submission.selftext.strip()) < 100:
            return False
        
        # Check if it's not deleted or removed
        if submission.selftext in ["[deleted]", "[removed]"]:
            return False
        
        return True
    
    def _extract_story_data(self, submission) -> Optional[Dict]:
        """
        Extract story data from a Reddit submission.
        
        Args:
            submission: Reddit submission object
            
        Returns:
            Dictionary containing story data, or None if extraction failed
        """
        try:
            story = {
                "id": submission.id,
                "title": submission.title,
                "content": submission.selftext,
                "author": str(submission.author) if submission.author else "Unknown",
                "score": submission.score,
                "upvote_ratio": submission.upvote_ratio,
                "num_comments": submission.num_comments,
                "created_utc": submission.created_utc,
                "created_datetime": datetime.fromtimestamp(submission.created_utc),
                "flair": submission.link_flair_text,
                "url": submission.url,
                "permalink": f"https://reddit.com{submission.permalink}",
                "is_nsfw": submission.over_18,
                "is_spoiler": submission.spoiler
            }
            
            return story
            
        except Exception as e:
            self.logger.error(f"Error extracting story data: {e}")
            return None
    
    def get_story_by_id(self, story_id: str) -> Optional[Dict]:
        """
        Get a specific story by its Reddit ID.
        
        Args:
            story_id: Reddit submission ID
            
        Returns:
            Story dictionary or None if not found
        """
        try:
            submission = self.reddit.submission(id=story_id)
            
            if self._is_valid_story(submission):
                return self._extract_story_data(submission)
            else:
                self.logger.warning(f"Story {story_id} does not meet criteria")
                return None
                
        except Exception as e:
            self.logger.error(f"Error fetching story {story_id}: {e}")
            return None
