"""
Developer toolbox commands for CMosSkillAV2 terminal.

This module provides utilities for developers such as JSON formatting,
base64 encoding/decoding, and simple text transformations.
"""

import os
import sys
import json
import base64
import re
import hashlib
import random
import string
import time
import datetime
from colorama import Fore, Style

def json_command(args):
    """
    JSON formatting and validation utility.
    
    Args:
        args (str): Subcommand and arguments.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    if not args:
        print(f"{Fore.YELLOW}JSON Utility{Style.RESET_ALL}")
        print("  format <json_string> - Format JSON string")
        print("  validate <json_string> - Validate JSON string")
        print("  format-file <filename> - Format JSON file")
        print("  minify <json_string> - Minify JSON string")
        return 0
    
    # Parse the subcommand
    parts = args.split(None, 1)
    subcmd = parts[0] if parts else ""
    subargs = parts[1] if len(parts) > 1 else ""
    
    if subcmd == "format" or subcmd == "validate":
        if not subargs:
            print(f"{Fore.RED}Error: JSON string required.{Style.RESET_ALL}")
            return 1
        
        try:
            # Parse JSON
            parsed = json.loads(subargs)
            
            if subcmd == "format":
                # Format with indentation
                formatted = json.dumps(parsed, indent=2, sort_keys=True)
                print(formatted)
            else:  # validate
                print(f"{Fore.GREEN}JSON is valid.{Style.RESET_ALL}")
            
            return 0
        except json.JSONDecodeError as e:
            print(f"{Fore.RED}Invalid JSON: {e}{Style.RESET_ALL}")
            return 1
            
    elif subcmd == "format-file":
        if not subargs:
            print(f"{Fore.RED}Error: Filename required.{Style.RESET_ALL}")
            return 1
        
        try:
            # Check if file exists
            if not os.path.isfile(subargs):
                print(f"{Fore.RED}Error: File not found: {subargs}{Style.RESET_ALL}")
                return 1
            
            # Read file
            with open(subargs, 'r') as f:
                content = f.read()
            
            # Parse and format JSON
            parsed = json.loads(content)
            formatted = json.dumps(parsed, indent=2, sort_keys=True)
            
            # Write back to file
            with open(subargs, 'w') as f:
                f.write(formatted)
            
            print(f"{Fore.GREEN}JSON file formatted: {subargs}{Style.RESET_ALL}")
            return 0
        except json.JSONDecodeError as e:
            print(f"{Fore.RED}Invalid JSON in file: {e}{Style.RESET_ALL}")
            return 1
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return 1
            
    elif subcmd == "minify":
        if not subargs:
            print(f"{Fore.RED}Error: JSON string required.{Style.RESET_ALL}")
            return 1
        
        try:
            # Parse and minify JSON
            parsed = json.loads(subargs)
            minified = json.dumps(parsed, separators=(',', ':'))
            print(minified)
            return 0
        except json.JSONDecodeError as e:
            print(f"{Fore.RED}Invalid JSON: {e}{Style.RESET_ALL}")
            return 1
    
    else:
        print(f"{Fore.RED}Error: Unknown JSON subcommand '{subcmd}'.{Style.RESET_ALL}")
        return 1

def base64_command(args):
    """
    Base64 encoding and decoding utility.
    
    Args:
        args (str): Subcommand and arguments.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    if not args:
        print(f"{Fore.YELLOW}Base64 Utility{Style.RESET_ALL}")
        print("  encode <text> - Encode text to Base64")
        print("  decode <base64> - Decode Base64 to text")
        print("  encode-file <filename> - Encode file to Base64")
        print("  decode-file <base64> <output_file> - Decode Base64 to file")
        return 0
    
    # Parse the subcommand
    parts = args.split(None, 1)
    subcmd = parts[0] if parts else ""
    subargs = parts[1] if len(parts) > 1 else ""
    
    if subcmd == "encode":
        if not subargs:
            print(f"{Fore.RED}Error: Text required for encoding.{Style.RESET_ALL}")
            return 1
        
        try:
            # Encode text to Base64
            encoded = base64.b64encode(subargs.encode('utf-8')).decode('utf-8')
            print(encoded)
            return 0
        except Exception as e:
            print(f"{Fore.RED}Error encoding to Base64: {e}{Style.RESET_ALL}")
            return 1
            
    elif subcmd == "decode":
        if not subargs:
            print(f"{Fore.RED}Error: Base64 string required for decoding.{Style.RESET_ALL}")
            return 1
        
        try:
            # Decode Base64 to text
            decoded = base64.b64decode(subargs).decode('utf-8')
            print(decoded)
            return 0
        except Exception as e:
            print(f"{Fore.RED}Error decoding Base64: {e}{Style.RESET_ALL}")
            return 1
            
    elif subcmd == "encode-file":
        if not subargs:
            print(f"{Fore.RED}Error: Filename required.{Style.RESET_ALL}")
            return 1
        
        try:
            # Check if file exists
            if not os.path.isfile(subargs):
                print(f"{Fore.RED}Error: File not found: {subargs}{Style.RESET_ALL}")
                return 1
            
            # Read and encode file
            with open(subargs, 'rb') as f:
                content = f.read()
            
            encoded = base64.b64encode(content).decode('utf-8')
            print(encoded)
            return 0
        except Exception as e:
            print(f"{Fore.RED}Error encoding file to Base64: {e}{Style.RESET_ALL}")
            return 1
            
    elif subcmd == "decode-file":
        parts = subargs.split(None, 1)
        if len(parts) < 2:
            print(f"{Fore.RED}Error: Both Base64 string and output filename required.{Style.RESET_ALL}")
            return 1
        
        base64_str = parts[0]
        output_file = parts[1]
        
        try:
            # Decode Base64 to file
            decoded = base64.b64decode(base64_str)
            
            with open(output_file, 'wb') as f:
                f.write(decoded)
            
            print(f"{Fore.GREEN}Decoded to file: {output_file}{Style.RESET_ALL}")
            return 0
        except Exception as e:
            print(f"{Fore.RED}Error decoding Base64 to file: {e}{Style.RESET_ALL}")
            return 1
    
    else:
        print(f"{Fore.RED}Error: Unknown Base64 subcommand '{subcmd}'.{Style.RESET_ALL}")
        return 1

