"""
Tests for the simplified snapshot restore functionality.
"""
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import os
import re
import tempfile
import shutil

from pkgmngr.snapshot.restore import (
    restore_from_snapshot,
    create_backup_snapshot,
    is_backup_snapshot,
    filter_files_by_patterns,
    restore_files_enhanced,
    cleanup_empty_directories,
    selective_restore,
    select_files_interactive
)
from pkgmngr.snapshot.snapshot import create_snapshot, parse_snapshot_file
from pkgmngr.common.utils import create_file


@pytest.fixture
def sample_project(temp_dir):
    """Create a sample project structure for snapshot testing."""
    # Create a simple project structure
    pkg_dir = temp_dir / "test_pkg"
    pkg_dir.mkdir()
    
    # Create some Python files
    init_py = pkg_dir / "__init__.py"
    init_py.write_text('"""Test package."""\n\n__version__ = "0.1.0"')
    
    main_py = pkg_dir / "__main__.py"
    main_py.write_text('"""Main module."""\n\nprint("Hello from test_pkg!")')
    
    # Create a README
    readme = temp_dir / "README.md"
    readme.write_text("# Test Package\n\nA test package for snapshot testing.")
    
    # Create a .gitignore file
    gitignore = temp_dir / ".gitignore"
    gitignore.write_text("__pycache__/\n*.py[cod]\n*$py.class\n\n# Snapshots\nsnapshots/")
    
    return temp_dir


@pytest.fixture
def sample_snapshot_file(temp_dir):
    """Create a sample snapshot markdown file with known content."""
    snapshot_dir = temp_dir / "snapshots"
    snapshot_dir.mkdir(exist_ok=True)
    
    # Create a manually constructed snapshot file with known content
    snapshot_file = snapshot_dir / "snapshot_2025-01-01_12-00-00.md"
    with open(snapshot_file, "w") as f:
        f.write("""# test-project - Package Snapshot - Generated on 2025-01-01_12-00-00

**Note:** This snapshot uses code blocks with varying numbers of backticks to properly handle nested code blocks.
The number of backticks in each file's code fence is intentionally set to be more than any sequence of backticks within the file content.

## Comments
Test snapshot comment

## Directory Structure
```
📦 test_project
├─ 📂 test_pkg
│  ├─ 🐍 __init__.py
│  └─ 🐍 __main__.py
└─ 📝 README.md
```

## Table of Contents
1. [test_pkg/__init__.py](#test_pkg-__init__py)
2. [test_pkg/__main__.py](#test_pkg-__main__py)
3. [README.md](#readmemd)

## Files

<a id="test_pkg-__init__py"></a>
### test_pkg/__init__.py
```python
\"\"\"Test package.\"\"\"

__version__ = "0.1.0"
```

<a id="test_pkg-__main__py"></a>
### test_pkg/__main__.py
```python
\"\"\"Main module.\"\"\"

print("Hello from test_pkg!")
```

<a id="readmemd"></a>
### README.md
```markdown
# Test Package

A test package for snapshot testing.
```
""")
    
    return snapshot_file


def test_restore_from_snapshot(sample_snapshot_file, temp_dir, monkeypatch):
    """Test restoring a project from a snapshot."""
    # Create a new empty directory to restore to
    restore_dir = temp_dir / "restore_test"
    restore_dir.mkdir()
    
    # Restore from snapshot
    monkeypatch.setattr('builtins.print', lambda *args, **kwargs: None)  # Silence prints
    backup_file = restore_from_snapshot(
        str(sample_snapshot_file), 
        str(restore_dir), 
        create_backup=False
    )
    
    # Check that files were restored
    assert (restore_dir / "test_pkg" / "__init__.py").exists()
    assert (restore_dir / "test_pkg" / "__main__.py").exists()
    assert (restore_dir / "README.md").exists()
    
    # Check content of a restored file
    with open(restore_dir / "test_pkg" / "__init__.py", 'r') as f:
        content = f.read()
        assert '__version__ = "0.1.0"' in content


