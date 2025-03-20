"""
File operation commands for the CMosSkillAV2 terminal.

This module provides implementations for common file system operations:
- cd: Change directory
- ls: List directory contents
- mkdir: Create directory
- touch: Create empty file
- rm: Remove file or directory
- cat: Display file contents
"""

import os
import shlex
import shutil
from datetime import datetime
from colorama import Fore, Style

from ..utils.color import get_file_color


def cd_command(args):
    """
    Change the current working directory.
    
    Args:
        args (str): Path to change to. Empty means change to home directory.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    # Parse arguments
    path = args.strip()
    
    # Empty path or ~ means home directory
    if not path or path == '~':
        path = os.path.expanduser('~')
    else:
        # Expand ~ in path
        path = os.path.expanduser(path)
    
    try:
        os.chdir(path)
        return 0
    except FileNotFoundError:
        print(f"{Fore.RED}Directory not found: {path}{Style.RESET_ALL}")
        return 1
    except NotADirectoryError:
        print(f"{Fore.RED}Not a directory: {path}{Style.RESET_ALL}")
        return 1
    except PermissionError:
        print(f"{Fore.RED}Permission denied: {path}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error changing directory: {e}{Style.RESET_ALL}")
        return 1


def ls_command(args):
    """
    List directory contents with color coding.
    
    Args:
        args (str): Path to list. Empty means current directory.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    # Parse arguments
    tokens = shlex.split(args) if args else []
    
    # Check for flags
    show_hidden = '-a' in tokens
    show_long = '-l' in tokens
    
    # Remove flags from tokens
    tokens = [t for t in tokens if not t.startswith('-')]
    
    # Determine path to list
    path = tokens[0] if tokens else '.'
    
    # Expand ~ in path
    path = os.path.expanduser(path)
    
    try:
        # Get list of files/directories
        items = os.listdir(path)
        
        # Sort items (directories first)
        dirs = []
        files = []
        
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                dirs.append(item)
            else:
                files.append(item)
        
        # Filter hidden files if needed
        if not show_hidden:
            dirs = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]
        
        # Sort alphabetically within each group
        dirs.sort()
        files.sort()
        
        # Combine the lists
        all_items = dirs + files
        
        if not all_items:
            print("Directory is empty.")
            return 0
        
        if show_long:
            # Long format listing
            for item in all_items:
                full_path = os.path.join(path, item)
                stat = os.stat(full_path)
                
                # Format file size
                size = stat.st_size
                if size > 1024*1024:
                    size_str = f"{size/(1024*1024):.1f}M"
                elif size > 1024:
                    size_str = f"{size/1024:.1f}K"
                else:
                    size_str = f"{size}B"
                
                # Format modified time
                mod_time = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                
                # Get color for item
                color = get_file_color(full_path)
                
                # Print item details
                print(f"{size_str:>7} {mod_time} {color}{item}{Style.RESET_ALL}")
        else:
            # Simple listing with colors
            for item in all_items:
                full_path = os.path.join(path, item)
                color = get_file_color(full_path)
                print(f"{color}{item}{Style.RESET_ALL}", end="  ")
            print()  # Newline at the end
            
        return 0
    
    except FileNotFoundError:
        print(f"{Fore.RED}Directory not found: {path}{Style.RESET_ALL}")
        return 1
    except NotADirectoryError:
        print(f"{Fore.RED}Not a directory: {path}{Style.RESET_ALL}")
        return 1
    except PermissionError:
        print(f"{Fore.RED}Permission denied: {path}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error listing directory: {e}{Style.RESET_ALL}")
        return 1


