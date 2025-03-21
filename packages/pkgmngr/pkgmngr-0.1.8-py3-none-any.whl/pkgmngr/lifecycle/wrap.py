"""
Functionality to wrap existing code into a proper package structure.
"""
import os
import shutil
from pathlib import Path
import re

from pkgmngr.common.utils import create_directory, create_file, sanitize_package_name
from pkgmngr.common.errors import PackageError, try_operation, assert_condition
from pkgmngr.common.cli import display_info, display_success, display_warning, confirm_action, get_input_with_default
from pkgmngr.common.config import create_default_config
from pkgmngr.common.templates import render_template
from pkgmngr.common.pypi import check_name_availability


def wrap_existing_code(package_name=None, overwrite=None):
    """
    Wrap existing code into a proper package structure.
    
    Args:
        package_name: Optional name for the package (defaults to current directory name)
        overwrite: Boolean to control overwriting existing files or None to prompt
        
    Returns:
        int: Exit code (0 for success)
        
    Raises:
        PackageError: If wrapping fails
    """
    try:
        # Get current directory as root
        root_dir = Path(os.getcwd())
        
        # Get package name (from parameter or prompt)
        package_name = get_package_name(package_name, root_dir)
        
        # Check PyPI availability
        if not check_name_availability(package_name, context="wrap"):
            display_info("Operation cancelled.")
            return 0
        
        # Create sanitized name for Python module
        sanitized_name = sanitize_package_name(package_name)
        
        # Create default config
        config_path = create_project_config(package_name, root_dir, overwrite)
        
        # Create standard project files
        create_standard_files(root_dir, sanitized_name, overwrite)
        
        # Create or update package directory structure
        pkg_dir = organize_package_files(root_dir, sanitized_name, overwrite)
        
        # Organize test files
        organize_test_files(root_dir, sanitized_name, overwrite)
        
        # Display success message
        display_success_message(package_name, root_dir)
        
        return 0
        
    except Exception as e:
        if isinstance(e, PackageError):
            raise e
        else:
            raise PackageError(f"Failed to wrap existing code: {str(e)}")


def get_package_name(provided_name, root_dir):
    """
    Get package name from parameter or prompt user.
    
    Args:
        provided_name: Name provided as parameter (if any)
        root_dir: Root directory path
        
    Returns:
        str: Package name
    """
    if provided_name:
        return provided_name
    
    # Default to current directory name
    default_name = root_dir.name
    
    # Prompt user for package name
    package_name = get_input_with_default(
        "Enter package name", 
        default=default_name
    )
    
    return package_name


def create_project_config(package_name, root_dir, overwrite=None):
    """
    Create default config file for the project.
    
    Args:
        package_name: Name of the package
        root_dir: Root directory path
        overwrite: Boolean to control overwriting existing files or None to prompt
        
    Returns:
        str: Path to the config file
    """
    config_path = root_dir / "pkgmngr.toml"
    
    if config_path.exists():
        if overwrite is None:
            if not confirm_action(f"Config file {config_path} already exists. Overwrite?", default=False):
                display_info("Using existing config file.")
                return str(config_path)
        elif not overwrite:
            display_info("Using existing config file.")
            return str(config_path)
    
    # Create new config file
    config_path = create_default_config(package_name, str(root_dir))
    display_info(f"Created config file: {config_path}")
    
    return config_path


def create_standard_files(root_dir, sanitized_name, overwrite=None):
    """
    Create standard project files.
    
    Args:
        root_dir: Root directory path
        sanitized_name: Sanitized package name
        overwrite: Boolean to control overwriting existing files or None to prompt
    """
    # List of standard files to create
    standard_files = [
        ("setup.py", "setup_py"),
        ("README.md", "readme"),
        ("MANIFEST.in", "manifest_in"),
        ("pyproject.toml", "pyproject_toml"),
        ("LICENSE", "license_mit"),
        (".gitignore", "gitignore")
    ]
    
    for filename, template in standard_files:
        file_path = root_dir / filename
        
        if file_path.exists():
            # If overwrite is None, ask the user
            if overwrite is None:
                if not confirm_action(f"File {filename} already exists. Overwrite?", default=False):
                    display_info(f"Keeping existing {filename}")
                    continue
            # If overwrite is False, skip this file
            elif not overwrite:
                display_info(f"File {filename} already exists, skipping.")
                continue
            # If overwrite is True, we proceed to overwrite without asking
        
        try:
            # Render template and create file
            content = render_template(template)
            create_file(file_path, content)
            display_info(f"Created {filename}")
        except Exception as e:
            display_warning(f"Failed to create {filename}: {str(e)}")