def test_restore_with_file_removal(temp_dir, monkeypatch):
    """Test restoring a project with file removal logic."""
    # Create a test project
    test_dir = temp_dir / "test_project"
    test_dir.mkdir()
    
    # Create some initial files
    os.makedirs(test_dir / "pkg_dir", exist_ok=True)
    with open(test_dir / "pkg_dir" / "file1.py", 'w') as f:
        f.write("content1")
    with open(test_dir / "pkg_dir" / "file2.py", 'w') as f:
        f.write("content2")
    with open(test_dir / "README.md", 'w') as f:
        f.write("readme")
    
    # Mock backup creation and parsing
    backup_contents = {
        "pkg_dir/file1.py": "content1",
        "pkg_dir/file2.py": "content2",
        "README.md": "readme"
    }
    
    # Create a snapshot with only some files
    snapshot_contents = {
        "pkg_dir/file1.py": "updated content1",
        "README.md": "updated readme"
    }
    
    # Silence prints
    monkeypatch.setattr('builtins.print', lambda *args, **kwargs: None)
    
    # Call the restore function directly
    files_restored, files_skipped, files_removed = restore_files_enhanced(
        snapshot_contents,
        backup_contents,
        str(test_dir)
    )
    
    # Check the results
    # file1.py should be updated
    assert (test_dir / "pkg_dir" / "file1.py").exists()
    with open(test_dir / "pkg_dir" / "file1.py", 'r') as f:
        assert f.read() == "updated content1"
    
    # README.md should be updated
    assert (test_dir / "README.md").exists()
    with open(test_dir / "README.md", 'r') as f:
        assert f.read() == "updated readme"
    
    # file2.py should be removed
    assert not (test_dir / "pkg_dir" / "file2.py").exists()
    
    # Check the counters
    assert files_restored == 2
    assert files_skipped == 0
    assert files_removed == 1


def test_cleanup_empty_directories(temp_dir):
    """Test that empty directories are removed after restoration."""
    # Create test directory structure
    test_dir = temp_dir / "cleanup_test"
    test_dir.mkdir()
    
    # Create directory structure
    os.makedirs(test_dir / "dir1" / "subdir", exist_ok=True)
    os.makedirs(test_dir / "dir2", exist_ok=True)
    
    # Add a file to dir1
    with open(test_dir / "dir1" / "file.txt", 'w') as f:
        f.write("test")
    
    # Silence prints
    with patch('builtins.print'):
        cleanup_empty_directories(test_dir)
    
    # dir2 should be removed (it's empty), dir1 should remain (it has content)
    assert (test_dir / "dir1").exists()
    assert not (test_dir / "dir2").exists()
    assert not (test_dir / "dir1" / "subdir").exists()

    os.makedirs(test_dir / "dir1" / "subdir", exist_ok=True)
    
    # Now make dir1/subdir non-empty to test partial cleanup
    with open(test_dir / "dir1" / "subdir" / "new_file.txt", 'w') as f:
        f.write("test")
        
    # Remove the file from dir1 but leave subdir non-empty
    os.remove(test_dir / "dir1" / "file.txt")
    
    # Run cleanup again
    with patch('builtins.print'):
        cleanup_empty_directories(test_dir)
    
    # dir1 should still exist because subdir still has content
    assert (test_dir / "dir1").exists()
    assert (test_dir / "dir1" / "subdir").exists()
    
    # Now remove the file from subdir
    os.remove(test_dir / "dir1" / "subdir" / "new_file.txt")
    
    # Run cleanup one more time
    with patch('builtins.print'):
        cleanup_empty_directories(test_dir)
    
    # Both dir1 and subdir should be gone now as they're both empty
    assert not (test_dir / "dir1").exists()
    assert not (test_dir / "dir1" / "subdir").exists()


