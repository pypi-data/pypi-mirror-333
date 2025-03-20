"""
sitecustomize.py for CMosSkillAV2

This module is copied into the site-packages directory during installation
and automatically imported by Python when the interpreter starts.
"""

import os
import sys

def print_debug_info():
    """Print debug information about the Python environment."""
    # Only print debug info if debug mode is enabled
    if os.environ.get('CMOSSKILLAV2_DEBUG', '0') == '1':
        print("\nDEBUG: sitecustomize.py loaded", file=sys.stderr)
        print(f"- sys.ps1 exists: {hasattr(sys, 'ps1')}", file=sys.stderr)
        print(f"- sys.flags.interactive: {sys.flags.interactive}", file=sys.stderr)
        print(f"- PYTHONINSPECT: {'PYTHONINSPECT' in os.environ}", file=sys.stderr)
        print(f"- IPython: {'__IPYTHON__' in sys.modules}", file=sys.stderr)
        print(f"- Jupyter: {'jupyter_core' in sys.modules}", file=sys.stderr)
        print(f"- sys.argv: {sys.argv}", file=sys.stderr)
        print(f"- sys.executable: {os.path.basename(sys.executable)}", file=sys.stderr)
        print(f"- sys.__stdin__.isatty(): {sys.__stdin__.isatty() if hasattr(sys, '__stdin__') and sys.__stdin__ is not None else 'N/A'}", file=sys.stderr)
        print(f"- CMOSSKILLAV2_AUTO_CONSOLE: {os.environ.get('CMOSSKILLAV2_AUTO_CONSOLE', '1')}", file=sys.stderr)
        print(f"- CMOSSKILLAV2_AUTO_LAUNCH: {os.environ.get('CMOSSKILLAV2_AUTO_LAUNCH', '1')}", file=sys.stderr)
        print(f"- CMOSSKILLAV2_DEBUG: {os.environ.get('CMOSSKILLAV2_DEBUG', '0')}", file=sys.stderr)
        print(f"- CMOSSKILLAV2_ACTIVE: {os.environ.get('CMOSSKILLAV2_ACTIVE', '0')}", file=sys.stderr)
        print(f"- pip in modules: {'pip' in sys.modules}", file=sys.stderr)
        print(f"- setup.py in args: {any(arg.endswith('setup.py') for arg in sys.argv)}", file=sys.stderr)
        print("", file=sys.stderr)

# Only try to activate CMosSkillAV2 in interactive mode
def should_activate_terminal():
    """Determine if we should activate the CMosSkillAV2 terminal."""
    # Print debug information
    print_debug_info()

    # Check if auto-console is disabled
    if os.environ.get('CMOSSKILLAV2_AUTO_CONSOLE', '1') == '0':
        print("Auto-console disabled by environment variable", file=sys.stderr)
        return False
        
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
        (len(sys.argv) <= 1 or sys.argv[0] == '' or sys.argv[0] == '-c') and os.path.basename(sys.executable) == 'python'
    )
    
    # Check if we're not in a test, setup, or other non-terminal context
    not_installation = (
        'pip' not in sys.modules and 
        not any(arg.endswith('setup.py') for arg in sys.argv)
    )
    
    result = is_interactive and not_installation
    print(f"Should activate terminal: {result}", file=sys.stderr)
    return result

# Auto-activate the terminal if conditions are met
if should_activate_terminal():
    # Only import and activate if not already activated
    if not os.environ.get('CMOSSKILLAV2_ACTIVE'):
        print("Setting CMOSSKILLAV2_ACTIVE=1", file=sys.stderr)
        os.environ['CMOSSKILLAV2_ACTIVE'] = '1'
        try:
            print("Importing cmosskillav2...", file=sys.stderr)
            import cmosskillav2
            print("Import successful", file=sys.stderr)
            # The terminal will auto-launch due to code in __init__.py
        except ImportError as e:
            # Package isn't installed, so just continue with normal Python startup
            print(f"Import error: {e}", file=sys.stderr)
    else:
        print("CMOSSKILLAV2_ACTIVE is already set", file=sys.stderr)