def hash_command(args):
    """
    Hash generation utility.
    
    Args:
        args (str): Subcommand and arguments.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    if not args:
        print(f"{Fore.YELLOW}Hash Utility{Style.RESET_ALL}")
        print("  md5 <text> - Generate MD5 hash")
        print("  sha1 <text> - Generate SHA1 hash")
        print("  sha256 <text> - Generate SHA256 hash")
        print("  sha512 <text> - Generate SHA512 hash")
        print("  file <algorithm> <filename> - Hash a file with specified algorithm")
        return 0
    
    # Parse the subcommand
    parts = args.split(None, 1)
    subcmd = parts[0].lower() if parts else ""
    subargs = parts[1] if len(parts) > 1 else ""
    
    # Handle file hashing specially
    if subcmd == "file":
        file_parts = subargs.split(None, 1)
        if len(file_parts) < 2:
            print(f"{Fore.RED}Error: Both algorithm and filename required.{Style.RESET_ALL}")
            print("Usage: hash file <algorithm> <filename>")
            return 1
        
        algorithm = file_parts[0].lower()
        filename = file_parts[1]
        
        # Check if algorithm is supported
        if algorithm not in ('md5', 'sha1', 'sha256', 'sha512'):
            print(f"{Fore.RED}Error: Unsupported algorithm '{algorithm}'.{Style.RESET_ALL}")
            print("Supported algorithms: md5, sha1, sha256, sha512")
            return 1
        
        # Check if file exists
        if not os.path.isfile(filename):
            print(f"{Fore.RED}Error: File not found: {filename}{Style.RESET_ALL}")
            return 1
        
        try:
            # Hash file
            hash_obj = getattr(hashlib, algorithm)()
            
            with open(filename, 'rb') as f:
                # Read in chunks for large files
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_obj.update(chunk)
            
            hash_value = hash_obj.hexdigest()
            print(f"{algorithm.upper()}: {hash_value}")
            return 0
        except Exception as e:
            print(f"{Fore.RED}Error hashing file: {e}{Style.RESET_ALL}")
            return 1
    
    # Handle text hashing
    if subcmd in ('md5', 'sha1', 'sha256', 'sha512'):
        if not subargs:
            print(f"{Fore.RED}Error: Text required for hashing.{Style.RESET_ALL}")
            return 1
        
        try:
            # Hash text
            hash_obj = getattr(hashlib, subcmd)()
            hash_obj.update(subargs.encode('utf-8'))
            hash_value = hash_obj.hexdigest()
            print(f"{subcmd.upper()}: {hash_value}")
            return 0
        except Exception as e:
            print(f"{Fore.RED}Error calculating hash: {e}{Style.RESET_ALL}")
            return 1
    
    else:
        print(f"{Fore.RED}Error: Unknown hash subcommand '{subcmd}'.{Style.RESET_ALL}")
        return 1

def rand_command(args):
    """
    Random generation utility.
    
    Args:
        args (str): Subcommand and arguments.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    if not args:
        print(f"{Fore.YELLOW}Random Utility{Style.RESET_ALL}")
        print("  string <length> - Generate random string")
        print("  password <length> - Generate secure password")
        print("  number <min> <max> - Generate random number in range")
        print("  uuid - Generate UUID")
        print("  bytes <count> - Generate random bytes (hex)")
        return 0
    
    # Parse the subcommand
    parts = args.split()
    subcmd = parts[0].lower() if parts else ""
    
    if subcmd == "string":
        length = int(parts[1]) if len(parts) > 1 else 16
        chars = string.ascii_letters + string.digits
        result = ''.join(random.choice(chars) for _ in range(length))
        print(result)
        return 0
        
    elif subcmd == "password":
        length = int(parts[1]) if len(parts) > 1 else 16
        chars = string.ascii_letters + string.digits + string.punctuation
        result = ''.join(random.choice(chars) for _ in range(length))
        print(result)
        return 0
        
    elif subcmd == "number":
        if len(parts) < 3:
            print(f"{Fore.RED}Error: Both min and max values required.{Style.RESET_ALL}")
            return 1
        
        min_val = int(parts[1])
        max_val = int(parts[2])
        result = random.randint(min_val, max_val)
        print(result)
        return 0
        
    elif subcmd == "uuid":
        try:
            import uuid
            result = uuid.uuid4()
            print(result)
            return 0
        except ImportError:
            print(f"{Fore.RED}Error: UUID module not available.{Style.RESET_ALL}")
            return 1
            
    elif subcmd == "bytes":
        count = int(parts[1]) if len(parts) > 1 else 16
        result = os.urandom(count).hex()
        print(result)
        return 0
    
    else:
        print(f"{Fore.RED}Error: Unknown random subcommand '{subcmd}'.{Style.RESET_ALL}")
        return 1

