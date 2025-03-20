"""
Core functionality for creating snapshots of directory structures.
"""
import os
import re
from pathlib import Path
import time
import pathspec

from pkgmngr.common.utils import is_binary_file
from pkgmngr.common.errors import SnapshotError, try_operation, assert_condition
from .utils import get_file_language, get_file_icon, create_filename_anchor


def create_snapshot(start_path: str, output_folder: str, config=None, comment=None):
    """
    Create a snapshot of all package files into a single markdown document.
    
    Args:
        start_path: The root directory to snapshot
        output_folder: Directory to store the output file
        config: Configuration options (not used in this version)
        comment: Optional comment to include in the snapshot
        
    Returns:
        Path to the created snapshot file
        
    Raises:
        SnapshotError: If snapshot creation fails
    """
    try:
        # Load gitignore patterns
        gitignore_spec, gitignore_path = load_gitignore_patterns(start_path)
        
        # Ensure output folder exists
        output_dir = create_output_directory(start_path, output_folder)

        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(output_dir, f"snapshot_{timestamp}.md")
        
        # Generate snapshot content
        content = generate_snapshot_content(start_path, gitignore_spec, output_folder, timestamp, comment)
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        return output_file
        
    except Exception as e:
        if isinstance(e, SnapshotError):
            raise e
        else:
            raise SnapshotError(f"Failed to create snapshot: {str(e)}")


def create_output_directory(start_path, output_folder):
    """
    Create the output directory for snapshots.
    
    Args:
        start_path: The root directory
        output_folder: Relative path for the output folder
        
    Returns:
        Path to the output directory
        
    Raises:
        SnapshotError: If directory creation fails
    """
    try:
        output_dir = os.path.join(start_path, output_folder)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        return output_dir
    except Exception as e:
        raise SnapshotError(f"Failed to create output directory: {str(e)}")


def generate_snapshot_content(start_path, gitignore_spec, output_folder, timestamp, comment=None):
    """
    Generate the full content for a snapshot.
    
    Args:
        start_path: The root directory to snapshot
        gitignore_spec: The gitignore patterns to apply
        output_folder: Output folder to exclude
        timestamp: Timestamp for the snapshot
        comment: Optional comment to include
        
    Returns:
        List of content lines for the snapshot
    """
    # Get package name from either config or directory name
    package_name = get_package_name_for_snapshot(start_path)
    
    # Start with header
    content = [
        f"# {package_name} - Package Snapshot - Generated on {timestamp}",
        "",
        "**Note:** This snapshot uses code blocks with varying numbers of backticks to properly handle nested code blocks.",
        "The number of backticks in each file's code fence is intentionally set to be more than any sequence of backticks within the file content.",
        "",
        "",
    ]
    
    # Add comments section if provided
    if comment:
        content.extend([
            "## Comments",
            comment,
            "",
        ])
    
    # Continue with directory structure
    content.extend([
        "## Directory Structure",
        get_file_tree(start_path, gitignore_spec, output_folder),
        "",
    ])
    
    # Collect file paths for table of contents
    file_paths = collect_file_paths(start_path, gitignore_spec, output_folder)
    
    # Add table of contents
    content.extend([
        "## Table of Contents",
        create_table_of_contents(file_paths),
        "",
        "## Files",
        "",
    ])
    
    # Add file contents with enhanced backtick handling
    file_contents = collect_file_contents(start_path, file_paths)
    content.extend(file_contents)
    
    return content


def get_package_name_for_snapshot(start_path):
    """
    Get the package name for the snapshot header.
    
    Args:
        start_path: The root directory to snapshot
        
    Returns:
        str: Package name or directory name if package name can't be determined
    """
    # First try to load from config
    try:
        from pkgmngr.common.config import load_config
        config, _ = load_config(start_path)
        if "package_name" in config:
            return config["package_name"]
    except Exception:
        # If config loading fails, use directory name
        pass
        
    # Use directory name as fallback
    import os
    return os.path.basename(os.path.abspath(start_path))


