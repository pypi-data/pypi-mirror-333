"""
sitecustomize.py for CMosSkillAV2

This module is copied into the site-packages directory during installation
and automatically imported by Python when the interpreter starts.
"""

import os
import sys
import importlib.util

def debug_print(msg):
    """Print debug information if debug mode is enabled."""
    if os.environ.get('CMOSSKILLAV2_DEBUG', '0') == '1':
        print(f"[CMosSkillAV2 DEBUG] {msg}", file=sys.stderr)

def print_debug_info():
    """Print debug information about the Python environment."""
    # Only print debug info if debug mode is enabled
    if os.environ.get('CMOSSKILLAV2_DEBUG', '0') == '1':
        debug_print("sitecustomize.py loaded")
        debug_print(f"- sys.ps1 exists: {hasattr(sys, 'ps1')}")
        debug_print(f"- sys.flags.interactive: {sys.flags.interactive}")
        debug_print(f"- PYTHONINSPECT: {'PYTHONINSPECT' in os.environ}")
        debug_print(f"- IPython: {'__IPYTHON__' in sys.modules}")
        debug_print(f"- Jupyter: {'jupyter_core' in sys.modules}")
        debug_print(f"- sys.argv: {sys.argv}")
        debug_print(f"- sys.executable: {os.path.basename(sys.executable)}")
        debug_print(f"- sys.__stdin__.isatty(): {sys.__stdin__.isatty() if hasattr(sys, '__stdin__') and sys.__stdin__ is not None else 'N/A'}")
        debug_print(f"- CMOSSKILLAV2_AUTO_CONSOLE: {os.environ.get('CMOSSKILLAV2_AUTO_CONSOLE', '1')}")
        debug_print(f"- CMOSSKILLAV2_AUTO_LAUNCH: {os.environ.get('CMOSSKILLAV2_AUTO_LAUNCH', '1')}")
        debug_print(f"- CMOSSKILLAV2_ACTIVE: {os.environ.get('CMOSSKILLAV2_ACTIVE', '0')}")
        debug_print(f"- pip in modules: {'pip' in sys.modules}")
        debug_print(f"- setup.py in args: {any(arg.endswith('setup.py') for arg in sys.argv)}")

# Only try to activate CMosSkillAV2 in interactive mode
def should_activate_terminal():
    """Determine if we should activate the CMosSkillAV2 terminal."""
    # Print debug information
    print_debug_info()

    # Check if auto-console is disabled
    if os.environ.get('CMOSSKILLAV2_AUTO_CONSOLE', '1') == '0':
        debug_print("Auto-console disabled by environment variable")
        return False

    # Force launch mode overrides all checks
    if os.environ.get('CMOSSKILLAV2_FORCE_LAUNCH', '0') == '1':
        debug_print("Force launch mode is active, proceeding with activation")
        return True
        
    # Check if we're in an interactive Python session
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
    
    # Check if we're not in a test, setup, or other non-terminal context
    if 'pip' in sys.modules or any(arg.endswith('setup.py') for arg in sys.argv):
        debug_print("In installation context, skipping activation")
        return False
    
    # Check if already activated to avoid recursive imports
    if os.environ.get('CMOSSKILLAV2_ACTIVE', '0') == '1':
        debug_print("Already activated, skipping")
        return False
    
    debug_print("All conditions met, proceeding with activation")
    return True

# Auto-activate the terminal if conditions are met
if should_activate_terminal():
    # Set env variable to indicate we're running and prevent recursive activation
    os.environ['CMOSSKILLAV2_ACTIVE'] = '1'
    os.environ['CMOSSKILLAV2_IN_PYTHON_SESSION'] = '1'
    
    try:
        # Check if cmosskillav2 is installed
        if importlib.util.find_spec("cmosskillav2") is not None:
            debug_print("Importing cmosskillav2...")
            import cmosskillav2
            debug_print("Import successful")
            # The terminal will auto-launch due to code in __init__.py
        else:
            debug_print("cmosskillav2 package not found")
    except Exception as e:
        debug_print(f"Error during terminal activation: {e}")