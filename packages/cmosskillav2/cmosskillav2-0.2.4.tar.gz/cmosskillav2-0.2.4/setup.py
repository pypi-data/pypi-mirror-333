from setuptools import setup, find_packages
import os
from setuptools.command.install import install
from setuptools.command.develop import develop
import shutil
import importlib.util
import site
import sysconfig

# Define function to install sitecustomize.py
def install_sitecustomize():
    """Install the sitecustomize.py file to site-packages."""
    try:
        # Find the source file
        src_file = os.path.join(os.path.dirname(__file__), 'cmosskillav2', 'sitecustomize.py')
        
        # Find site-packages directory
        try:
            site_packages = site.getsitepackages()[0]
        except (AttributeError, IndexError):
            # Fallback for user installs
            site_packages = sysconfig.get_path('purelib')
        
        dst_file = os.path.join(site_packages, 'sitecustomize.py')
        
        # Copy the file with safety checks
        if os.path.exists(src_file):
            # Backup existing file if needed
            if os.path.exists(dst_file):
                with open(dst_file, 'r') as f:
                    content = f.read()
                    if 'CMosSkillAV2' not in content:
                        backup = dst_file + '.backup'
                        shutil.copy2(dst_file, backup)
                        print(f"Backed up existing sitecustomize.py to {backup}")
            
            # Copy our custom file
            shutil.copy2(src_file, dst_file)
            print(f"Installed sitecustomize.py to {dst_file}")
            return True
        else:
            print(f"Warning: source file {src_file} not found")
            return False
    except Exception as e:
        print(f"Error installing sitecustomize.py: {e}")
        return False

# Define function to install the auto-import .pth file
def install_auto_import_pth():
    """Create a .pth file that automatically imports cmosskillav2 on Python startup."""
    try:
        # Create pth file content directly to avoid importing cmosskillav2 module
        # during installation (which causes the "No module named 'cmosskillav2'" error)
        import os
        import site
        import sysconfig
        
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
        
        print(f"Successfully created auto-import .pth file at {pth_file}")
        return True
    except Exception as e:
        print(f"Error creating auto-import .pth file: {e}")
        return False

# Custom install command
class CustomInstall(install):
    def run(self):
        install.run(self)
        install_sitecustomize()
        install_auto_import_pth()

# Custom develop command
class CustomDevelop(develop):
    def run(self):
        develop.run(self)
        install_sitecustomize()
        install_auto_import_pth()

# Use setup.py for backward compatibility and to handle sitecustomize.py installation
# Main package configuration is in pyproject.toml
setup(
    cmdclass={
        'install': CustomInstall,
        'develop': CustomDevelop,
    },
)