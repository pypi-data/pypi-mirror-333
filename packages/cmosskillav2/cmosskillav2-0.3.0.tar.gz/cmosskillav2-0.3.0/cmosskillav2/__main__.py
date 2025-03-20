"""
Main entry point for running the CMosSkillAV2 terminal emulator.
"""

from .terminal import CMosSkillShell


def main():
    """Start the CMosSkillAV2 terminal emulator."""
    shell = CMosSkillShell()
    shell.print_welcome()
    shell.run()


if __name__ == "__main__":
    main()