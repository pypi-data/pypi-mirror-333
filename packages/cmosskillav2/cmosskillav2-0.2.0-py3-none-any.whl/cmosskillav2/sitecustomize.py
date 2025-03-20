"""
sitecustomize.py for CMosSkillAV2

This module is copied into the site-packages directory during installation
and automatically imported by Python when the interpreter starts.
"""

import os
import sys

# Only try to activate CMosSkillAV2 in interactive mode
def should_activate_terminal():
    # Check if auto-console is disabled
    if os.environ.get('CMOSSKILLAV2_AUTO_CONSOLE', '1') == '0':
        return False
        
    # Check if we're in an interactive Python session
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
    
    # Check if we're not in a test, setup, or other non-terminal context
    not_installation = (
        'pip' not in sys.modules and 
        not any(arg.endswith('setup.py') for arg in sys.argv)
    )
    
    return is_interactive and not_installation

# Auto-activate the terminal if conditions are met
if should_activate_terminal():
    # Only import and activate if not already activated
    if not os.environ.get('CMOSSKILLAV2_ACTIVE'):
        os.environ['CMOSSKILLAV2_ACTIVE'] = '1'
        try:
            import cmosskillav2
            # The terminal will auto-launch due to code in __init__.py
        except ImportError:
            # Package isn't installed, so just continue with normal Python startup
            pass