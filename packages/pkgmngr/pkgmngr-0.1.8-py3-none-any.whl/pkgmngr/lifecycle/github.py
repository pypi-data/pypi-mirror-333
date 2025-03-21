"""
GitHub integration for package creation.
"""

import os
import subprocess
import json
import requests
from pathlib import Path

from pkgmngr.common.errors import GitError, GithubError, try_operation, assert_condition
from pkgmngr.common.cli import display_info, display_success, display_warning


def init_git_repo(directory, package_name, github_token=None, github_username=None, private=False):
    """
    Initialize a Git repository and optionally create a GitHub repository and push to it.
    
    Args:
        directory: Path to the directory
        package_name: Name of the package
        github_token: GitHub personal access token
        github_username: GitHub username
        private: Whether the GitHub repository should be private
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Change to the package directory if not already there
        original_dir = os.getcwd()
        os.chdir(directory)
        
        # Initialize local git repository first
        initialize_local_git_repo()
        
        # If GitHub token and username are provided, create a GitHub repository
        if github_token and github_username:
            github_success = create_github_repo(package_name, github_token, github_username, private)
            os.chdir(original_dir)
            return github_success
        elif github_username and not github_token:
            display_warning(f"No GitHub token provided. Skipping GitHub repository creation.")
            display_info(f"To create a GitHub repository later, set the GITHUB_TOKEN environment variable")
            display_info(f"and run 'pkgmngr create init-repo' again.")
        else:
            display_info("Local Git repository initialized. No GitHub repository created.")
        
        os.chdir(original_dir)
        return True
    
    except Exception as e:
        # Ensure we always return to the original directory
        os.chdir(original_dir)
        
        # Re-raise as appropriate error type
        if isinstance(e, (GitError, GithubError)):
            raise e
        else:
            raise GitError(f"Error initializing Git repository: {str(e)}")


def initialize_local_git_repo():
    """
    Initialize a local Git repository if not already initialized.
    
    Raises:
        GitError: If Git initialization fails
    """
    # Check if Git is already initialized
    if os.path.exists(".git"):
        display_info("Git repository already initialized")
        return
    
    # Initialize git repository
    try_operation(
        lambda: subprocess.run(["git", "init"], check=True, stdout=subprocess.PIPE),
        "Failed to initialize Git repository",
        GitError
    )
    display_info("Initialized empty Git repository")
    
    # Add all files
    try_operation(
        lambda: subprocess.run(["git", "add", "."], check=True, stdout=subprocess.PIPE),
        "Failed to add files to Git repository",
        GitError
    )
    
    # Commit
    try_operation(
        lambda: subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            check=True,
            stdout=subprocess.PIPE
        ),
        "Failed to create initial commit",
        GitError
    )
    display_info("Created initial commit")


def create_github_repo(package_name, github_token, github_username, private=False):
    """
    Create a GitHub repository and push the local repository to it.
    
    Args:
        package_name: Name of the package
        github_token: GitHub personal access token
        github_username: GitHub username
        private: Whether the GitHub repository should be private
    
    Returns:
        bool: True if successful, False otherwise
    
    Raises:
        GithubError: If GitHub API request fails
        GitError: If Git operations fail
    """
    # Check if remote origin already exists
    if has_github_remote():
        return True
    
    # Create the repository on GitHub
    repo_url = create_github_repository(package_name, github_token, github_username, private)
    
    # Configure and push to the remote
    setup_and_push_to_remote(repo_url)
    
    return True


def has_github_remote():
    """
    Check if a GitHub remote already exists.
    
    Returns:
        bool: True if remote exists, False otherwise
    """
    try:
        remote_url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            stderr=subprocess.PIPE,
            universal_newlines=True
        ).strip()
        display_info(f"GitHub remote already exists: {remote_url}")
        return True
    except subprocess.CalledProcessError:
        # Remote doesn't exist
        return False


def create_github_repository(package_name, github_token, github_username, private=False):
    """
    Create a repository on GitHub via the API.
    
    Args:
        package_name: Name of the package
        github_token: GitHub personal access token
        github_username: GitHub username
        private: Whether the repository should be private
    
    Returns:
        str: URL of the created repository
    
    Raises:
        GithubError: If repository creation fails
    """
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "name": package_name,
        "private": private,
        "description": f"Python package: {package_name}",
        "auto_init": False
    }
    
    display_info(f"Creating GitHub repository: {github_username}/{package_name}...")
    
    try:
        response = requests.post(
            "https://api.github.com/user/repos",
            headers=headers,
            data=json.dumps(data)
        )
        
        if response.status_code == 201:
            display_success(f"Created GitHub repository: {github_username}/{package_name}")
            repo_data = response.json()
            return repo_data["html_url"]
        else:
            error_message = response.json().get('message', 'Unknown error')
            raise GithubError(f"Failed to create GitHub repository: {error_message}")
    except requests.RequestException as e:
        raise GithubError(f"GitHub API request failed: {str(e)}")


def setup_and_push_to_remote(repo_url):
    """
    Add remote and push to GitHub.
    
    Args:
        repo_url: URL of the GitHub repository
    
    Raises:
        GitError: If Git operations fail
    """
    # Add remote
    remote_url = f"{repo_url}.git"
    try_operation(
        lambda: subprocess.run(
            ["git", "remote", "add", "origin", remote_url],
            check=True,
            stdout=subprocess.PIPE
        ),
        f"Failed to add remote origin: {remote_url}",
        GitError
    )
    
    # Push to GitHub with appropriate branch name detection
    push_to_github(remote_url)


def push_to_github(remote_url):
    """
    Push to GitHub repository, handling different branch name conventions.
    
    Args:
        remote_url: URL of the GitHub repository
    
    Raises:
        GitError: If push fails
    """
    display_info("Pushing code to GitHub...")
    
    # Try main branch first (newer Git versions)
    try:
        subprocess.run(
            ["git", "push", "-u", "origin", "main"],
            check=True,
            stdout=subprocess.PIPE
        )
        display_success(f"Pushed code to GitHub: {remote_url}")
        return
    except subprocess.CalledProcessError:
        pass
    
    # Try master branch (older Git versions)
    try:
        subprocess.run(
            ["git", "push", "-u", "origin", "master"],
            check=True,
            stdout=subprocess.PIPE
        )
        display_success(f"Pushed code to GitHub: {remote_url}")
        return
    except subprocess.CalledProcessError:
        pass
    
    # Determine current branch as a fallback
    try:
        current_branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            universal_newlines=True
        ).strip()
        
        subprocess.run(
            ["git", "push", "-u", "origin", current_branch],
            check=True,
            stdout=subprocess.PIPE
        )
        display_success(f"Pushed code to GitHub: {remote_url}")
    except subprocess.CalledProcessError as e:
        raise GitError(f"Failed to push to GitHub repository: {remote_url}. Error: {str(e)}")

def get_user_email_from_git():
    """
    Try to get GitHub username from git config.
    
    Returns:
        str: GitHub username or None if not found
    """
    try:
        # First try to get user.name
        email = subprocess.check_output(
            ["git", "config", "user.email"], 
            stderr=subprocess.PIPE,
            universal_newlines=True
        ).strip()
        return email
    except subprocess.CalledProcessError:
        return None

def get_github_username_from_git():
    """
    Try to get GitHub username from git config.
    
    Returns:
        str: GitHub username or None if not found
    """
    try:
        # First try to get user.name
        name = subprocess.check_output(
            ["git", "config", "user.name"], 
            stderr=subprocess.PIPE,
            universal_newlines=True
        ).strip()
        return name
    except subprocess.CalledProcessError:
        return None