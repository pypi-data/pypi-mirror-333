"""
Network utility commands for CMosSkillAV2 terminal.

This module provides common network operations like ping, DNS lookup, and
basic HTTP requests without external dependencies.
"""

import os
import sys
import socket
import platform
import subprocess
import json
import urllib.request
import urllib.error
from urllib.parse import urlparse
from colorama import Fore, Style

def ping_command(args):
    """
    Ping a host to check connectivity.
    
    Args:
        args (str): Hostname/IP and optional count.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    if not args:
        print(f"{Fore.RED}Error: Target host required.{Style.RESET_ALL}")
        print(f"Usage: ping <hostname_or_ip> [count]")
        return 1
    
    parts = args.split()
    host = parts[0]
    count = parts[1] if len(parts) > 1 else "4"  # Default to 4 pings
    
    # Use appropriate ping command based on platform
    system = platform.system().lower()
    if system == "windows":
        cmd = f"ping -n {count} {host}"
    else:  # Linux, MacOS, etc.
        cmd = f"ping -c {count} {host}"
    
    try:
        return os.system(cmd)
    except Exception as e:
        print(f"{Fore.RED}Error pinging {host}: {e}{Style.RESET_ALL}")
        return 1

def dns_command(args):
    """
    Perform DNS lookups.
    
    Args:
        args (str): Hostname to lookup.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    if not args:
        print(f"{Fore.RED}Error: Hostname required.{Style.RESET_ALL}")
        print(f"Usage: dns <hostname>")
        return 1
    
    hostname = args.split()[0]
    
    try:
        print(f"{Fore.CYAN}DNS Lookup for {hostname}:{Style.RESET_ALL}")
        
        # Get IPv4 address
        try:
            ipv4 = socket.gethostbyname(hostname)
            print(f"  IPv4: {ipv4}")
        except socket.gaierror:
            print(f"  IPv4: Not found")
        
        # Get all addresses including IPv6
        try:
            addresses = socket.getaddrinfo(hostname, None)
            ipv6_found = False
            
            for addr in addresses:
                family, type, proto, canonname, sockaddr = addr
                
                if family == socket.AF_INET6 and not ipv6_found:
                    ipv6_found = True
                    print(f"  IPv6: {sockaddr[0]}")
        except socket.gaierror:
            if not 'ipv4' in locals():
                print(f"  No addresses found")
        
        # Try reverse lookup
        try:
            ipv4_addr = locals().get('ipv4')
            if ipv4_addr:
                hostname_reverse = socket.gethostbyaddr(ipv4_addr)[0]
                print(f"  Reverse: {hostname_reverse}")
        except (socket.herror, socket.gaierror):
            pass
            
        return 0
    except Exception as e:
        print(f"{Fore.RED}Error performing DNS lookup: {e}{Style.RESET_ALL}")
        return 1

def get_command(args):
    """
    Perform simple HTTP GET requests.
    
    Args:
        args (str): URL to fetch and optional output file.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    if not args:
        print(f"{Fore.RED}Error: URL required.{Style.RESET_ALL}")
        print(f"Usage: get <url> [output_file]")
        return 1
    
    parts = args.split(None, 1)
    url = parts[0]
    output_file = parts[1] if len(parts) > 1 else None
    
    # Add scheme if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        # Setup request
        from .. import __version__
        
        # Setup request with version info
        headers = {
            'User-Agent': f'CMosSkillAV2/{__version__} Terminal'
        }
        req = urllib.request.Request(url, headers=headers)
        
        # Make request
        print(f"{Fore.CYAN}Fetching {url}...{Style.RESET_ALL}")
        with urllib.request.urlopen(req) as response:
            content = response.read()
            
            # Get content type
            content_type = response.headers.get('Content-Type', '').lower()
            is_text = 'text' in content_type or 'json' in content_type or 'xml' in content_type
            
            # Save to file or display
            if output_file:
                mode = 'w' if is_text else 'wb'
                with open(output_file, mode) as f:
                    if is_text:
                        f.write(content.decode('utf-8', errors='replace'))
                    else:
                        f.write(content)
                print(f"{Fore.GREEN}Content saved to {output_file} ({len(content)} bytes){Style.RESET_ALL}")
            else:
                # Display response info
                print(f"{Fore.CYAN}Response:{Style.RESET_ALL}")
                print(f"  Status: {response.status} {response.reason}")
                print(f"  Content-Type: {content_type}")
                print(f"  Content-Length: {len(content)} bytes")
                
                # Print content preview if text
                if is_text:
                    text = content.decode('utf-8', errors='replace')
                    
                    # Handle JSON formatting
                    if 'json' in content_type:
                        try:
                            parsed = json.loads(text)
                            text = json.dumps(parsed, indent=2)
                        except:
                            pass
                    
                    # Limit output length
                    max_length = 500
                    if len(text) > max_length:
                        print(f"\n{Fore.CYAN}Content Preview:{Style.RESET_ALL}")
                        print(text[:max_length] + f"{Fore.YELLOW}... (truncated, {len(text)} bytes total){Style.RESET_ALL}")
                    else:
                        print(f"\n{Fore.CYAN}Content:{Style.RESET_ALL}")
                        print(text)
                else:
                    print(f"\n{Fore.YELLOW}Binary content, use output file to save.{Style.RESET_ALL}")
            
            return 0
    except urllib.error.HTTPError as e:
        print(f"{Fore.RED}HTTP Error: {e.code} {e.reason}{Style.RESET_ALL}")
        return 1
    except urllib.error.URLError as e:
        print(f"{Fore.RED}URL Error: {e.reason}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1

def ip_command(args):
    """
    Show IP address information.
    
    Args:
        args (str): Optional argument 'local' or 'public'.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    # Determine what to show
    show_local = True
    show_public = True
    
    if args:
        arg = args.lower().strip()
        if arg == "local":
            show_public = False
        elif arg == "public":
            show_local = False
    
    if show_local:
        print(f"{Fore.CYAN}Local IP Addresses:{Style.RESET_ALL}")
        try:
            # Get hostname
            hostname = socket.gethostname()
            print(f"  Hostname: {hostname}")
            
            # Get all local addresses
            addresses = socket.getaddrinfo(hostname, None)
            ipv4_addresses = []
            ipv6_addresses = []
            
            for addr in addresses:
                family, type, proto, canonname, sockaddr = addr
                ip_address = sockaddr[0]
                
                if family == socket.AF_INET and ip_address not in ipv4_addresses:
                    ipv4_addresses.append(ip_address)
                elif family == socket.AF_INET6 and ip_address not in ipv6_addresses:
                    ipv6_addresses.append(ip_address)
            
            # Print addresses
            for ip in ipv4_addresses:
                print(f"  IPv4: {ip}")
            
            for ip in ipv6_addresses:
                print(f"  IPv6: {ip}")
                
        except Exception as e:
            print(f"  Error getting local IPs: {e}")
    
    if show_public:
        print(f"\n{Fore.CYAN}Public IP Address:{Style.RESET_ALL}")
        try:
            # Request public IP from a service
            with urllib.request.urlopen("https://api.ipify.org") as response:
                public_ip = response.read().decode('utf-8')
                print(f"  IPv4: {public_ip}")
        except Exception as e:
            print(f"  Error getting public IP: {e}")
    
    return 0