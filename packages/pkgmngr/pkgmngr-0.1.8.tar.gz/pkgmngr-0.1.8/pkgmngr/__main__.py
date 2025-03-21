#!/usr/bin/env python
"""
Main entry point for pkgmngr CLI.
"""
import os
import sys
import argparse
from pathlib import Path

from pkgmngr.common.errors import error_handler
from pkgmngr.common.cli import display_info, display_error

def create_main_parser():
    """
    Create the main argument parser with all subparsers.
    
    Returns:
        argparse.ArgumentParser: The configured argument parser
    """
    # Create the top-level parser
    parser = argparse.ArgumentParser(
        description="pkgmngr: Comprehensive Python package management utilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a new package
  pkgmngr new my-package
  
  # Generate package files in the current directory
  pkgmngr create
  
  # Initialize Git and GitHub repositories
  pkgmngr init-repo
  
  # Create a snapshot of the current state
  pkgmngr snapshot
  
  # Restore from a snapshot
  pkgmngr restore [snapshot_id]
  
  # Rename a package (including GitHub repository)
  pkgmngr rename old-package-name new-package-name

  # Replace text across the package
  pkgmngr replace old-text new-text
  
  # Push changes to GitHub
  pkgmngr push
  
  # Publish to PyPI
  pkgmngr publish
        """
    )
    
    # Add version argument
    parser.add_argument(
        '-v', '--version',
        action='store_true',
        help="Show pkgmngr version and exit"
    )
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Register all command subparsers
    register_create_commands(subparsers)
    register_wrap_commands(subparsers)
    register_update_commands(subparsers)
    register_snapshot_commands(subparsers)
    register_restore_commands(subparsers)
    register_rename_commands(subparsers)
    register_replace_commands(subparsers)
    register_push_commands(subparsers)
    register_publish_commands(subparsers)
    
    return parser

def register_create_commands(subparsers):
    """
    Register commands related to package creation.
    
    Args:
        subparsers: Subparsers object to add to
    """
    # 'new' command
    new_parser = subparsers.add_parser("new", help="Create a new package directory with config file")
    new_parser.add_argument("package_name", help="Name of the package to create")
    
    # 'create' command - Generate project from config (no arguments needed)
    subparsers.add_parser("create", help="Create package structure from config file in current directory")
    
    # 'init-repo' command - Initialize git and GitHub repositories
    subparsers.add_parser("init-repo", help="Initialize Git and GitHub repositories")

def register_wrap_commands(subparsers):
    """
    Register commands related to wrapping existing code.
    
    Args:
        subparsers: Subparsers object to add to
    """
    # 'wrap' command
    wrap_parser = subparsers.add_parser("wrap", help="Wrap existing code into a proper package structure")
    wrap_parser.add_argument(
        "--name", 
        type=str,
        dest="package_name",
        help="Name for the package (defaults to current directory name)"
    )
    wrap_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Automatically overwrite existing files without prompting"
    )
    wrap_parser.add_argument(
        "--no-overwrite",
        action="store_true",
        help="Never overwrite existing files"
    )

def register_update_commands(subparsers):
    """
    Register commands related to updating package structure.
    
    Args:
        subparsers: Subparsers object to add to
    """
    # 'update' command
    update_parser = subparsers.add_parser("update", help="Update package structure to match current configuration")
    update_parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force updates without confirmation prompts"
    )

def register_snapshot_commands(subparsers):
    """
    Register commands related to snapshot functionality.
    
    Args:
        subparsers: Subparsers object to add to
    """
    # 'snapshot' command
    snapshot_parser = subparsers.add_parser("snapshot", help="Create a snapshot of the current state")
    snapshot_parser.add_argument(
        '-m', '--message',
        type=str,
        help="Add a comment message to the snapshot describing its purpose."
    )
    snapshot_parser.add_argument(
        '--no-comment-prompt',
        action='store_true',
        help="Don't prompt for a comment message if one isn't provided."
    )
    snapshot_parser.add_argument(
        '-l', '--list',
        action='store_true',
        help="List all available snapshots and exit"
    )
    
def register_restore_commands(subparsers):
    # 'restore' command - simplified without mode parameter
    restore_parser = subparsers.add_parser("restore", help="Restore from a snapshot")
    restore_parser.add_argument(
        'snapshot_id',
        nargs='?',
        help="ID or path of the snapshot to restore from"
    )
    restore_parser.add_argument(
        '--no-backup',
        action='store_true',
        help="Skip creating a backup before restoration."
    )
    restore_parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help="Interactively select files to restore"
    )
    restore_parser.add_argument(
        '-p', '--pattern',
        action='append',
        dest='patterns',
        help="Include only files matching this glob pattern (can be used multiple times)"
    )
    restore_parser.add_argument(
        '-e', '--exclude',
        action='append',
        dest='exclude_patterns',
        help="Exclude files matching this glob pattern (can be used multiple times)"
    )

def register_rename_commands(subparsers):
    """
    Register commands related to lifecycle management.
    
    Args:
        subparsers: Subparsers object to add to
    """
    # 'rename' command - Updated to only require new name
    rename_parser = subparsers.add_parser("rename", help="Rename the package, update all references, and optionally rename GitHub repository")
    rename_parser.add_argument("new_name", help="New name for the package")
    rename_parser.add_argument("--skip-github", action="store_true", help="Skip GitHub repository renaming even if GitHub token is available")

def register_push_commands(subparsers):
    # Other commands remain unchanged
    # 'push' command
    subparsers.add_parser("push", help="Commit all changes and push to GitHub")

def register_publish_commands(subparsers):    
    # 'publish' command
    publish_parser = subparsers.add_parser("publish", help="Build and upload package to PyPI")
    publish_parser.add_argument(
        '--test',
        action='store_true',
        help="Upload to TestPyPI instead of PyPI"
    )
    publish_parser.add_argument(
        '--bump',
        choices=['patch', 'minor', 'major'],
        default='patch',
        help="Version increment type (default: patch)"
    )

def register_replace_commands(subparsers):
    # 'replace' command
    replace_parser = subparsers.add_parser("replace", help="Safely replace text across all files")
    replace_parser.add_argument("old_pattern", help="Pattern to search for")
    replace_parser.add_argument("new_pattern", help="Pattern to replace with")
    replace_parser.add_argument("-r", "--regex", action="store_true", help="Treat patterns as regular expressions")
    replace_parser.add_argument("-i", "--case-insensitive", action="store_true", help="Perform case-insensitive matching")
    replace_parser.add_argument("-p", "--pattern", action="append", dest="patterns", help="Only process files matching this glob pattern")
    replace_parser.add_argument("-e", "--exclude", action="append", dest="exclude_patterns", help="Exclude files matching this glob pattern")
    replace_parser.add_argument("--no-backup", action="store_true", help="Don't create a backup snapshot before replacement")
    replace_parser.add_argument("--no-preview", action="store_true", help="Don't show preview of changes")

@error_handler
def handle_version_command():
    """
    Handle the version command.
    
    Returns:
        int: Exit code
    """
    from pkgmngr import __version__
    print(f"pkgmngr version {__version__}")
    return 0

@error_handler
def dispatch_command(args):
    """
    Dispatch to the appropriate command handler based on arguments.
    
    Args:
        args: The parsed arguments
        
    Returns:
        int: Exit code
    """
    # No command specified
    if not args.command:
        return 1
    
    # Execute commands
    if args.command == "new":
        from pkgmngr.lifecycle.cli import create_package_config
        return create_package_config(args.package_name)
    
    elif args.command == "create":
        from pkgmngr.lifecycle.cli import create_from_config
        return create_from_config()
        
    elif args.command == "wrap":
        from pkgmngr.lifecycle.wrap import wrap_existing_code
        # Determine overwrite mode based on args
        overwrite = True if args.overwrite else (False if args.no_overwrite else None)
        return wrap_existing_code(args.package_name, overwrite)
        
    elif args.command == "update":
        from pkgmngr.lifecycle.update import update_package_structure
        return update_package_structure(None, args.force)
    
    elif args.command == "init-repo":
        from pkgmngr.lifecycle.cli import init_repository
        return init_repository()
            
    elif args.command == "rename":
        from pkgmngr.lifecycle.rename import rename_project
        return rename_project(args.new_name, args.skip_github)
    
    elif args.command == "replace":
        from pkgmngr.lifecycle.replace import handle_replace_command
        return handle_replace_command(args)
    
    elif args.command == "snapshot":
        return handle_snapshot_command(args)
    
    elif args.command == "restore":
        return handle_restore_command(args)
    
    elif args.command == "push":
        from pkgmngr.lifecycle.repo import dump_to_github
        return dump_to_github()
        
    elif args.command == "publish":
        from pkgmngr.lifecycle.pypi import upload_to_pypi
        return upload_to_pypi(test=args.test, bump=args.bump)
    
    else:
        return 1

@error_handler
def handle_snapshot_command(args):
    """
    Handle the snapshot command.
    
    Args:
        args: The parsed arguments
        
    Returns:
        int: Exit code
    """
    from pkgmngr.snapshot.utils import list_available_snapshots, display_snapshot_list
    from pkgmngr.snapshot.cli import handle_snapshot_create
    
    # Special handling for --list option
    if args.list:
        snapshots = list_available_snapshots()
        display_snapshot_list(snapshots)
        return 0
    
    # Default snapshot behavior
    return handle_snapshot_create(args)

@error_handler
def handle_restore_command(args):
    """
    Handle the restore command.
    
    Args:
        args: The parsed arguments
        
    Returns:
        int: Exit code
    """
    from pkgmngr.snapshot.utils import get_snapshot_path, select_snapshot_interactive
    from pkgmngr.snapshot.restore import restore_from_snapshot, selective_restore
    
    # Convert snapshot arg to a path if it's a number
    snapshot_file = None
    if args.snapshot_id:
        snapshot_file = get_snapshot_path(args.snapshot_id)
        if not snapshot_file:
            return 1
    else:
        # If no snapshot file is specified, prompt for selection
        snapshot_file = select_snapshot_interactive()
        if not snapshot_file:
            return 1
    
    # Make target directory absolute
    target_dir = os.path.abspath('.')
    
    # Create backup?
    create_backup = not args.no_backup
    
    # Check if selective restore is being used
    if args.patterns or args.exclude_patterns or args.interactive:
        return handle_selective_restore(snapshot_file, target_dir, args, create_backup)
    else:
        # Use the standard restore
        return handle_standard_restore(snapshot_file, target_dir, create_backup)

def handle_selective_restore(snapshot_file, target_dir, args, create_backup):
    """
    Handle selective restore operation.
    
    Args:
        snapshot_file: Path to the snapshot file
        target_dir: Directory to restore to
        args: The parsed arguments
        create_backup: Whether to create a backup
        
    Returns:
        int: Exit code
    """
    from pkgmngr.snapshot.restore import selective_restore
    
    try:
        backup_file = selective_restore(
            snapshot_file,
            target_dir,
            args.patterns,
            args.exclude_patterns,
            args.interactive,
            create_backup,
            None  # No custom backup path
        )
        return 0
    except Exception as e:
        display_error(f"Error during selective restoration: {e}")
        return 1

def handle_standard_restore(snapshot_file, target_dir, create_backup):
    """
    Handle standard restore operation.
    
    Args:
        snapshot_file: Path to the snapshot file
        target_dir: Directory to restore to
        create_backup: Whether to create a backup
        
    Returns:
        int: Exit code
    """
    from pkgmngr.snapshot.restore import restore_from_snapshot
    
    try:
        backup_file = restore_from_snapshot(
            snapshot_file, 
            target_dir,
            create_backup,
            None  # No custom backup path
        )
        return 0
    except Exception as e:
        display_error(f"Error during restoration: {e}")
        return 1

def main():
    """
    Main entry point for the package.
    Parse arguments and dispatch to the appropriate handlers.
    """
    # Create the argument parser
    parser = create_main_parser()
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle version command
    if args.version:
        return handle_version_command()
    
    # No command specified
    if not args.command:
        parser.print_help()
        return 1
    
    # Dispatch to the appropriate handler
    return dispatch_command(args)


if __name__ == "__main__":
    sys.exit(main())