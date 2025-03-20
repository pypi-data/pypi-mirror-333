# CMosSkillAV2 Terminal Emulator

A Python package that provides an enhanced cross-platform terminal emulator with built-in file operations, Python execution, developer utilities, network tools, and mobile platform support.

## Features

- **File Operations**: Built-in commands for managing files and directories (cd, ls, mkdir, touch, rm, cat, find)
- **Python Execution**: Run Python scripts or execute Python code directly in the terminal
- **Package Management**: Manage Python packages with built-in pip integration
- **Network Utilities**: Built-in network commands for connectivity testing and data retrieval (ping, dns, get, ip)
- **Developer Tools**: Utilities for common development tasks (json, base64, hash, rand, time)
- **System Monitoring**: Commands for system information and process management (sysinfo, proc, kill, disk)
- **Mobile Platform Support**: Special commands for Termux and Pydroid environments on Android
- **Cross-Platform Compatibility**: Works on Windows, macOS, Linux, and Android platforms
- **Syntax Highlighting**: Color-coded output for better readability
- **Tab Completion**: Command and path completion with Tab key
- **Command History**: Navigate through previously entered commands
- **Automatic Console Integration**: Seamlessly activates in interactive Python environments

## Installation

```bash
pip install cmosskillav2
```

## Usage

After installation, you can start the terminal emulator with:

```bash
cmosskillav2
```

Or you can run it as a module:

```bash
python -m cmosskillav2
```

### Auto-Launch Features

CMosSkillAV2 version 0.3.0 includes powerful and reliable auto-launch capabilities:

#### 1. Auto-Import Launch

When imported in interactive Python sessions, the terminal automatically launches:

```python
# In an interactive Python session
import cmosskillav2  # The terminal will automatically launch
```

You can disable this behavior by setting:

```bash
export CMOSSKILLAV2_AUTO_LAUNCH=0
```

#### 2. Auto-Console Launch

After installation, CMosSkillAV2 automatically activates whenever you start a new Python console/REPL without having to explicitly import it. This makes it instantly available in any Python interactive session.

This works in:
- Standard Python REPL (`python` without arguments)
- Interactive Python sessions (`python -i script.py`)
- IPython and Jupyter environments
- Any Python environment with PYTHONINSPECT set

You can disable the auto-console feature by setting:

```bash
export CMOSSKILLAV2_AUTO_CONSOLE=0
```

Both auto-launch features are especially useful for enhancing Python REPL environments, IPython, and Jupyter notebooks with terminal capabilities.

#### How Auto-Console Works

The package uses a dual approach for maximum reliability:

1. **sitecustomize.py**: Installed in the site-packages directory, this module is automatically imported when Python starts. It detects interactive mode and can trigger the terminal.

2. **.pth file mechanism**: A special `.pth` file with embedded Python code that executes when Python starts, providing a secondary activation method.

The system intelligently examines the Python environment to determine if it's appropriate to launch the terminal, avoiding activation during package installation, testing, or when running scripts non-interactively.

#### Advanced Configuration Options

CMosSkillAV2 provides several environment variables to control its behavior:

```bash
# Disable automatic launch when importing the package
export CMOSSKILLAV2_AUTO_LAUNCH=0

# Disable automatic launch in Python console
export CMOSSKILLAV2_AUTO_CONSOLE=0

# Enable debug output for tracing activation logic
export CMOSSKILLAV2_DEBUG=1

# Force terminal launch even in non-interactive mode (for testing)
export CMOSSKILLAV2_FORCE_LAUNCH=1
```

#### Debugging Auto-Launch Features

You can enable debugging output for the auto-launch functionality by setting:

```bash
export CMOSSKILLAV2_DEBUG=1
```

This will display detailed information about the Python environment and the decision-making process for auto-launching the terminal.

#### Demo Scripts

The package includes demo scripts that show how the auto-launch features work:

```bash
# Display auto-launch capabilities and configuration options
python demo_autolaunch.py

# Test interactive mode (terminal should launch after script completes)
python -i demo_autolaunch.py

# Test auto-launch detection and troubleshooting
python test_auto_console.py

# Test with debug output
CMOSSKILLAV2_DEBUG=1 python -i test_auto_console.py
```

## Available Commands

### File Operations
- `cd [directory]` - Change directory
- `ls [directory]` - List directory contents
- `mkdir [-p] directory` - Create directory
- `touch file [file2 ...]` - Create empty file(s)
- `rm [-r] file_or_directory` - Remove file(s) or directory
- `cat file [file2 ...]` - Display file contents
- `find pattern [path]` - Find files and directories matching a pattern

### Python Execution
- `python script.py [args]` - Execute Python script file
- `>>> [python_code]` - Execute Python code inline
- `pyshell` - Start interactive Python shell

### Package Management
- `pip install package` - Install Python package
- `pip uninstall package` - Uninstall Python package
- `pip list` - List installed packages
- `pip freeze` - Output installed packages in requirements format

### Network Utilities
- `ping host [count]` - Ping a host to check connectivity
- `dns hostname` - Perform DNS lookup for a hostname
- `get url [output_file]` - Perform HTTP GET request
- `ip [local|public]` - Show IP address information

### Developer Tools
- `json format|validate file_or_text` - Format or validate JSON
- `base64 encode|decode text` - Encode or decode Base64
- `hash md5|sha1|sha256 text` - Generate hash for text
- `rand int|float|string [options]` - Generate random values
- `time [format]` - Display current date and time

### System Utilities
- `sysinfo` - Display system information
- `proc [filter]` - List running processes
- `kill pid_or_name` - Terminate a process
- `disk [path]` - Show disk usage information

### Mobile Platform Tools
- `termux [command]` - Termux-specific utilities
- `pydroid [command]` - Pydroid-specific utilities
- `device` - Show device information
- `battery` - Display battery status (if available)

### Shell Built-ins
- `help [command]` - Display help for commands
- `exit` or `quit` - Exit the shell
- `clear` - Clear the terminal screen
- `updates` - Check for daily updates and tips

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.