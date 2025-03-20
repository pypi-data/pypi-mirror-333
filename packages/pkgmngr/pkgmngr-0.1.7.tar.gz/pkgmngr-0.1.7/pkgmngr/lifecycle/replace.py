"""
Safe package-wide text replacement.
"""
import os
import re
import fnmatch
from pathlib import Path
import difflib
from typing import List, Dict, Tuple, Set, Optional
import time

from pkgmngr.common.utils import is_binary_file
from pkgmngr.common.errors import PackageError, error_handler
from pkgmngr.common.cli import display_info, display_success, display_warning, confirm_action
from pkgmngr.snapshot.snapshot import create_snapshot

@error_handler
def handle_replace_command(args):
    """
    Handle the replace command from CLI arguments.
    
    Args:
        args: The parsed CLI arguments
        
    Returns:
        int: Exit code
    """
    # Get all parameters from args
    old_pattern = args.old_pattern
    new_pattern = args.new_pattern
    regex = args.regex
    case_sensitive = not args.case_insensitive
    create_backup = not args.no_backup
    preview = not args.no_preview
    
    # Get base directory (current directory)
    base_dir = os.getcwd()
    
    # Perform the replacement
    changes = safe_replace(
        base_dir=base_dir,
        old_pattern=old_pattern,
        new_pattern=new_pattern,
        file_patterns=args.patterns,
        exclude_patterns=args.exclude_patterns,
        regex=regex,
        create_backup=create_backup,
        preview=preview,
        case_sensitive=case_sensitive,
    )
    
    # If we got here, the operation was successful
    return 0

def safe_replace(
    base_dir: str,
    old_pattern: str,
    new_pattern: str,
    file_patterns: List[str] = None,
    exclude_patterns: List[str] = None,
    regex: bool = False,
    create_backup: bool = True,
    preview: bool = True,
    case_sensitive: bool = True,
) -> Dict[str, int]:
    """
    Safely replace text across multiple files in a package.
    
    Args:
        base_dir: Base directory to start from
        old_pattern: Pattern to search for
        new_pattern: Pattern to replace with
        file_patterns: List of glob patterns to include (e.g. ['*.py', 'docs/*.md'])
        exclude_patterns: List of glob patterns to exclude
        regex: If True, treat old_pattern as a regular expression
        create_backup: If True, create a snapshot before replacement
        preview: If True, show a preview of changes and confirm before applying
        case_sensitive: If True, perform case-sensitive matching
        
    Returns:
        Dict mapping file paths to number of replacements made
        
    Raises:
        PackageError: If replacement fails
    """
    try:
        base_dir = os.path.abspath(base_dir)
        
        # Create a backup snapshot if requested
        if create_backup:
            backup_path = create_backup_snapshot(base_dir)
            display_info(f"Created backup snapshot: {backup_path}")
        
        # Find all text files
        all_files = find_text_files(base_dir)
        
        # Filter by patterns
        filtered_files = filter_files(all_files, file_patterns, exclude_patterns)
        if not filtered_files:
            display_warning("No matching files found")
            return {}
        
        # Prepare the replacement function
        replace_func = create_replace_function(old_pattern, new_pattern, regex, case_sensitive)
        
        # Process files
        return process_files(filtered_files, replace_func, preview)
    
    except Exception as e:
        if isinstance(e, PackageError):
            raise e
        else:
            raise PackageError(f"Replacement failed: {str(e)}")


def find_text_files(base_dir: str) -> List[str]:
    """Find all text files in the directory."""
    text_files = []
    
    for root, _, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip .git directory
            if ".git" in file_path.split(os.sep):
                continue
                
            # Skip binary files
            if is_binary_file(file_path):
                continue
                
            text_files.append(file_path)
    
    return text_files


