"""
Command-line interface for the snapshot module of pkgmngr.
"""
import os
import sys

from pkgmngr.common.errors import error_handler, SnapshotError
from pkgmngr.common.cli import display_success, display_error, display_info
from .snapshot import create_snapshot
from .restore import restore_from_snapshot, selective_restore
from .utils import list_available_snapshots, display_snapshot_list, get_snapshot_path, select_snapshot_interactive


@error_handler
def handle_snapshot_create(args):
    """
    Handle the snapshot create command.
    
    Args:
        args: The parsed arguments
        
    Returns:
        int: Exit code
    """
    # Set default values for attributes that might not exist in the flattened CLI
    start_path = getattr(args, 'start_path', '.')
    start_path = os.path.abspath(start_path)
    output_folder = getattr(args, 'output_folder', 'snapshots')
    
    # Handle comment
    comment = get_snapshot_comment(args)
    
    # Validate directory
    if not validate_snapshot_directory(start_path):
        return 1
    
    # Create the snapshot
    try:
        output_file = create_snapshot(start_path, output_folder, None, comment)
        display_success(f"Snapshot saved to: {output_file}")
        return 0
    except Exception as e:
        display_error(f"Error creating snapshot: {e}")
        return 1


def get_snapshot_comment(args):
    """
    Get a comment for the snapshot, prompting if necessary.
    
    Args:
        args: The parsed arguments
        
    Returns:
        str: Comment text or None
    """
    comment = getattr(args, 'message', None)
    no_comment_prompt = getattr(args, 'no_comment_prompt', False)
    
    if not comment and not no_comment_prompt:
        try:
            user_input = input("Would you like to add a comment for this snapshot? (y/n): ")
            if user_input.lower() in ('y', 'yes'):
                comment = input("Enter comment: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nComment prompt cancelled.")
            comment = None
    
    return comment


def validate_snapshot_directory(start_path):
    """
    Validate that the snapshot directory exists.
    
    Args:
        start_path: Directory to snapshot
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not os.path.isdir(start_path):
        display_error(f"{start_path} is not a valid directory.")
        return False
    
    print(f"Creating markdown snapshot from {start_path}...")
    return True


@error_handler
def handle_restore_from_snapshot(snapshot_file, target_dir='.',
                               mode='overwrite', create_backup=True, backup_path=None):
    """
    Handle restoration from a snapshot file.
    
    Args:
        snapshot_file: Path to the snapshot file
        target_dir: Directory to restore to
        mode: Restoration mode
        create_backup: Whether to create a backup
        backup_path: Custom path for the backup file
        
    Returns:
        int: Exit code
    """
    # Make target directory absolute
    target_dir = os.path.abspath(target_dir)
    
    try:
        backup_file = restore_from_snapshot(
            snapshot_file, 
            target_dir,
            mode,
            create_backup,
            backup_path
        )
        return 0
    except Exception as e:
        display_error(f"Error during restoration: {e}")
        return 1


@error_handler
def handle_selective_restore(snapshot_file, target_dir, patterns=None, exclude_patterns=None,
                          interactive=False, mode='overwrite', create_backup=True, backup_path=None):
    """
    Handle selective restoration from a snapshot file.
    
    Args:
        snapshot_file: Path to the snapshot file
        target_dir: Directory to restore to
        patterns: List of glob patterns to include
        exclude_patterns: List of glob patterns to exclude
        interactive: Whether to interactively select files
        mode: Restoration mode
        create_backup: Whether to create a backup
        backup_path: Custom path for the backup file
        
    Returns:
        int: Exit code
    """
    # Make target directory absolute
    target_dir = os.path.abspath(target_dir)
    
    try:
        backup_file = selective_restore(
            snapshot_file,
            target_dir,
            patterns,
            exclude_patterns,
            interactive,
            mode,
            create_backup,
            backup_path
        )
        return 0
    except Exception as e:
        display_error(f"Error during selective restoration: {e}")
        return 1


@error_handler
def list_snapshots():
    """
    List all available snapshots.
    
    Returns:
        int: Exit code
    """
    snapshots = list_available_snapshots()
    display_snapshot_list(snapshots)
    return 0


@error_handler
def select_and_restore_snapshot(args):
    """
    Select a snapshot and restore from it.
    
    Args:
        args: The parsed arguments
        
    Returns:
        int: Exit code
    """
    # Get the snapshot file
    snapshot_file = get_snapshot_file(args)
    if not snapshot_file:
        return 1
    
    # Get target directory
    target_dir = getattr(args, 'target_dir', '.')
    
    # Get backup options
    create_backup = not getattr(args, 'no_backup', False)
    backup_path = getattr(args, 'backup_path', None)
    
    # Check if this is a selective restore
    if hasattr(args, 'patterns') and (
        args.patterns or 
        getattr(args, 'exclude_patterns', None) or 
        getattr(args, 'interactive', False)
    ):
        return handle_selective_restore(
            snapshot_file,
            target_dir,
            getattr(args, 'patterns', None),
            getattr(args, 'exclude_patterns', None),
            getattr(args, 'interactive', False),
            getattr(args, 'mode', 'overwrite'),
            create_backup,
            backup_path
        )
    else:
        return handle_restore_from_snapshot(
            snapshot_file,
            target_dir,
            getattr(args, 'mode', 'overwrite'),
            create_backup,
            backup_path
        )


def get_snapshot_file(args):
    """
    Get the snapshot file from arguments or interactive selection.
    
    Args:
        args: The parsed arguments
        
    Returns:
        str: Path to the snapshot file or None if canceled
    """
    if hasattr(args, 'snapshot_file') and args.snapshot_file:
        # Convert to path if it's a number
        return get_snapshot_path(args.snapshot_file)
    elif hasattr(args, 'snapshot_id') and args.snapshot_id:
        # Convert to path if it's a number
        return get_snapshot_path(args.snapshot_id)
    else:
        # If no snapshot file is specified, prompt for selection
        return select_snapshot_interactive()