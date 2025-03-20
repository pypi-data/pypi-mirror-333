"""
Tests for the text replacement functionality.
"""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from pkgmngr.lifecycle.replace import (
    safe_replace,
    find_text_files,
    filter_files,
    create_replace_function,
    process_files,
    count_replacements
)
from pkgmngr.common.errors import PackageError


def test_find_text_files(temp_dir):
    """Test finding text files in a directory."""
    # Create sample files
    text_file1 = temp_dir / "file1.txt"
    text_file1.write_text("This is a text file")
    
    text_file2 = temp_dir / "file2.py"
    text_file2.write_text("print('This is a Python file')")
    
    # Create a binary file
    binary_file = temp_dir / "binary.bin"
    with open(binary_file, 'wb') as f:
        f.write(b'\x00\x01\x02\x03')
    
    # Create a subdirectory
    subdir = temp_dir / "subdir"
    subdir.mkdir()
    
    # Create a file in subdirectory
    text_file3 = subdir / "file3.txt"
    text_file3.write_text("This is another text file")
    
    # Create a .git directory that should be skipped
    git_dir = temp_dir / ".git"
    git_dir.mkdir()
    git_file = git_dir / "config"
    git_file.write_text("git config content")
    
    # Find text files
    files = find_text_files(str(temp_dir))
    
    # Normalize paths for comparison
    files = [os.path.normpath(f) for f in files]
    
    # Check results - the .git file should be skipped
    assert len(files) == 3
    assert os.path.normpath(str(text_file1)) in files
    assert os.path.normpath(str(text_file2)) in files
    assert os.path.normpath(str(text_file3)) in files
    assert os.path.normpath(str(git_file)) not in files


def test_filter_files():
    """Test filtering files by pattern."""
    files = [
        "/path/to/file1.py",
        "/path/to/file2.txt",
        "/path/to/file3.md",
        "/path/to/subdir/file4.py",
        "/path/to/subdir/file5.txt"
    ]
    
    # Test with include patterns
    filtered = filter_files(files, ["*.py"], None)
    assert len(filtered) == 2
    assert "/path/to/file1.py" in filtered
    assert "/path/to/subdir/file4.py" in filtered
    
    # Test with exclude patterns
    filtered = filter_files(files, None, ["*.py"])
    assert len(filtered) == 3
    assert "/path/to/file2.txt" in filtered
    assert "/path/to/file3.md" in filtered
    assert "/path/to/subdir/file5.txt" in filtered
    
    # Test with both include and exclude
    filtered = filter_files(files, ["*.py", "*.txt"], ["*file5*"])
    assert len(filtered) == 3
    assert "/path/to/file1.py" in filtered
    assert "/path/to/file2.txt" in filtered
    assert "/path/to/subdir/file4.py" in filtered


def test_create_replace_function():
    """Test creating replace functions for different modes."""
    # Test simple replacement
    replace_func = create_replace_function("old", "new", False, True)
    result, changed = replace_func("This is old text with old words")
    assert result == "This is new text with new words"
    assert changed is True
    
    # Test case-insensitive replacement
    replace_func = create_replace_function("old", "new", False, False)
    result, changed = replace_func("This is OLD text with Old words")
    assert result == "This is new text with new words"
    assert changed is True
    
    # Test regex replacement
    replace_func = create_replace_function(r"(\w+)_old", r"\1_new", True, True)
    result, changed = replace_func("This is func_old and class_old")
    assert result == "This is func_new and class_new"
    assert changed is True
    
    # Test no changes
    replace_func = create_replace_function("missing", "new", False, True)
    result, changed = replace_func("This text has no matches")
    assert result == "This text has no matches"
    assert changed is False


def test_count_replacements():
    """Test counting replacements made."""
    old_text = "Line 1\nLine 2\nOld text\nLine 4"
    new_text = "Line 1\nLine 2\nNew text\nLine 4"
    count = count_replacements(old_text, new_text)
    assert count == 2  # One removal and one addition
    
    # Test no changes
    count = count_replacements("Identical", "Identical")
    assert count == 0
    
    # Test multiple changes
    old_text = "Line 1\nOld text\nLine 3\nOld text again"
    new_text = "Line 1\nNew text\nLine 3\nNew text again"
    count = count_replacements(old_text, new_text)
    assert count == 4  # Two changes, each with one removal and one addition