def load_gitignore_patterns(start_path):
    """
    Load patterns from .gitignore file or create default if none exists.
    
    Args:
        start_path: Directory to look for .gitignore file
        
    Returns:
        A tuple of (pathspec.PathSpec object, gitignore_path)
        
    Raises:
        SnapshotError: If loading patterns fails
    """
    gitignore_path = os.path.join(start_path, '.gitignore')
    
    # Create default .gitignore if it doesn't exist
    if not os.path.isfile(gitignore_path):
        print(f"No .gitignore file found at {gitignore_path}")
        print(f"Creating default .gitignore file...")
        create_default_gitignore(gitignore_path)
    
    try:
        with open(gitignore_path, 'r') as f:
            lines = f.readlines()
            # Process snapshot-specific patterns
            processed_lines = []
            for line in lines:
                if line.startswith("#pkgmngr"):
                    # Remove the #pkgmngr prefix to use it as a pattern
                    processed_lines.append(line[len('#pkgmngr'):].strip())
                else:
                    processed_lines.append(line)
                    
            # Create a PathSpec object from the gitignore patterns
            spec = pathspec.PathSpec.from_lines('gitwildmatch', processed_lines)
            print(f"Using patterns from .gitignore at {gitignore_path}")
            return spec, gitignore_path
    except Exception as e:
        print(f"Warning: Error loading .gitignore file {gitignore_path}: {e}")
        print("Creating and using a default .gitignore file...")
        create_default_gitignore(gitignore_path)
        
        try:
            with open(gitignore_path, 'r') as f:
                lines = f.readlines()
                processed_lines = [line[len('#pkgmngr'):].strip() if line.startswith("#pkgmngr") else line for line in lines]
                spec = pathspec.PathSpec.from_lines('gitwildmatch', processed_lines)
                return spec, gitignore_path
        except Exception as e2:
            raise SnapshotError(f"Failed to load gitignore patterns: {str(e2)}")


def create_default_gitignore(gitignore_path):
    """
    Create a default .gitignore file with common patterns.
    Includes examples of snapshot_pkg specific exclusions.
    
    Args:
        gitignore_path: Path to create the .gitignore file
        
    Raises:
        SnapshotError: If file creation fails
    """
    from pkgmngr.common.templates import render_template
    
    try:
        with open(gitignore_path, 'w') as f:
            f.write(render_template('gitignore'))
        
        print(f"Created default .gitignore file at: {gitignore_path}")
    except Exception as e:
        raise SnapshotError(f"Failed to create default .gitignore file: {str(e)}")


def should_ignore(path: str, gitignore_spec, root_path: str, output_folder: str = None) -> bool:
    """
    Check if path should be ignored based on gitignore patterns.
    
    Args:
        path: Absolute path to check
        gitignore_spec: A pathspec.PathSpec object with gitignore patterns
        root_path: The root path of the project
        output_folder: Output folder path to exclude
        
    Returns:
        True if the path should be ignored, False otherwise
    """
    # Always ignore the output folder
    if output_folder:
        output_path = os.path.normpath(os.path.abspath(os.path.join(root_path, output_folder)))
        path_abs = os.path.normpath(os.path.abspath(path))
        # Check if path is output_path or is inside output_path
        if path_abs == output_path or path_abs.startswith(output_path + os.sep):
            return True
    
    # Handle .gitignore file specially - we want to include it in snapshots
    if os.path.basename(path) == '.gitignore':
        return True
    
    # Get path relative to the project root
    rel_path = os.path.relpath(path, root_path)
    
    # Use pathspec to check if the path matches any gitignore pattern
    return gitignore_spec.match_file(rel_path)


def get_file_tree(start_path: str, gitignore_spec, output_folder: str) -> str:
    """
    Generate a markdown tree representation of the directory structure.
    
    Args:
        start_path: The root directory to start from
        gitignore_spec: The gitignore patterns to apply
        output_folder: The output folder to always exclude
        
    Returns:
        A string representing the directory tree in markdown format
        
    Raises:
        SnapshotError: If tree generation fails
    """
    try:
        start_path = os.path.abspath(start_path)
        
        # Find directories that contain non-ignored content
        visible_directories = find_directories_with_visible_content(start_path, gitignore_spec, output_folder)
        
        # Build the tree using only directories with visible content
        tree_lines = build_tree_representation_markdown(start_path, visible_directories, gitignore_spec, output_folder)
        
        # Return a code block with the tree content for better formatting
        return "```\n" + "\n".join(tree_lines) + "\n```"
    except Exception as e:
        raise SnapshotError(f"Failed to generate directory tree: {str(e)}")


