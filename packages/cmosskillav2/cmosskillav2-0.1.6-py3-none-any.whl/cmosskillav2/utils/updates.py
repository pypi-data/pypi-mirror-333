"""
Daily updates functionality for the CMosSkillAV2 terminal.

This module provides functionality to check for and display daily updates.
"""

import os
import json
import datetime
from datetime import date
import random
import time
import sys
import importlib.metadata
from urllib.request import urlopen, Request
from urllib.error import URLError
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
        self.last_version_check = None
        self.latest_version = None
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
            "You can run system commands directly from the terminal.",
            "Use 'mkdir' followed by a name to create a new directory.",
            "The 'rm' command can remove files and directories.",
            "Use 'clear' to clean the terminal screen.",
            "Check for daily tips with the 'updates' command.",
            "Python virtual environments help isolate project dependencies.",
            "The 'touch' command creates empty files.",
            "Use 'cd ..' to navigate up one directory level.",
            "Press Tab twice to see all possible completions.",
            "Try 'py >>> print(\"Hello, World!\")' to test Python inline execution.",
            "The 'pip list' command shows all installed packages."
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
                    # Load last update date
                    last_date_str = data.get('last_update_date')
                    if last_date_str:
                        year, month, day = map(int, last_date_str.split('-'))
                        self.last_update_date = date(year, month, day)
                    
                    # Load version check information
                    self.last_version_check = data.get('last_version_check')
                    self.latest_version = data.get('latest_version')
            except (json.JSONDecodeError, ValueError, TypeError):
                # If file is corrupted, start fresh
                self.last_update_date = None
                self.last_version_check = None
                self.latest_version = None
        else:
            self.last_update_date = None
            self.last_version_check = None
            self.latest_version = None
    
    def save_update_status(self):
        """Save the update status to file."""
        data = {
            'last_update_date': self.last_update_date.isoformat() if self.last_update_date else None,
            'last_version_check': self.last_version_check,
            'latest_version': self.latest_version
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
    
    def check_for_newer_version(self, force=False):
        """
        Check if a newer version is available on PyPI.
        
        Args:
            force (bool): If True, always check regardless of last check time.
            
        Returns:
            tuple: (bool, str) - (is_newer_available, latest_version)
        """
        # Only check once per day unless forced
        current_time = time.time()
        check_interval = 24 * 60 * 60  # 24 hours
        
        if (not force and self.last_version_check and 
            current_time - self.last_version_check < check_interval):
            # Use cached version info
            if self.latest_version:
                current_version = importlib.metadata.version('cmosskillav2')
                return self.latest_version != current_version, self.latest_version
            return False, None
        
        # Get current version
        current_version = importlib.metadata.version('cmosskillav2')
        
        try:
            # Create a request with a user agent to avoid being blocked
            headers = {
                'User-Agent': f'cmosskillav2/{current_version} Python/{sys.version.split()[0]}'
            }
            req = Request('https://pypi.org/pypi/cmosskillav2/json', headers=headers)
            
            # Fetch data from PyPI
            with urlopen(req, timeout=2) as response:
                data = json.loads(response.read().decode('utf-8'))
                latest_version = data['info']['version']
                
                # Update cache
                self.last_version_check = current_time
                self.latest_version = latest_version
                self.save_update_status()
                
                return latest_version != current_version, latest_version
        except (URLError, json.JSONDecodeError, KeyError, TimeoutError) as e:
            # On error, use current version
            return False, current_version
    
    def display_daily_updates(self, force=False):
        """
        Display daily updates if available.
        
        Args:
            force (bool): If True, always show updates regardless of date.
        """
        if self.check_for_updates(force):
            date_str = self.get_date_message()
            tip = self.get_daily_tip()
            
            # Check for newer version
            has_newer, latest_version = self.check_for_newer_version(force)
            current_version = importlib.metadata.version('cmosskillav2')
            
            print(f"\n{Fore.CYAN}╔═══════════════════ Daily Update ═══════════════════╗{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.YELLOW}{date_str}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}Tip of the day:{Style.RESET_ALL} {tip}")
            
            # Display version information
            if has_newer:
                print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.MAGENTA}Version:{Style.RESET_ALL} {current_version} → {Fore.YELLOW}New version {latest_version} available!{Style.RESET_ALL}")
                print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.WHITE}Run 'pip install --upgrade cmosskillav2' to update.{Style.RESET_ALL}")
            else:
                print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.MAGENTA}Version:{Style.RESET_ALL} {current_version} (up to date)")
                
            print(f"{Fore.CYAN}╚════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")