"""
Tests for enhanced backtick handling in snapshot functionality.
"""
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import os
import re
import tempfile
import shutil

from pkgmngr.snapshot.snapshot import (
    detect_max_backtick_sequence,
    format_text_file,
    collect_file_contents,
    extract_file_contents_from_snapshot,
    create_snapshot
)
from pkgmngr.common.utils import create_file


def test_detect_max_backtick_sequence():
    """Test detecting maximum consecutive backticks in content."""
    # No backticks
    assert detect_max_backtick_sequence("Text without any backticks") == 3  # Minimum is 3
    
    # Single backticks
    assert detect_max_backtick_sequence("Text with `single` backticks") == 3  # Minimum is 3
    
    # Triple backticks (common for code blocks)
    assert detect_max_backtick_sequence("```python\ncode block\n```") == 4  # 3+1
    
    # Multiple sequences
    assert detect_max_backtick_sequence("```code``` and then ``more`` backticks") == 4  # 3+1
    
    # Sequence at the end
    assert detect_max_backtick_sequence("Ending with ````") == 5  # 4+1
    
    # Longer sequence with 7 backticks
    seq = "Very long " + "`" * 7 + " sequence"
    assert detect_max_backtick_sequence(seq) == 8  # 7+1
    
    # Multiple sequences with different lengths
    content = "This has `single` and ```triple``` and `````five````` backticks"
    assert detect_max_backtick_sequence(content) == 6  # 5+1


def test_format_text_file():
    """Test formatting a text file with enhanced backtick handling."""
    # Simple content
    result = format_text_file(
        "example.py",
        "example_py",
        "python",
        "def hello():\n    print('Hello world')"
    )
    
    assert result[0] == '<a id="example_py"></a>'
    assert result[1] == '### example.py'
    assert result[2] == '```python'  # Default 3 backticks when no backticks in content
    assert result[3] == "def hello():\n    print('Hello world')"
    assert result[4] == '```'
    
    # Content with backticks
    result = format_text_file(
        "markdown.md",
        "markdown_md",
        "markdown",
        "# Title\n\n```python\ndef hello():\n    print('Hello world')\n```"
    )
    
    assert result[0] == '<a id="markdown_md"></a>'
    assert result[1] == '### markdown.md'
    assert result[2].startswith('````')  # Should use at least 4 backticks
    assert "# Title" in result[3]
    assert "```python" in result[3]
    assert result[4].startswith('````')  # Matching closing fence


def test_collect_file_contents(temp_dir):
    """Test collecting file contents with proper backtick handling."""
    # Create files with different backtick patterns
    normal_file = temp_dir / "normal.py"
    normal_file.write_text('def hello():\n    print("Hello world")')
    
    markdown_file = temp_dir / "readme.md"
    markdown_file.write_text('# Title\n\n```python\ndef example():\n    return True\n```')
    
    nested_file = temp_dir / "nested.md"
    nested_file.write_text('# Nested\n\n````\n```\nTriple backticks inside quadruple\n```\n````')
    
    # Collect file contents
    file_paths = ["normal.py", "readme.md", "nested.md"]
    contents = collect_file_contents(temp_dir, file_paths)
    
    # Convert to a single string for easier testing
    content_str = "\n".join(contents)
    
    # Check for correct fence sizes
    assert re.search(r'### normal.py\n```python', content_str)
    assert re.search(r'### readme.md\n````markdown', content_str)
    assert re.search(r'### nested.md\n`````markdown', content_str)


def test_extract_file_contents_from_snapshot():
    """Test extracting file contents from various fence formats."""
    snapshot_content = """# test-project - Package Snapshot - Generated on 2025-01-01

## Files

<a id="normal_py"></a>
### normal.py
```python
def hello():
    print("Hello world")
```

<a id="readme_md"></a>
### readme.md
````markdown
# Title

```python
def example():
    return True
```
````

<a id="nested_md"></a>
### nested.md
`````markdown
# Nested

````
```
Triple backticks inside quadruple
```
````
`````

<a id="binary_file"></a>
### binary.bin
_Binary file - contents not shown_
"""

    # Extract contents
    file_contents = extract_file_contents_from_snapshot(snapshot_content)
    
    # Check that all files were extracted correctly
    assert len(file_contents) == 4
    assert file_contents["normal.py"] == 'def hello():\n    print("Hello world")'
    assert '```python' in file_contents["readme.md"]
    assert '````' in file_contents["nested.md"]
    assert '```' in file_contents["nested.md"]
    assert file_contents["binary.bin"] == "[Binary file - contents not shown]"


def test_snapshot_with_nested_backticks(temp_dir, monkeypatch):
    """Test creating a snapshot with nested backticks."""
    # Create files with nested backticks
    os.makedirs(temp_dir / "src", exist_ok=True)
    
    # Create a file with markdown code blocks
    create_file(
        temp_dir / "README.md",
        "# Test Project\n\n"
        "Example code:\n\n"
        "```python\n"
        "def example():\n"
        "    print('This is a code block')\n"
        "```\n"
    )
    
    # Create a file with nested code blocks (for documentation)
    create_file(
        temp_dir / "src" / "nested.md",
        "# Nested Code Examples\n\n"
        "Here's how to create a code block:\n\n"
        "````markdown\n"
        "```python\n"
        "print('Hello world')\n"
        "```\n"
        "````\n"
    )
    
    # Mock time.strftime for consistent output
    monkeypatch.setattr('time.strftime', lambda *args, **kwargs: "2025-01-01_12-00-00")
    
    # Create the snapshot
    snapshot_file = create_snapshot(temp_dir, "snapshots", comment="Testing nested backticks")
    
    # Read the snapshot file
    with open(snapshot_file, 'r') as f:
        snapshot_content = f.read()
    
    # Check if the note about backtick handling is present
    assert "varying numbers of backticks" in snapshot_content
    
    # Check that proper fence sizes were used
    assert re.search(r'### README.md\n````markdown', snapshot_content)
    assert re.search(r'### src/nested.md\n`````markdown', snapshot_content)
    
    # Parse the snapshot and check the contents
    file_contents = extract_file_contents_from_snapshot(snapshot_content)
    assert "```python" in file_contents["README.md"]
    assert "````markdown" in file_contents["src/nested.md"]
    assert "```python" in file_contents["src/nested.md"]


def test_round_trip_preservation(temp_dir, monkeypatch):
    """Test round-trip preservation of nested backticks."""
    # Create a file with nested backticks
    nested_file = temp_dir / "nested.md"
    original_content = (
        "# Nested Backticks\n\n"
        "Example with triple backticks:\n"
        "```python\n"
        "def example():\n"
        "    return 'code'\n"
        "```\n\n"
        "Example with quadruple backticks:\n"
        "````\n"
        "This is inside quadruple backticks\n"
        "````\n"
    )
    nested_file.write_text(original_content)
    
    # Mock time.strftime for consistent output
    monkeypatch.setattr('time.strftime', lambda *args, **kwargs: "2025-01-01_12-00-00")
    
    # Create snapshot
    snapshot_file = create_snapshot(temp_dir, "snapshots")
    
    # Parse snapshot
    from pkgmngr.snapshot.snapshot import parse_snapshot_file
    file_contents, _, _ = parse_snapshot_file(snapshot_file)
    
    # Check content was preserved exactly
    assert file_contents["nested.md"] == original_content