def find_directories_with_visible_content(start_path, gitignore_spec, output_folder):
    """
    Scans the directory structure to identify directories that should be visible in the tree.
    A directory is visible if it contains non-ignored files or has subdirectories with visible content.
    
    Args:
        start_path: The root directory to start from
        gitignore_spec: The gitignore patterns to apply
        output_folder: The output folder to exclude
        
    Returns:
        A set of directories that contain visible content
    """
    directories_with_content = set()
    
    # Traverse bottom-up to properly propagate visibility up the tree
    for root, dirs, files in os.walk(start_path, topdown=False):
        root_path = os.path.abspath(root)
        
        # Check if this directory is explicitly ignored
        if root != start_path and should_ignore(root, gitignore_spec, start_path, output_folder):
            continue
            
        # Check if this directory has any visible files
        has_visible_files = any(
            not should_ignore(os.path.join(root, file), gitignore_spec, start_path, output_folder)
            for file in files
        )
                
        # Check if any subdirectories have visible content
        has_visible_subdirs = any(
            os.path.join(root, dir_name) in directories_with_content
            for dir_name in dirs
        )
                
        # If this directory has visible content or is the root, mark it as visible
        if has_visible_files or has_visible_subdirs or root == start_path:
            directories_with_content.add(root_path)
    
    return directories_with_content


# Structure to hold our tree hierarchy
class TreeNode:
    def __init__(self, name, is_dir=False):
        self.name = name
        self.is_dir = is_dir
        self.children = []

def build_tree_representation_markdown(start_path, visible_directories, gitignore_spec, output_folder):
    """
    Builds a markdown tree representation, showing only directories with visible content.
    Uses prettier formatting with unicode box-drawing characters inside a code block.
    
    Args:
        start_path: The root directory to start from
        visible_directories: Set of directories that contain visible content
        gitignore_spec: The gitignore patterns to apply
        output_folder: The output folder to always exclude
        
    Returns:
        A list of strings representing the directory tree in markdown format
    """
    # Get project root name
    root_name = os.path.basename(start_path)
    
    # Create the root node
    root = TreeNode(root_name, True)
    
    # Build the tree structure
    build_tree_structure(root, start_path, visible_directories, gitignore_spec, output_folder)
    
    # Render the tree
    lines = []
    render_tree(root, lines)
    
    return lines


def build_tree_structure(root_node, start_path, visible_directories, gitignore_spec, output_folder):
    """
    Build the tree structure by walking the directory.
    
    Args:
        root_node: The root TreeNode to populate
        start_path: The root directory path
        visible_directories: Set of directories that contain visible content
        gitignore_spec: The gitignore patterns to apply
        output_folder: The output folder to exclude
    """
    for current_dir, dirs, files in os.walk(start_path):
        # Skip directories without visible content
        dirs[:] = [d for d in dirs if os.path.join(current_dir, d) in visible_directories]
        
        # Skip explicitly ignored directories
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(current_dir, d), gitignore_spec, start_path, output_folder)]
        
        # Get the path relative to start_path
        rel_path = os.path.relpath(current_dir, start_path)
        
        # Find the parent node for the current path
        if rel_path == '.':
            parent_node = root_node
        else:
            # Navigate to the correct parent node
            parent_node = find_parent_node(root_node, rel_path)
        
        # Add directory nodes
        for d in sorted(dirs):
            dir_path = os.path.join(current_dir, d)
            if not should_ignore(dir_path, gitignore_spec, start_path, output_folder):
                dir_node = TreeNode(d, True)
                parent_node.children.append(dir_node)
        
        # Add file nodes
        for f in sorted(files):
            file_path = os.path.join(current_dir, f)
            if not should_ignore(file_path, gitignore_spec, start_path, output_folder):
                file_node = TreeNode(f, False)
                parent_node.children.append(file_node)