def organize_package_files(root_dir, sanitized_name, overwrite=None):
    """
    Organize Python files and folders into package structure.
    
    Args:
        root_dir: Root directory path
        sanitized_name: Sanitized package name
        overwrite: Boolean to control overwriting existing files or None to prompt
        
    Returns:
        Path: Package directory path
    """
    # Create package directory if it doesn't exist
    pkg_dir = root_dir / sanitized_name
    if not pkg_dir.exists():
        create_directory(pkg_dir)
        display_info(f"Created package directory: {sanitized_name}")
    
    # Create __init__.py if it doesn't exist
    init_file = pkg_dir / "__init__.py"
    if not init_file.exists():
        content = render_template("init_py")
        create_file(init_file, content)
        display_info(f"Created {sanitized_name}/__init__.py")
    
    # Create __main__.py if it doesn't exist
    main_file = pkg_dir / "__main__.py"
    if not main_file.exists():
        content = render_template("main_py")
        create_file(main_file, content)
        display_info(f"Created {sanitized_name}/__main__.py")
    
    # Find Python files in root directory (excluding tests)
    root_py_files = [
        f for f in root_dir.glob("*.py") 
        if not f.name.startswith("test_") and f.name != "setup.py"
    ]
    
    # Move Python files to package directory
    for py_file in root_py_files:
        target_path = pkg_dir / py_file.name
        
        if target_path.exists():
            # Handle overwrite based on parameter or user choice
            if overwrite is None:
                if not confirm_action(f"File {py_file.name} already exists in package directory. Overwrite?", default=False):
                    display_info(f"Keeping existing {target_path.name}")
                    continue
            elif not overwrite:
                display_warning(f"File {target_path.name} already exists in package directory, skipping.")
                continue
                
        if confirm_action(f"Move {py_file.name} to {sanitized_name}/ directory?", default=True):
            shutil.move(str(py_file), str(target_path))
            display_info(f"Moved {py_file.name} to {sanitized_name}/ directory")
    
    # Find subdirectories in root (excluding standard ones)
    subdirs = [
        d for d in root_dir.iterdir()
        if d.is_dir() and d.name not in [sanitized_name, 'tests', 'build', 'dist', '.git', 'venv', '.venv', '__pycache__', '.pytest_cache']
    ]
    
    # Process each subdirectory
    for subdir in subdirs:
        if confirm_action(f"Move directory '{subdir.name}' into the {sanitized_name}/ package?", default=False):
            target_dir = pkg_dir / subdir.name
            
            # Check if target directory already exists
            if target_dir.exists():
                if overwrite is None:
                    if not confirm_action(f"Directory {target_dir.name} already exists in package. Merge contents?", default=False):
                        display_info(f"Skipping directory {subdir.name}")
                        continue
                elif not overwrite:
                    display_warning(f"Directory {subdir.name} already exists in package, skipping.")
                    continue
                # If we're merging, we'll handle files individually
                merge_directories(subdir, target_dir, overwrite)
            else:
                # Move the whole directory
                shutil.move(str(subdir), str(target_dir))
                display_info(f"Moved directory {subdir.name}/ to {sanitized_name}/{subdir.name}/")
            
            # Ensure the subdirectory has an __init__.py
            init_file = target_dir / "__init__.py"
            if not init_file.exists():
                create_file(init_file, f'"""\n{subdir.name} module for {sanitized_name}.\n"""\n')
                display_info(f"Created {sanitized_name}/{subdir.name}/__init__.py")
    
    # Now recursively handle other subdirectories in the package
    add_init_to_subdirs(pkg_dir, sanitized_name)
    
    return pkg_dir


def merge_directories(source_dir, target_dir, overwrite=None):
    """
    Merge the contents of source directory into target directory.
    
    Args:
        source_dir: Source directory path
        target_dir: Target directory path
        overwrite: Boolean to control overwriting existing files or None to prompt
    """
    # Create target directory if it doesn't exist
    if not target_dir.exists():
        create_directory(target_dir)
    
    # Process each file in the source directory
    for item in source_dir.iterdir():
        target_item = target_dir / item.name
        
        if item.is_dir():
            # Recursively merge subdirectories
            merge_directories(item, target_item, overwrite)
        else:
            if target_item.exists():
                # Handle overwrite based on parameter or user choice
                if overwrite is None:
                    if not confirm_action(f"File {item.name} already exists in {target_dir}. Overwrite?", default=False):
                        continue
                elif not overwrite:
                    display_info(f"Skipping existing file: {target_item}")
                    continue
            
            # Copy the file
            shutil.copy2(str(item), str(target_item))
            display_info(f"Copied {item} to {target_item}")
    
    # After successful merge, optionally remove the source directory
    if confirm_action(f"Remove original directory {source_dir} after merging?", default=False):
        shutil.rmtree(str(source_dir))
        display_info(f"Removed original directory: {source_dir}")


