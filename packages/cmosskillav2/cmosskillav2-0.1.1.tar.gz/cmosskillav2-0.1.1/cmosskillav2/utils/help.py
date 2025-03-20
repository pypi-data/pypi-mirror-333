"""
Help system for the CMosSkillAV2 terminal.

This module provides help documentation for all commands.
"""

from colorama import Fore, Style

# Help documentation for commands
HELP_DOCS = {
    # File operations
    'cd': {
        'syntax': 'cd [directory]',
        'description': 'Change the current working directory.',
        'examples': [
            'cd Documents',
            'cd ..',
            'cd ~',
        ]
    },
    'ls': {
        'syntax': 'ls [directory]',
        'description': 'List directory contents with color coding.',
        'examples': [
            'ls',
            'ls Documents',
            'ls -a',  # Shows hidden files
        ]
    },
    'mkdir': {
        'syntax': 'mkdir [-p] directory',
        'description': 'Create a new directory.',
        'options': [
            '-p: Create parent directories as needed',
        ],
        'examples': [
            'mkdir new_folder',
            'mkdir -p parent/child/grandchild',
        ]
    },
    'touch': {
        'syntax': 'touch file [file2 ...]',
        'description': 'Create empty file(s) or update timestamps of existing files.',
        'examples': [
            'touch newfile.txt',
            'touch file1.py file2.py file3.py',
        ]
    },
    'rm': {
        'syntax': 'rm [-r] file_or_directory',
        'description': 'Remove files or directories.',
        'options': [
            '-r: Recursively remove directories and their contents',
        ],
        'examples': [
            'rm file.txt',
            'rm -r directory',
        ]
    },
    'cat': {
        'syntax': 'cat file [file2 ...]',
        'description': 'Display the contents of files.',
        'examples': [
            'cat file.txt',
            'cat file1.py file2.py',
        ]
    },
    
    # Python execution
    'python': {
        'syntax': 'python script.py [args]',
        'description': 'Execute a Python script file.',
        'examples': [
            'python script.py',
            'python script.py arg1 arg2',
        ]
    },
    'py': {
        'syntax': '>>> [python_code]',
        'description': 'Execute Python code inline.',
        'examples': [
            '>>> print("Hello, world!")',
            '>>> import math; print(math.pi)',
        ]
    },
    'pyshell': {
        'syntax': 'pyshell',
        'description': 'Start an interactive Python shell.',
        'examples': [
            'pyshell',
        ]
    },
    
    # Package management
    'pip': {
        'syntax': 'pip command [options]',
        'description': 'Manage Python packages with pip.',
        'subcommands': [
            'install: Install packages',
            'uninstall: Uninstall packages',
            'freeze: Output installed packages',
            'list: List installed packages',
            'show: Show information about installed packages',
            'search: Search PyPI for packages',
        ],
        'examples': [
            'pip install requests',
            'pip uninstall requests',
            'pip list',
            'pip freeze > requirements.txt',
        ]
    },
    
    # Shell built-ins
    'help': {
        'syntax': 'help [command]',
        'description': 'Display help for commands.',
        'examples': [
            'help',
            'help cd',
            'help pip',
        ]
    },
    'exit': {
        'syntax': 'exit',
        'description': 'Exit the shell.',
        'examples': [
            'exit',
        ]
    },
    'quit': {
        'syntax': 'quit',
        'description': 'Alias for exit - quit the shell.',
        'examples': [
            'quit',
        ]
    },
    'clear': {
        'syntax': 'clear',
        'description': 'Clear the terminal screen.',
        'examples': [
            'clear',
        ]
    },
}

def show_help(topic=None, commands=None):
    """
    Display help information for commands.
    
    Args:
        topic (str, optional): The command to show help for.
        commands (dict, optional): Dictionary of available commands.
        
    Returns:
        int: 0 for success, 1 for failure
    """
    if topic is None or topic.strip() == '':
        # Show general help
        print(f"{Fore.GREEN}Available Commands:{Style.RESET_ALL}")
        print("\nFile Operations:")
        print("  cd, ls, mkdir, touch, rm, cat")
        print("\nPython Execution:")
        print("  python, py (prefix with >>>), pyshell")
        print("\nPackage Management:")
        print("  pip")
        print("\nShell Built-ins:")
        print("  help, exit, quit, clear")
        print(f"\nUse {Fore.YELLOW}help command{Style.RESET_ALL} for detailed help on a specific command.")
        return 0
    
    # Show help for specific command
    topic = topic.strip().lower()
    if topic in HELP_DOCS:
        doc = HELP_DOCS[topic]
        
        # Print command syntax
        print(f"{Fore.GREEN}Command:{Style.RESET_ALL} {topic}")
        print(f"{Fore.GREEN}Syntax:{Style.RESET_ALL} {doc['syntax']}")
        
        # Print description
        print(f"{Fore.GREEN}Description:{Style.RESET_ALL}")
        print(f"  {doc['description']}")
        
        # Print options if available
        if 'options' in doc:
            print(f"{Fore.GREEN}Options:{Style.RESET_ALL}")
            for option in doc['options']:
                print(f"  {option}")
        
        # Print subcommands if available
        if 'subcommands' in doc:
            print(f"{Fore.GREEN}Subcommands:{Style.RESET_ALL}")
            for subcmd in doc['subcommands']:
                print(f"  {subcmd}")
        
        # Print examples
        if 'examples' in doc:
            print(f"{Fore.GREEN}Examples:{Style.RESET_ALL}")
            for example in doc['examples']:
                print(f"  {example}")
        
        return 0
    else:
        print(f"{Fore.RED}No help available for '{topic}'{Style.RESET_ALL}")
        print(f"Type {Fore.YELLOW}help{Style.RESET_ALL} to see all available commands.")
        return 1