def find_parent_node(root_node, rel_path):
    """
    Find the parent node for a given relative path.
    
    Args:
        root_node: The root TreeNode
        rel_path: Relative path to find parent for
        
    Returns:
        The parent TreeNode
    """
    # Build the path to this node
    path_parts = rel_path.split(os.sep)
    
    # Navigate to the correct parent node
    current_node = root_node
    for part in path_parts:
        found = False
        for child in current_node.children:
            if child.name == part and child.is_dir:
                current_node = child
                found = True
                break
        if not found:
            # This shouldn't happen if the walker is operating correctly
            new_node = TreeNode(part, True)
            current_node.children.append(new_node)
            current_node = new_node
    
    return current_node


def render_tree(node, lines, prefix="", is_last=True, is_root=True):
    """
    Render a tree node and its children.
    
    Args:
        node: The TreeNode to render
        lines: List to append lines to
        prefix: Current line prefix
        is_last: Whether this is the last child of its parent
        is_root: Whether this is the root node
    """
    # Add the current node
    if is_root:
        lines.append(f"📦 {node.name}")
    else:
        connector = "└─" if is_last else "├─"
        icon = "📂" if node.is_dir else get_file_icon(node.name)
        lines.append(f"{prefix}{connector} {icon} {node.name}")
    
    # Prepare the prefix for children
    child_prefix = "" if is_root else prefix + ("   " if is_last else "│  ")
    
    # Render children
    for i, child in enumerate(node.children):
        is_last_child = i == len(node.children) - 1
        render_tree(child, lines, child_prefix, is_last_child, False)


def create_table_of_contents(file_paths):
    """
    Create a markdown table of contents with links to file sections.
    
    Args:
        file_paths: List of file paths to include in the TOC
        
    Returns:
        A string containing the markdown TOC
    """
    toc_lines = []
    
    for i, file_path in enumerate(sorted(file_paths), 1):
        anchor = create_filename_anchor(file_path)
        toc_lines.append(f"{i}. [{file_path}](#{anchor})")
    
    return '\n'.join(toc_lines)


def collect_file_paths(start_path, gitignore_spec, output_folder):
    """
    Collect file paths for inclusion in the snapshot.
    
    Args:
        start_path: The root directory to snapshot
        gitignore_spec: The gitignore patterns to apply
        output_folder: The output folder to exclude
        
    Returns:
        List of relative file paths
    """
    file_paths = []
    for root, dirs, files in os.walk(start_path):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), gitignore_spec, start_path, output_folder)]
        
        for file in sorted(files):
            file_path = os.path.join(root, file)
            if not should_ignore(file_path, gitignore_spec, start_path, output_folder):
                rel_path = os.path.relpath(file_path, start_path)
                file_paths.append(rel_path)
    
    return file_paths


def detect_max_backtick_sequence(content: str) -> int:
    """
    Detect the maximum number of consecutive backticks in the content.
    
    Args:
        content: The content to analyze
        
    Returns:
        The maximum number of consecutive backticks found plus one
    """
    # Use regex to find all sequences of backticks
    import re
    backtick_sequences = re.findall(r'`+', content)
    
    if not backtick_sequences:
        return 3  # Default minimum for code blocks
    
    # Find the length of the longest sequence
    max_backticks = max(len(seq) for seq in backtick_sequences)
    
    # Return the max count plus one to ensure we have one more than any inner sequence
    # Minimum of 3 backticks for code blocks
    return max(3, max_backticks + 1)


def format_text_file(rel_path, anchor, language, file_content):
    """
    Format a text file entry for the snapshot with enhanced backtick handling.
    
    Args:
        rel_path: Relative path of the file
        anchor: HTML anchor for the file
        language: Language identifier for syntax highlighting
        file_content: Content of the file
        
    Returns:
        List of formatted content lines
    """
    # Detect the maximum number of consecutive backticks in the content
    # and use one more for our code block
    backtick_count = detect_max_backtick_sequence(file_content)
    code_fence = '`' * backtick_count
    
    return [
        f"<a id=\"{anchor}\"></a>",
        f"### {rel_path}",
        f"{code_fence}{language}",
        file_content,
        code_fence,
        "",  # Empty line after file content
    ]


