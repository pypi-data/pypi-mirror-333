import os
import subprocess
import shutil
from pathlib import Path

from pkgmngr.common.utils import sanitize_package_name, change_directory, find_python_executable, is_git_repository, update_file_content
from pkgmngr.common.errors import PackageError, GitError, GithubError, ConfigError, error_handler, try_operation
from pkgmngr.common.cli import display_info, display_success, display_warning, display_error, get_input_with_default
from pkgmngr.common.config import load_config, save_config, get_github_info

def increment_version(base_dir=None, increment_type='patch'):
    """
    Increment the package version according to semantic versioning.
    
    Args:
        base_dir: Base directory (default: current directory)
        increment_type: Type of increment ('major', 'minor', or 'patch')
        
    Returns:
        Tuple of (old_version, new_version)
    """
    base_dir = base_dir or os.getcwd()
    
    # Load config to get package name and current version
    config, config_path = load_config(base_dir)
    
    # Get current version
    current_version = config.get("version", "0.1.0")
    
    # Parse semantic version
    try:
        major, minor, patch = map(int, current_version.split('.'))
    except ValueError:
        display_warning(f"Could not parse version '{current_version}'. Using 0.1.0.")
        major, minor, patch = 0, 1, 0
    
    # Increment according to level
    if increment_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif increment_type == 'minor':
        minor += 1
        patch = 0
    else:  # patch by default
        patch += 1
    
    # Build new version string
    new_version = f"{major}.{minor}.{patch}"
    
    # Update version in config
    config["version"] = new_version
    save_config(config, config_path)
    display_info(f"Updated version in config: {current_version} → {new_version}")
    
    # Update version in __init__.py
    package_name = config.get("package_name")
    sanitized_name = sanitize_package_name(package_name)
    init_py_path = os.path.join(base_dir, sanitized_name, "__init__.py")
    if os.path.exists(init_py_path):
        update_file_content(init_py_path, f'__version__ = "{current_version}"', f'__version__ = "{new_version}"')
        display_info(f"Updated version in {init_py_path}")
    
    # Update version in setup.py
    setup_py_path = os.path.join(base_dir, "setup.py")
    if os.path.exists(setup_py_path):
        update_file_content(setup_py_path, f'version="{current_version}"', f'version="{new_version}"')
        display_info(f"Updated version in {setup_py_path}")
    
    return current_version, new_version

@error_handler
def upload_to_pypi(test=False, bump="patch", base_dir=None):
    """
    Build and upload the package to PyPI or TestPyPI.
    
    Args:
        test: If True, upload to TestPyPI instead of PyPI
        bump: Version increment type ('major', 'minor', or 'patch')
        base_dir: Base directory (default: current directory)
    
    Returns:
        int: 0 if successful, 1 otherwise
    """
    base_dir = base_dir or os.getcwd()
    
    # Check if necessary tools are installed
    verify_required_tools()
    
    with change_directory(base_dir):
        # Increment version if requested
        if bump:
            old_version, new_version = increment_version(base_dir, bump)
            display_success(f"Incremented version: {old_version} → {new_version}")
        
        # Clean, build and upload
        clean_build_artifacts()
        build_package()
        upload_package(test, base_dir)
        
        return 0

def verify_required_tools():
    """
    Verify that required tools are installed.
    
    Raises:
        PackageError: If required tools are missing
    """
    # Check for Python executable
    try:
        python_exe = find_python_executable()
    except PackageError as e:
        raise e
    
    # Check for pip and twine as modules rather than executables
    # Since we'll use them with the Python executable we found
    try:
        subprocess.run(
            [python_exe, "-m", "pip", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError:
        raise PackageError("pip module not found. Please install pip and try again")
    
    try:
        subprocess.run(
            [python_exe, "-m", "twine", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError:
        raise PackageError("twine module not found. Please install twine using 'pip install twine' and try again")


def clean_build_artifacts():
    """
    Clean up any existing build artifacts.
    
    Raises:
        PackageError: If cleanup fails
    """
    try:
        for directory in ["build", "dist", "*.egg-info"]:
            for path in Path(".").glob(directory):
                if path.is_dir():
                    shutil.rmtree(path)
                    display_info(f"Removed directory: {path}")
    except Exception as e:
        raise PackageError(f"Failed to clean build artifacts: {str(e)}")


def build_package():
    """
    Build the Python package.
    
    Raises:
        PackageError: If building the package fails
    """
    display_info("Building package...")
    python_exe = find_python_executable()
    
    try_operation(
        lambda: subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "build"], check=True),
        "Failed to install build package",
        PackageError
    )
    
    try_operation(
        lambda: subprocess.run([python_exe, "-m", "build"], check=True),
        "Failed to build package",
        PackageError
    )


def upload_package(test, base_dir):
    """
    Upload the package to PyPI or TestPyPI.
    
    Args:
        test: If True, upload to TestPyPI
        base_dir: Base directory
        
    Raises:
        PackageError: If uploading fails
    """
    if test:
        # Upload to TestPyPI
        upload_to_test_pypi(base_dir)
    else:
        # Upload to PyPI
        upload_to_real_pypi()


def upload_to_test_pypi(base_dir):
    """
    Upload to TestPyPI and display instructions.
    
    Args:
        base_dir: Base directory
        
    Raises:
        PackageError: If uploading fails
    """
    display_info("Uploading to TestPyPI...")
    python_exe = find_python_executable()
    
    try_operation(
        lambda: subprocess.run([
            python_exe, "-m", "twine", "upload", "--repository-url", "https://test.pypi.org/legacy/", "dist/*"
        ], check=True),
        "Failed to upload to TestPyPI",
        PackageError
    )
    
    # Get package name from config
    config, _ = load_config(base_dir)
    package_name = config.get("package_name")
    
    display_success("\nPackage uploaded to TestPyPI successfully!")
    display_info(f"You can install it with:")
    display_info(f"pip install --index-url https://test.pypi.org/simple/ {package_name}")


def upload_to_real_pypi():
    """
    Upload to PyPI.
    
    Raises:
        PackageError: If uploading fails
    """
    display_info("Uploading to PyPI...")
    python_exe = find_python_executable()
    
    try_operation(
        lambda: subprocess.run([python_exe, "-m", "twine", "upload", "dist/*"], check=True),
        "Failed to upload to PyPI",
        PackageError
    )
    display_success("\nPackage uploaded to PyPI successfully!")