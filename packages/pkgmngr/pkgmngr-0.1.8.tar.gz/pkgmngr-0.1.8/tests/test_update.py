"""
Tests for the update command functionality.
"""
import os
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from pkgmngr.lifecycle.update import (
    update_package_structure,
    detect_current_package_name,
    update_setup_py,
    update_standard_files,
    update_git_repo_info,
    get_github_remote_info,
    update_github_repo
)


@pytest.fixture
def temp_package_structure(temp_dir):
    """Create a temporary package structure for testing the update command."""
    # Create package directory with basic files
    pkg_dir = temp_dir / "test_pkg"
    pkg_dir.mkdir()
    
    # Create __init__.py with version
    init_file = pkg_dir / "__init__.py" 
    init_file.write_text('"""Test package."""\n\n__version__ = "0.1.0"')
    
    # Create __main__.py
    main_file = pkg_dir / "__main__.py"
    main_file.write_text('"""Main module."""\n\ndef main():\n    print("Hello!")\n\nif __name__ == "__main__":\n    main()')
    
    # Create basic setup.py
    setup_file = temp_dir / "setup.py"
    setup_file.write_text('from setuptools import setup\n\nsetup(\n    name="test-pkg",\n    version="0.1.0",\n    author="Original Author",\n    description="Original description",\n)')
    
    # Create basic LICENSE file
    license_file = temp_dir / "LICENSE"
    license_file.write_text('MIT License\n\nCopyright (c) 2024 Original Author\n')
    
    # Create basic config file
    config_file = temp_dir / "pkgmngr.toml"
    config_file.write_text("""
package_name = "test-pkg"
version = "0.1.0"
author = "Original Author"
year = "2024"
description = "Original description"

[github]
username = "original-user"
private = false
""")
    
    # Create test directory
    tests_dir = temp_dir / "tests"
    tests_dir.mkdir()
    test_file = tests_dir / "test_test_pkg.py"
    test_file.write_text('"""Tests for test_pkg."""\n\ndef test_example():\n    assert True')
    
    return temp_dir


def test_detect_current_package_name(temp_package_structure):
    """Test detecting the current package name from directory structure."""
    # Test with standard package structure
    name = detect_current_package_name(temp_package_structure)
    assert name == "test_pkg"
    
    # Test with no package structure
    empty_dir = temp_package_structure / "empty"
    empty_dir.mkdir()
    name = detect_current_package_name(empty_dir)
    assert name is None
    
    # Test with multiple package directories
    another_pkg = temp_package_structure / "another_pkg"
    another_pkg.mkdir()
    (another_pkg / "__init__.py").write_text("# Another package")
    
    # The one with __main__.py should be preferred
    name = detect_current_package_name(temp_package_structure)
    assert name == "test_pkg"


def test_update_setup_py(temp_package_structure, monkeypatch):
    """Test updating setup.py file."""
    # Mock template rendering
    monkeypatch.setattr(
        'pkgmngr.lifecycle.update.render_template', 
        lambda template: "# Updated setup.py content\nfrom setuptools import setup\n\nsetup(name='test-pkg', version='0.2.0')"
    )
    
    # Update without confirmation (force=True)
    update_setup_py(temp_package_structure, force=True)
    
    # Check that setup.py was updated
    with open(temp_package_structure / "setup.py", "r") as f:
        content = f.read()
    assert "Updated setup.py content" in content
    assert "version='0.2.0'" in content


def test_update_standard_files(temp_package_structure, monkeypatch):
    """Test updating standard files that depend on config."""
    # Mock template rendering
    monkeypatch.setattr(
        'pkgmngr.lifecycle.update.render_template', 
        lambda template: "MIT License\n\nCopyright (c) 2025 New Author" if template == "license_mit" else ""
    )
    
    # Update without confirmation (force=True)
    update_standard_files(temp_package_structure, force=True)
    
    # Check that LICENSE was updated
    with open(temp_package_structure / "LICENSE", "r") as f:
        content = f.read()
    assert "2025 New Author" in content


def test_get_github_remote_info(monkeypatch):
    """Test extracting GitHub information from remote URL."""
    # Mock subprocess.run for different URL formats
    def mock_run(*args, **kwargs):
        class CompletedProcess:
            def __init__(self, stdout):
                self.stdout = stdout
                self.returncode = 0
        
        if args[0][0] == "git" and args[0][1] == "remote":
            # Return different URL formats for testing
            cwd_str = str(kwargs.get('cwd', ''))  # Convert PosixPath to string
            if "https" in cwd_str:
                return CompletedProcess("https://github.com/username/repo.git")
            elif "ssh" in cwd_str:
                return CompletedProcess("git@github.com:username/repo.git")
            else:
                return CompletedProcess("https://gitlab.com/username/repo.git")  # Non-GitHub URL
    
    monkeypatch.setattr('subprocess.run', mock_run)
    
    # Test with HTTPS URL
    info = get_github_remote_info(Path("/fake/path/https"))
    assert info is not None
    assert info["username"] == "username"
    assert info["repo_name"] == "repo"
    
    # Test with SSH URL
    info = get_github_remote_info(Path("/fake/path/ssh"))
    assert info is not None
    assert info["username"] == "username"
    assert info["repo_name"] == "repo"
    
    # Test with non-GitHub URL
    info = get_github_remote_info(Path("/fake/path/other"))
    assert info is None


