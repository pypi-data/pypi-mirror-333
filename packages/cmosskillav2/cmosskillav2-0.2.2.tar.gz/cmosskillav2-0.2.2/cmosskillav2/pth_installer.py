"""
Path file installer for CMosSkillAV2.

This module creates a .pth file in the site-packages directory
that will automatically import cmosskillav2 when Python starts.
"""

import os
import site
import sys
import sysconfig

def create_auto_import_pth():
    """
    Create a .pth file that will automatically import cmosskillav2.
    
    The .pth file has special behavior: any line starting with 'import '
    will be executed when Python starts.
    """
    try:
        # Find site-packages directory
        try:
            site_packages = site.getsitepackages()[0]
        except (AttributeError, IndexError):
            # Fallback for user installs
            site_packages = sysconfig.get_path('purelib')
        
        # Create the .pth file content
        content = """# Auto-import CMosSkillAV2
import sys, os; 
CMOSSKILLAV2_AUTO_CONSOLE = os.environ.get('CMOSSKILLAV2_AUTO_CONSOLE', '1');
CMOSSKILLAV2_DEBUG = os.environ.get('CMOSSKILLAV2_DEBUG', '0');
exec_mode = (hasattr(sys, 'ps1') or sys.flags.interactive or 'PYTHONINSPECT' in os.environ or '__IPYTHON__' in sys.modules);
not_install_mode = (not 'pip' in sys.modules and not any(arg.endswith('setup.py') for arg in sys.argv));
if CMOSSKILLAV2_AUTO_CONSOLE == '1' and exec_mode and not_install_mode and not os.environ.get('CMOSSKILLAV2_ACTIVE'):
    os.environ['CMOSSKILLAV2_ACTIVE'] = '1';
    if CMOSSKILLAV2_DEBUG == '1': print('Auto-importing CMosSkillAV2');
    try: import cmosskillav2
    except ImportError as e: pass
"""
        
        # Write the .pth file
        pth_file = os.path.join(site_packages, 'cmosskillav2_auto.pth')
        with open(pth_file, 'w') as f:
            f.write(content)
        
        print(f"Created auto-import .pth file at: {pth_file}")
        return True
        
    except Exception as e:
        print(f"Error creating .pth file: {e}")
        return False

if __name__ == "__main__":
    create_auto_import_pth()