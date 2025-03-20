"""
Package snapshot module for pkgmngr.

This module provides functionality for creating and restoring snapshots
of Python packages and directory structures.
"""

from .snapshot import create_snapshot, parse_snapshot_file
from .restore import restore_from_snapshot, create_backup_snapshot, selective_restore