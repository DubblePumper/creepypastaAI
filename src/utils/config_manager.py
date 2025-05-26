"""
Configuration Manager

This module handles loading and managing configuration from YAML files and environment variables.
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Any, Optional
from dotenv import load_dotenv


class ConfigManager:
    """
    Manages application configuration from YAML files and environment variables.
    
    Loads configuration from YAML files and provides access to both config
    settings and environment variables.
    """
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        """
        Initialize the configuration manager.
          Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = Path(config_path)
        self.config = {}
        
        # Initialize logger first
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Load environment variables from .env file
        load_dotenv()
        
        # Load configuration
        self._load_config()
        
        self.logger.info(f"Configuration loaded from {config_path}")
    
    def _load_config(self):
        """Load configuration from YAML file."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as file:
                    self.config = yaml.safe_load(file) or {}
            else:
                self.logger.warning(f"Config file not found: {self.config_path}")
                self.config = {}
                
        except Exception as e:
            self.logger.error(f"Error loading config file: {e}")
            self.config = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key: Configuration key (supports dot notation like 'redis.host')
            default: Default value if key is not found
            
        Returns:
            Configuration value or default
            
        Example:
            config.get('redis.host', 'localhost')
            config.get('tts.provider', 'gtts')
        """
        try:
            keys = key.split('.')
            value = self.config
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            
            return value
            
        except Exception:
            return default
    
    def get_env(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get an environment variable.
        
        Args:
            key: Environment variable name
            default: Default value if not found
            
        Returns:
            Environment variable value or default
        """
        return os.getenv(key, default)
    
    def set(self, key: str, value: Any):
        """
        Set a configuration value using dot notation.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        try:
            keys = key.split('.')
            config = self.config
            
            # Navigate to the parent dictionary
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            # Set the value
            config[keys[-1]] = value
            
        except Exception as e:
            self.logger.error(f"Error setting config value: {e}")
    
    def save(self):
        """Save current configuration to file."""
        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as file:
                yaml.dump(self.config, file, default_flow_style=False, indent=2)
            
            self.logger.info(f"Configuration saved to {self.config_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving config file: {e}")
    
    def reload(self):
        """Reload configuration from file."""
        self._load_config()
        self.logger.info("Configuration reloaded")
    
    def get_all(self) -> dict:
        """
        Get all configuration as a dictionary.
        
        Returns:
            Complete configuration dictionary
        """
        return self.config.copy()
    
    def update(self, new_config: dict):
        """
        Update configuration with new values.
        
        Args:
            new_config: Dictionary of new configuration values
        """
        def deep_update(base_dict, update_dict):
            """Recursively update nested dictionaries."""
            for key, value in update_dict.items():
                if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                    deep_update(base_dict[key], value)
                else:
                    base_dict[key] = value
        
        deep_update(self.config, new_config)
        self.logger.info("Configuration updated")
    
    def validate_required_env_vars(self, required_vars: list) -> bool:
        """
        Validate that required environment variables are set.
        
        Args:
            required_vars: List of required environment variable names
            
        Returns:
            True if all required variables are set, False otherwise
        """
        missing_vars = []
        
        for var in required_vars:
            if not self.get_env(var):
                missing_vars.append(var)
        
        if missing_vars:
            self.logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            return False
        
        return True