def format_binary_file(rel_path, anchor):
    """
    Format a binary file entry for the snapshot.
    
    Args:
        rel_path: Relative path of the file
        anchor: HTML anchor for the file
        
    Returns:
        List of formatted content lines
    """
    return [
        f"<a id=\"{anchor}\"></a>",
        f"### {rel_path}",
        "_Binary file - contents not shown_",
        "",
    ]


def collect_file_contents(start_path, file_paths):
    """
    Collect file contents for all paths with enhanced backtick handling.
    
    Args:
        start_path: The root directory to snapshot
        file_paths: List of file paths to include
        
    Returns:
        List of content lines for all files
    """
    content = []
    
    for rel_path in file_paths:
        file_path = os.path.join(start_path, rel_path)
        anchor = create_filename_anchor(rel_path)
        # Determine language for syntax highlighting
        language = get_file_language(file_path)

        if is_binary_file(file_path):
            content.extend(format_binary_file(rel_path, anchor))
        else:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    content.extend(format_text_file(rel_path, anchor, language, file_content))
            except UnicodeDecodeError:
                content.extend(format_binary_file(rel_path, anchor))
    
    return content


def parse_snapshot_file(snapshot_file_path: str):
    """
    Parse a markdown snapshot file to extract the file structure and content.
    
    Args:
        snapshot_file_path: Path to the markdown snapshot file to parse
        
    Returns:
        Tuple of (file_contents, comment, project_name) where:
        - file_contents: Dictionary mapping file paths to their contents
        - comment: Optional comment from the snapshot
        - project_name: Optional project name from the snapshot header
        
    Raises:
        SnapshotError: If parsing fails
    """
    try:
        print(f"Parsing snapshot file: {snapshot_file_path}")
        
        with open(snapshot_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract file contents and metadata
        file_contents = extract_file_contents_from_snapshot(content)
        comment = extract_comment_from_snapshot(content)
        project_name = extract_project_name_from_snapshot(content)
        
        return file_contents, comment, project_name
    except Exception as e:
        raise SnapshotError(f"Failed to parse snapshot file: {str(e)}")


def extract_comment_from_snapshot(content):
    """
    Extract the comment section from snapshot content.
    
    Args:
        content: The full snapshot content
        
    Returns:
        The extracted comment or None if not found
    """
    comment_match = re.search(r"## Comments\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
    if comment_match:
        return comment_match.group(1).strip()
    return None


def extract_project_name_from_snapshot(content):
    """
    Extract the project name from snapshot header.
    
    Args:
        content: The full snapshot content
        
    Returns:
        The project name or None if not found
    """
    # Match both the old and new format
    header_match = re.search(r"^# (.*?)( - )?Package Snapshot - Generated on", content)
    if header_match and header_match.group(1):
        return header_match.group(1)
    return None


def extract_file_contents_from_snapshot(content):
    """
    Extract file contents from snapshot content with enhanced backtick handling.
    
    Args:
        content: The full snapshot content
        
    Returns:
        Dictionary mapping file paths to their contents
    """
    file_contents = {}
    
    # Pattern to match binary files
    binary_pattern = r'<a id="[^"]+"></a>\n### ([^\n]+)\n_Binary file - contents not shown_'
    for match in re.finditer(binary_pattern, content):
        file_path = match.group(1).strip()
        file_contents[file_path] = "[Binary file - contents not shown]"
    
    # Enhanced pattern to match regular files with code blocks using variable-length code fences
    # The pattern captures:
    # 1. The filename
    # 2. The opening code fence with optional language identifier
    # 3. The language identifier
    # 4. The content inside the code block
    file_pattern = r'<a id="[^"]+"></a>\n### ([^\n]+)\n(`{3,})([^\n]*)\n(.*?)\n\2'
    
    for match in re.finditer(file_pattern, content, re.DOTALL):
        file_path = match.group(1).strip()
        file_content = match.group(4)  # The content inside the code block
        file_contents[file_path] = file_content
    
    return file_contents