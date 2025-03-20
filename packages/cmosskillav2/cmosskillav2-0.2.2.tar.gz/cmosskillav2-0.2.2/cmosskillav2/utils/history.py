"""
Command history management for the CMosSkillAV2 terminal.
"""

import os
import readline


class HistoryManager:
    """
    Manages command history including loading, saving, and navigation.
    """
    
    def __init__(self, history_size=1000):
        """
        Initialize the history manager.
        
        Args:
            history_size (int): Maximum number of history entries to keep.
        """
        self.history_size = history_size
        self.history_file = os.path.expanduser("~/.cmosskillav2_history")
        
        # Configure readline history
        readline.set_history_length(history_size)
    
    def load_history(self):
        """Load command history from file if it exists."""
        try:
            if os.path.exists(self.history_file):
                readline.read_history_file(self.history_file)
        except Exception as e:
            print(f"Error loading history: {e}")
    
    def save_history(self):
        """Save command history to file."""
        try:
            readline.write_history_file(self.history_file)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def add_to_history(self, command):
        """
        Add a command to the history.
        
        Args:
            command (str): The command to add to history.
        """
        if command and command.strip():
            # This actually adds the command to the readline history
            readline.add_history(command)
    
    def clear_history(self):
        """Clear the command history."""
        # Clear readline history
        readline.clear_history()
        
        # Remove history file
        try:
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
        except Exception as e:
            print(f"Error clearing history file: {e}")