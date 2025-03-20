"""
Common utility functions for PyGen
"""

import logging
import sys
import os
import shutil
from pathlib import Path

LOG = logging.getLogger(__name__)


def exit_with_code(code, msg=""):
    """Exit the application with a specific code and optional message
    
    Args:
        code (int): Exit code
        msg (str, optional): Optional error message. Defaults to "".
    """
    if msg:
        LOG.error(msg)
    sys.exit(code)


def ensure_directory(path):
    """Ensure a directory exists, creating it if necessary
    
    Args:
        path (str): Directory path to create
        
    Returns:
        bool: True if directory exists or was created, False otherwise
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        LOG.error(f"Failed to create directory {path}: {str(e)}")
        return False


def copy_directory_contents(src, dest):
    """Copy all contents from source directory to destination
    
    Args:
        src (str): Source directory path
        dest (str): Destination directory path
        
    Returns:
        bool: True if copy was successful, False otherwise
    """
    try:
        if not os.path.exists(dest):
            os.makedirs(dest)
            
        for item in os.listdir(src):
            src_item = os.path.join(src, item)
            dest_item = os.path.join(dest, item)
            
            if os.path.isdir(src_item):
                shutil.copytree(src_item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy2(src_item, dest_item)
        return True
    except Exception as e:
        LOG.error(f"Failed to copy directory contents: {str(e)}")
        return False