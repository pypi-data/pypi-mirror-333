"""
Lifecycle management functions for package creation and maintenance.
"""

import os
import subprocess
import shutil
from pathlib import Path

from pkgmngr.common.utils import sanitize_package_name, change_directory, find_python_executable, is_git_repository, update_file_content
from pkgmngr.common.errors import PackageError, GitError, GithubError, ConfigError, error_handler, try_operation
from pkgmngr.common.cli import display_info, display_success, display_warning, display_error, get_input_with_default
from pkgmngr.common.config import load_config, save_config, get_github_info


@error_handler
def dump_to_github(base_dir=None):
    """
    Commit all changes and push to GitHub.
    
    Args:
        base_dir: Base directory (default: current directory)
    
    Returns:
        int: 0 if successful, 1 otherwise
    """
    base_dir = base_dir or os.getcwd()
    
    # Check if inside a Git repository
    if not is_git_repository(base_dir):
        raise GitError("Not inside a Git repository. Run 'pkgmngr create init-repo' first to initialize Git")
    
    # Ask for commit message
    display_info("Enter a commit message:")
    commit_message = input("> ").strip()
    if not commit_message:
        commit_message = "Update package files"
    
    with change_directory(base_dir):
        return execute_git_operations(commit_message)


def execute_git_operations(commit_message):
    """
    Execute Git operations (add, commit, push).
    
    Args:
        commit_message: Commit message
        
    Returns:
        int: 0 if successful, 1 otherwise
        
    Raises:
        GitError: If Git operations fail
    """
    # Check if there are changes to commit
    status_output = check_git_status()
    if not status_output:
        display_info("No changes to commit")
        return 0
    
    # Add all changes
    add_changes_to_git()
    
    # Commit changes
    commit_changes(commit_message)
    
    # Push to remote
    push_changes_to_remote()
    
    return 0


def check_git_status():
    """
    Check Git status to see if there are changes.
    
    Returns:
        Status output or empty string if no changes
    """
    status_output = subprocess.check_output(
        ["git", "status", "--porcelain"],
        universal_newlines=True
    )
    return status_output.strip()


def add_changes_to_git():
    """
    Add all changes to Git staging area.
    
    Raises:
        GitError: If adding changes fails
    """
    try_operation(
        lambda: subprocess.run(["git", "add", "."], check=True),
        "Failed to add changes to Git staging area",
        GitError
    )
    display_info("Added all changes to staging area")


def commit_changes(commit_message):
    """
    Commit changes to Git.
    
    Args:
        commit_message: Commit message
        
    Raises:
        GitError: If committing changes fails
    """
    try_operation(
        lambda: subprocess.run(["git", "commit", "-m", commit_message], check=True),
        "Failed to commit changes",
        GitError
    )
    display_info(f"Committed changes with message: '{commit_message}'")


def push_changes_to_remote():
    """
    Push changes to remote Git repository.
    
    Raises:
        GitError: If pushing changes fails
    """
    # Get current branch
    current_branch = subprocess.check_output(
        ["git", "branch", "--show-current"],
        universal_newlines=True
    ).strip()
    
    try_operation(
        lambda: subprocess.run(["git", "push", "origin", current_branch], check=True),
        f"Failed to push changes to GitHub branch '{current_branch}'",
        GitError
    )
    display_success(f"Pushed changes to GitHub (branch: {current_branch})")