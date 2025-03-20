"""
Tab completion functionality for the CMosSkillAV2 terminal.
"""

import os
import glob
import readline


class CMosSkillCompleter:
    """
    Custom completer for CMosSkillAV2 commands and file paths.
    """
    
    def __init__(self):
        """Initialize the completer with commands and special paths."""
        # Built-in commands that should be auto-completed
        self.commands = [
            'cd', 'ls', 'mkdir', 'touch', 'rm', 'cat',  # File operations
            'python', 'py', 'pyshell',  # Python execution
            'pip',  # Package management
            'help', 'exit', 'quit', 'clear',  # Shell built-ins
        ]
        
        # Pip subcommands for completion
        self.pip_subcommands = [
            'install', 'uninstall', 'freeze', 'list', 'show',
            'search', 'download', 'wheel', 'hash', 'check',
        ]
    
    def _list_directory(self, path):
        """
        List the contents of a directory for path completion.
        
        Args:
            path (str): The directory path to list.
            
        Returns:
            list: List of files and directories in the path.
        """
        if not path:
            path = '.'
        
        try:
            if os.path.isdir(path):
                # If the path is a directory, list its contents
                return [f for f in os.listdir(path) if not f.startswith('.')]
            else:
                # If the path is a partial path, get the directory part
                directory = os.path.dirname(path) or '.'
                prefix = os.path.basename(path)
                
                # List directory contents that match the prefix
                return [f for f in os.listdir(directory) 
                        if f.startswith(prefix) and not f.startswith('.')]
        except (FileNotFoundError, PermissionError):
            return []
    
    def complete_command(self, prefix):
        """
        Complete a command name based on the prefix.
        
        Args:
            prefix (str): Command prefix to complete.
            
        Returns:
            list: Matching command names.
        """
        return [cmd for cmd in self.commands if cmd.startswith(prefix)]
    
    def complete_path(self, path):
        """
        Complete a file path based on the partial path.
        
        Args:
            path (str): Partial path to complete.
            
        Returns:
            list: Matching paths.
        """
        # Handle ~/ expansion
        if path.startswith('~/'):
            path = os.path.expanduser(path)
        
        # Get matching paths using glob
        try:
            matches = glob.glob(path + '*')
            
            # Format paths (add trailing slash for directories)
            formatted_matches = []
            for match in matches:
                if os.path.isdir(match):
                    formatted_matches.append(match + os.sep)
                else:
                    formatted_matches.append(match)
            
            return formatted_matches
        except Exception:
            return []
    
    def complete_pip_subcommand(self, prefix):
        """
        Complete pip subcommands.
        
        Args:
            prefix (str): Subcommand prefix to complete.
            
        Returns:
            list: Matching pip subcommands.
        """
        return [cmd for cmd in self.pip_subcommands if cmd.startswith(prefix)]
    
    def complete_help_topic(self, prefix):
        """
        Complete help topics.
        
        Args:
            prefix (str): Topic prefix to complete.
            
        Returns:
            list: Matching help topics.
        """
        # Help topics are the same as the available commands
        return self.complete_command(prefix)
    
    def complete(self, text, state):
        """
        Main completion method called by readline.
        
        Args:
            text (str): The text to complete.
            state (int): The state of completion (0 for first match, etc.)
            
        Returns:
            str: The completed text or None if no more matches.
        """
        # Get the current line buffer and cursor position
        line_buffer = readline.get_line_buffer()
        cursor_pos = readline.get_endidx()
        
        # If we're at the start of the line, complete command names
        if cursor_pos == len(text):
            matches = self.complete_command(text)
        else:
            # Parse the line to determine what we're completing
            tokens = line_buffer.split()
            
            if len(tokens) == 0:
                matches = []
            elif len(tokens) == 1 and not line_buffer.endswith(' '):
                # Still completing the command
                matches = self.complete_command(text)
            else:
                # Completing arguments to a command
                command = tokens[0].lower()
                
                if command == 'help' and len(tokens) <= 2:
                    # Completing help topics
                    matches = self.complete_help_topic(text)
                elif command == 'pip' and len(tokens) == 2:
                    # Completing pip subcommands
                    matches = self.complete_pip_subcommand(text)
                else:
                    # Default to path completion for most commands
                    matches = self.complete_path(text)
        
        # Return the match for the current state
        try:
            return matches[state]
        except IndexError:
            return None