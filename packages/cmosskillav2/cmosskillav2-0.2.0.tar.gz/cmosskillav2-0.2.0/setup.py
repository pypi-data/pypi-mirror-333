from setuptools import setup, find_packages
import os
from setuptools.command.install import install
from setuptools.command.develop import develop
import shutil
import importlib.util
import site

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
            import sysconfig
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

# Custom install command
class CustomInstall(install):
    def run(self):
        install.run(self)
        install_sitecustomize()

# Custom develop command
class CustomDevelop(develop):
    def run(self):
        develop.run(self)
        install_sitecustomize()

# Use setup.py for backward compatibility and to handle sitecustomize.py installation
# Main package configuration is in pyproject.toml
setup(
    cmdclass={
        'install': CustomInstall,
        'develop': CustomDevelop,
    },
)