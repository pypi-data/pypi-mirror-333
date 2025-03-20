"""
System utility commands for CMosSkillAV2 terminal.

This module provides system monitoring and management tools.
"""

import os
import sys
import platform
import subprocess
import shutil
import time
from datetime import datetime
from colorama import Fore, Style

def sysinfo_command(args):
    """
    Display system information.
    
    Args:
        args (str): Not used.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    print(f"{Fore.CYAN}System Information:{Style.RESET_ALL}")
    
    # Basic platform info
    print(f"  OS: {platform.system()} {platform.release()}")
    print(f"  Platform: {platform.platform()}")
    print(f"  Architecture: {platform.machine()}")
    print(f"  Python: {platform.python_version()} ({sys.executable})")
    
    # CPU info
    try:
        if platform.system() == "Linux":
            # Get CPU info from /proc/cpuinfo
            cpu_info = {}
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if line.strip():
                            key, value = line.split(':', 1)
                            cpu_info[key.strip()] = value.strip()
                
                if 'model name' in cpu_info:
                    print(f"  CPU: {cpu_info['model name']}")
                if 'processor' in cpu_info:
                    print(f"  Cores: {int(cpu_info.get('processor', 0)) + 1}")
            except:
                pass
        elif platform.system() == "Darwin":  # macOS
            try:
                model = subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string']).decode().strip()
                cores = subprocess.check_output(['sysctl', '-n', 'hw.ncpu']).decode().strip()
                print(f"  CPU: {model}")
                print(f"  Cores: {cores}")
            except:
                pass
        elif platform.system() == "Windows":
            try:
                # Use WMI on Windows if available
                model = "Unknown"
                try:
                    # Alternative approach using subprocess
                    output = subprocess.check_output("wmic cpu get name", shell=True).decode().split('\n')
                    if len(output) > 1:
                        model = output[1].strip()
                except:
                    pass
                
                print(f"  CPU: {model}")
                print(f"  Cores: {os.cpu_count() or 'Unknown'}")
            except:
                print(f"  Cores: {os.cpu_count() or 'Unknown'}")
    except:
        print(f"  Cores: {os.cpu_count() or 'Unknown'}")
    
    # Memory info
    try:
        import psutil
        vm = psutil.virtual_memory()
        print(f"  Memory: Total: {vm.total / (1024**3):.2f} GB, Available: {vm.available / (1024**3):.2f} GB")
        print(f"  Memory Usage: {vm.percent}%")
        
        # Disk info
        disk = psutil.disk_usage('/')
        print(f"  Disk: Total: {disk.total / (1024**3):.2f} GB, Free: {disk.free / (1024**3):.2f} GB")
        print(f"  Disk Usage: {disk.percent}%")
    except ImportError:
        # Fallback for disk info
        try:
            total, used, free = shutil.disk_usage('/')
            print(f"  Disk: Total: {total / (1024**3):.2f} GB, Free: {free / (1024**3):.2f} GB")
            print(f"  Disk Usage: {(used / total) * 100:.1f}%")
        except:
            pass
    
    # Get environment info
    print(f"\n{Fore.CYAN}Environment:{Style.RESET_ALL}")
    print(f"  User: {os.environ.get('USER', os.environ.get('USERNAME', 'Unknown'))}")
    print(f"  Home: {os.path.expanduser('~')}")
    print(f"  Working Directory: {os.getcwd()}")
    print(f"  PATH: {os.environ.get('PATH', 'Not available')}")
    
    return 0

def proc_command(args):
    """
    Display process information.
    
    Args:
        args (str): Optional process name filter.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    try:
        import psutil
    except ImportError:
        print(f"{Fore.YELLOW}The 'psutil' module is required for process monitoring.{Style.RESET_ALL}")
        print(f"Install with: pip install psutil")
        return 1
    
    # Get all processes
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']):
        try:
            pinfo = proc.info
            processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    # Filter processes if a filter was provided
    if args:
        filtered = []
        filter_term = args.lower()
        for proc in processes:
            if filter_term in proc['name'].lower():
                filtered.append(proc)
        processes = filtered
    
    # Sort by memory usage
    processes = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)
    
    # Display processes
    print(f"{Fore.CYAN}{'PID':<8} {'User':<12} {'Memory %':<10} {'CPU %':<8} {'Name'}{Style.RESET_ALL}")
    print("-" * 60)
    
    # Limit to top 20 processes
    for proc in processes[:20]:
        print(f"{proc['pid']:<8} {proc['username'][:12]:<12} {proc['memory_percent']:<10.1f} {proc['cpu_percent']:<8.1f} {proc['name']}")
    
    if len(processes) > 20:
        print(f"\n{Fore.YELLOW}Showing top 20 of {len(processes)} matching processes. Refine filter to see more.{Style.RESET_ALL}")
    
    return 0

