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
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Find site-packages directory
        try:
            site_packages = site.getsitepackages()[0]
        except (AttributeError, IndexError):
            # Fallback for user installs
            site_packages = sysconfig.get_path('purelib')
        
        # Define the .pth file path
        pth_file = os.path.join(site_packages, 'cmosskillav2_auto.pth')
        
        # The content to write - Python code to run at startup
        # This is a special feature of .pth files - lines starting with "import"
        # are executed when Python starts
        pth_content = """# CMosSkillAV2 auto-activation PTH file
# Lines starting with "import" are executed at Python startup
import sys, os
# Only proceed if we're in an interactive mode and not during pip/setup operations
if (hasattr(sys, 'ps1') or 
    sys.flags.interactive or 
    'PYTHONINSPECT' in os.environ or 
    '__IPYTHON__' in sys.modules or
    os.environ.get('CMOSSKILLAV2_AUTO_LAUNCH', '1') == '1') and not any(p in sys.modules for p in ['pip', '_pytest']):
    # Only import if not already activated
    if os.environ.get('CMOSSKILLAV2_ACTIVE', '0') != '1':
        try:
            # Only attempt import if the package is available
            import importlib.util
            if importlib.util.find_spec("cmosskillav2") is not None:
                import cmosskillav2
        except Exception:
            pass
"""
        
        # Write the .pth file
        with open(pth_file, 'w') as f:
            f.write(pth_content)
        
        return True
    except Exception as e:
        print(f"Error creating auto-import .pth file: {e}")
        return False

if __name__ == "__main__":
    # This allows the module to be run directly for testing
    success = create_auto_import_pth()
    if success:
        print("Successfully created auto-import .pth file")
    else:
        print("Failed to create auto-import .pth file")