def test_filter_files_by_patterns():
    """Test the file filtering logic."""
    # Sample file contents
    file_contents = {
        "file1.py": "content1",
        "file2.txt": "content2",
        "dir/file3.py": "content3",
        "dir/file4.txt": "content4",
        "dir/subdir/file5.py": "content5"
    }
    
    # Test with no patterns (should return all files)
    result = filter_files_by_patterns(file_contents)
    assert len(result) == 5
    assert set(result.keys()) == set(file_contents.keys())
    
    # Test with inclusion patterns
    result = filter_files_by_patterns(file_contents, patterns=["*.py"])
    assert len(result) == 3
    assert "file1.py" in result
    assert "dir/file3.py" in result
    assert "dir/subdir/file5.py" in result
    assert "file2.txt" not in result
    
    # Test with directory pattern
    result = filter_files_by_patterns(file_contents, patterns=["dir/*"])
    assert len(result) == 3
    assert "dir/file3.py" in result
    assert "dir/file4.txt" in result
    assert "dir/subdir/file5.py" in result
    
    # Test with exclusion patterns
    result = filter_files_by_patterns(file_contents, exclude_patterns=["*.txt"])
    assert len(result) == 3
    assert "file1.py" in result
    assert "dir/file3.py" in result
    assert "dir/subdir/file5.py" in result
    
    # Test with both inclusion and exclusion
    result = filter_files_by_patterns(file_contents, patterns=["*.*"], exclude_patterns=["dir/subdir/*"])
    assert len(result) == 4
    assert "dir/subdir/file5.py" not in result


def test_selective_restore(sample_snapshot_file, temp_dir, monkeypatch):
    """Test selective restoration from a snapshot."""
    # Create a new empty directory to restore to
    restore_dir = temp_dir / "selective_restore_test"
    restore_dir.mkdir()
    
    # Selectively restore only Python files
    monkeypatch.setattr('builtins.print', lambda *args, **kwargs: None)  # Silence prints
    backup_file = selective_restore(
        str(sample_snapshot_file),
        str(restore_dir),
        patterns=["*.py"],  # Only restore Python files
        exclude_patterns=None,
        interactive=False,
        create_backup=False
    )
    
    # Check that Python files were restored but README was not
    assert (restore_dir / "test_pkg" / "__init__.py").exists()
    assert (restore_dir / "test_pkg" / "__main__.py").exists()
    assert not (restore_dir / "README.md").exists()
    assert not (restore_dir / ".gitignore").exists()


def test_selective_restore_interactive(sample_snapshot_file, temp_dir, monkeypatch):
    """Test interactive selective restoration."""
    # Create a new empty directory to restore to
    restore_dir = temp_dir / "interactive_restore_test"
    restore_dir.mkdir()
    
    # First, parse the snapshot file to get actual file contents
    from pkgmngr.snapshot.snapshot import parse_snapshot_file
    actual_file_contents, _, _ = parse_snapshot_file(sample_snapshot_file)
    
    # Verify 'README.md' exists in the actual contents before proceeding
    assert 'README.md' in actual_file_contents, "Test snapshot is missing README.md"
    
    # Mock the interactive selection to return README.md from actual content
    def mock_select_interactive(files, target):
        # Only return README.md from the actual files
        return {'README.md': files['README.md']} if 'README.md' in files else {}
    
    monkeypatch.setattr(
        'pkgmngr.snapshot.restore.select_files_interactive',
        mock_select_interactive
    )
    
    # Silence prints
    monkeypatch.setattr('builtins.print', lambda *args, **kwargs: None)
    
    # Perform interactive restore
    backup_file = selective_restore(
        str(sample_snapshot_file),
        str(restore_dir),
        patterns=None,
        exclude_patterns=None,
        interactive=True,
        create_backup=False
    )
    
    # Check that only README.md was restored
    assert (restore_dir / "README.md").exists()
    assert not (restore_dir / "test_pkg").exists()
    assert not (restore_dir / ".gitignore").exists()


