"""
Tests for the package creation core functionality.
"""
import os
import pytest
from pathlib import Path
from pkgmngr.lifecycle.create import create_package_structure


def test_create_package_structure(temp_dir, monkeypatch):
    """Test creating a basic package structure."""
    # Change to the temp directory for this test
    original_dir = os.getcwd()
    os.chdir(temp_dir)
    
    try:
        # Mock the print function to avoid console output during tests
        monkeypatch.setattr('builtins.print', lambda *args, **kwargs: None)
        
        # Create package structure
        package_name = "test-package"
        author = "Test Author"
        year = "2025"
        github_username = "test-user"

        # Create config file first (mimicking the 'new' command)
        from pkgmngr.common.config import create_default_config
        config_path = create_default_config(
            package_name=package_name,
            output_dir=str(temp_dir),
            author=author,
            year=year,
            github={'username':github_username, 'private':False}
        )
        
        create_package_structure(package_name)
        
        # Check that the basic structure was created
        package_dir = temp_dir / "test_package"
        assert package_dir.exists()
        assert package_dir.is_dir()
        
        # Check key files
        assert (package_dir / "__init__.py").exists()
        assert (package_dir / "__main__.py").exists()
        assert (temp_dir / "setup.py").exists()
        assert (temp_dir / "README.md").exists()
        assert (temp_dir / "LICENSE").exists()
        assert (temp_dir / ".gitignore").exists()
        
        # Check tests directory
        tests_dir = temp_dir / "tests"
        assert tests_dir.exists()
        assert (tests_dir / "test_test_package.py").exists()
        assert (tests_dir / "run_tests.py").exists()
        
        # Check content of a file to ensure templates are properly formatted
        with open(package_dir / "__init__.py", 'r') as f:
            content = f.read()
            assert "test-package package" in content
            
        with open(temp_dir / "setup.py", 'r') as f:
            content = f.read()
            assert 'name="test-package"' in content
            assert f'author="{author}"' in content
    
    finally:
        # Restore the original working directory
        os.chdir(original_dir)