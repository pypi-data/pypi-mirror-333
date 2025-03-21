"""
Common utility functions used across pkgmngr modules.
"""
import os
import re
from pathlib import Path
from contextlib import contextmanager
from distutils.spawn import find_executable
import sys
import subprocess

from .errors import PackageError
from .cli import display_info

def update_file_content(file_path, pattern, replacement):
    """
    Update content in a file based on a pattern.
    
    Args:
        file_path: Path to the file
        pattern: Regex pattern to search for
        replacement: Replacement string
        
    Raises:
        PackageError: If updating file content fails
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        updated_content = re.sub(pattern, replacement, content)
        
        if content != updated_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            display_info(f"Updated references in {file_path}")
    except Exception as e:
        raise PackageError(f"Failed to update file content in {file_path}: {str(e)}")

def is_git_repository(base_dir=None):
    """
    Check if the current directory is a Git repository.
    
    Args:
        base_dir: Base directory to check (default: current directory)
        
    Returns:
        bool: True if it's a Git repository, False otherwise
    """
    base_dir = base_dir or os.getcwd()
    
    with change_directory(base_dir):
        try:
            subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

def find_python_executable():
    """
    Find the appropriate Python executable.
    Tries python, python3, and sys.executable in that order.
    
    Returns:
        str: Path to the Python executable
    
    Raises:
        PackageError: If no Python executable can be found
    """
    # First, try the current Python executable (from sys.executable)
    # This is most likely to be the correct one, especially in a virtual environment
    if sys.executable and os.path.exists(sys.executable):
        return sys.executable
    
    # Try common Python executable names
    for executable in ["python", "python3"]:
        if find_executable(executable):
            return executable
    
    # If we get here, we couldn't find a Python executable
    raise RuntimeError("No Python executable found. Please make sure Python is in your PATH.")

@contextmanager
def change_directory(path):
    """
    Context manager for changing the current working directory.
    
    Args:
        path: Path to change to
    """
    old_dir = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old_dir)

def create_directory(path):
    """
    Create a directory if it doesn't exist.
    
    Args:
        path: Path to the directory
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")


def create_file(path, content):
    """
    Create a file with the given content.
    
    Args:
        path: Path to the file
        content: Content of the file
    """
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")


def sanitize_package_name(name):
    """
    Sanitize package name to be a valid Python package name.
    
    Args:
        name: Package name to sanitize
    
    Returns:
        str: Sanitized package name
    """
    # Replace dashes with underscores for Python compatibility
    return name.replace('-', '_')


def is_binary_file(file_path):
    """
    Determine if a file is binary by checking its content.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        True if the file appears to be binary, False otherwise
    """
    try:
        # Try to open the file in text mode
        with open(file_path, 'r', encoding='utf-8') as f:
            # Read first chunk of the file (4KB is usually enough to determine)
            chunk = f.read(4096)
            
            # Check for common binary file signatures
            # This approach looks for null bytes and other control characters
            # that are uncommon in text files
            binary_chars = [
                char for char in chunk 
                if ord(char) < 9 or (ord(char) > 13 and ord(char) < 32)
            ]
            
            # If we found binary characters, it's likely a binary file
            # Use a threshold to avoid false positives with some text files
            if len(binary_chars) > 0:
                return True
                
            return False
    except UnicodeDecodeError:
        # If we can't decode it as UTF-8, it's a binary file
        return True
    except Exception:
        # For any other error, assume it's binary to be safe
        return True