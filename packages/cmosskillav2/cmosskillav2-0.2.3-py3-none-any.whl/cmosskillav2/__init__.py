"""
CMosSkillAV2 - Python Terminal Emulator with Enhanced Developer Utilities.

A feature-rich terminal emulator that provides file operations,
Python execution, and developer utilities.
"""

__version__ = "0.2.3"

# Imports
import sys
import os
import importlib.util

# Debug function
def debug_print(msg):
    """Print debug information if debug mode is enabled."""
    if os.environ.get('CMOSSKILLAV2_DEBUG', '0') == '1':
        print(f"[CMosSkillAV2 DEBUG] {msg}", file=sys.stderr)

# Auto-activation logic for when the package is imported
def auto_activate():
    """Auto-activate the terminal if conditions are met."""
    debug_print("Package imported, checking activation conditions")
    
    # Skip activation during installation or non-interactive mode
    if (__name__.startswith('_') or 
        'pip' in sys.modules or 
        any(arg.endswith('setup.py') for arg in sys.argv)):
        debug_print("Skipping activation during installation process")
        return False
    
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
        (len(sys.argv) <= 1 or sys.argv[0] == '' or sys.argv[0] == '-c')
    )
    
    if not is_interactive:
        debug_print("Not in interactive mode, skipping activation")
        return False
    
    # Check if auto-launch is enabled via environment variable
    auto_launch = os.environ.get('CMOSSKILLAV2_AUTO_LAUNCH', '1') == '1'
    if not auto_launch:
        debug_print("Auto-launch disabled by environment variable")
        return False
    
    # Check if already activated to avoid recursive imports
    if os.environ.get('CMOSSKILLAV2_ACTIVE', '0') == '1':
        debug_print("Already activated, skipping")
        return False
    
    debug_print("All conditions met, proceeding with activation")
    return True

# Display a message when the package is imported
if auto_activate():
    # Display welcome message
    print("\033[1;36m")  # Bright cyan color
    print("╔════════════════════════════════════════════════════════╗")
    print("║ CMosSkillAV2 Terminal has been successfully installed! ║")
    print("║                                                        ║")
    print("║ \033[1;33mLaunching terminal automatically...\033[1;36m                 ║") 
    print("╚════════════════════════════════════════════════════════╝")
    print("\033[0m")  # Reset color
    
    # Set env variables to indicate we're running and prevent recursive activation
    os.environ['CMOSSKILLAV2_IN_PYTHON_SESSION'] = '1'
    os.environ['CMOSSKILLAV2_ACTIVE'] = '1'
    
    try:
        # Use imports here to avoid circular imports
        from .terminal import CMosSkillShell
        shell = CMosSkillShell()
        shell.print_welcome()
        shell.run()
    except Exception as e:
        debug_print(f"Error during terminal activation: {e}")
else:
    # Only show welcome message in specific contexts, not during every import
    if not __name__.startswith('_') and 'pip' not in sys.modules and not any(arg.endswith('setup.py') for arg in sys.argv):
        print("\033[1;36m")  # Bright cyan color
        print("╔════════════════════════════════════════════════════════╗")
        print("║ CMosSkillAV2 Terminal has been successfully installed! ║")
        print("║                                                        ║")
        print("║ Please type \033[1;33mcmosskillav2\033[1;36m to activate the terminal      ║")
        print("╚════════════════════════════════════════════════════════╝")
        print("\033[0m")  # Reset color