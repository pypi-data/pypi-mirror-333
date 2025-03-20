"""
Mobile platform specific commands for CMosSkillAV2 terminal.

This module provides commands optimized for mobile environments like Termux and Pydroid.
"""

import os
import sys
import platform
import shutil
import subprocess
from colorama import Fore, Style

def is_termux():
    """Check if running in Termux environment."""
    return 'com.termux' in os.environ.get('PREFIX', '')

def is_pydroid():
    """Check if running in Pydroid environment."""
    return 'com.googlecode.pydroid3' in os.environ.get('ANDROID_DATA', '') or \
           os.environ.get('PYDROID', '') == '1'

def is_android():
    """Check if running on Android platform."""
    return is_termux() or is_pydroid() or 'ANDROID_ROOT' in os.environ

def termux_command(args):
    """
    Termux specific utilities and commands.
    
    Args:
        args (str): Subcommand and its arguments.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    if not is_termux():
        print(f"{Fore.RED}Error: This command only works in Termux environment.{Style.RESET_ALL}")
        return 1
    
    if not args:
        print(f"{Fore.YELLOW}Termux Tools{Style.RESET_ALL}")
        print("  pkg - Package management (shortcut for apt)")
        print("  api - Access Termux API")
        print("  storage - Request storage access")
        print("  battery - Show battery status")
        print("  vibrate - Vibrate device")
        print("  toast <msg> - Show Android toast notification")
        return 0
    
    # Parse the subcommand
    parts = args.split(None, 1)
    subcmd = parts[0] if parts else ""
    subargs = parts[1] if len(parts) > 1 else ""
    
    # Execute the appropriate subcommand
    if subcmd == "pkg":
        return os.system(f"apt {subargs}")
    elif subcmd == "api":
        return os.system(f"termux-api {subargs}")
    elif subcmd == "storage":
        return os.system("termux-setup-storage")
    elif subcmd == "battery":
        return os.system("termux-battery-status")
    elif subcmd == "vibrate":
        duration = subargs or "1000"
        return os.system(f"termux-vibrate -d {duration}")
    elif subcmd == "toast":
        if not subargs:
            print(f"{Fore.RED}Error: Message required for toast notification.{Style.RESET_ALL}")
            return 1
        return os.system(f"termux-toast '{subargs}'")
    else:
        print(f"{Fore.RED}Error: Unknown termux subcommand '{subcmd}'.{Style.RESET_ALL}")
        return 1

def pydroid_command(args):
    """
    Pydroid specific utilities and commands.
    
    Args:
        args (str): Subcommand and its arguments.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    if not is_pydroid() and not is_android():
        print(f"{Fore.RED}Error: This command only works in Pydroid or Android environment.{Style.RESET_ALL}")
        return 1
    
    if not args:
        print(f"{Fore.YELLOW}Pydroid Tools{Style.RESET_ALL}")
        print("  pip - Manage pip packages")
        print("  storage - Show storage paths")
        print("  perms - Check permissions")
        return 0
    
    # Parse the subcommand
    parts = args.split(None, 1)
    subcmd = parts[0] if parts else ""
    subargs = parts[1] if len(parts) > 1 else ""
    
    # Execute the appropriate subcommand
    if subcmd == "pip":
        return os.system(f"pip {subargs}")
    elif subcmd == "storage":
        print(f"{Fore.CYAN}Storage Paths:{Style.RESET_ALL}")
        print(f"  Current directory: {os.getcwd()}")
        print(f"  Home directory: {os.path.expanduser('~')}")
        print(f"  External storage: {os.environ.get('EXTERNAL_STORAGE', 'Not available')}")
        print(f"  SD Card: {os.environ.get('SECONDARY_STORAGE', 'Not available')}")
        return 0
    elif subcmd == "perms":
        print(f"{Fore.CYAN}Checking permissions:{Style.RESET_ALL}")
        paths = [
            os.path.expanduser("~"),
            "/sdcard",
            os.environ.get("EXTERNAL_STORAGE", ""),
            os.environ.get("SECONDARY_STORAGE", "")
        ]
        
        for path in paths:
            if path and os.path.exists(path):
                readable = os.access(path, os.R_OK)
                writable = os.access(path, os.W_OK)
                executable = os.access(path, os.X_OK)
                print(f"  {path}: R={readable}, W={writable}, X={executable}")
        return 0
    else:
        print(f"{Fore.RED}Error: Unknown pydroid subcommand '{subcmd}'.{Style.RESET_ALL}")
        return 1

def device_info_command(args):
    """
    Display device and platform information.
    
    Args:
        args (str): Not used.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    print(f"{Fore.CYAN}Device Information:{Style.RESET_ALL}")
    print(f"  Platform: {platform.platform()}")
    print(f"  System: {platform.system()}")
    print(f"  Release: {platform.release()}")
    print(f"  Python: {platform.python_version()}")
    print(f"  Architecture: {platform.machine()}")
    
    if is_android():
        print(f"\n{Fore.CYAN}Android Environment:{Style.RESET_ALL}")
        print(f"  Termux: {is_termux()}")
        print(f"  Pydroid: {is_pydroid()}")
        if is_termux():
            try:
                # Get Termux version if available
                result = subprocess.run("termux-info", shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"\n{Fore.CYAN}Termux Info:{Style.RESET_ALL}")
                    print(result.stdout)
            except:
                pass
    
    # Display memory info if psutil is available
    try:
        import psutil
        mem = psutil.virtual_memory()
        print(f"\n{Fore.CYAN}Memory Information:{Style.RESET_ALL}")
        print(f"  Total: {mem.total / (1024**3):.2f} GB")
        print(f"  Available: {mem.available / (1024**3):.2f} GB")
        print(f"  Used: {mem.used / (1024**3):.2f} GB ({mem.percent}%)")
    except ImportError:
        pass
        
    return 0

def battery_command(args):
    """
    Display battery information if available.
    
    Args:
        args (str): Not used.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    if is_termux():
        # Use Termux API if available
        return os.system("termux-battery-status")
    
    # Try psutil for other platforms
    try:
        import psutil
        battery = psutil.sensors_battery()
        if battery:
            print(f"{Fore.CYAN}Battery Information:{Style.RESET_ALL}")
            print(f"  Percent: {battery.percent}%")
            print(f"  Power plugged: {'Yes' if battery.power_plugged else 'No'}")
            
            # Calculate remaining time
            if battery.secsleft != psutil.POWER_TIME_UNLIMITED and battery.secsleft != psutil.POWER_TIME_UNKNOWN:
                minutes, seconds = divmod(battery.secsleft, 60)
                hours, minutes = divmod(minutes, 60)
                print(f"  Remaining: {hours}h {minutes}m {seconds}s")
            return 0
        else:
            print(f"{Fore.YELLOW}Battery information not available on this device.{Style.RESET_ALL}")
            return 1
    except ImportError:
        print(f"{Fore.YELLOW}Battery information requires psutil module.{Style.RESET_ALL}")
        print(f"Install with: pip install psutil")
        return 1