"""
Tests for the Ptermy command implementations.
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from ptermy.commands.file_operations import cd_command, ls_command, mkdir_command, touch_command, rm_command, cat_command
from ptermy.commands.python_execution import execute_python_script, execute_python_inline


class TestFileOperations(unittest.TestCase):
    """Test cases for file operation commands."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.TemporaryDirectory()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir.name)
        
        # Create some test files
        with open('test_file.txt', 'w') as f:
            f.write('Test content')
        
        with open('test_script.py', 'w') as f:
            f.write('print("Hello from test script")')
    
    def tearDown(self):
        """Clean up after tests."""
        os.chdir(self.old_cwd)
        self.test_dir.cleanup()
    
    @patch('builtins.print')
    def test_cd_command(self, mock_print):
        """Test changing directories."""
        # Test cd to subdirectory
        os.mkdir('subdir')
        result = cd_command('subdir')
        self.assertEqual(result, 0)
        self.assertEqual(os.path.basename(os.getcwd()), 'subdir')
        
        # Test cd with invalid directory
        result = cd_command('nonexistent')
        self.assertEqual(result, 1)
    
    @patch('builtins.print')
    def test_mkdir_command(self, mock_print):
        """Test making directories."""
        # Test creating single directory
        result = mkdir_command('new_dir')
        self.assertEqual(result, 0)
        self.assertTrue(os.path.isdir('new_dir'))
        
        # Test creating nested directories with -p
        result = mkdir_command('-p parent/child/grandchild')
        self.assertEqual(result, 0)
        self.assertTrue(os.path.isdir('parent/child/grandchild'))
    
    @patch('builtins.print')
    def test_touch_command(self, mock_print):
        """Test creating files."""
        # Test creating new file
        result = touch_command('new_file.txt')
        self.assertEqual(result, 0)
        self.assertTrue(os.path.exists('new_file.txt'))
        
        # Test creating multiple files
        result = touch_command('file1.txt file2.txt')
        self.assertEqual(result, 0)
        self.assertTrue(os.path.exists('file1.txt'))
        self.assertTrue(os.path.exists('file2.txt'))
    
    @patch('builtins.print')
    def test_rm_command(self, mock_print):
        """Test removing files and directories."""
        # Test removing file
        touch_command('to_remove.txt')
        result = rm_command('to_remove.txt')
        self.assertEqual(result, 0)
        self.assertFalse(os.path.exists('to_remove.txt'))
        
        # Test removing directory
        os.mkdir('dir_to_remove')
        # Should fail without -r
        result = rm_command('dir_to_remove')
        self.assertEqual(result, 1)
        # Should succeed with -r
        result = rm_command('-r dir_to_remove')
        self.assertEqual(result, 0)
        self.assertFalse(os.path.exists('dir_to_remove'))
    
    @patch('builtins.print')
    def test_cat_command(self, mock_print):
        """Test displaying file contents."""
        # Test displaying text file
        result = cat_command('test_file.txt')
        self.assertEqual(result, 0)
        
        # Test displaying nonexistent file
        result = cat_command('nonexistent.txt')
        self.assertEqual(result, 1)


class TestPythonExecution(unittest.TestCase):
    """Test cases for Python execution commands."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.TemporaryDirectory()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir.name)
        
        # Create test Python script
        with open('test_script.py', 'w') as f:
            f.write('print("Hello from test script")')
    
    def tearDown(self):
        """Clean up after tests."""
        os.chdir(self.old_cwd)
        self.test_dir.cleanup()
    
    @patch('builtins.print')
    @patch('subprocess.run')
    def test_execute_python_script(self, mock_run, mock_print):
        """Test executing Python scripts."""
        # Configure subprocess mock
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        # Test executing a script
        result = execute_python_script('test_script.py')
        self.assertEqual(result, 0)
        mock_run.assert_called_once()
        
        # Test executing nonexistent script
        result = execute_python_script('nonexistent.py')
        self.assertEqual(result, 1)
    
    @patch('builtins.print')
    def test_execute_python_inline(self, mock_print):
        """Test executing inline Python code."""
        # Test simple expression
        result = execute_python_inline('1 + 1')
        self.assertEqual(result, 0)
        
        # Test syntax error
        result = execute_python_inline('1 +')
        self.assertEqual(result, 1)
        
        # Test exception
        result = execute_python_inline('1/0')
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