def kill_command(args):
    """
    Kill a process by PID or name.
    
    Args:
        args (str): PID or process name.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    if not args:
        print(f"{Fore.RED}Error: PID or process name required.{Style.RESET_ALL}")
        print(f"Usage: kill <pid_or_name>")
        return 1
    
    try:
        import psutil
    except ImportError:
        print(f"{Fore.YELLOW}The 'psutil' module is required for process management.{Style.RESET_ALL}")
        print(f"Install with: pip install psutil")
        return 1
    
    # Check if argument is a PID
    if args.isdigit():
        pid = int(args)
        
        try:
            process = psutil.Process(pid)
            process_name = process.name()
            
            # Confirm before killing
            print(f"Kill process {pid} ({process_name})? [y/N] ", end='')
            confirm = input().strip().lower()
            
            if confirm == 'y':
                process.terminate()
                print(f"{Fore.GREEN}Process {pid} terminated.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}")
            
            return 0
        except psutil.NoSuchProcess:
            print(f"{Fore.RED}Error: No process with PID {pid}.{Style.RESET_ALL}")
            return 1
    else:
        # Argument is a process name
        # Find matching processes
        matching = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if args.lower() in proc.info['name'].lower():
                    matching.append((proc.info['pid'], proc.info['name']))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if not matching:
            print(f"{Fore.RED}Error: No processes matching '{args}'.{Style.RESET_ALL}")
            return 1
        
        # Multiple matches
        if len(matching) > 1:
            print(f"{Fore.CYAN}Found {len(matching)} matching processes:{Style.RESET_ALL}")
            for i, (pid, name) in enumerate(matching):
                print(f"  {i+1}. {pid}: {name}")
            
            # Ask which one to kill
            print(f"\nEnter number to kill (0 to cancel): ", end='')
            try:
                choice = int(input().strip())
                
                if choice == 0:
                    print(f"{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}")
                    return 0
                
                if 1 <= choice <= len(matching):
                    pid, name = matching[choice-1]
                    
                    # Confirm kill
                    print(f"Kill process {pid} ({name})? [y/N] ", end='')
                    confirm = input().strip().lower()
                    
                    if confirm == 'y':
                        psutil.Process(pid).terminate()
                        print(f"{Fore.GREEN}Process {pid} terminated.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid input.{Style.RESET_ALL}")
        else:
            # Single match
            pid, name = matching[0]
            
            # Confirm kill
            print(f"Kill process {pid} ({name})? [y/N] ", end='')
            confirm = input().strip().lower()
            
            if confirm == 'y':
                psutil.Process(pid).terminate()
                print(f"{Fore.GREEN}Process {pid} terminated.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}")
    
    return 0

def diskusage_command(args):
    """
    Display disk usage information.
    
    Args:
        args (str): Optional path to check.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    # Determine path to check
    path = args or '.'
    
    if not os.path.exists(path):
        print(f"{Fore.RED}Error: Path does not exist: {path}{Style.RESET_ALL}")
        return 1
    
    # Check if path is a directory
    if os.path.isdir(path):
        print(f"{Fore.CYAN}Disk Usage for: {os.path.abspath(path)}{Style.RESET_ALL}")
        
        # Get total disk usage
        try:
            total, used, free = shutil.disk_usage(path)
            print(f"  Total: {total / (1024**3):.2f} GB")
            print(f"  Used: {used / (1024**3):.2f} GB ({(used / total) * 100:.1f}%)")
            print(f"  Free: {free / (1024**3):.2f} GB")
        except Exception as e:
            print(f"{Fore.RED}Error getting disk usage: {e}{Style.RESET_ALL}")
        
        # Get directory sizes
        print(f"\n{Fore.CYAN}Directory Sizes:{Style.RESET_ALL}")
        
        # Get subdirectories and their sizes
        sizes = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            
            if os.path.isdir(item_path):
                try:
                    size = get_dir_size(item_path)
                    sizes.append((item, size))
                except:
                    sizes.append((item, 0))
        
        # Sort by size, largest first
        sizes = sorted(sizes, key=lambda x: x[1], reverse=True)
        
        # Display top directories
        for name, size in sizes[:15]:  # Show top 15
            print(f"  {name}: {format_size(size)}")
        
        if len(sizes) > 15:
            print(f"\n{Fore.YELLOW}Showing top 15 of {len(sizes)} directories.{Style.RESET_ALL}")
    else:
        # Path is a file, show its size
        try:
            size = os.path.getsize(path)
            print(f"{Fore.CYAN}File Size:{Style.RESET_ALL} {format_size(size)}")
        except Exception as e:
            print(f"{Fore.RED}Error getting file size: {e}{Style.RESET_ALL}")
    
    return 0

def get_dir_size(path):
    """Get the size of a directory and its subdirectories."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(file_path)
            except (FileNotFoundError, PermissionError):
                pass
    return total_size

def format_size(size_bytes):
    """Format size in bytes to human readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.2f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes/(1024**2):.2f} MB"
    else:
        return f"{size_bytes/(1024**3):.2f} GB"

def find_command(args):
    """
    Find files and directories.
    
    Args:
        args (str): Search parameters.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    if not args:
        print(f"{Fore.RED}Error: Search pattern required.{Style.RESET_ALL}")
        print(f"Usage: find <pattern> [path]")
        return 1
    
    # Parse arguments
    parts = args.split(None, 1)
    pattern = parts[0]
    path = parts[1] if len(parts) > 1 else '.'
    
    # Check if path exists
    if not os.path.exists(path):
        print(f"{Fore.RED}Error: Path does not exist: {path}{Style.RESET_ALL}")
        return 1
    
    # Compile pattern for faster matching
    import fnmatch
    import re
    regex = fnmatch.translate(pattern)
    matcher = re.compile(regex)
    
    # Find matching files and directories
    print(f"{Fore.CYAN}Searching for '{pattern}' in {os.path.abspath(path)}{Style.RESET_ALL}")
    
    matches = []
    for root, dirnames, filenames in os.walk(path):
        # Process directories
        for dirname in dirnames:
            if matcher.match(dirname):
                matches.append(os.path.join(root, dirname))
        
        # Process files
        for filename in filenames:
            if matcher.match(filename):
                matches.append(os.path.join(root, filename))
    
    # Sort matches
    matches.sort()
    
    # Display results
    if matches:
        for match in matches:
            if os.path.isdir(match):
                print(f"{Fore.BLUE}{match}/{Style.RESET_ALL}")
            else:
                print(match)
        
        print(f"\n{Fore.GREEN}Found {len(matches)} matches.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}No matches found.{Style.RESET_ALL}")
    
    return 0