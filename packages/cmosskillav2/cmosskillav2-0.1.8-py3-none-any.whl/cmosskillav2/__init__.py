"""
CMosSkillAV2 - Python Terminal Emulator with Enhanced Developer Utilities.

A feature-rich terminal emulator that provides file operations,
Python execution, and developer utilities.
"""

__version__ = "0.1.8"

# Imports
import sys
import os
import importlib.util

# Display a message when the package is imported
if not __name__.startswith('_') and 'pip' not in sys.modules and not any(arg.endswith('setup.py') for arg in sys.argv):
    is_interactive = hasattr(sys, 'ps1') or sys.flags.interactive
    
    # Display welcome message
    print("\033[1;36m")  # Bright cyan color
    print("╔════════════════════════════════════════════════════════╗")
    print("║ CMosSkillAV2 Terminal has been successfully installed! ║")
    
    # Check if we are in an interactive Python session
    auto_launch = os.environ.get('CMOSSKILLAV2_AUTO_LAUNCH', '1') == '1'
    
    if is_interactive and auto_launch:
        print("║                                                        ║")
        print("║ \033[1;33mLaunching terminal automatically...\033[1;36m                 ║") 
        print("╚════════════════════════════════════════════════════════╝")
        print("\033[0m")  # Reset color
        
        # Set env variable to indicate we're running in a Python session
        os.environ['CMOSSKILLAV2_IN_PYTHON_SESSION'] = '1'
        
        # Use importlib to avoid circular imports
        from .terminal import CMosSkillShell
        shell = CMosSkillShell()
        shell.print_welcome()
        shell.run()
    else:
        print("║                                                        ║")
        print("║ Please type \033[1;33mcmosskillav2\033[1;36m to activate the terminal      ║")
        print("╚════════════════════════════════════════════════════════╝")
        print("\033[0m")  # Reset color