def filter_files(files: List[str], include_patterns: List[str], exclude_patterns: List[str]) -> List[str]:
    """Filter files based on include and exclude patterns."""
    if not include_patterns:
        filtered_files = files
    else:
        # Include files matching any include pattern
        filtered_files = []
        for file_path in files:
            rel_path = os.path.basename(file_path)
            if any(fnmatch.fnmatch(rel_path, pattern) for pattern in include_patterns):
                filtered_files.append(file_path)
    
    if exclude_patterns:
        # Remove files matching any exclude pattern
        filtered_files = [
            file_path for file_path in filtered_files
            if not any(fnmatch.fnmatch(os.path.basename(file_path), pattern) for pattern in exclude_patterns)
        ]
    
    return filtered_files


def create_replace_function(old_pattern, new_pattern, is_regex, case_sensitive):
    """Create appropriate replacement function based on parameters."""
    if is_regex:
        flags = 0 if case_sensitive else re.IGNORECASE
        pattern = re.compile(old_pattern, flags)
        
        def replace_func(text):
            new_text = pattern.sub(new_pattern, text)
            return new_text, text != new_text
    else:
        def replace_func(text):
            if case_sensitive:
                new_text = text.replace(old_pattern, new_pattern)
            else:
                new_text = re.sub(re.escape(old_pattern), new_pattern, text, flags=re.IGNORECASE)
            return new_text, text != new_text
    
    return replace_func


def process_files(files, replace_func, preview):
    """Process all files with the replacement function."""
    changes = {}
    to_apply = {}
    
    # First pass: identify changes
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content, has_changes = replace_func(content)
            if has_changes:
                # Count replacements
                replacements = count_replacements(content, new_content)
                changes[file_path] = replacements
                to_apply[file_path] = new_content
        except Exception as e:
            display_warning(f"Error processing {file_path}: {str(e)}")
    
    if not changes:
        display_info("No changes to apply")
        return {}
    
    # Preview and confirm
    if preview:
        show_preview(changes, files, to_apply)
        if not confirm_action("Apply these changes?", default=False):
            display_info("Operation cancelled")
            return {}
    
    # Apply changes
    for file_path, new_content in to_apply.items():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    display_success(f"Applied changes to {len(changes)} files")
    return changes


def count_replacements(old_text, new_text):
    """Count how many replacements were made."""
    if old_text == new_text:
        return 0
        
    # Count line differences as an approximation
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()
    
    diff = difflib.ndiff(old_lines, new_lines)
    return sum(1 for line in diff if line.startswith('- ') or line.startswith('+ '))


def show_preview(changes, all_files, new_contents):
    """Show preview of changes to be made."""
    display_info(f"Changes to be applied in {len(changes)} of {len(all_files)} files:")
    
    for file_path, count in sorted(changes.items(), key=lambda x: x[1], reverse=True):
        rel_path = os.path.relpath(file_path)
        display_info(f"  {rel_path}: {count} replacements")
    
    # Show detailed diff for the top 3 files with most changes
    top_files = sorted(changes.items(), key=lambda x: x[1], reverse=True)[:3]
    
    for file_path, count in top_files:
        show_file_diff(file_path, new_contents[file_path])


def show_file_diff(file_path, new_content):
    """Show diff for a specific file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        old_content = f.read()
    
    old_lines = old_content.splitlines(True)
    new_lines = new_content.splitlines(True)
    
    diff = difflib.unified_diff(
        old_lines, new_lines,
        fromfile=f"a/{os.path.basename(file_path)}",
        tofile=f"b/{os.path.basename(file_path)}",
        n=3
    )
    
    display_info(f"\nChanges in {os.path.relpath(file_path)}:")
    print(''.join(diff))


def create_backup_snapshot(base_dir):
    """Create a backup snapshot before replacement."""
    from pkgmngr.snapshot.snapshot import create_snapshot
    
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    return create_snapshot(
        base_dir, 
        "snapshots", 
        None,
        f"Automatic backup before text replacement operation"
    )