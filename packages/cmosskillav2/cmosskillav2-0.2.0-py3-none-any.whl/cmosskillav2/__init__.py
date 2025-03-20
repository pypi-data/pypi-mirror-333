"""
CMosSkillAV2 - Python Terminal Emulator with Enhanced Developer Utilities.

A feature-rich terminal emulator that provides file operations,
Python execution, and developer utilities.
"""

__version__ = "0.2.0"

# Imports
import sys
import os
import importlib.util

# Display a message when the package is imported
if not __name__.startswith('_') and 'pip' not in sys.modules and not any(arg.endswith('setup.py') for arg in sys.argv):
    # Better detection of interactive mode
    # Check both standard flags and interpret the calling context more carefully
    is_interactive = (
        hasattr(sys, 'ps1') or                # Has prompt
        sys.flags.interactive or              # -i flag
        'PYTHONINSPECT' in os.environ or      # PYTHONINSPECT set
        '__IPYTHON__' in sys.modules or       # IPython
        'jupyter_core' in sys.modules or      # Jupyter
        os.path.basename(sys.argv[0]) in ('ipython', 'jupyter', 'jupyter-notebook') or
        # Check if run in a way that suggests interactive use
        len(sys.argv) <= 1 and os.path.basename(sys.executable) == 'python'
    )
    
    # Display welcome message
    print("\033[1;36m")  # Bright cyan color
    print("╔════════════════════════════════════════════════════════╗")
    print("║ CMosSkillAV2 Terminal has been successfully installed! ║")
    
    # Check if auto-launch is enabled via environment variable
    auto_launch = os.environ.get('CMOSSKILLAV2_AUTO_LAUNCH', '1') == '1'
    
    # Start the terminal automatically in interactive mode if auto-launch is enabled
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