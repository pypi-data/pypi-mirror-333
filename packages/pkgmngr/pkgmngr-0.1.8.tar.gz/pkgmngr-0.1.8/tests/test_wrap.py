"""
Tests for the wrap command functionality.
"""
import os
import shutil
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from pkgmngr.lifecycle.wrap import (
    wrap_existing_code,
    get_package_name,
    create_project_config,
    create_standard_files,
    organize_package_files,
    organize_test_files,
    merge_directories,
    add_init_to_subdirs
)
from pkgmngr.common.config import load_config


@pytest.fixture
def temp_project_with_files(temp_dir):
    """Create a temporary directory with some Python files for testing the wrap command."""
    # Create some Python files in the root
    (temp_dir / "hello.py").write_text('print("Hello, world!")\n')
    (temp_dir / "helpers.py").write_text('def helper_function():\n    return "I am helping"\n')
    
    # Create a test file
    (temp_dir / "test_hello.py").write_text(
        'def test_hello():\n    assert True, "This test should pass"\n'
    )
    
    # Create a subdirectory with Python files
    utils_dir = temp_dir / "utils"
    utils_dir.mkdir()
    (utils_dir / "math_utils.py").write_text(
        'def add(a, b):\n    return a + b\n'
    )
    
    return temp_dir


def test_get_package_name():
    """Test getting a package name from parameter or using default."""
    # Test with provided name
    assert get_package_name("custom-name", Path("/some/path")) == "custom-name"
    
    # Test with default (would normally prompt user, but we'll mock it)
    with patch("pkgmngr.lifecycle.wrap.get_input_with_default", return_value="default-name"):
        assert get_package_name(None, Path("/path/dir")) == "default-name"


def test_create_project_config(temp_dir, monkeypatch):
    """Test creating a project configuration file."""
    # Mock confirm_action to avoid prompts
    monkeypatch.setattr('pkgmngr.lifecycle.wrap.confirm_action', lambda *args, **kwargs: True)
    # Mock create_default_config to avoid actual file creation
    mock_config_path = str(temp_dir / "pkgmngr.toml")
    monkeypatch.setattr(
        'pkgmngr.lifecycle.wrap.create_default_config', 
        lambda *args, **kwargs: mock_config_path
    )
    
    # Test creating new config
    result = create_project_config("test-pkg", temp_dir)
    assert result == mock_config_path
    
    # Test with existing config (overwrite=True)
    (temp_dir / "pkgmngr.toml").touch()
    result = create_project_config("test-pkg", temp_dir, overwrite=True)
    assert result == mock_config_path


def test_create_standard_files(temp_dir, monkeypatch):
    """Test creating standard package files."""
    # Mock template rendering to avoid file system dependencies
    monkeypatch.setattr(
        'pkgmngr.lifecycle.wrap.render_template', 
        lambda template: f"Mock content for {template}"
    )
    
    # Test with no existing files
    create_standard_files(temp_dir, "test_pkg", overwrite=True)
    
    # Verify files were created
    assert (temp_dir / "setup.py").exists()
    assert (temp_dir / "README.md").exists()
    assert (temp_dir / "MANIFEST.in").exists()
    assert (temp_dir / "pyproject.toml").exists()
    assert (temp_dir / "LICENSE").exists()
    assert (temp_dir / ".gitignore").exists()
    
    # Test with existing files, no overwrite
    # First, modify a file to check it doesn't get overwritten
    with open(temp_dir / "README.md", "w") as f:
        f.write("Custom README content")
    
    create_standard_files(temp_dir, "test_pkg", overwrite=False)
    
    # Verify the custom README wasn't changed
    with open(temp_dir / "README.md", "r") as f:
        content = f.read()
    assert content == "Custom README content"


def test_organize_package_files_basic(temp_project_with_files, monkeypatch):
    """Test organizing Python files into a package structure."""
    # Mock confirm_action to always return True
    monkeypatch.setattr('pkgmngr.lifecycle.wrap.confirm_action', lambda *args, **kwargs: True)
    
    # Mock template rendering
    monkeypatch.setattr(
        'pkgmngr.lifecycle.wrap.render_template', 
        lambda template: f"Mock content for {template}"
    )
    
    # Organize files
    pkg_dir = organize_package_files(temp_project_with_files, "test_pkg", overwrite=True)
    
    # Verify package directory was created with proper files
    assert pkg_dir.exists()
    assert (pkg_dir / "__init__.py").exists()
    assert (pkg_dir / "__main__.py").exists()
    
    # Verify Python files were moved
    assert (pkg_dir / "hello.py").exists()
    assert (pkg_dir / "helpers.py").exists()
    
    # Original files should be gone
    assert not (temp_project_with_files / "hello.py").exists()
    assert not (temp_project_with_files / "helpers.py").exists()
    
    # Test file should still be in root
    assert (temp_project_with_files / "test_hello.py").exists()