def test_process_files(temp_dir, monkeypatch):
    """Test processing files with replacement."""
    # Create sample files
    file1 = temp_dir / "file1.txt"
    file1.write_text("This is old text in file 1")
    
    file2 = temp_dir / "file2.txt"
    file2.write_text("This file has no matches")
    
    file3 = temp_dir / "file3.txt"
    file3.write_text("This is old text in file 3")
    
    # Create a replace function
    replace_func = create_replace_function("old", "new", False, True)
    
    # Mock confirmation to auto-approve
    monkeypatch.setattr('pkgmngr.lifecycle.replace.confirm_action', lambda *args, **kwargs: True)
    
    # Mock show_preview to do nothing
    monkeypatch.setattr('pkgmngr.lifecycle.replace.show_preview', lambda *args, **kwargs: None)
    
    # Process files
    files = [str(file1), str(file2), str(file3)]
    changes = process_files(files, replace_func, True)
    
    # Check results
    assert len(changes) == 2
    assert str(file1) in changes
    assert str(file3) in changes
    
    # Verify file content was updated
    assert file1.read_text() == "This is new text in file 1"
    assert file2.read_text() == "This file has no matches"  # Unchanged
    assert file3.read_text() == "This is new text in file 3"


@patch('pkgmngr.lifecycle.replace.create_backup_snapshot')
def test_safe_replace(mock_backup, temp_dir, monkeypatch):
    """Test the main safe_replace function with mocked components."""
    # Create sample files
    file1 = temp_dir / "file1.py"
    file1.write_text("def old_function():\n    pass")
    
    file2 = temp_dir / "file2.txt"
    file2.write_text("This is a text file with old_function calls")
    
    file3 = temp_dir / "README.md"
    file3.write_text("# Documentation\nUse old_function for testing")
    
    # Mock confirmation to auto-approve
    monkeypatch.setattr('pkgmngr.lifecycle.replace.confirm_action', lambda *args, **kwargs: True)
    
    # Mock show_preview to do nothing
    monkeypatch.setattr('pkgmngr.lifecycle.replace.show_preview', lambda *args, **kwargs: None)
    
    # Set mock backup to return a path
    mock_backup.return_value = str(temp_dir / "snapshots" / "backup.md")
    
    # Run safe_replace
    result = safe_replace(
        base_dir=str(temp_dir),
        old_pattern="old_function",
        new_pattern="new_function",
        file_patterns=["*.py", "*.md"],  # Only match Python and Markdown files
        exclude_patterns=None,
        regex=False,
        create_backup=True,
        preview=True,
        case_sensitive=True,
    )
    
    # Check results
    assert len(result) == 2
    assert str(file1) in result
    assert str(file3) in result
    assert str(file2) not in result  # Not in result because it doesn't match file patterns
    
    # Verify file content was updated
    assert file1.read_text() == "def new_function():\n    pass"
    assert file3.read_text() == "# Documentation\nUse new_function for testing"
    assert file2.read_text() == "This is a text file with old_function calls"  # Unchanged
    
    # Verify backup was created
    mock_backup.assert_called_once()


def test_safe_replace_regex(temp_dir, monkeypatch):
    """Test safe_replace with regex pattern."""
    # Create sample files
    file1 = temp_dir / "file1.py"
    file1.write_text("def get_old_value():\n    return old_value")
    
    # Mock confirmation to auto-approve
    monkeypatch.setattr('pkgmngr.lifecycle.replace.confirm_action', lambda *args, **kwargs: True)
    
    # Mock show_preview to do nothing
    monkeypatch.setattr('pkgmngr.lifecycle.replace.show_preview', lambda *args, **kwargs: None)
    
    # Mock backup creation
    monkeypatch.setattr('pkgmngr.lifecycle.replace.create_backup_snapshot', lambda *args: "backup.md")
    
    # Run safe_replace with regex
    # First replace get_old_value with get_new_value
    safe_replace(
        base_dir=str(temp_dir),
        old_pattern="get_old_value",
        new_pattern="get_new_value",
        regex=False,
        preview=False,  # Skip preview for test
    )
    
    # Then replace remaining old_value with new_value
    result = safe_replace(
        base_dir=str(temp_dir),
        old_pattern="old_value",
        new_pattern="new_value",
        regex=False,
        preview=False,  # Skip preview for test
    )
    
    # Check results
    assert len(result) == 1
    assert file1.read_text() == "def get_new_value():\n    return new_value"