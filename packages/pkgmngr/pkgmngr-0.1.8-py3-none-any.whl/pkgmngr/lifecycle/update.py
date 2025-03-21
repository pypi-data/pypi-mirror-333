"""
Update package structure to match current configuration.
"""
import os
import shutil
import json
import requests
import subprocess
from pathlib import Path
import re

from pkgmngr.common.utils import create_directory, create_file, sanitize_package_name, is_git_repository
from pkgmngr.common.errors import PackageError, GitError, GithubError, try_operation, assert_condition
from pkgmngr.common.cli import display_info, display_success, display_warning, confirm_action
from pkgmngr.common.config import load_config
from pkgmngr.common.templates import render_template
from pkgmngr.lifecycle.rename import rename_project


def update_package_structure(base_dir=None, force=False):
    """
    Update the package structure to match current configuration.
    
    Args:
        base_dir: Base directory to start from (default: current directory)
        force: If True, force updates without confirmation
        
    Returns:
        int: Exit code (0 for success)
        
    Raises:
        PackageError: If update fails
    """
    try:
        # Get current directory as root
        base_dir = base_dir or os.getcwd()
        root_dir = Path(base_dir)
        
        # Load configuration
        config, config_path = load_config(base_dir)
        package_name = config.get("package_name")
        
        if not package_name:
            raise PackageError("Package name not defined in config file")
        
        # 1. Regenerate setup.py
        update_setup_py(root_dir, force)
        
        # 2. Regenerate standard files that depend on config options
        update_standard_files(root_dir, force)
        
        # 3. Check if package name has changed and rename if necessary
        current_sanitized_name = detect_current_package_name(root_dir)
        target_sanitized_name = sanitize_package_name(package_name)
        
        if current_sanitized_name and current_sanitized_name != target_sanitized_name:
            display_info(f"Detected package name change: {current_sanitized_name} -> {target_sanitized_name}")
            
            # Confirm package rename
            if force or confirm_action(f"Rename package from {current_sanitized_name} to {target_sanitized_name}?", default=False):
                # Use the existing rename functionality
                rename_project(package_name, skip_github=True, base_dir=base_dir)
                display_success(f"Package renamed to {package_name}")
        
        # 4. Update Git and GitHub repository information
        update_git_repo_info(config, root_dir, force)
        
        display_success("Package structure updated successfully")
        return 0
        
    except Exception as e:
        if isinstance(e, PackageError):
            raise e
        else:
            raise PackageError(f"Failed to update package structure: {str(e)}")


def detect_current_package_name(root_dir):
    """
    Detect the current package name from the directory structure.
    
    Args:
        root_dir: Root directory path
        
    Returns:
        str: Current sanitized package name or None if not found
    """
    # Look for a directory that contains __init__.py
    potential_pkg_dirs = []
    
    for item in root_dir.iterdir():
        if item.is_dir() and (item / "__init__.py").exists():
            # Skip 'tests' and similar directories
            if item.name not in ['tests', 'test', 'docs', 'examples']:
                potential_pkg_dirs.append(item)
    
    if not potential_pkg_dirs:
        return None
        
    # If multiple potential package directories, use heuristics
    if len(potential_pkg_dirs) > 1:
        # Prefer the one with __main__.py
        for pkg_dir in potential_pkg_dirs:
            if (pkg_dir / "__main__.py").exists():
                return pkg_dir.name
                
        # Otherwise use the directory with the most Python files
        return max(
            potential_pkg_dirs,
            key=lambda d: len(list(d.glob("*.py")))
        ).name
    
    return potential_pkg_dirs[0].name


def update_setup_py(root_dir, force=False):
    """
    Update setup.py from template.
    
    Args:
        root_dir: Root directory path
        force: If True, force update without confirmation
    """
    file_path = root_dir / "setup.py"
    
    # Always regenerate setup.py to reflect current configuration
    if file_path.exists():
        if force or confirm_action("Regenerate setup.py to match current configuration?", default=True):
            content = render_template("setup_py")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            display_info("Updated setup.py")
    else:
        display_info("setup.py not found, creating new file")
        content = render_template("setup_py")
        create_file(file_path, content)


