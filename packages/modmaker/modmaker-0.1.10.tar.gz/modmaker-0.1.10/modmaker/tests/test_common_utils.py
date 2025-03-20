"""
Unit tests for _common_utils.py
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys
import tempfile
import shutil

# Add the parent directory to the path so Python can find the modules
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import module directly using relative imports
from _common_utils import (
    exit_with_code,
    ensure_directory,
    copy_directory_contents,
)


class TestCommonUtils(unittest.TestCase):
    """Test cases for common utilities"""

    @patch("sys.exit")
    def test_exit_with_code_no_message(self, mock_exit):
        """Test exit with code and no message"""
        exit_with_code(1)
        mock_exit.assert_called_once_with(1)

    @patch("sys.exit")
    def test_exit_with_code_with_message(self, mock_exit):
        """Test exit with code and message"""
        # We can't easily mock the logger since it's created at import time
        # So we'll just verify that sys.exit is called correctly
        exit_with_code(1, "Error message")
        mock_exit.assert_called_once_with(1)

    def test_ensure_directory_exists(self):
        """Test ensure_directory when directory exists"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Directory already exists
            result = ensure_directory(temp_dir)
            self.assertTrue(result)
            self.assertTrue(os.path.isdir(temp_dir))

    def test_ensure_directory_create(self):
        """Test ensure_directory creates directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            new_dir = os.path.join(temp_dir, "new_dir")
            
            # Directory doesn't exist yet
            self.assertFalse(os.path.exists(new_dir))
            
            # Should create the directory
            result = ensure_directory(new_dir)
            self.assertTrue(result)
            self.assertTrue(os.path.isdir(new_dir))

    @patch("os.makedirs")
    def test_ensure_directory_error(self, mock_makedirs):
        """Test ensure_directory with error"""
        mock_makedirs.side_effect = PermissionError("Permission denied")
        
        # Should handle the error and return False
        result = ensure_directory("/some/path")
        self.assertFalse(result)

    def test_copy_directory_contents(self):
        """Test copying directory contents"""
        # Create source directory with some files
        with tempfile.TemporaryDirectory() as src_dir:
            with tempfile.TemporaryDirectory() as dst_dir:
                # Create a file in source
                src_file = os.path.join(src_dir, "test.txt")
                with open(src_file, "w") as f:
                    f.write("test content")
                
                # Create a subdirectory with a file
                src_subdir = os.path.join(src_dir, "subdir")
                os.makedirs(src_subdir)
                src_subfile = os.path.join(src_subdir, "subfile.txt")
                with open(src_subfile, "w") as f:
                    f.write("subfile content")
                
                # Copy contents
                copy_directory_contents(src_dir, dst_dir)
                
                # Verify files were copied
                self.assertTrue(os.path.exists(os.path.join(dst_dir, "test.txt")))
                self.assertTrue(os.path.exists(os.path.join(dst_dir, "subdir", "subfile.txt")))
                
                # Verify content is correct
                with open(os.path.join(dst_dir, "test.txt"), "r") as f:
                    self.assertEqual(f.read(), "test content")
                with open(os.path.join(dst_dir, "subdir", "subfile.txt"), "r") as f:
                    self.assertEqual(f.read(), "subfile content")

    @patch("shutil.copy2")
    def test_copy_directory_contents_error(self, mock_copy2):
        """Test error handling in copy_directory_contents"""
        mock_copy2.side_effect = PermissionError("Permission denied")
        
        with tempfile.TemporaryDirectory() as src_dir:
            with tempfile.TemporaryDirectory() as dst_dir:
                # Create a file in source
                src_file = os.path.join(src_dir, "test.txt")
                with open(src_file, "w") as f:
                    f.write("test content")
                
                # This should not raise an exception despite the error
                copy_directory_contents(src_dir, dst_dir)


if __name__ == "__main__":
    unittest.main()