def add_init_to_subdirs(directory, package_name):
    """
    Recursively add __init__.py files to all subdirectories of a directory.
    
    Args:
        directory: Directory to process
        package_name: Name of the package for docstrings
    """
    # Process each subdirectory
    for item in directory.iterdir():
        if item.is_dir() and not item.name.startswith("__pycache__"):
            # Add __init__.py to this subdirectory if it doesn't exist
            init_file = item / "__init__.py"
            if not init_file.exists():
                relative_path = os.path.relpath(item, directory.parent)
                create_file(init_file, f'"""\n{item.name} module for {package_name}.\n"""\n')
                display_info(f"Created {relative_path}/__init__.py")
            
            # Recursively process subdirectories
            add_init_to_subdirs(item, package_name)


def organize_test_files(root_dir, sanitized_name, overwrite=None):
    """
    Organize test files into tests directory.
    
    Args:
        root_dir: Root directory path
        sanitized_name: Sanitized package name
        overwrite: Boolean to control overwriting existing files or None to prompt
    """
    # Create tests directory if it doesn't exist
    tests_dir = root_dir / "tests"
    if not tests_dir.exists():
        create_directory(tests_dir)
        display_info("Created tests/ directory")
    
    # Create an empty __init__.py in tests directory if it doesn't exist
    init_file = tests_dir / "__init__.py"
    if not init_file.exists():
        create_file(init_file, '"""Test package."""\n')
        display_info("Created tests/__init__.py")
    
    # Create run_tests.py if it doesn't exist
    run_tests_file = tests_dir / "run_tests.py"
    if not run_tests_file.exists():
        content = render_template("run_tests_py")
        create_file(run_tests_file, content)
        display_info("Created tests/run_tests.py")
    
    # Find test files in root directory
    test_files = [
        f for f in root_dir.glob("*.py") 
        if f.name.startswith("test_")
    ]
    
    # Create a default test file if none exist
    if not test_files and not list(tests_dir.glob("test_*.py")):
        content = render_template("test_py")
        create_file(tests_dir / f"test_{sanitized_name}.py", content)
        display_info(f"Created tests/test_{sanitized_name}.py")
    
    # Move test files to tests directory
    for test_file in test_files:
        target_path = tests_dir / test_file.name
        
        if target_path.exists():
            # Handle overwrite based on parameter or user choice
            if overwrite is None:
                if not confirm_action(f"File {test_file.name} already exists in tests directory. Overwrite?", default=False):
                    display_info(f"Keeping existing {target_path.name}")
                    continue
            elif not overwrite:
                display_warning(f"File {test_file.name} already exists in tests directory, skipping.")
                continue
                
        if confirm_action(f"Move {test_file.name} to tests/ directory?", default=True):
            shutil.move(str(test_file), str(target_path))
            display_info(f"Moved {test_file.name} to tests/ directory")


def display_success_message(package_name, root_dir):
    """
    Display success message with actual package structure.
    
    Args:
        package_name: Name of the package
        root_dir: Root directory path
    """
    display_success(f"Successfully wrapped existing code into package structure: {package_name}")
    
    # Get the actual directory structure
    print("\nCreated/Updated structure:")
    
    # We can reuse the package tree visualization from the snapshot module
    try:
        from pkgmngr.snapshot.snapshot import get_file_tree
        # Create a mock gitignore spec that ignores common patterns
        from pathspec import PathSpec
        mock_patterns = [
            "*.pyc", "__pycache__/", "*.egg-info/", "build/", "dist/",
            ".git/", ".env/", "venv/", ".venv/"
        ]
        gitignore_spec = PathSpec.from_lines('gitwildmatch', mock_patterns)
        
        # Get and print the tree
        tree = get_file_tree(root_dir, gitignore_spec, None)
        print(tree)
    except Exception:
        # Fallback to simpler visualization if we can't import or run the tree function
        sanitized_name = sanitize_package_name(package_name)
        print(f"./{root_dir.name}/")
        print(f"├── {sanitized_name}/")
        print(f"│   ├── __init__.py")
        print(f"│   └── __main__.py")
        print(f"├── tests/")
        print(f"├── setup.py")
        print(f"├── README.md")
        print(f"└── pkgmngr.toml")
    
    print("\nNext steps:")
    print("1. Review the generated files and make any necessary adjustments")
    print("2. Run 'pkgmngr init-repo' to initialize Git and GitHub repositories (optional)")
    print("3. Run 'pkgmngr snapshot' to create a snapshot of your package")