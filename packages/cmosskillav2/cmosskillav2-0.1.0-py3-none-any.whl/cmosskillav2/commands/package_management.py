"""
Package management commands for the CMosSkillAV2 terminal.

This module provides functionality to manage Python packages with pip.
"""

import sys
import shlex
import subprocess
from colorama import Fore, Style


def pip_command(args):
    """
    Run pip commands to manage Python packages.
    
    Args:
        args (str): Pip command and arguments.
    
    Returns:
        int: Return code from pip execution
    """
    if not args.strip():
        print(f"{Fore.RED}Usage: pip <command> [options]{Style.RESET_ALL}")
        print(f"Common commands: install, uninstall, list, freeze, show, search")
        return 1
    
    try:
        # Parse the arguments
        tokens = shlex.split(args)
        
        # Construct the command
        cmd = [sys.executable, '-m', 'pip'] + tokens
        
        # Execute pip
        print(f"{Fore.CYAN}Running pip command...{Style.RESET_ALL}")
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print(f"{Fore.GREEN}Pip command completed successfully.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Pip command exited with code {result.returncode}{Style.RESET_ALL}")
        
        return result.returncode
    except Exception as e:
        print(f"{Fore.RED}Error executing pip command: {e}{Style.RESET_ALL}")
        return 1