def test_is_backup_snapshot(temp_dir):
    """Test detection of backup snapshot files."""
    # Create a regular snapshot file
    regular = temp_dir / "regular_snapshot.md"
    regular.write_text("# test-project - Package Snapshot - Generated on 2025-01-01\n\n## Comments\nRegular snapshot\n")
    
    # Create a backup snapshot file by filename
    backup_by_name = temp_dir / "pre_restore_backup_2025-01-01.md"
    backup_by_name.write_text("# test-project - Package Snapshot - Generated on 2025-01-01\n\n## Comments\nSome comment\n")
    
    # Create a backup snapshot file by content
    backup_by_content = temp_dir / "snapshot_with_backup_comment.md"
    backup_by_content.write_text("# test-project - Package Snapshot - Generated on 2025-01-01\n\n## Comments\nAutomatic backup created before restoration\n")
    
    # Test detection
    assert not is_backup_snapshot(str(regular))
    assert is_backup_snapshot(str(backup_by_name))
    assert is_backup_snapshot(str(backup_by_content))


def test_create_backup_snapshot(temp_dir, monkeypatch):
    """Test creating a backup snapshot."""
    # Create a simple test project
    os.makedirs(temp_dir / "src", exist_ok=True)
    with open(temp_dir / "src" / "test.py", 'w') as f:
        f.write("print('test')")
    
    # Mock time.strftime to get consistent results
    monkeypatch.setattr('time.strftime', lambda *args, **kwargs: "2025-01-01_12-00-00")
    
    # Silence prints
    monkeypatch.setattr('builtins.print', lambda *args, **kwargs: None)
    
    # Create the backup
    backup_path = create_backup_snapshot(str(temp_dir))
    
    # Check the backup was created with correct naming
    assert "pre_restore_backup_2025-01-01_12-00-00.md" in backup_path
    assert os.path.exists(backup_path)
    
    # Check comment in content
    with open(backup_path, 'r') as f:
        content = f.read()
    assert "Automatic backup created before restoration" in content


def test_restore_with_backup_creation(sample_project, temp_dir, monkeypatch):
    """Test that a backup is created before restoration."""
    # Create a snapshot
    monkeypatch.setattr('time.strftime', lambda *args, **kwargs: "2025-01-01_12-00-00")
    snapshot_file = create_snapshot(sample_project, "snapshots", comment="Test snapshot")
    
    # Create a test project with some content
    restore_dir = temp_dir / "backup_test"
    restore_dir.mkdir()
    os.makedirs(restore_dir / "existing_dir", exist_ok=True)
    with open(restore_dir / "existing_dir" / "file.txt", 'w') as f:
        f.write("existing content")
    
    # Silence prints
    monkeypatch.setattr('builtins.print', lambda *args, **kwargs: None)
    
    # Create a mock backup file
    mock_backup_path = str(temp_dir / "mock_backup.md")
    with open(mock_backup_path, 'w') as f:
        f.write("# Mock Backup Content\n\n## Comments\nMock backup for testing\n")
    
    # Mock create_backup_snapshot to return our real file
    mock_backup = MagicMock(return_value=mock_backup_path)
    monkeypatch.setattr('pkgmngr.snapshot.restore.create_backup_snapshot', mock_backup)
    
    # Mock parse_snapshot_file for the backup to return empty data
    from pkgmngr.snapshot.snapshot import parse_snapshot_file as original_parse
    
    def mock_parse(file_path):
        if file_path == mock_backup_path:
            return {}, "Mock backup", "test-project"
        return original_parse(file_path)
    
    monkeypatch.setattr('pkgmngr.snapshot.restore.parse_snapshot_file', mock_parse)
    
    # Restore with backup
    backup_file = restore_from_snapshot(
        snapshot_file,
        str(restore_dir),
        create_backup=True
    )
    
    # Verify backup was created
    assert mock_backup.called
    assert backup_file == mock_backup_path