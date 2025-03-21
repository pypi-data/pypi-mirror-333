"""
Tests for package lifecycle management.
"""
import os
import pytest
import toml
from pathlib import Path
from pkgmngr.lifecycle.rename import (
    rename_project
)

@pytest.fixture
def rename_test_project(temp_dir):
    """Create a test project structure for renaming tests."""
    # Create a simple package structure
    pkg_dir = temp_dir / "old_package"
    pkg_dir.mkdir()
    
    # Create Python files
    init_py = pkg_dir / "__init__.py"
    init_py.write_text('"""old-package."""\n__version__ = "0.1.0"')
    
    main_py = pkg_dir / "__main__.py"
    main_py.write_text('"""Main module for old-package."""')
    
    # Create tests directory
    tests_dir = temp_dir / "tests"
    tests_dir.mkdir()
    test_py = tests_dir / "test_old_package.py"
    test_py.write_text('import old_package\n\ndef test_version():\n    assert old_package.__version__')
    
    # Create setup.py
    setup_py = temp_dir / "setup.py"
    setup_content = 'from setuptools import setup\n\nsetup(\n    name="old-package",\n    packages=["old_package"],\n    entry_points={\n        "console_scripts": [\n            "old-package=old_package.__main__:main",\n        ],\n    },\n)'
    setup_py.write_text(setup_content)
    
    # Create README
    readme = temp_dir / "README.md"
    readme.write_text("# old-package\n\nInstall with `pip install old-package`")
    
    # Create config file
    config = {
        "package_name": "old-package",
        "author": "Test Author",
        "github": {
            "username": "testuser"
        }
    }
    config_file = temp_dir / "pkgmngr.toml"
    with open(config_file, "w") as f:
        toml.dump(config, f)
    
    # Simply return the temp directory
    return temp_dir

@pytest.mark.parametrize("skip_github", [True])
def test_rename_project(rename_test_project, skip_github, monkeypatch):
    """Test renaming a project with the updated rename function."""
    temp_dir = rename_test_project
    
    # Mock functions that interact with external systems
    monkeypatch.setattr('pkgmngr.lifecycle.rename.is_git_repository', lambda base_dir: True)
    monkeypatch.setattr('pkgmngr.lifecycle.rename.get_github_remote_info',
                       lambda base_dir: ("https://github.com/testuser/old-package.git", "testuser"))
    
    # Mock check_name_availability to bypass PyPI check and user input
    monkeypatch.setattr('pkgmngr.common.pypi.check_name_availability', lambda name, context: True)
    monkeypatch.setattr('builtins.input', lambda _: 'y')  # Simulate user input "y"
    
    # Mock safe_replace to avoid actually replacing contents in tests
    def mock_safe_replace(**kwargs):
        return {"mock_file.py": 1}  # Return mock changes
    monkeypatch.setattr('pkgmngr.lifecycle.rename.safe_replace', mock_safe_replace)
    
    # Mock GitHub token (if not skipping)
    if not skip_github:
        monkeypatch.setenv("GITHUB_TOKEN", "fake_token")
        monkeypatch.setattr('pkgmngr.lifecycle.rename.rename_github_repository',
                           lambda username, old_name, new_name, token, remote_url, base_dir: True)
    
    # Run the rename function with only the new name
    result = rename_project("new-package", skip_github, temp_dir)
    
    # Check that renaming was successful
    assert result == 0
    
    # Check directory structure changes
    assert not (temp_dir / "old_package").exists()
    assert (temp_dir / "new_package").exists()
    
    # Check config file update
    with open(temp_dir / "pkgmngr.toml", 'r') as f:
        config = toml.load(f)
        assert config["package_name"] == "new-package"