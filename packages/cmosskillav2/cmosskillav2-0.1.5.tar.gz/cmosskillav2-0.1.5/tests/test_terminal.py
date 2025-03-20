"""
Tests for the Ptermy terminal core functionality.
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from ptermy.terminal import PtermyShell


class TestPtermyShell(unittest.TestCase):
    """Test cases for the PtermyShell class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.TemporaryDirectory()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir.name)
        
        # Initialize shell with mocked components
        with patch('ptermy.terminal.HistoryManager'):
            with patch('ptermy.terminal.PtermyCompleter'):
                with patch('readline.set_completer'):
                    with patch('readline.parse_and_bind'):
                        self.shell = PtermyShell()
    
    def tearDown(self):
        """Clean up after tests."""
        os.chdir(self.old_cwd)
        self.test_dir.cleanup()
    
    def test_parse_command(self):
        """Test command parsing."""
        # Test basic command
        cmd, args = self.shell.parse_command("ls -a")
        self.assertEqual(cmd, "ls")
        self.assertEqual(args, "-a")
        
        # Test command with no args
        cmd, args = self.shell.parse_command("clear")
        self.assertEqual(cmd, "clear")
        self.assertEqual(args, "")
        
        # Test inline Python
        cmd, args = self.shell.parse_command(">>> print('test')")
        self.assertEqual(cmd, "python_inline")
        self.assertEqual(args, "print('test')")
        
        # Test empty input
        cmd, args = self.shell.parse_command("  ")
        self.assertIsNone(cmd)
        self.assertIsNone(args)
    
    @patch('builtins.print')  
    def test_show_help(self, mock_print):
        """Test help command."""
        # Test general help
        result = self.shell.show_help()
        self.assertEqual(result, 0)
        
        # Test specific command help
        result = self.shell.show_help("ls")
        self.assertEqual(result, 0)
        
        # Test invalid command help
        result = self.shell.show_help("invalid_command")
        self.assertEqual(result, 1)
    
    @patch('builtins.print')
    @patch('sys.exit')
    def test_exit_shell(self, mock_exit, mock_print):
        """Test exit command."""
        self.shell.exit_shell()
        mock_exit.assert_called_once_with(0)
    
    @patch('os.system')
    def test_clear_screen(self, mock_system):
        """Test clear screen command."""
        result = self.shell.clear_screen()
        self.assertEqual(result, 0)
        mock_system.assert_called_once()


if __name__ == '__main__':
    unittest.main()
