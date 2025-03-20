"""
FileSync-Guardian: A robust file synchronization and backup library for Python.

This library provides powerful tools for file synchronization, versioning,
encryption, and automation with a simple and intuitive API.
"""

from filesync_guardian.sync_manager import SyncManager
from filesync_guardian.filters.pattern import Pattern
from filesync_guardian.utils.progress import ProgressReporter
from filesync_guardian.exceptions import (
    SyncError,
    FileAccessError,
    EncryptionError,
    VersioningError
)

__version__ = "0.1.0"
__all__ = [
    "SyncManager",
    "Pattern",
    "ProgressReporter",
    "SyncError",
    "FileAccessError",
    "EncryptionError",
    "VersioningError",
]