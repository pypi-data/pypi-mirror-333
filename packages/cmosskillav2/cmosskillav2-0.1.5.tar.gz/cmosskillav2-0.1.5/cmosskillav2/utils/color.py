"""
Color and syntax highlighting utilities for the CMosSkillAV2 terminal.
"""

import os
import re
from colorama import Fore, Style

# File type to color mapping
FILE_COLORS = {
    'py': Fore.BLUE,      # Python files
    'txt': Fore.WHITE,    # Text files
    'md': Fore.YELLOW,    # Markdown
    'json': Fore.MAGENTA, # JSON files
    'exe': Fore.GREEN,    # Executables
    'sh': Fore.GREEN,     # Shell scripts
    'bat': Fore.GREEN,    # Batch files
}

# Command categories to color mapping
COMMAND_COLORS = {
    'file': Fore.CYAN,     # File operations (ls, cd, etc.)
    'python': Fore.BLUE,   # Python-related commands
    'shell': Fore.YELLOW,  # Shell built-ins
    'package': Fore.GREEN, # Package management
}

# Command to category mapping
COMMAND_CATEGORIES = {
    'cd': 'file',
    'ls': 'file',
    'mkdir': 'file',
    'touch': 'file',
    'rm': 'file',
    'cat': 'file',
    
    'python': 'python',
    'py': 'python',
    'pyshell': 'python',
    
    'pip': 'package',
    
    'help': 'shell',
    'exit': 'shell',
    'quit': 'shell',
    'clear': 'shell',
}

def highlight_command(command):
    """
    Highlight a command string based on its type.
    
    Args:
        command (str): The command to highlight.
        
    Returns:
        str: Highlighted command string.
    """
    # Get the base command without arguments
    base_cmd = command.split()[0] if command else ""
    
    # Get the category and corresponding color
    category = COMMAND_CATEGORIES.get(base_cmd, None)
    color = COMMAND_COLORS.get(category, Fore.WHITE) if category else Fore.WHITE
    
    return f"{color}{command}{Style.RESET_ALL}"

def colorize_syntax(code):
    """
    Apply syntax highlighting to Python code.
    
    Args:
        code (str): Python code to highlight.
        
    Returns:
        str: Syntax highlighted code.
    """
    # This is a simplified syntax highlighter
    # For a real implementation, consider using a library like pygments
    
    # Keywords
    keywords = [
        'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
        'def', 'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
        'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None',
        'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True', 'try',
        'while', 'with', 'yield'
    ]
    
    # Simple pattern-based highlighting
    highlighted = code
    
    # Highlight strings
    highlighted = re.sub(r'"([^"]*)"', f"{Fore.GREEN}\"\\1\"{Style.RESET_ALL}", highlighted)
    highlighted = re.sub(r"'([^']*)'", f"{Fore.GREEN}'\\1'{Style.RESET_ALL}", highlighted)
    
    # Highlight numbers
    highlighted = re.sub(r'\b(\d+)\b', f"{Fore.MAGENTA}\\1{Style.RESET_ALL}", highlighted)
    
    # Highlight keywords
    for keyword in keywords:
        pattern = r'\b' + keyword + r'\b'
        highlighted = re.sub(pattern, f"{Fore.BLUE}{keyword}{Style.RESET_ALL}", highlighted)
    
    # Highlight function definitions
    highlighted = re.sub(r'\bdef\s+(\w+)', f"{Fore.BLUE}def{Style.RESET_ALL} {Fore.YELLOW}\\1{Style.RESET_ALL}", highlighted)
    
    # Highlight class definitions
    highlighted = re.sub(r'\bclass\s+(\w+)', f"{Fore.BLUE}class{Style.RESET_ALL} {Fore.YELLOW}\\1{Style.RESET_ALL}", highlighted)
    
    return highlighted

def get_file_color(filename):
    """
    Get the appropriate color for a file based on its extension.
    
    Args:
        filename (str): The filename to color.
        
    Returns:
        str: The colorama color code.
    """
    if os.path.isdir(filename):
        return Fore.BLUE
    
    ext = filename.split('.')[-1] if '.' in filename else ''
    return FILE_COLORS.get(ext, Fore.WHITE)