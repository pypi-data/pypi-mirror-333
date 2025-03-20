"""
Custom exceptions for the FileSync-Guardian library.
"""


class SyncError(Exception):
    """Base exception for all synchronization errors."""
    pass


class FileAccessError(SyncError):
    """Raised when there's an issue accessing a file or directory."""
    pass


class EncryptionError(SyncError):
    """Raised when there's an issue with encryption or decryption."""
    pass


class VersioningError(SyncError):
    """Raised when there's an issue with file versioning."""
    pass


class TransferError(SyncError):
    """Raised when there's an issue transferring files."""
    pass


class ConfigurationError(SyncError):
    """Raised when there's an issue with configuration."""
    pass


class StorageError(SyncError):
    """Raised when there's an issue with storage backends."""
    pass


class IntegrityError(SyncError):
    """Raised when file integrity verification fails."""
    pass


class ConflictError(SyncError):
    """Raised when there's a conflict between files that can't be automatically resolved."""
    pass


class SchedulerError(SyncError):
    """Raised when there's an issue with scheduling jobs."""
    pass