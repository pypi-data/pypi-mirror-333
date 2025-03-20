"""
Configuration management for pkgmngr.
"""
import os
import toml
from pathlib import Path
from typing import Dict, Tuple, Any, Optional


def find_config_file(start_dir: Optional[str] = None) -> Optional[str]:
    """
    Find the nearest pkgmngr.toml file by traversing up the directory tree.
    
    Args:
        start_dir: Directory to start the search (default: current directory)
        
    Returns:
        Path to the config file or None if not found
    """
    current_dir = Path(start_dir or os.getcwd())
    
    # Traverse up to find the config file
    max_depth = 10  # Prevent infinite loops
    for _ in range(max_depth):
        config_path = current_dir / "pkgmngr.toml"
        if config_path.exists():
            return str(config_path)
        
        # Move up one directory
        parent_dir = current_dir.parent
        if parent_dir == current_dir:  # Reached root directory
            break
        current_dir = parent_dir
    
    return None


def load_config(base_dir: Optional[str] = None) -> Tuple[Dict[str, Any], str]:
    """
    Load configuration from pkgmngr.toml file.
    
    Args:
        base_dir: Base directory to look for config (default: current directory)
        
    Returns:
        Tuple of (config dict, config path)
        
    Raises:
        FileNotFoundError: If config file not found
    """
    if base_dir:
        config_path = os.path.join(base_dir, "pkgmngr.toml")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
    else:
        config_path = find_config_file()
        if not config_path:
            raise FileNotFoundError("Config file pkgmngr.toml not found in current directory or parents")
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = toml.load(f)
    
    return config, config_path


def save_config(config: Dict[str, Any], config_path: str) -> None:
    """
    Save configuration to file.
    
    Args:
        config: Configuration dictionary
        config_path: Path to save the configuration
    """
    with open(config_path, "w", encoding="utf-8") as f:
        toml.dump(config, f)


def get_package_name(base_dir: Optional[str] = None) -> str:
    """
    Get the package name from configuration.
    
    Args:
        base_dir: Base directory to look for config (default: current directory)
        
    Returns:
        Package name as string
        
    Raises:
        FileNotFoundError: If config file not found
        KeyError: If package_name not defined in config
    """
    config, _ = load_config(base_dir)
    
    if "package_name" not in config:
        raise KeyError("package_name not defined in config file")
    
    return config["package_name"]


def get_github_info(base_dir: Optional[str] = None) -> Tuple[Optional[str], bool]:
    """
    Get GitHub username and private flag from configuration.
    
    Args:
        base_dir: Base directory to look for config (default: current directory)
        
    Returns:
        Tuple of (github_username, private_flag)
    """
    try:
        config, _ = load_config(base_dir)
        github_config = config.get("github", {})
        
        username = github_config.get("username")
        private = github_config.get("private", False)
        
        return username, private
    except (FileNotFoundError, KeyError):
        return None, False


def create_default_config(package_name: str, output_dir: str,**kwargs) -> str:
    """
    Create a default configuration file for a new package.
    
    Args:
        package_name: Name of the package
        output_dir: Directory to create the config file in
        
    Returns:
        Path to the created config file
    """
    import datetime
    from pkgmngr.lifecycle.github import get_github_username_from_git, get_user_email_from_git
    
    # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Default config values
    current_year = datetime.datetime.now().year
    author = os.environ.get("USER", "Your Name")
    github_username = get_github_username_from_git()
    author_email=get_user_email_from_git()
    
    config = {
        "package_name": package_name,
        "version": "0.1.0",
        "author": author,
        "author_email":author_email,
        "year": str(current_year),
        "description": f"A Python package named {package_name}",
        
        "github": {
            "username": github_username,
            "private": False
        },
        
        "python_requires": ">=3.6",
        "classifiers": [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        "install_requires":[],
        "extra_requires":{
            'dev':[
                "pytest",
                "pytest-cov",
                "flake8",
                "black",
            ]
        }
    }

    config.update(kwargs)
    
    # Create the config file
    config_path = os.path.join(output_dir, "pkgmngr.toml")
    save_config(config, config_path)
    
    return config_path