def test_update_github_repo(monkeypatch):
    """Test updating GitHub repository information."""
    # Mock requests.patch
    class MockResponse:
        def __init__(self, status_code, data=None):
            self.status_code = status_code
            self.data = data or {}
        
        def json(self):
            return self.data
    
    def mock_patch(*args, **kwargs):
        if "error" in args[0]:
            return MockResponse(422, {"message": "Validation failed"})
        return MockResponse(200)
    
    # Mock display functions
    mock_display_success = MagicMock()
    mock_display_warning = MagicMock()
    
    monkeypatch.setattr('requests.patch', mock_patch)
    monkeypatch.setattr('pkgmngr.lifecycle.update.display_success', mock_display_success)
    monkeypatch.setattr('pkgmngr.lifecycle.update.display_warning', mock_display_warning)
    
    # Test successful update
    update_github_repo("username", "repo", "New description", "fake-token")
    mock_display_success.assert_called_once()
    
    # Test failed update
    mock_display_success.reset_mock()
    update_github_repo("username", "error-repo", "New description", "fake-token")
    mock_display_warning.assert_called_once()


@patch('pkgmngr.lifecycle.update.rename_project')
def test_update_package_name(mock_rename, temp_package_structure, monkeypatch):
    """Test updating the package name."""
    # Prepare mocks
    mock_load_config = MagicMock(return_value=(
        {"package_name": "new-package", "version": "0.2.0", "description": "New description"},
        str(temp_package_structure / "pkgmngr.toml")
    ))
    
    # Mock confirm_action to always return True
    monkeypatch.setattr('pkgmngr.lifecycle.update.confirm_action', lambda *args, **kwargs: True)
    monkeypatch.setattr('pkgmngr.lifecycle.update.load_config', mock_load_config)
    monkeypatch.setattr('pkgmngr.lifecycle.update.update_setup_py', lambda *args, **kwargs: None)
    monkeypatch.setattr('pkgmngr.lifecycle.update.update_standard_files', lambda *args, **kwargs: None)
    monkeypatch.setattr('pkgmngr.lifecycle.update.update_git_repo_info', lambda *args, **kwargs: None)
    
    # Run the update
    update_package_structure(temp_package_structure, force=True)
    
    # Verify rename was called
    mock_rename.assert_called_once_with("new-package", skip_github=True, base_dir=temp_package_structure)


@patch('pkgmngr.lifecycle.update.is_git_repository')
@patch('pkgmngr.lifecycle.update.update_git_description')
@patch('pkgmngr.lifecycle.update.get_github_remote_info')
@patch('pkgmngr.lifecycle.update.update_github_repo')
def test_update_git_repo_info(mock_update_github, mock_get_info, mock_update_desc, mock_is_git, 
                              temp_package_structure, monkeypatch):
    """Test updating Git repository information."""
    # Setup mocks
    mock_is_git.return_value = True
    mock_get_info.return_value = {"username": "test-user", "repo_name": "test-repo"}
    
    # Mock os.environ to include GITHUB_TOKEN
    monkeypatch.setattr('os.environ.get', lambda key, default=None: "fake-token" if key == "GITHUB_TOKEN" else default)
    monkeypatch.setattr('pkgmngr.lifecycle.update.confirm_action', lambda *args, **kwargs: True)
    
    # Create config with description
    config = {
        "package_name": "test-pkg",
        "description": "Updated description",
    }
    
    # Run the update
    update_git_repo_info(config, temp_package_structure, force=True)
    
    # Verify Git description was updated
    mock_update_desc.assert_called_once_with("Updated description", temp_package_structure)
    
    # Verify GitHub repo was updated
    mock_update_github.assert_called_once_with("test-user", "test-repo", "Updated description", "fake-token")


@patch('pkgmngr.lifecycle.update.update_git_repo_info')
def test_update_package_structure_integration(mock_update_git, temp_package_structure, monkeypatch):
    """Integration test for the whole update function."""
    # Update the config file with new values
    config_content = """
package_name = "test-pkg"  # Same name, no rename needed
version = "0.2.0"  # New version
author = "New Author"  # New author
year = "2025"  # New year
description = "Updated package description"  # New description

[github]
username = "new-user"
private = false
"""
    with open(temp_package_structure / "pkgmngr.toml", "w") as f:
        f.write(config_content)
    
    # Mock confirmations to always be true
    monkeypatch.setattr('pkgmngr.lifecycle.update.confirm_action', lambda *args, **kwargs: True)
    
    # Mock template rendering to return predictable content
    monkeypatch.setattr(
        'pkgmngr.lifecycle.update.render_template', 
        lambda template: (
            "# Updated setup.py\nversion='0.2.0'\nauthor='New Author'" if template == "setup_py" else
            "MIT License\n\nCopyright (c) 2025 New Author" if template == "license_mit" else
            "Unknown template"
        )
    )
    
    # Run the update
    old_cwd = os.getcwd()
    os.chdir(temp_package_structure)
    try:
        result = update_package_structure(force=True)
        
        # Verify result
        assert result == 0
        
        # Verify setup.py was updated
        with open("setup.py", "r") as f:
            setup_content = f.read()
        assert "Updated setup.py" in setup_content
        assert "version='0.2.0'" in setup_content
        assert "author='New Author'" in setup_content
        
        # Verify LICENSE was updated
        with open("LICENSE", "r") as f:
            license_content = f.read()
        assert "Copyright (c) 2025 New Author" in license_content
        
        # Verify Git repo info update was called
        mock_update_git.assert_called_once()
    finally:
        os.chdir(old_cwd)