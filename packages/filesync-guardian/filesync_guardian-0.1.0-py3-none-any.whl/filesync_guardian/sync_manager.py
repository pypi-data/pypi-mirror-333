"""
Main SyncManager class for coordinating file synchronization operations.
"""

import os
import time
import logging
from typing import Callable, Dict, List, Optional, Tuple, Union

from filesync_guardian.file_system.scanner import FileScanner
from filesync_guardian.file_system.transfer import FileTransfer
from filesync_guardian.file_system.watcher import FileWatcher
from filesync_guardian.versioning.version_store import VersionStore
from filesync_guardian.encryption.crypto import Crypto
from filesync_guardian.filters.pattern import Pattern
from filesync_guardian.utils.progress import ProgressReporter
from filesync_guardian.utils.logger import setup_logger
from filesync_guardian.exceptions import ConfigurationError, SyncError
from filesync_guardian.storage.local import LocalStorage


class SyncManager:
    """
    Main class for managing file synchronization operations.

    This class coordinates file scanning, comparison, transfer, versioning,
    encryption, and progress reporting.
    """

    def __init__(
            self,
            source_path: str,
            target_path: str,
            *,
            encryption: bool = False,
            encryption_key: Optional[str] = None,
            versioning: bool = False,
            max_versions: int = 5,
            filters: Optional[List[str]] = None,
            bidirectional: bool = False,
            verify_integrity: bool = True,
            log_level: int = logging.INFO
    ):
        """
        Initialize a SyncManager instance.

        Args:
            source_path: The source directory path
            target_path: The target directory path
            encryption: Whether to enable encryption for transferred files
            encryption_key: Custom encryption key (generated if None)
            versioning: Whether to keep previous versions of files
            max_versions: Maximum number of versions to keep per file
            filters: List of include/exclude patterns
            bidirectional: Whether synchronization should be two-way
            verify_integrity: Whether to verify file integrity after transfer
            log_level: Logging level

        Raises:
            ConfigurationError: If the configuration is invalid
        """
        # Set up logging
        self.logger = setup_logger("filesync_guardian", log_level)
        self.logger.info(f"Initializing SyncManager: {source_path} -> {target_path}")

        # Validate and store paths
        self._validate_paths(source_path, target_path)
        self.source_path = os.path.abspath(source_path) if '://' not in source_path else source_path
        self.target_path = os.path.abspath(target_path) if '://' not in target_path else target_path

        # Initialize components
        self._init_storage()

        # Initialize scanner and transfer
        self.scanner = FileScanner(
            self.source_storage,
            self.target_storage,
            verify_integrity=verify_integrity
        )
        self.transfer = FileTransfer(
            self.source_storage,
            self.target_storage,
            verify_integrity=verify_integrity
        )

        # Configure optional components
        self._setup_filters(filters)
        self._setup_encryption(encryption, encryption_key)
        self._setup_versioning(versioning, max_versions)

        # Additional settings
        self.bidirectional = bidirectional
        self.verify_integrity = verify_integrity

        # State tracking
        self.is_running = False
        self.progress_reporter = ProgressReporter()
        self.last_sync_time = None
        self.last_error = None

        self.logger.info("SyncManager initialized successfully")

    def _validate_paths(self, source_path: str, target_path: str) -> None:
        """Validate source and target paths."""
        # Basic validation
        if not source_path or not target_path:
            raise ConfigurationError("Source and target paths must be specified")

        # For local paths, check existence
        if '://' not in source_path and not os.path.exists(source_path):
            raise ConfigurationError(f"Source path does not exist: {source_path}")

        # Check if source and target are the same
        if source_path == target_path:
            raise ConfigurationError("Source and target paths cannot be the same")

    def _init_storage(self) -> None:
        """Initialize storage backends based on paths."""
        # For now, only local storage is implemented
        # In the full version, we'd detect S3://, FTP://, etc.
        self.source_storage = LocalStorage(self.source_path)
        self.target_storage = LocalStorage(self.target_path)

    def _setup_filters(self, filters: Optional[List[str]]) -> None:
        """Set up filter patterns."""
        self.filters = []
        if filters:
            for pattern in filters:
                self.filters.append(Pattern(pattern))

    def _setup_encryption(self, encryption: bool, key: Optional[str]) -> None:
        """Set up encryption if enabled."""
        self.encryption_enabled = encryption
        if encryption:
            self.crypto = Crypto(key)
        else:
            self.crypto = None

    def _setup_versioning(self, versioning: bool, max_versions: int) -> None:
        """Set up versioning if enabled."""
        self.versioning_enabled = versioning
        if versioning:
            version_dir = os.path.join(self.target_path, '.versions')
            self.version_store = VersionStore(version_dir, max_versions)
        else:
            self.version_store = None

    def start(
            self,
            *,
            on_progress: Optional[Callable[[float], None]] = None,
            on_complete: Optional[Callable[[], None]] = None,
            on_error: Optional[Callable[[Exception], None]] = None
    ) -> bool:
        """
        Start the synchronization process.

        Args:
            on_progress: Callback for progress updates (0-100)
            on_complete: Callback when synchronization completes
            on_error: Callback when an error occurs

        Returns:
            bool: Whether the synchronization completed successfully
        """
        if self.is_running:
            self.logger.warning("Sync already in progress, ignoring request")
            return False

        self.is_running = True
        self.progress_reporter.reset()
        self.progress_reporter.on_progress = on_progress

        try:
            self.logger.info("Starting synchronization process")

            # 1. Scan directories and find differences
            self.logger.info("Scanning source and target directories")
            self.progress_reporter.update_stage("Scanning", 0)

            differences = self.scanner.find_differences(self.filters)

            self.logger.info(f"Found {len(differences)} differences to synchronize")
            self.progress_reporter.update_stage("Transferring files", 20)

            # 2. Process the differences
            total_files = len(differences)
            for i, diff in enumerate(differences):
                # Update progress
                progress_percent = 20 + (i / total_files * 80) if total_files > 0 else 100
                self.progress_reporter.update(progress_percent)

                # Process based on difference type
                if diff.action == 'create' or diff.action == 'update':
                    self._process_file_update(diff.source_path, diff.target_path)
                elif diff.action == 'delete':
                    self._process_file_deletion(diff.target_path)

            # 3. Finalize
            self.last_sync_time = time.time()
            self.progress_reporter.update(100)
            self.logger.info("Synchronization completed successfully")

            if on_complete:
                on_complete()

            return True

        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"Synchronization failed: {e}", exc_info=True)

            if on_error:
                on_error(e)

            return False

        finally:
            self.is_running = False

    def _process_file_update(self, source_path: str, target_path: str) -> None:
        """Process file creation or update."""
        # 1. Handle versioning if enabled
        if self.versioning_enabled and self.target_storage.exists(target_path):
            self.logger.debug(f"Creating version for {target_path}")
            self.version_store.add_version(target_path)

        # 2. Handle encryption if enabled
        if self.encryption_enabled:
            self.logger.debug(f"Encrypting file {source_path}")
            temp_encrypted = self.crypto.encrypt_file(source_path)
            self.transfer.transfer_file(temp_encrypted, target_path)
            os.unlink(temp_encrypted)  # Remove temporary encrypted file
        else:
            # 3. Transfer the file
            self.logger.debug(f"Transferring file {source_path} to {target_path}")
            self.transfer.transfer_file(source_path, target_path)

    def _process_file_deletion(self, target_path: str) -> None:
        """Process file deletion."""
        # 1. Handle versioning if enabled
        if self.versioning_enabled:
            self.logger.debug(f"Creating version before deleting {target_path}")
            self.version_store.add_version(target_path)

        # 2. Delete the file
        self.logger.debug(f"Deleting file {target_path}")
        self.target_storage.delete(target_path)

    def stop(self) -> None:
        """Stop the current synchronization process if running."""
        if self.is_running:
            self.logger.info("Stopping synchronization process")
            # In reality, we would signal the transfer process to stop
            # and clean up any temporary files
            self.is_running = False

    def get_status(self) -> Dict:
        """Get the current status of the synchronization manager."""
        return {
            "is_running": self.is_running,
            "last_sync_time": self.last_sync_time,
            "last_error": self.last_error,
            "progress": self.progress_reporter.current_progress if self.is_running else None,
            "source_path": self.source_path,
            "target_path": self.target_path,
            "encryption_enabled": self.encryption_enabled,
            "versioning_enabled": self.versioning_enabled,
            "bidirectional": self.bidirectional,
            "verify_integrity": self.verify_integrity
        }

    def schedule(self, interval: int, start_now: bool = False) -> None:
        """
        Schedule automatic synchronization at fixed intervals.

        Args:
            interval: Sync interval in seconds
            start_now: Whether to start the first sync immediately

        Note:
            This is a simplified version that doesn't use a proper scheduling system.
            A full implementation would use APScheduler or a similar library.
        """
        # In a real implementation, this would use a proper scheduler
        self.logger.error("Scheduling not implemented in this version")
        raise NotImplementedError("Scheduling is not implemented in this version")

    def restore_version(self, file_path: str, version_id: Optional[str] = None) -> bool:
        """
        Restore a previous version of a file.

        Args:
            file_path: Path to the file to restore
            version_id: Specific version ID to restore (latest if None)

        Returns:
            bool: Whether the restore was successful
        """
        if not self.versioning_enabled:
            self.logger.error("Cannot restore version: versioning is not enabled")
            return False

        try:
            self.logger.info(f"Restoring version of {file_path}")
            return self.version_store.restore_version(file_path, version_id)
        except Exception as e:
            self.logger.error(f"Failed to restore version: {e}", exc_info=True)
            return False