def update_standard_files(root_dir, force=False):
    """
    Update standard files that depend on configuration options.
    
    Args:
        root_dir: Root directory path
        force: If True, force update without confirmation
    """
    # Files that depend on config values like author, year, etc.
    config_dependent_files = [
        ("LICENSE", "license_mit"),
    ]
    
    for filename, template in config_dependent_files:
        file_path = root_dir / filename
        
        if file_path.exists():
            if force or confirm_action(f"Regenerate {filename} to match current configuration?", default=False):
                content = render_template(template)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                display_info(f"Updated {filename}")
        else:
            display_info(f"{filename} not found, creating new file")
            content = render_template(template)
            create_file(file_path, content)


def update_git_repo_info(config, root_dir, force=False):
    """
    Update Git repository information and GitHub repository description.
    
    Args:
        config: Configuration dictionary
        root_dir: Root directory path
        force: If True, force update without confirmation
    """
    description = config.get("description", "")
    
    # Only proceed if we have a description to update
    if not description:
        return
    
    # Check if this is a Git repository
    if not is_git_repository(root_dir):
        return
    
    # Update local Git repository description
    try:
        if force or confirm_action("Update Git repository description?", default=True):
            update_git_description(description, root_dir)
    except Exception as e:
        display_warning(f"Failed to update Git repository description: {str(e)}")
    
    # Check if there's a GitHub remote
    github_info = get_github_remote_info(root_dir)
    if not github_info:
        return
    
    # Try to update GitHub repository
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        if force or confirm_action("Update GitHub repository information?", default=True):
            update_github_repo(github_info["username"], github_info["repo_name"], description, github_token)


def update_git_description(description, root_dir):
    """
    Update Git repository description.
    
    Args:
        description: New repository description
        root_dir: Root directory path
    """
    try:
        subprocess.run(
            ["git", "config", "github.description", description],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        display_info("Updated Git repository description")
    except subprocess.CalledProcessError:
        # This is not critical, so just warn
        display_warning("Failed to update Git repository description")


def get_github_remote_info(root_dir):
    """
    Get GitHub username and repository name from remote URL.
    
    Args:
        root_dir: Root directory path
        
    Returns:
        dict: Dictionary with username and repo_name, or None if not a GitHub repository
    """
    try:
        # Get remote URL
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=root_dir,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        remote_url = result.stdout.strip()
        
        # Parse GitHub username and repository name
        if "github.com" in remote_url:
            # HTTPS URL format: https://github.com/username/repo.git
            if remote_url.startswith("https://"):
                parts = remote_url.split("/")
                if len(parts) >= 5:
                    username = parts[3]
                    repo_name = parts[4].replace(".git", "")
                    return {"username": username, "repo_name": repo_name}
            
            # SSH URL format: git@github.com:username/repo.git
            elif remote_url.startswith("git@"):
                parts = remote_url.split(":")
                if len(parts) >= 2:
                    username_repo = parts[1].split("/")
                    if len(username_repo) >= 2:
                        username = username_repo[0]
                        repo_name = username_repo[1].replace(".git", "")
                        return {"username": username, "repo_name": repo_name}
    
    except (subprocess.CalledProcessError, IndexError):
        pass
    
    return None


def update_github_repo(username, repo_name, description, token):
    """
    Update GitHub repository information.
    
    Args:
        username: GitHub username
        repo_name: Repository name
        description: New repository description
        token: GitHub API token
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "description": description
    }
    
    try:
        response = requests.patch(
            f"https://api.github.com/repos/{username}/{repo_name}",
            headers=headers,
            data=json.dumps(data)
        )
        
        if response.status_code == 200:
            display_success(f"Updated GitHub repository description")
        else:
            error_msg = response.json().get('message', 'Unknown error')
            display_warning(f"Failed to update GitHub repository: {error_msg}")
    
    except Exception as e:
        display_warning(f"Error updating GitHub repository: {str(e)}")