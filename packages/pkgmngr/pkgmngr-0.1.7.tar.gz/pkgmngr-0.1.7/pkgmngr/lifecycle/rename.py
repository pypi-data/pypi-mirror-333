"""
Simplified package renaming functionality.
"""
import os
import subprocess
import json
import requests
from pathlib import Path

from pkgmngr.common.utils import sanitize_package_name, change_directory, is_git_repository
from pkgmngr.common.errors import PackageError, GitError, GithubError, ConfigError, error_handler, try_operation
from pkgmngr.common.cli import display_info, display_success, display_warning, display_error
from pkgmngr.common.config import load_config, save_config
from pkgmngr.lifecycle.replace import safe_replace

@error_handler
def rename_project(new_name, skip_github=False, base_dir=None):
    """
    Rename a project, updating all references to the old name,
    and optionally renaming the GitHub repository.
    
    Args:
        new_name: New name for the package
        skip_github: If True, skip GitHub repository renaming even if token is available
        base_dir: Base directory (default: current directory)
    
    Returns:
        int: 0 if successful, 1 otherwise
    """
    # Use provided base directory or current directory
    base_dir = base_dir or os.getcwd()
    
    # Load config and get the current package name
    try:
        config, config_path = load_config(base_dir)
        old_name = config.get("package_name")
        if not old_name:
            raise ConfigError("Current package name not found in config file")
    except FileNotFoundError:
        raise ConfigError("Config file not found in current directory. Run 'pkgmngr new PACKAGE_NAME' first or change to the package directory.")
    
    # Check PyPI availability for the new name
    from pkgmngr.common.pypi import check_name_availability
    
    if not check_name_availability(new_name, context="rename"):
        display_info("Rename operation cancelled.")
        return 0
    
    # Create sanitized versions of names
    old_sanitized = sanitize_package_name(old_name)
    new_sanitized = sanitize_package_name(new_name)
    
    # Check if GitHub integration is needed
    github_info = check_github_integration(base_dir, skip_github)
    
    # Update config file
    update_config_file(config, new_name, config_path)
    
    # Rename package directory
    rename_directory(base_dir, old_sanitized, new_sanitized)
    
    # Replace all occurrences of package name in all files
    replace_package_name_references(base_dir, old_name, new_name, old_sanitized, new_sanitized)
    
    # Handle GitHub repository renaming if applicable
    handle_github_rename(github_info, old_name, new_name, base_dir, skip_github)
    
    display_success(f"\nProject successfully renamed from '{old_name}' to '{new_name}'")
    display_info("All references to the old name have been updated.")
    return 0

def rename_directory(base_dir, old_sanitized, new_sanitized):
    """
    Rename the package directory.
    
    Args:
        base_dir: Base directory
        old_sanitized: Sanitized old package name
        new_sanitized: Sanitized new package name
    """
    old_pkg_dir = os.path.join(base_dir, old_sanitized)
    new_pkg_dir = os.path.join(base_dir, new_sanitized)
    
    if os.path.exists(old_pkg_dir) and os.path.isdir(old_pkg_dir):
        if os.path.exists(new_pkg_dir):
            raise PackageError(f"Cannot rename: Directory {new_pkg_dir} already exists")
        os.rename(old_pkg_dir, new_pkg_dir)
        display_info(f"Renamed package directory: {old_sanitized} → {new_sanitized}")

def update_config_file(config, new_name, config_path):
    """
    Update the configuration file with the new package name.
    
    Args:
        config: Configuration dictionary
        new_name: New package name
        config_path: Path to the config file
    """
    config["package_name"] = new_name
    save_config(config, config_path)
    display_info(f"Updated config file with new package name: {new_name}")

def replace_package_name_references(base_dir, old_name, new_name, old_sanitized, new_sanitized):
    """
    Replace all references to the old package name and its sanitized version.
    
    Args:
        base_dir: Base directory
        old_name: Old package name
        new_name: New package name
        old_sanitized: Sanitized old package name
        new_sanitized: Sanitized new package name
    """
    # Replace the exact hyphenated package name
    display_info(f"Replacing occurrences of '{old_name}' with '{new_name}'...")
    safe_replace(
        base_dir=base_dir,
        old_pattern=old_name,
        new_pattern=new_name,
        preview=False,
        create_backup=False,  # Skip backup since we only do it once
    )
    
    # Only replace sanitized name if it's different from the original
    if old_sanitized != old_name:
        display_info(f"Replacing occurrences of '{old_sanitized}' with '{new_sanitized}'...")
        safe_replace(
            base_dir=base_dir,
            old_pattern=old_sanitized,
            new_pattern=new_sanitized,
            preview=False,
            create_backup=False,  # Skip backup since we only do it once
        )

def check_github_integration(base_dir, skip_github):
    """
    Check if GitHub integration is needed and available.
    
    Args:
        base_dir: Base directory
        skip_github: Whether to skip GitHub operations
        
    Returns:
        Dictionary with GitHub information or None if not needed
    """
    # Check if this is a git repository
    is_git_repo = is_git_repository(base_dir)
    if not is_git_repo:
        display_info("Not inside a Git repository. GitHub renaming will be skipped.")
        return None
    
    # If this is a git repo, check if GitHub remote exists
    github_remote_url, github_username = get_github_remote_info(base_dir)
    if github_username:
        display_info(f"Detected GitHub repository: {github_username}/{github_remote_url.split('/')[-1].replace('.git', '')}")
        return {
            "remote_url": github_remote_url,
            "username": github_username
        }
    
    return None