def mkdir_command(args):
    """
    Create directory.
    
    Args:
        args (str): Directory path to create.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    # Parse arguments
    tokens = shlex.split(args)
    
    if not tokens:
        print(f"{Fore.RED}Usage: mkdir [-p] directory{Style.RESET_ALL}")
        return 1
    
    # Check for -p flag
    create_parents = False
    if tokens[0] == '-p':
        create_parents = True
        tokens.pop(0)
    
    if not tokens:
        print(f"{Fore.RED}No directory specified{Style.RESET_ALL}")
        return 1
    
    # Get directory path
    path = tokens[0]
    
    # Expand ~ in path
    path = os.path.expanduser(path)
    
    try:
        if create_parents:
            os.makedirs(path, exist_ok=True)
        else:
            os.mkdir(path)
        return 0
    except FileExistsError:
        print(f"{Fore.RED}Directory already exists: {path}{Style.RESET_ALL}")
        return 1
    except FileNotFoundError:
        print(f"{Fore.RED}Parent directory not found. Use -p to create parent directories.{Style.RESET_ALL}")
        return 1
    except PermissionError:
        print(f"{Fore.RED}Permission denied: {path}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error creating directory: {e}{Style.RESET_ALL}")
        return 1


def touch_command(args):
    """
    Create empty file(s) or update timestamps.
    
    Args:
        args (str): File path(s) to create.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    # Parse arguments
    tokens = shlex.split(args)
    
    if not tokens:
        print(f"{Fore.RED}Usage: touch file [file2 ...]{Style.RESET_ALL}")
        return 1
    
    success = True
    
    for path in tokens:
        # Expand ~ in path
        path = os.path.expanduser(path)
        
        try:
            # Open the file in 'a' mode (create if not exists, append otherwise)
            with open(path, 'a'):
                # Update the file's modification time to current time
                os.utime(path, None)
        except PermissionError:
            print(f"{Fore.RED}Permission denied: {path}{Style.RESET_ALL}")
            success = False
        except Exception as e:
            print(f"{Fore.RED}Error touching file: {e}{Style.RESET_ALL}")
            success = False
    
    return 0 if success else 1


def rm_command(args):
    """
    Remove file(s) or directories.
    
    Args:
        args (str): Path(s) to remove.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    # Parse arguments
    tokens = shlex.split(args)
    
    if not tokens:
        print(f"{Fore.RED}Usage: rm [-r] file_or_directory{Style.RESET_ALL}")
        return 1
    
    # Check for -r flag
    recursive = False
    if tokens[0] == '-r' or tokens[0] == '-rf':
        recursive = True
        tokens.pop(0)
    
    if not tokens:
        print(f"{Fore.RED}No file or directory specified{Style.RESET_ALL}")
        return 1
    
    # Get path to remove
    path = tokens[0]
    
    # Expand ~ in path
    path = os.path.expanduser(path)
    
    try:
        if os.path.isdir(path):
            if recursive:
                shutil.rmtree(path)
            else:
                print(f"{Fore.RED}Cannot remove directory without -r flag: {path}{Style.RESET_ALL}")
                return 1
        else:
            os.remove(path)
        return 0
    except FileNotFoundError:
        print(f"{Fore.RED}No such file or directory: {path}{Style.RESET_ALL}")
        return 1
    except PermissionError:
        print(f"{Fore.RED}Permission denied: {path}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error removing: {e}{Style.RESET_ALL}")
        return 1


def cat_command(args):
    """
    Display file contents.
    
    Args:
        args (str): File path(s) to display.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    # Parse arguments
    tokens = shlex.split(args)
    
    if not tokens:
        print(f"{Fore.RED}Usage: cat file [file2 ...]{Style.RESET_ALL}")
        return 1
    
    success = True
    
    for path in tokens:
        # Expand ~ in path
        path = os.path.expanduser(path)
        
        try:
            with open(path, 'r') as f:
                print(f.read())
        except FileNotFoundError:
            print(f"{Fore.RED}File not found: {path}{Style.RESET_ALL}")
            success = False
        except IsADirectoryError:
            print(f"{Fore.RED}Is a directory: {path}{Style.RESET_ALL}")
            success = False
        except PermissionError:
            print(f"{Fore.RED}Permission denied: {path}{Style.RESET_ALL}")
            success = False
        except UnicodeDecodeError:
            print(f"{Fore.RED}Cannot display binary file: {path}{Style.RESET_ALL}")
            success = False
        except Exception as e:
            print(f"{Fore.RED}Error reading file: {e}{Style.RESET_ALL}")
            success = False
    
    return 0 if success else 1