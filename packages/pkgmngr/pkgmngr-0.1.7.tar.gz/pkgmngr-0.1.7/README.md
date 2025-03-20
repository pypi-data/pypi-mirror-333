# 📦 pkgmngr

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)

A powerful CLI utility that streamlines the entire Python package lifecycle - from creation to publication. Built for modern Python development workflows, pkgmngr helps you create, document, manage, and share Python packages efficiently.

## Why pkgmngr?

Python package management involves repetitive and often tedious steps: setting up project structure, maintaining documentation, syncing with GitHub, handling version changes, publishing to PyPI, and more.

pkgmngr addresses these challenges with a streamlined workflow:

- **Save Time**: Automate repetitive setup and maintenance tasks
- **Standardize Structure**: Ensure consistent package layout across projects
- **Document Easily**: Create comprehensive markdown snapshots for documentation and context sharing
- **Collaborate Better**: Perfect for sharing code context with AI assistants and collaborators
- **Manage Lifecycle**: Seamlessly handle package renaming, version updates, and publication

## 🛠️ Installation

```bash
# Install from PyPI
pip install pkgmngr

# Or install from source
git clone https://github.com/B4PT0R/pkgmngr.git
cd pkgmngr
pip install -e .
```

## 🚀 Quick Start

```bash
# Install from PyPI
pip install pkgmngr

# Create a new package
pkgmngr new my-package
cd my-package

# Generate the package files
pkgmngr create

# Initialize Git and GitHub repositories (requires GITHUB_TOKEN)
pkgmngr init-repo

# Make some changes to your code...

# Take a snapshot of your project
pkgmngr snapshot -m "Initial implementation"

# Push changes to GitHub
pkgmngr push

# Publish to PyPI when ready
pkgmngr publish
```

## ✨ Features

### 📝 Package Creation

With a single command, pkgmngr creates a standardized Python package structure:

```bash
# Create a new package directory with config file
pkgmngr new my-package

# Edit the generated config file (optional)
cd my-package
nano pkgmngr.toml

# Generate the package structure
pkgmngr create
```

This creates a complete package structure with:
- Python module files with proper imports
- tests directory with pytest setup
- setup.py and pyproject.toml with appropriate metadata
- README.md, LICENSE, and other standard files
- .gitignore with sensible defaults

### 📸 Package Snapshots

Create comprehensive code documentation snapshots with a single command:

```bash
# Create a snapshot with an optional comment
pkgmngr snapshot -m "Implemented core features"

# List all available snapshots
pkgmngr snapshot -l
```

Snapshots include:
- Visual directory structure with file type icons
- Navigable table of contents
- All file contents with proper syntax highlighting
- Metadata and comments

These snapshots are perfect for:
- Sharing code context with AI assistants
- Documenting code for team members
- Creating restoration points
- Providing self-contained project documentation

### 🔄 Package Lifecycle Management

#### Rename Packages

Easily rename your package and automatically update all references:

```bash
# Rename a package (updates all references and directory structure)
pkgmngr rename new-package-name
```

This updates the package directory name, all references in your code, and even renames the GitHub repository if available.

#### Global Search & Replace

Safely perform search and replace operations across your entire codebase:

```bash
# Replace text across all files
pkgmngr replace "old_text" "new_text"

# Use regular expressions
pkgmngr replace --regex "function\s+old_name" "function new_name"
```

Includes preview mode, automatic backups, and selective file targeting for safety.

#### GitHub Integration

Seamlessly integrate with GitHub:

```bash
# Initialize Git and create GitHub repository
pkgmngr init-repo

# Push changes with an interactive commit message
pkgmngr push
```

#### PyPI Publishing

Publish your package with automatic version increments:

```bash
# Publish to TestPyPI for testing
pkgmngr publish --test

# Publish to PyPI with automatic version increment
pkgmngr publish

# Publish with specific version increment
pkgmngr publish --bump minor
```

## 📋 Detailed Usage Guide

### Creating a New Package

```bash
# Create a new package
pkgmngr new my-package
cd my-package
```

This creates a directory with a `pkgmngr.toml` configuration file that lets you customize:
- Package metadata (name, version, author, etc.)
- GitHub integration settings
- Python version requirements
- Dependencies and development dependencies

After editing the config (if desired), generate the package structure:

```bash
pkgmngr create
```

This creates a complete package structure:
```
./
├── my_package/
│   ├── __init__.py
│   └── __main__.py
├── tests/
│   ├── test_my_package.py
│   └── run_tests.py
├── setup.py
├── README.md
├── MANIFEST.in
├── pyproject.toml
├── LICENSE
└── .gitignore
```

### Taking and Restoring Snapshots

#### Creating Snapshots

```bash
# Create a snapshot with a comment
pkgmngr snapshot -m "Implemented core features"
```

Snapshots are saved as markdown files in a `snapshots` directory, containing:
- Pretty-printed directory tree
- Table of contents with links to each file
- Full file contents with syntax highlighting
- Metadata about the snapshot

#### Restoring from Snapshots

```bash
# Restore from a specific snapshot (by number)
pkgmngr restore 1

# Interactively select files to restore
pkgmngr restore -i

# Restore only Python files
pkgmngr restore -p "*.py"

# Exclude certain files
pkgmngr restore -e "temp_*.py"
```

Restoration modes:
- `safe`: Skips existing files
- `overwrite`: Replaces existing files (default)
- `force`: Replaces all files, including read-only

### GitHub Integration

To use GitHub integration, set up a GitHub Personal Access Token:

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate a new token with the `repo` scope
3. Set it as an environment variable:
   ```bash
   export GITHUB_TOKEN=your_token_here
   ```

Initialize Git and create a GitHub repository:

```bash
pkgmngr init-repo
```

Push changes to GitHub:

```bash
pkgmngr push
```

### PyPI Publishing

Before publishing, ensure you have configured your PyPI credentials using one of these methods:
- A `.pypirc` file in your home directory
- Environment variables: `TWINE_USERNAME` and `TWINE_PASSWORD`
- API tokens (recommended for security)

Publishing commands:

```bash
# Publish to TestPyPI
pkgmngr publish --test

# Publish to PyPI with automatic patch version increment
pkgmngr publish

# Publish with a specific version increment type
pkgmngr publish --bump minor
```

### Package-wide Text Replacement

The `replace` command provides a safe way to perform global find/replace operations:

```bash
# Basic replacement
pkgmngr replace "old_text" "new_text"

# Advanced options
pkgmngr replace "old_api" "new_api" --pattern "*.py" --regex --case-insensitive
```

Safety features:
- Automatic backup snapshot before changes
- Preview of changes with file diffs
- Confirmation prompt before applying changes
- Filtering by file patterns and exclusions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

This project is almost entirely coded by Claude 3.7 following my general outlines. As it began to be functional, pkgmngr was itself used to facilitate the process: take a snapshot, give it to Claude, suggest changes, Claude does the changes and updates tests, copy/paste to the actual codebase, run tests, push to github, publish once in a while, repeat...