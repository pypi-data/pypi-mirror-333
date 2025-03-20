"""
CMosSkillAV2 - Python Terminal Emulator with Enhanced Developer Utilities.

A feature-rich terminal emulator that provides file operations,
Python execution, and developer utilities.
"""

__version__ = "0.2.1"

# Imports
import sys
import os
import importlib.util

# Display a message when the package is imported
if not __name__.startswith('_') and 'pip' not in sys.modules and not any(arg.endswith('setup.py') for arg in sys.argv):
    # Enhanced detection of interactive mode
    # The key is to detect when Python is launched directly as a REPL
    is_interactive = (
        # Has prompt already set
        hasattr(sys, 'ps1') or
        # -i flag explicitly set
        sys.flags.interactive or
        # Environment variable for inspection set
        'PYTHONINSPECT' in os.environ or
        # IPython or Jupyter
        '__IPYTHON__' in sys.modules or
        'jupyter_core' in sys.modules or
        # IPython/Jupyter executables
        (os.path.basename(sys.argv[0]) in ('ipython', 'jupyter', 'jupyter-notebook') if len(sys.argv) > 0 else False) or
        # The most important check - Python started with no script arguments (REPL mode)
        (len(sys.argv) <= 1 or sys.argv[0] == '' or sys.argv[0] == '-c') and os.path.basename(sys.executable) == 'python'
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