def test_organize_package_files_with_subdir(temp_project_with_files, monkeypatch):
    """Test organizing subdirectories into a package."""
    # Mock confirm_action to always return True
    monkeypatch.setattr('pkgmngr.lifecycle.wrap.confirm_action', lambda *args, **kwargs: True)
    
    # Organize files
    pkg_dir = organize_package_files(temp_project_with_files, "test_pkg", overwrite=True)
    
    # Verify utils directory was moved to package
    assert (pkg_dir / "utils").exists()
    assert (pkg_dir / "utils" / "math_utils.py").exists()
    
    # Verify __init__.py was added to utils
    assert (pkg_dir / "utils" / "__init__.py").exists()
    
    # Original utils directory should be gone
    assert not (temp_project_with_files / "utils").exists()


def test_organize_test_files(temp_project_with_files, monkeypatch):
    """Test organizing test files into tests directory."""
    # Mock confirm_action to always return True
    monkeypatch.setattr('pkgmngr.lifecycle.wrap.confirm_action', lambda *args, **kwargs: True)
    
    # Mock template rendering
    monkeypatch.setattr(
        'pkgmngr.lifecycle.wrap.render_template', 
        lambda template: f"Mock content for {template}"
    )
    
    # Organize test files
    organize_test_files(temp_project_with_files, "test_pkg", overwrite=True)
    
    # Verify tests directory was created
    tests_dir = temp_project_with_files / "tests"
    assert tests_dir.exists()
    assert (tests_dir / "__init__.py").exists()
    assert (tests_dir / "run_tests.py").exists()
    
    # Verify test file was moved
    assert (tests_dir / "test_hello.py").exists()
    
    # Original test file should be gone
    assert not (temp_project_with_files / "test_hello.py").exists()


def test_merge_directories(temp_dir, monkeypatch):
    """Test merging two directories."""
    # Create source directory with files
    source_dir = temp_dir / "source"
    source_dir.mkdir()
    (source_dir / "file1.py").write_text("content1")
    
    # Create nested directory in source
    nested_dir = source_dir / "nested"
    nested_dir.mkdir()
    (nested_dir / "nested_file.py").write_text("nested content")
    
    # Create target directory with different files
    target_dir = temp_dir / "target"
    target_dir.mkdir()
    (target_dir / "file2.py").write_text("content2")
    
    # Mock confirm_action for removing source
    monkeypatch.setattr('pkgmngr.lifecycle.wrap.confirm_action', lambda *args, **kwargs: True)
    
    # Merge directories
    merge_directories(source_dir, target_dir, overwrite=True)
    
    # Verify files were merged correctly
    assert (target_dir / "file1.py").exists()
    assert (target_dir / "file2.py").exists()
    assert (target_dir / "nested").exists()
    assert (target_dir / "nested" / "nested_file.py").exists()
    
    # Source directory should be removed
    assert not source_dir.exists()


def test_add_init_to_subdirs(temp_dir):
    """Test adding __init__.py to subdirectories."""
    # Create nested directory structure
    (temp_dir / "pkg").mkdir()
    (temp_dir / "pkg" / "subdir1").mkdir()
    (temp_dir / "pkg" / "subdir1" / "subdir2").mkdir()
    
    # Add __init__.py files
    add_init_to_subdirs(temp_dir / "pkg", "test_pkg")
    
    # Verify __init__.py files were added
    assert (temp_dir / "pkg" / "subdir1" / "__init__.py").exists()
    assert (temp_dir / "pkg" / "subdir1" / "subdir2" / "__init__.py").exists()