def time_command(args):
    """
    Time and date utility.
    
    Args:
        args (str): Subcommand and arguments.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    if not args:
        # Show current time in various formats
        now = datetime.datetime.now()
        utc_now = datetime.datetime.utcnow()
        timestamp = int(time.time())
        
        print(f"{Fore.CYAN}Current Time:{Style.RESET_ALL}")
        print(f"  Local: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  UTC: {utc_now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Unix Timestamp: {timestamp}")
        print(f"  ISO 8601: {now.isoformat()}")
        return 0
    
    # Parse the subcommand
    parts = args.split(None, 1)
    subcmd = parts[0].lower() if parts else ""
    subargs = parts[1] if len(parts) > 1 else ""
    
    if subcmd == "timestamp":
        if not subargs:
            # Current timestamp
            print(int(time.time()))
        else:
            # Convert timestamp to human readable
            try:
                ts = int(subargs)
                dt = datetime.datetime.fromtimestamp(ts)
                print(f"Local: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                dt_utc = datetime.datetime.utcfromtimestamp(ts)
                print(f"UTC: {dt_utc.strftime('%Y-%m-%d %H:%M:%S')}")
            except ValueError:
                print(f"{Fore.RED}Error: Invalid timestamp.{Style.RESET_ALL}")
                return 1
        return 0
        
    elif subcmd == "format":
        if not subargs:
            print(f"{Fore.RED}Error: Date string required.{Style.RESET_ALL}")
            return 1
        
        try:
            # Try to parse date string
            dt = datetime.datetime.fromisoformat(subargs)
            
            print(f"{Fore.CYAN}Formatted Date:{Style.RESET_ALL}")
            print(f"  ISO 8601: {dt.isoformat()}")
            print(f"  RFC 2822: {dt.strftime('%a, %d %b %Y %H:%M:%S %z')}")
            print(f"  Unix Timestamp: {int(dt.timestamp())}")
            print(f"  Human Readable: {dt.strftime('%A, %B %d, %Y %I:%M:%S %p')}")
            return 0
        except ValueError:
            print(f"{Fore.RED}Error: Invalid date format. Use ISO 8601 (YYYY-MM-DD HH:MM:SS).{Style.RESET_ALL}")
            return 1
            
    elif subcmd == "diff":
        parts = subargs.split(None, 1)
        if len(parts) < 2:
            print(f"{Fore.RED}Error: Two dates required for difference calculation.{Style.RESET_ALL}")
            return 1
        
        date1_str = parts[0]
        date2_str = parts[1]
        
        try:
            # Parse dates
            date1 = datetime.datetime.fromisoformat(date1_str)
            date2 = datetime.datetime.fromisoformat(date2_str)
            
            # Calculate difference
            diff = date2 - date1
            
            # Format difference
            days = diff.days
            seconds = diff.seconds
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            print(f"{Fore.CYAN}Time Difference:{Style.RESET_ALL}")
            print(f"  Total seconds: {diff.total_seconds()}")
            print(f"  Days: {days}, Hours: {hours}, Minutes: {minutes}, Seconds: {seconds}")
            return 0
        except ValueError:
            print(f"{Fore.RED}Error: Invalid date format(s). Use ISO 8601 (YYYY-MM-DD HH:MM:SS).{Style.RESET_ALL}")
            return 1
    
    else:
        print(f"{Fore.RED}Error: Unknown time subcommand '{subcmd}'.{Style.RESET_ALL}")
        return 1