def get_github_remote_info(base_dir=None):
    """
    Get GitHub remote URL and username from a Git repository.
    
    Args:
        base_dir: Base directory to check (default: current directory)
        
    Returns:
        tuple: (remote_url, username) or (None, None) if not found
    """
    base_dir = base_dir or os.getcwd()
    
    with change_directory(base_dir):
        try:
            # Get remote URL
            remote_url = subprocess.check_output(
                ["git", "remote", "get-url", "origin"],
                stderr=subprocess.PIPE,
                universal_newlines=True
            ).strip()
            
            # Extract username from remote URL
            return extract_github_username(remote_url)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None, None

def extract_github_username(remote_url):
    """
    Extract GitHub username from a remote URL.
    
    Args:
        remote_url: GitHub remote URL
        
    Returns:
        Tuple of (remote_url, username) or (remote_url, None) if not found
    """
    username = None
    if "github.com" in remote_url:
        if remote_url.startswith("https://"):
            # Format: https://github.com/username/repo.git
            parts = remote_url.split("/")
            if len(parts) >= 4:
                username = parts[3]
        elif remote_url.startswith("git@"):
            # Format: git@github.com:username/repo.git
            parts = remote_url.split(":")
            if len(parts) >= 2:
                username = parts[1].split("/")[0]
    
    return remote_url, username

def handle_github_rename(github_info, old_name, new_name, base_dir, skip_github):
    """
    Handle GitHub repository renaming if applicable.
    
    Args:
        github_info: GitHub information dictionary or None
        old_name: Old package name
        new_name: New package name
        base_dir: Base directory
        skip_github: Whether to skip GitHub operations
    """
    if not github_info or skip_github:
        return
        
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        success = rename_github_repository(
            github_info["username"], 
            old_name, 
            new_name, 
            github_token, 
            github_info["remote_url"],
            base_dir
        )
        if not success:
            display_warning("Local project renamed successfully, but GitHub repository remains unchanged.")
            display_info("You may need to manually rename the GitHub repository.")
    else:
        display_warning("GITHUB_TOKEN environment variable not set. Skipping GitHub repository renaming.")
        display_info("Local project renamed successfully, but GitHub repository remains unchanged.")
        display_info("To rename the GitHub repository, set the GITHUB_TOKEN environment variable and run:")
        display_info(f"  pkgmngr rename {new_name}")

def rename_github_repository(username, old_name, new_name, token, remote_url, base_dir=None):
    """
    Rename a GitHub repository and update the remote URL.
    
    Args:
        username: GitHub username
        old_name: Current repository name
        new_name: New repository name
        token: GitHub token
        remote_url: Current remote URL
        base_dir: Base directory (default: current directory)
        
    Returns:
        bool: True if successful, False otherwise
    """
    base_dir = base_dir or os.getcwd()
    display_info(f"Renaming GitHub repository from {old_name} to {new_name}...")
    
    success = github_api_rename_repo(username, old_name, new_name, token)
    if not success:
        return False
    
    # Update git remote URL
    new_remote_url = generate_new_remote_url(remote_url, old_name, new_name)
    update_git_remote(base_dir, new_remote_url)
    
    return True

def github_api_rename_repo(username, old_name, new_name, token):
    """
    Use GitHub API to rename a repository.
    
    Args:
        username: GitHub username
        old_name: Current repository name
        new_name: New repository name
        token: GitHub token
        
    Returns:
        bool: True if successful, False otherwise
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "name": new_name
    }
    
    try:
        response = requests.patch(
            f"https://api.github.com/repos/{username}/{old_name}",
            headers=headers,
            data=json.dumps(data)
        )
        
        if response.status_code == 200:
            display_success(f"Successfully renamed GitHub repository to {username}/{new_name}")
            return True
        else:
            error_msg = response.json().get('message', 'Unknown error')
            raise GithubError(f"Failed to rename GitHub repository: {error_msg}")
    except Exception as e:
        display_error(f"Error renaming GitHub repository: {str(e)}")
        return False

def generate_new_remote_url(remote_url, old_name, new_name):
    """
    Generate a new remote URL with the new repository name.
    
    Args:
        remote_url: Current remote URL
        old_name: Current repository name
        new_name: New repository name
        
    Returns:
        New remote URL
    """
    if "https://" in remote_url:
        return remote_url.replace(f"/{old_name}.git", f"/{new_name}.git")
    else:  # SSH format
        return remote_url.replace(f"/{old_name}.git", f"/{new_name}.git")

def update_git_remote(base_dir, new_remote_url):
    """
    Update Git remote URL.
    
    Args:
        base_dir: Base directory
        new_remote_url: New remote URL
    """
    with change_directory(base_dir):
        # Set the new remote URL
        try_operation(
            lambda: subprocess.run(
                ["git", "remote", "set-url", "origin", new_remote_url],
                check=True,
                stdout=subprocess.PIPE
            ),
            f"Failed to update Git remote URL",
            GitError
        )
        display_info(f"Updated git remote URL to {new_remote_url}")