def test_wrap_existing_code_integration(temp_project_with_files, monkeypatch):
    """Integration test for the whole wrap_existing_code function."""
    # Mock check_name_availability in the common.pypi module
    monkeypatch.setattr('pkgmngr.common.pypi.check_name_availability', lambda *args, **kwargs: True)
    
    # Mock user input functions
    monkeypatch.setattr('pkgmngr.lifecycle.wrap.get_input_with_default', lambda *args, **kwargs: "test-pkg")
    monkeypatch.setattr('pkgmngr.lifecycle.wrap.confirm_action', lambda *args, **kwargs: True)
    
    # Mock display functions to avoid console output
    for func_name in ['display_info', 'display_success', 'display_warning']:
        monkeypatch.setattr(f'pkgmngr.lifecycle.wrap.{func_name}', lambda *args, **kwargs: None)
        monkeypatch.setattr(f'pkgmngr.common.pypi.{func_name}', lambda *args, **kwargs: None)
    
    # Mock input function to avoid stdin issues with pytest
    monkeypatch.setattr('builtins.input', lambda *args: 'y')
    
    # Mock the success message function to avoid external dependencies
    monkeypatch.setattr(
        'pkgmngr.lifecycle.wrap.display_success_message',
        lambda *args, **kwargs: None
    )
    
    # Mock template rendering to avoid file system dependencies
    monkeypatch.setattr(
        'pkgmngr.lifecycle.wrap.render_template', 
        lambda template: f"Mock content for {template}"
    )
    
    # Mock create_default_config to avoid actual config creation
    monkeypatch.setattr(
        'pkgmngr.lifecycle.wrap.create_project_config',
        lambda *args, **kwargs: str(temp_project_with_files / "pkgmngr.toml")
    )
    
    # Change to the temp directory
    old_cwd = os.getcwd()
    os.chdir(temp_project_with_files)
    
    try:
        # Run the wrap command
        result = wrap_existing_code(package_name="test-pkg", overwrite=True)
        
        # Verify result
        assert result == 0
        
        # Verify package structure was created
        assert (temp_project_with_files / "test_pkg").exists()
        assert (temp_project_with_files / "test_pkg" / "__init__.py").exists()
        assert (temp_project_with_files / "test_pkg" / "__main__.py").exists()
        assert (temp_project_with_files / "tests").exists()
        
        # Verify Python files were moved
        assert (temp_project_with_files / "test_pkg" / "hello.py").exists()
        assert (temp_project_with_files / "test_pkg" / "helpers.py").exists()
        assert (temp_project_with_files / "tests" / "test_hello.py").exists()
        assert (temp_project_with_files / "test_pkg" / "utils").exists()
    finally:
        # Restore the original working directory
        os.chdir(old_cwd)


def test_wrap_existing_code_with_existing_structure(temp_dir, monkeypatch):
    """Test wrap command with existing package structure."""
    # Create an existing package structure
    pkg_dir = temp_dir / "existing_pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text('__version__ = "0.1.0"')
    
    # Create a config file
    config_content = """
    package_name = "existing-pkg"
    version = "0.1.0"
    """
    (temp_dir / "pkgmngr.toml").write_text(config_content)
    
    # Mock user input functions
    monkeypatch.setattr('pkgmngr.lifecycle.wrap.get_input_with_default', lambda *args, **kwargs: "existing-pkg")
    monkeypatch.setattr('pkgmngr.lifecycle.wrap.confirm_action', lambda *args, **kwargs: False)  # Decline all changes
    
    # Mock display functions to avoid console output
    for func_name in ['display_info', 'display_success', 'display_warning']:
        monkeypatch.setattr(f'pkgmngr.lifecycle.wrap.{func_name}', lambda *args, **kwargs: None)
    
    # Mock load_config to return our config
    mock_config = {"package_name": "existing-pkg", "version": "0.1.0"}
    monkeypatch.setattr(
        'pkgmngr.common.config.load_config', 
        lambda *args, **kwargs: (mock_config, str(temp_dir / "pkgmngr.toml"))
    )
    
    # Mock check_name_availability
    monkeypatch.setattr(
        'pkgmngr.common.pypi.check_name_availability',
        lambda *args, **kwargs: True
    )
    
    # Mock the success message function
    monkeypatch.setattr(
        'pkgmngr.lifecycle.wrap.display_success_message',
        lambda *args, **kwargs: None
    )
    
    # Change to the temp directory
    old_cwd = os.getcwd()
    os.chdir(temp_dir)
    
    try:
        # Run the wrap command
        result = wrap_existing_code(package_name="existing-pkg")
        
        # Verify result
        assert result == 0
        
        # Verify original structure was preserved (since we declined all changes)
        assert (temp_dir / "existing_pkg").exists()
        assert (temp_dir / "existing_pkg" / "__init__.py").exists()
    finally:
        # Restore the original working directory
        os.chdir(old_cwd)