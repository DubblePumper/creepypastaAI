"""
Command Line Interface Handler for CreepyPasta AI

This module provides command-line interface functionality for running
different components of the CreepyPasta AI application independently.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from src.utils.logger import setup_logger


class CLIHandler:
    """
    Handles command-line interface for CreepyPasta AI application.
    
    Allows users to run different components independently:
    - Scraping only
    - Audio generation only  
    - Video generation only
    - Complete workflow
    """
    
    def __init__(self):
        """Initialize the CLI handler."""
        self.logger = setup_logger("CLIHandler", "INFO")
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create the argument parser for the CLI.
        
        Returns:
            Configured ArgumentParser instance
        """
        parser = argparse.ArgumentParser(
            description="CreepyPasta AI - Generate atmospheric horror content",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Run complete workflow for 5 stories
  python main.py --stories 5
  
  # Scrape stories only
  python main.py --mode scrape --stories 10
  
  # Generate audio for existing stories only
  python main.py --mode audio
  
  # Generate videos for existing audio files only
  python main.py --mode video
  
  # Display system information
  python main.py --info
  
  # Display tracking statistics
  python main.py --stats
            """
        )
        
        # Mode selection
        parser.add_argument(
            "--mode", "-m",
            choices=["complete", "scrape", "audio", "video"],
            default="complete",
            help="Execution mode: complete workflow, scraping only, audio only, or video only (default: complete)"
        )
        
        # Number of stories
        parser.add_argument(
            "--stories", "-s",
            type=int,
            help="Number of stories to process (for scraping mode or complete workflow)"
        )
        
        # Configuration file
        parser.add_argument(
            "--config", "-c",
            type=str,
            default="config/settings.yaml",
            help="Path to configuration file (default: config/settings.yaml)"
        )
        
        # System information
        parser.add_argument(
            "--info", "-i",
            action="store_true",
            help="Display system information and exit"
        )
        
        # Statistics
        parser.add_argument(
            "--stats",
            action="store_true",
            help="Display tracking statistics and exit"
        )
        
        # Video generation options
        parser.add_argument(
            "--video-all",
            action="store_true",
            help="Generate videos for all existing audio files (only for video mode)"
        )
        
        # Verbose output
        parser.add_argument(
            "--verbose", "-v",
            action="store_true",
            help="Enable verbose output"
        )
        
        # Force regeneration
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force regeneration of existing files"
        )
        
        return parser
    
    def parse_args(self, args: Optional[list] = None) -> argparse.Namespace:
        """
        Parse command line arguments.
        
        Args:
            args: List of arguments to parse (uses sys.argv if None)
            
        Returns:
            Parsed arguments namespace
        """
        return self.parser.parse_args(args)
    
    def validate_args(self, args: argparse.Namespace) -> bool:
        """
        Validate parsed arguments.
        
        Args:
            args: Parsed arguments namespace
            
        Returns:
            True if arguments are valid, False otherwise
        """
        try:
            # Check if config file exists
            config_path = Path(args.config)
            if not config_path.exists():
                self.logger.error(f"Configuration file not found: {args.config}")
                return False
            
            # Validate stories count
            if args.stories is not None and args.stories <= 0:
                self.logger.error("Number of stories must be greater than 0")
                return False
            
            # Check mode-specific requirements
            if args.mode == "scrape" and args.stories is None:
                self.logger.warning("No story count specified for scraping mode, will use config default")
            
            if args.video_all and args.mode != "video":
                self.logger.warning("--video-all flag is only relevant for video mode")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating arguments: {e}")
            return False
    
    def display_help(self):
        """Display help message."""
        self.parser.print_help()
    
    def display_banner(self):
        """Display application banner."""
        banner = """
        ╔══════════════════════════════════════════════╗
        ║              CreepyPasta AI                  ║
        ║      Horror Story Audio & Video Generator    ║
        ╚══════════════════════════════════════════════╝
        """
        print(banner)
