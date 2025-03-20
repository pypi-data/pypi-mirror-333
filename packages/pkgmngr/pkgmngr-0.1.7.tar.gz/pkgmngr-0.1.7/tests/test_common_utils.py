"""
Tests for the common utilities module.
"""
import os
import pytest
from pkgmngr.common.utils import (
    create_directory,
    create_file,
    sanitize_package_name,
    is_binary_file
)


def test_create_directory(temp_dir):
    """Test creating a directory."""
    test_dir = temp_dir / "test_dir"
    create_directory(test_dir)
    assert test_dir.exists()
    assert test_dir.is_dir()


def test_create_file(temp_dir):
    """Test creating a file with content."""
    test_file = temp_dir / "test_file.txt"
    content = "Test content"
    create_file(test_file, content)
    
    assert test_file.exists()
    assert test_file.is_file()
    
    with open(test_file, 'r') as f:
        assert f.read() == content


def test_sanitize_package_name():
    """Test sanitizing package names."""
    assert sanitize_package_name("my-package") == "my_package"
    assert sanitize_package_name("package_name") == "package_name"
    assert sanitize_package_name("my-cool-package") == "my_cool_package"


def test_is_binary_file(temp_dir):
    """Test binary file detection."""
    # Create a text file
    text_file = temp_dir / "text_file.txt"
    with open(text_file, 'w') as f:
        f.write("This is a text file")
    
    # Create a binary file
    binary_file = temp_dir / "binary_file.bin"
    with open(binary_file, 'wb') as f:
        f.write(b'\x00\x01\x02\x03')
    
    assert not is_binary_file(text_file)
    assert is_binary_file(binary_file)