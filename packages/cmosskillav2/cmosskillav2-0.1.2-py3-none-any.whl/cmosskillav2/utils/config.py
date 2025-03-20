"""
Configuration utilities for the CMosSkillAV2 terminal.
"""

import os
import json


class ConfigManager:
    """
    Manages configuration settings for the CMosSkillAV2 terminal.
    """
    
    def __init__(self):
        """Initialize the configuration manager with default settings."""
        self.config_dir = os.path.expanduser("~/.cmosskillav2")
        self.config_file = os.path.join(self.config_dir, "config.json")
        
        # Default configuration
        self.default_config = {
            'prompt_style': 'default',
            'history_size': 1000,
            'show_hidden_files': False,
            'theme': 'default',
            'tab_completion': True,
            'auto_suggest': True,
        }
        
        # Current configuration (loaded from file or defaults)
        self.config = self.load_config()
    
    def load_config(self):
        """
        Load configuration from file, or create with defaults if not exists.
        
        Returns:
            dict: The configuration dictionary.
        """
        # Create config directory if it doesn't exist
        if not os.path.exists(self.config_dir):
            try:
                os.makedirs(self.config_dir)
            except Exception as e:
                print(f"Error creating config directory: {e}")
                return self.default_config.copy()
        
        # Load config file if it exists
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                
                # Merge with defaults (to ensure all keys exist)
                config = self.default_config.copy()
                config.update(loaded_config)
                return config
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.default_config.copy()
        else:
            # Create config file with defaults
            config = self.default_config.copy()
            self.save_config(config)
            return config
    
    def save_config(self, config=None):
        """
        Save configuration to file.
        
        Args:
            config (dict, optional): Configuration to save. If None, uses the current config.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """
        Get a configuration value.
        
        Args:
            key (str): Configuration key.
            default: Value to return if key not found.
            
        Returns:
            The configuration value or default.
        """
        return self.config.get(key, default)
    
    def set(self, key, value):
        """
        Set a configuration value and save to file.
        
        Args:
            key (str): Configuration key.
            value: Value to set.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        self.config[key] = value
        return self.save_config()