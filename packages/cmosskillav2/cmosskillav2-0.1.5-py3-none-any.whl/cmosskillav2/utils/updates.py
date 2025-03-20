"""
Daily updates functionality for the CMosSkillAV2 terminal.

This module provides functionality to check for and display daily updates.
"""

import os
import json
import datetime
from datetime import date
import random
from colorama import Fore, Style

class UpdateManager:
    """
    Manages daily updates and tips for the terminal.
    """
    
    def __init__(self):
        """Initialize the update manager."""
        self.config_dir = os.path.expanduser("~/.cmosskillav2")
        self.updates_file = os.path.join(self.config_dir, "updates.json")
        self.last_update_date = None
        self.tips = [
            "Use the 'py >>>' command to quickly execute Python code inline.",
            "The 'pyshell' command starts an interactive Python shell.",
            "Use tab completion to quickly enter commands and file paths.",
            "The 'pip' command allows you to manage Python packages.",
            "Use the 'help' command followed by a command name to get specific help.",
            "The 'cat' command shows file contents with syntax highlighting for code files.",
            "Press Ctrl+D or type 'exit' to exit the terminal.",
            "Use the up and down arrow keys to navigate command history.",
            "The 'ls' command shows directories and files in different colors.",
            "You can run system commands directly from the terminal."
        ]
        self.load_update_status()
    
    def load_update_status(self):
        """Load the update status from file."""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir, exist_ok=True)
        
        if os.path.exists(self.updates_file):
            try:
                with open(self.updates_file, 'r') as f:
                    data = json.load(f)
                    last_date_str = data.get('last_update_date')
                    if last_date_str:
                        year, month, day = map(int, last_date_str.split('-'))
                        self.last_update_date = date(year, month, day)
            except (json.JSONDecodeError, ValueError, TypeError):
                # If file is corrupted, start fresh
                self.last_update_date = None
        else:
            self.last_update_date = None
    
    def save_update_status(self):
        """Save the update status to file."""
        data = {
            'last_update_date': self.last_update_date.isoformat() if self.last_update_date else None
        }
        
        with open(self.updates_file, 'w') as f:
            json.dump(data, f)
    
    def check_for_updates(self, force=False):
        """
        Check if there are new updates to display.
        
        Args:
            force (bool): If True, always show updates regardless of date.
            
        Returns:
            bool: True if updates should be displayed, False otherwise.
        """
        today = date.today()
        
        if force or self.last_update_date is None or today > self.last_update_date:
            self.last_update_date = today
            self.save_update_status()
            return True
        
        return False
    
    def get_daily_tip(self):
        """
        Get a random tip for the day.
        
        Returns:
            str: A tip message.
        """
        # Use the current date as a seed to ensure the same tip is shown all day
        today = date.today()
        random.seed(f"{today.year}-{today.month}-{today.day}")
        tip = random.choice(self.tips)
        random.seed()  # Reset the seed
        
        return tip
    
    def get_date_message(self):
        """
        Get a formatted date message.
        
        Returns:
            str: The formatted date message.
        """
        today = date.today()
        return today.strftime("%A, %B %d, %Y")
    
    def display_daily_updates(self, force=False):
        """
        Display daily updates if available.
        
        Args:
            force (bool): If True, always show updates regardless of date.
        """
        if self.check_for_updates(force):
            date_str = self.get_date_message()
            tip = self.get_daily_tip()
            
            print(f"\n{Fore.CYAN}╔═══════════════════ Daily Update ═══════════════════╗{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.YELLOW}{date_str}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}Tip of the day:{Style.RESET_ALL} {tip}")
            print(f"{Fore.CYAN}╚════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")