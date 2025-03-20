"""
Core terminal emulator implementation for CMosSkillAV2.
"""

import os
import readline
import shlex
import subprocess
import sys
from colorama import Fore, Back, Style, init

from .utils.color import highlight_command
from .utils.help import show_help
from .utils.completion import CMosSkillCompleter
from .utils.history import HistoryManager
from .utils.updates import UpdateManager
from .commands.file_operations import cd_command, ls_command, mkdir_command, touch_command, rm_command, cat_command
from .commands.python_execution import execute_python_script, execute_python_inline, InteractivePythonShell
from .commands.package_management import pip_command


class CMosSkillShell:
    """
    Interactive shell for CMosSkillAV2 with command handling and user interface.
    """
    
    def __init__(self):
        """Initialize the CMosSkillAV2 shell with all necessary components."""
        # Initialize colorama
        init(autoreset=True)
        
        # Set up command history
        self.history_manager = HistoryManager()
        self.history_manager.load_history()
        
        # Set up tab completion
        self.completer = CMosSkillCompleter()
        readline.set_completer(self.completer.complete)
        readline.parse_and_bind("tab: complete")
        
        # Set up daily updates
        self.update_manager = UpdateManager()
        
        # Command dictionary maps command names to their handler functions
        self.commands = {
            # File operations
            'cd': cd_command,
            'ls': ls_command,
            'mkdir': mkdir_command,
            'touch': touch_command,
            'rm': rm_command,
            'cat': cat_command,
            
            # Python execution
            'python': execute_python_script,
            'py': execute_python_inline,
            'pyshell': self.start_python_shell,
            
            # Package management
            'pip': pip_command,
            
            # Shell built-ins
            'help': self.show_help,
            'exit': self.exit_shell,
            'quit': self.exit_shell,
            'clear': self.clear_screen,
            'updates': self.check_updates,
        }
    
    def print_welcome(self):
        """Display a welcome message when the shell starts."""
        print("╔══════════════════════════════════════════╗")
        print("║ Welcome to CMosSkillAV2 - Python Terminal ║")
        print("║ Type 'help' to see available commands    ║")
        print("╚══════════════════════════════════════════╝")
    
    def get_prompt(self):
        """Generate the shell prompt with the current directory."""
        cwd = os.getcwd()
        home = os.path.expanduser("~")
        
        # Replace home directory with ~
        if cwd.startswith(home):
            cwd = "~" + cwd[len(home):]
        
        return f"{Fore.CYAN}{cwd}{Style.RESET_ALL} $ "
    
    def parse_command(self, user_input):
        """
        Parse the user input and determine how to handle it.
        """
        if not user_input.strip():
            return None, []
        
        # Special case for Python inline code
        if user_input.startswith('>>>'):
            py_code = user_input[3:].strip()
            return 'py', py_code
        
        # Parse the command into tokens (handling quoted strings correctly)
        try:
            tokens = shlex.split(user_input)
        except ValueError as e:
            print(f"{Fore.RED}Error parsing command: {e}{Style.RESET_ALL}")
            return None, []
        
        if not tokens:
            return None, []
        
        command = tokens[0].lower()
        args = " ".join(tokens[1:]) if len(tokens) > 1 else ""
        
        return command, args
    
    def execute_command(self, command, args):
        """
        Execute the specified command with the given arguments.
        """
        if command in self.commands:
            # Call the command handler
            return self.commands[command](args)
        else:
            # Try to execute as system command
            try:
                cmd = [command] + shlex.split(args)
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.stdout:
                    print(result.stdout, end="")
                if result.stderr:
                    print(f"{Fore.RED}{result.stderr}{Style.RESET_ALL}", end="")
                
                return result.returncode
            except FileNotFoundError:
                print(f"{Fore.RED}Command not found: {command}{Style.RESET_ALL}")
                print(f"Type {Fore.GREEN}help{Style.RESET_ALL} to see available commands.")
                return 1
            except Exception as e:
                print(f"{Fore.RED}Error executing command: {e}{Style.RESET_ALL}")
                return 1
    
    def show_help(self, topic=None):
        """Show help information about commands."""
        return show_help(topic, self.commands)
    
    def exit_shell(self, args=None):
        """Exit the shell gracefully."""
        print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
        # Save command history before exiting
        self.history_manager.save_history()
        sys.exit(0)
    
    def clear_screen(self, args=None):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        return 0
    
    def start_python_shell(self, args=None):
        """Start an interactive Python shell."""
        print(f"{Fore.GREEN}Starting Python interactive shell. Type 'exit()' to return to CMosSkillAV2.{Style.RESET_ALL}")
        shell = InteractivePythonShell()
        shell.run()
        return 0
    
    def check_updates(self, args=None):
        """
        Check for updates and display daily information.
        
        Args:
            args: Not used, included for command handler compatibility.
            
        Returns:
            int: Return code (always 0)
        """
        # Force display of updates when explicitly called
        self.update_manager.display_daily_updates(force=True)
        return 0
        
    def run(self):
        """
        Run the main shell loop that handles user input and command execution.
        """
        # Display welcome message and daily updates
        self.print_welcome()
        self.update_manager.display_daily_updates()
        
        while True:
            try:
                # Display prompt and get user input
                user_input = input(self.get_prompt())
                
                # Add command to history if not empty
                if user_input.strip():
                    self.history_manager.add_to_history(user_input)
                
                # Parse and execute the command
                command, args = self.parse_command(user_input)
                if command:
                    self.execute_command(command, args)
            
            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                print("\n^C")
            except EOFError:
                # Handle Ctrl+D as exit
                print("")
                self.exit_shell()
            except Exception as e:
                print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")