"""
Logger Configuration Module

This module provides centralized logging configuration for the CreepyPasta AI application.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

try:
    import colorlog
    COLORLOG_AVAILABLE = True
except ImportError:
    colorlog = None
    COLORLOG_AVAILABLE = False


def setup_logger(name: str, level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with both console and file output.
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Set level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
      # Create formatters
    if COLORLOG_AVAILABLE and colorlog is not None:
        console_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
    else:
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_level)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger or create a new one with default settings.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    
    # If logger has no handlers, set it up with defaults
    if not logger.handlers:
        return setup_logger(name)
    
    return logger


def set_log_level(logger_name: str, level: str):
    """
    Set the log level for a specific logger.
    
    Args:
        logger_name: Name of the logger
        level: New log level
    """
    logger = logging.getLogger(logger_name)
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Update handler levels too
    for handler in logger.handlers:
        handler.setLevel(log_level)
