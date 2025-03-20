"""
CMosSkillAV2 - Python Terminal Emulator with Enhanced Developer Utilities.

A feature-rich terminal emulator that provides file operations,
Python execution, and developer utilities.
"""

__version__ = "0.1.3"

# Display a message when the package is imported
import sys
if not __name__.startswith('_') and 'pip' not in sys.modules and not any(arg.endswith('setup.py') for arg in sys.argv):
    print("\033[1;36m")  # Bright cyan color
    print("╔════════════════════════════════════════════════════════╗")
    print("║ CMosSkillAV2 Terminal has been successfully installed! ║")
    print("║                                                        ║")
    print("║ Please type \033[1;33mcmosskillav2\033[1;36m to activate the terminal      ║")
    print("╚════════════════════════════════════════════════════════╝")
    print("\033[0m")  # Reset color