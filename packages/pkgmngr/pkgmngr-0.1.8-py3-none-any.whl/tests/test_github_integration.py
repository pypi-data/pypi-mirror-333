"""
Tests for GitHub integration functionality.
"""
import os
import pytest
import json
import requests
from unittest.mock import patch, MagicMock
from pkgmngr.lifecycle.github import (
    init_git_repo,
    create_github_repo,
    get_github_username_from_git
)


@pytest.fixture
def mock_requests(monkeypatch):
    """Mock requests module for GitHub API tests."""
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            
        def json(self):
            return self.json_data
    
    def mock_post(*args, **kwargs):
        # Mock creating a GitHub repository
        if "api.github.com/user/repos" in args[0]:
            data = json.loads(kwargs.get("data", "{}"))
            repo_name = data.get("name", "unknown")
            return MockResponse(
                {
                    "name": repo_name,
                    "full_name": f"testuser/{repo_name}",
                    "html_url": f"https://github.com/testuser/{repo_name}"
                },
                201
            )
        return MockResponse({}, 404)
    
    monkeypatch.setattr(requests, "post", mock_post)


def test_init_git_repo_locally(mock_git_repo, monkeypatch):
    """Test initializing a git repository locally (without GitHub)."""
    # Set up
    package_name = "test-pkg"
    
    # Run the function
    result = init_git_repo(mock_git_repo, package_name)
    
    # Verify the result
    assert result is True


def test_create_github_repo(mock_git_repo, mock_requests):
    """Test creating a GitHub repository."""
    # Set up
    package_name = "test-pkg"
    github_token = "fake_token"
    github_username = "testuser"
    
    # Run the function
    result = create_github_repo(package_name, github_token, github_username)
    
    # Verify the result
    assert result is True


def test_get_github_username_from_git(monkeypatch):
    """Test getting GitHub username from git config."""
    # Mock subprocess.check_output to return a fake username
    def mock_check_output(*args, **kwargs):
        if "user.name" in args[0]:
            return b"testuser\n"
        elif "user.email" in args[0]:
            return b"test@example.com\n"
        return b""
    
    import subprocess
    monkeypatch.setattr(subprocess, "check_output", mock_check_output)
    
    # Run the function
    username = get_github_username_from_git()
    
    # Verify the result - add .decode() to convert bytes to string
    assert (username.decode() if isinstance(username, bytes) else username) == "testuser"