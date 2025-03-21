"""
Utility functions for the snapshot module.
"""

import os
import re
import time
import glob
from typing import List, Dict, Optional


def get_file_language(file_path):
    """
    Determine the language for syntax highlighting based on file extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        A string representing the language for markdown code blocks
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    # Map common extensions to languages
    language_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'jsx',
        '.ts': 'typescript',
        '.tsx': 'tsx',
        '.html': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.xml': 'xml',
        '.json': 'json',
        '.md': 'markdown',
        '.sh': 'bash',
        '.bash': 'bash',
        '.zsh': 'bash',
        '.c': 'c',
        '.cpp': 'cpp',
        '.h': 'c',
        '.hpp': 'cpp',
        '.cs': 'csharp',
        '.java': 'java',
        '.go': 'go',
        '.rb': 'ruby',
        '.php': 'php',
        '.pl': 'perl',
        '.swift': 'swift',
        '.rs': 'rust',
        '.r': 'r',
        '.lua': 'lua',
        '.sql': 'sql',
        '.yml': 'yaml',
        '.yaml': 'yaml',
        '.toml': 'toml',
        '.ini': 'ini',
        '.cfg': 'ini',
        '.conf': 'ini',
        '.txt': 'text',
        '.gitignore': 'gitignore',
    }
    
    return language_map.get(ext, '')  # Empty string if no match found


def get_file_icon(filename):
    """
    Returns an appropriate emoji icon for a file based on its extension.
    
    Args:
        filename: Name of the file
        
    Returns:
        String emoji representing the file type
    """
    ext = os.path.splitext(filename)[1].lower()
    
    # Map common extensions to icons
    icon_map = {
        '.py': '🐍',     # Python
        '.js': '📜',     # JavaScript
        '.ts': '📜',     # TypeScript
        '.html': '🌐',   # HTML
        '.css': '🎨',    # CSS
        '.json': '📋',   # JSON
        '.md': '📝',     # Markdown
        '.txt': '📄',    # Text
        '.xml': '📋',    # XML
        '.csv': '📊',    # CSV
        '.xlsx': '📊',   # Excel
        '.pdf': '📑',    # PDF
        '.png': '🖼️',    # PNG image
        '.jpg': '🖼️',    # JPEG image
        '.jpeg': '🖼️',   # JPEG image
        '.gif': '🖼️',    # GIF image
        '.svg': '🖼️',    # SVG image
        '.mp3': '🎵',    # Audio
        '.mp4': '🎬',    # Video
        '.zip': '📦',    # ZIP archive
        '.tar': '📦',    # TAR archive
        '.gz': '📦',     # GZIP archive
        '.gitignore': '🔧', # Git
        '.sh': '⚙️',      # Shell
        '.bash': '⚙️',    # Bash
        '.sql': '💾',    # SQL
        '.cpp': '⚙️',    # C++
        '.c': '⚙️',      # C
        '.h': '⚙️',      # Header
        '.java': '☕',   # Java
        '.rb': '💎',     # Ruby
        '.php': '🐘',    # PHP
        '.go': '🔹',     # Go
        '.rs': '🦀',     # Rust
        '.dart': '🎯',   # Dart
        '.swift': '🔶',  # Swift
        '.kt': '🔷',     # Kotlin
        '.in': '📄',     # .in files
        '.toml': '📄',   # TOML files
    }
    
    return icon_map.get(ext, '📄')  # Default file icon


def create_filename_anchor(file_path):
    """
    Create a GitHub-compatible anchor for a file path.
    
    Args:
        file_path: The file path to create an anchor for
        
    Returns:
        A string suitable for use as an HTML anchor
    """
    # Convert to lowercase, replace / with -, and remove special characters
    anchor = file_path.lower().replace('/', '-').replace('\\', '-')
    # Remove unwanted characters
    anchor = re.sub(r'[^a-z0-9\-_]', '', anchor)
    return anchor


def list_available_snapshots(snapshot_dir: str = None) -> List[Dict[str, str]]:
    """
    List all available snapshots with their timestamps and comments.
    
    Args:
        snapshot_dir: Directory to search for snapshots (default: ./snapshots)
        
    Returns:
        List of dictionaries containing snapshot information
    """
    # Use default directory if none provided
    if not snapshot_dir:
        snapshot_dir = os.path.join(os.getcwd(), 'snapshots')
    
    # Ensure directory exists
    if not os.path.exists(snapshot_dir):
        print(f"Snapshot directory not found: {snapshot_dir}")
        return []
    
    # Find all snapshot files (markdown only)
    snapshot_files = glob.glob(os.path.join(snapshot_dir, "*.md"))
    if not snapshot_files:
        print(f"No snapshots found in {snapshot_dir}")
        return []
    
    snapshots = []
    
    # Extract information from each snapshot file
    for file_path in sorted(snapshot_files, key=os.path.getmtime, reverse=True):
        snapshot_info = {
            'path': file_path,
            'filename': os.path.basename(file_path),
            'modified': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(file_path))),
            'comment': extract_snapshot_comment(file_path),
            'is_backup': 'pre_restore_backup_' in os.path.basename(file_path)
        }
        snapshots.append(snapshot_info)
    
    return snapshots


def extract_snapshot_comment(snapshot_file_path: str) -> str:
    """
    Extract the comment from a snapshot file.
    
    Args:
        snapshot_file_path: Path to the snapshot file
        
    Returns:
        The comment string, or a default message if no comment is found
    """
    try:
        with open(snapshot_file_path, 'r', encoding='utf-8') as f:
            # Read first 2000 characters which should include the header and comment
            header = f.read(2000)
            
            # Look for the comment section in markdown
            comment_match = re.search(r"## Comments\n(.*?)(?=\n##|\Z)", header, re.DOTALL)
            if comment_match:
                return comment_match.group(1).strip()
    except Exception as e:
        pass
            
    return "(No comment)"


def display_snapshot_list(snapshots: List[Dict[str, str]]) -> None:
    """
    Display formatted list of snapshots with their details.
    
    Args:
        snapshots: List of snapshot information dictionaries
    """
    if not snapshots:
        print("No snapshots available.")
        return
    
    print("\nAvailable snapshots:")
    print("-" * 100)
    print(f"{'#':<3} {'Type':<8} {'Date':<19} {'Filename':<30} {'Comment'}")
    print("-" * 100)
    
    for i, snapshot in enumerate(snapshots, 1):
        # Truncate filename if it's too long
        filename = snapshot['filename']
        if len(filename) > 29:
            filename = filename[:26] + "..."
            
        # Truncate comment if it's too long
        comment = snapshot['comment']
        max_comment_len = 100 - 3 - 8 - 19 - 30 - 1  # Total width minus other columns
        if len(comment) > max_comment_len:
            comment = comment[:max_comment_len-3] + "..."
            
        snapshot_type = "BACKUP" if snapshot['is_backup'] else "SNAPSHOT"
        
        print(f"{i:<3} {snapshot_type:<8} {snapshot['modified']:<19} {filename:<30} {comment}")
    
    print("-" * 100)


def select_snapshot_interactive() -> Optional[str]:
    """
    Show list of available snapshots and let user select one.
    
    Returns:
        Path to the selected snapshot file, or None if cancelled
    """
    # Get snapshot list
    snapshots = list_available_snapshots()
    
    if not snapshots:
        return None
    
    # Display snapshots
    display_snapshot_list(snapshots)
    
    # Let user select
    while True:
        try:
            choice = input("\nEnter number to select a snapshot (or 'q' to quit): ").strip()
            
            if choice.lower() in ('q', 'quit', 'exit'):
                print("Selection cancelled.")
                return None
                
            idx = int(choice) - 1
            if 0 <= idx < len(snapshots):
                selected = snapshots[idx]['path']
                print(f"Selected: {selected}")
                return selected
            else:
                print(f"Please enter a number between 1 and {len(snapshots)}.")
        except ValueError:
            print("Please enter a valid number.")
        except (KeyboardInterrupt, EOFError):
            print("\nSelection cancelled.")
            return None


def get_snapshot_path(arg_value) -> Optional[str]:
    """
    Convert a snapshot argument (path or index) to a valid snapshot path.
    
    Args:
        arg_value: Either a path to a snapshot file or an index (as string)
        
    Returns:
        Path to the selected snapshot file, or None if not found
    """
    if arg_value is None:
        return None
        
    # Try to interpret as an index
    try:
        idx = int(arg_value) - 1
        snapshots = list_available_snapshots()
        if 0 <= idx < len(snapshots):
            return snapshots[idx]['path']
        else:
            print(f"Error: Snapshot index {arg_value} is out of range (1-{len(snapshots)}).")
            return None
    except ValueError:
        # Not an integer, interpret as a path
        if os.path.isfile(arg_value):
            return arg_value
        else:
            print(f"Error: Snapshot file '{arg_value}' not found.")
            return None