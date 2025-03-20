"""
Python code execution commands for the CMosSkillAV2 terminal.

This module provides functionality to:
- Execute Python scripts
- Run Python code inline
"""

import os
import sys
import code
import shlex
import subprocess
import traceback
from colorama import Fore, Style

from ..utils.color import colorize_syntax


def execute_python_script(args):
    """
    Execute a Python script file.
    
    Args:
        args (str): Script filename and arguments.
    
    Returns:
        int: Return code from script execution
    """
    # Parse arguments
    tokens = shlex.split(args)
    
    if not tokens:
        print(f"{Fore.RED}Usage: python script.py [args]{Style.RESET_ALL}")
        return 1
    
    # Get script path
    script_path = tokens[0]
    
    # Expand ~ in path
    script_path = os.path.expanduser(script_path)
    
    # Check if script exists
    if not os.path.exists(script_path):
        print(f"{Fore.RED}Script not found: {script_path}{Style.RESET_ALL}")
        return 1
    
    try:
        # Execute the script using subprocess
        cmd = [sys.executable, script_path] + tokens[1:]
        result = subprocess.run(cmd)
        return result.returncode
    except Exception as e:
        print(f"{Fore.RED}Error executing script: {e}{Style.RESET_ALL}")
        return 1


def execute_python_inline(py_code):
    """
    Execute Python code inline.
    
    Args:
        py_code (str): Python code to execute.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    if not py_code.strip():
        print(f"{Fore.RED}No Python code provided.{Style.RESET_ALL}")
        return 1
    
    # Display the code with syntax highlighting
    print(f"{Fore.CYAN}Executing:{Style.RESET_ALL}")
    highlighted_code = colorize_syntax(py_code)
    print(highlighted_code)
    print("-" * 40)
    
    try:
        # Create a local namespace for execution
        local_ns = {}
        
        # Execute the code
        exec(py_code, globals(), local_ns)
        
        # Show any defined variables
        if local_ns:
            print(f"{Fore.CYAN}Variables defined:{Style.RESET_ALL}")
            for key, value in local_ns.items():
                if not key.startswith('__'):
                    if isinstance(value, (int, float, str, bool, list, dict, tuple, set)):
                        print(f"{key} = {value}")
                    else:
                        print(f"{key} = {type(value).__name__} object")
        
        return 0
    except SyntaxError as e:
        print(f"{Fore.RED}Syntax error: {e}{Style.RESET_ALL}")
        print(f"Line: {e.lineno}, Offset: {e.offset}")
        print(f"Text: {e.text}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        traceback.print_exc()
        return 1


class InteractivePythonShell:
    """
    Interactive Python shell with history and proper support for
    multiline statements.
    """
    
    def __init__(self):
        """Initialize the interactive Python shell."""
        # Create an interactive console
        self.console = code.InteractiveConsole()
        
        # Set up banner
        self.banner = f"{Fore.GREEN}Python {sys.version.split()[0]} Interactive Shell{Style.RESET_ALL}"
        self.banner += f"\n{Fore.YELLOW}Type 'exit()' to return to CMosSkillAV2{Style.RESET_ALL}"
    
    def run(self):
        """Run the interactive console."""
        self.console.interact(banner=self.banner, exitmsg="Returning to CMosSkillAV2...")