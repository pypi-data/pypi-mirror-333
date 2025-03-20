"""
Unit tests for _logger.py
"""

import unittest
from unittest.mock import patch, MagicMock
import logging

# Add the parent directory to the path so Python can find the modules
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import module directly using relative imports
from _logger import (
    init_modmaker_cli_logger,
    AppFilter,
)


class TestLogger(unittest.TestCase):
    """Test cases for logger module"""

    def test_app_filter(self):
        """Test AppFilter class"""
        # Create a test record
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname=__file__,
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        # Apply filter
        app_filter = AppFilter()
        result = app_filter.filter(record)
        
        # Check that filter returns True
        self.assertTrue(result)
        
        # Check that record is modified with color_loglevel attribute
        self.assertTrue(hasattr(record, 'color_loglevel'))

    def test_init_modmaker_cli_logger_default(self):
        """Test logger initialization with default settings"""
        # Create new logger with default settings
        logger = init_modmaker_cli_logger()
        
        # Check that logger is returned
        self.assertIsNotNone(logger)
        self.assertTrue(isinstance(logger, logging.Logger))
        
        # Check logger has at least one handler
        self.assertGreaterEqual(len(logger.handlers), 1)

    def test_init_modmaker_cli_logger_custom_level(self):
        """Test logger initialization with custom log level"""
        # Create new logger with debug level
        logger = init_modmaker_cli_logger(loglevel="DEBUG")
        
        # Check that logger is returned
        self.assertIsNotNone(logger)
        self.assertTrue(isinstance(logger, logging.Logger))
        
        # Verify it has the correct level
        self.assertEqual(logger.level, logging.DEBUG)

    def test_init_modmaker_cli_logger_invalid_level(self):
        """Test logger initialization with invalid log level"""
        # Create logger with invalid level
        logger = init_modmaker_cli_logger(loglevel="INVALID")
        
        # Check that logger is returned
        self.assertIsNotNone(logger)
        self.assertTrue(isinstance(logger, logging.Logger))
        
        # Should default to INFO level (20)
        self.assertEqual(logger.level, logging.INFO)


if __name__ == "__main__":
    unittest.main()