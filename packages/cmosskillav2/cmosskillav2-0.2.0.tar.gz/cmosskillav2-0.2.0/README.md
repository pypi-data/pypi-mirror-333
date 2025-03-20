# CMosSkillAV2 Terminal Emulator

A Python package that provides an enhanced terminal emulator with built-in file operations, Python execution, and developer utilities.

## Features

- **File Operations**: Built-in commands for managing files and directories (cd, ls, mkdir, touch, rm, cat)
- **Python Execution**: Run Python scripts or execute Python code directly in the terminal
- **Package Management**: Manage Python packages with built-in pip integration
- **Syntax Highlighting**: Color-coded output for better readability
- **Tab Completion**: Command and path completion with Tab key
- **Command History**: Navigate through previously entered commands

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

CMosSkillAV2 offers two powerful auto-launch capabilities:

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

You can disable the auto-console feature by setting:

```bash
export CMOSSKILLAV2_AUTO_CONSOLE=0
```

Both auto-launch features are especially useful for enhancing Python REPL environments, IPython, and Jupyter notebooks with terminal capabilities.

## Available Commands

### File Operations
- `cd [directory]` - Change directory
- `ls [directory]` - List directory contents
- `mkdir [-p] directory` - Create directory
- `touch file [file2 ...]` - Create empty file(s)
- `rm [-r] file_or_directory` - Remove file(s) or directory
- `cat file [file2 ...]` - Display file contents

### Python Execution
- `python script.py [args]` - Execute Python script file
- `>>> [python_code]` - Execute Python code inline
- `pyshell` - Start interactive Python shell

### Package Management
- `pip install package` - Install Python package
- `pip uninstall package` - Uninstall Python package
- `pip list` - List installed packages
- `pip freeze` - Output installed packages in requirements format

### Shell Built-ins
- `help [command]` - Display help for commands
- `exit` or `quit` - Exit the shell
- `clear` - Clear the terminal screen

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.