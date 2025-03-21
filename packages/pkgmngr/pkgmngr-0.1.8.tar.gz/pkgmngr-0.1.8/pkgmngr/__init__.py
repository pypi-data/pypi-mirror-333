"""
pkgmngr - Comprehensive Python Package Utilities

A collection of tools for Python package creation, snapshotting, and lifecycle management.
Includes functionality for:
- Creating new Python packages with standard project structure
- Taking and restoring snapshots of package states
- Managing the package lifecycle (renaming, GitHub integration, PyPI publishing)
"""

__version__ = "0.1.8"

# Import common utilities for easier access
from pkgmngr.common.errors import PkgUtilsError, ConfigError, GitError, SnapshotError, RestoreError