"""
Command-line interface for the create module of pkgmngr.
"""
import os
import sys
from pathlib import Path

from pkgmngr.common.config import load_config, create_default_config, get_github_info
from pkgmngr.common.cli import confirm_action, display_success, display_error, display_info, display_warning
from pkgmngr.common.errors import error_handler, ConfigError, GitError
from .create import create_package_structure
from .github import init_git_repo


@error_handler
def create_package_config(package_name):
    """
    Create a new package directory with a default config file.
    
    Args:
        package_name: Name of the package
        
    Returns:
        int: Exit code
    """
    # Check PyPI availability
    from pkgmngr.common.pypi import check_name_availability
    
    if not check_name_availability(package_name, context="create"):
        display_info("Operation cancelled.")
        return 0
    
    # Create root directory
    root_dir = Path(package_name)
    
    if not handle_directory_creation(root_dir, package_name):
        return 0
    
    # Create the config file
    config_path = create_default_config(package_name, str(root_dir))
    
    # Display success message and next steps
    display_success_message(package_name, config_path)
    
    return 0


def handle_directory_creation(root_dir, package_name):
    """
    Handle creation of the package directory.
    
    Args:
        root_dir: Directory to create
        package_name: Name of the package
        
    Returns:
        bool: True if directory was created or user confirmed to proceed, False otherwise
    """
    # Check if directory exists
    if root_dir.exists():
        if not confirm_action(f"Directory '{package_name}' already exists. Continue?", default=False):
            display_info("Operation cancelled.")
            return False
    else:
        os.makedirs(root_dir)
    
    return True


def display_success_message(package_name, config_path):
    """
    Display success message and instructions for next steps.
    
    Args:
        package_name: Name of the package
        config_path: Path to the config file
    """
    display_success(f"Created package directory and config file for '{package_name}':")
    print(f"- {config_path}")
    print("\nTo finish creating your package:")
    print(f"- Change to the project's directory: `cd {package_name}`")
    print(f"- Review and edit the config file in your favorite editor: e.g. `nano pkgmngr.toml`")
    print("- Then run `pkgmngr create` to generate the project files.")
    print("Optionally you may want to initialize a Git repository synced with Github: `pkgmngr init-repo`")
    print("(Using the Github API requires that you expose a valid GITHUB_TOKEN with repo scope as environment variable)")
    print("\nHappy coding!")


@error_handler
def create_from_config(base_dir=None):
    """
    Create a package structure based on the config file.
    
    Args:
        base_dir: Base directory to look for config (default: current directory)
        
    Returns:
        int: Exit code
    """
    # Load configuration
    config, config_path = load_and_validate_config(base_dir)
    
    # Extract package name (the only parameter we still need)
    package_name = config.get("package_name")
    
    # Create package structure
    display_info(f"Creating package structure for '{package_name}'...")
    create_package_structure(package_name)
    
    display_success("Package created successfully!")
    return 0


def load_and_validate_config(base_dir):
    """
    Load and validate the configuration from pkgmngr.toml.
    
    Args:
        base_dir: Base directory to look for config
        
    Returns:
        Tuple of (config, config_path)
        
    Raises:
        ConfigError: If config is missing or invalid
    """
    try:
        config, config_path = load_config(base_dir)
    except FileNotFoundError:
        raise ConfigError("Config file not found. Run 'pkgmngr new PACKAGE_NAME' first or change to the package directory.")
    
    package_name = config.get("package_name")
    if not package_name:
        raise ConfigError("Package name not specified in config file")
    
    return config, config_path


@error_handler
def init_repository(base_dir=None):
    """
    Initialize Git and GitHub repositories based on the config file.
    
    Args:
        base_dir: Base directory to look for config (default: current directory)
    
    Returns:
        int: Exit code
    """
    # Load configuration
    config, config_path = load_and_validate_config(base_dir)
    package_name = config.get("package_name")
    
    # Get GitHub configuration
    github_info = get_github_configuration(config)
    
    # Initialize repositories
    return initialize_repositories(base_dir, package_name, github_info)


def get_github_configuration(config):
    """
    Get GitHub configuration from the config file and environment.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Dictionary with GitHub information
    """
    github_username, private = get_github_info()
    
    # Get GitHub token from environment
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token and github_username:
        display_warning("GitHub token not found in environment")
        print("Please set the GITHUB_TOKEN environment variable to create a GitHub repository")
        print("For local Git repository only, press Enter to continue")
        input()
    
    return {
        "username": github_username,
        "token": github_token,
        "private": private
    }


def initialize_repositories(base_dir, package_name, github_info):
    """
    Initialize Git and GitHub repositories.
    
    Args:
        base_dir: Base directory
        package_name: Name of the package
        github_info: GitHub configuration
        
    Returns:
        int: Exit code
    """
    current_dir = Path(base_dir) if base_dir else Path(".")
    
    success = init_git_repo(
        current_dir,
        package_name,
        github_info["token"],
        github_info["username"],
        github_info["private"]
    )
    
    if success:
        display_success("Repository initialization completed successfully!")
        return 0
    else:
        display_error("Repository initialization completed with some issues")
        return 1