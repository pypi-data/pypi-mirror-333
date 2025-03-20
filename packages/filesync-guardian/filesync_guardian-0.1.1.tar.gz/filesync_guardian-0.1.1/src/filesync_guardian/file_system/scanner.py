"""
FileScanner for analyzing directories and identifying differences.
"""

import os
import hashlib
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

from filesync_guardian.filters.pattern import Pattern
from filesync_guardian.exceptions import FileAccessError
from filesync_guardian.utils.checksum import calculate_checksum


@dataclass
class FileDifference:
    """Represents a difference between source and target files."""
    action: str  # 'create', 'update', or 'delete'
    source_path: str
    target_path: str
    reason: str  # Why this difference exists (e.g., 'size_mismatch', 'missing')


@dataclass
class FileInfo:
    """Information about a single file."""
    path: str
    size: int
    mtime: float
    checksum: Optional[str] = None  # Only calculated when needed


class FileScanner:
    """
    Scanner for analyzing directories and identifying differences.

    This class scans source and target directories, compares files, and
    identifies which files need to be created, updated, or deleted.
    """

    def __init__(self, source_storage, target_storage, verify_integrity: bool = True):
        """
        Initialize a FileScanner instance.

        Args:
            source_storage: Source storage backend
            target_storage: Target storage backend
            verify_integrity: Whether to verify file integrity using checksums
        """
        self.source_storage = source_storage
        self.target_storage = target_storage
        self.verify_integrity = verify_integrity

    def find_differences(self, filters: Optional[List[Pattern]] = None) -> List[FileDifference]:
        """
        Find differences between source and target directories.

        Args:
            filters: Optional list of include/exclude patterns

        Returns:
            List of FileDifference objects representing differences

        Raises:
            FileAccessError: If there's an issue accessing the directories
        """
        try:
            # 1. Scan source and target directories
            source_files = self._scan_directory(self.source_storage)
            target_files = self._scan_directory(self.target_storage)

            # 2. Apply filters if provided
            if filters:
                source_files = self._apply_filters(source_files, filters)

            # 3. Compare files and identify differences
            differences = []

            # Files to create or update
            for rel_path, source_info in source_files.items():
                # Skip special files
                if self._should_skip(rel_path):
                    continue

                target_info = target_files.get(rel_path)

                if target_info is None:
                    # File doesn't exist in target, create it
                    differences.append(FileDifference(
                        action='create',
                        source_path=source_info.path,
                        target_path=self.target_storage.get_full_path(rel_path),
                        reason='missing_in_target'
                    ))
                elif self._files_differ(source_info, target_info):
                    # File exists but is different, update it
                    differences.append(FileDifference(
                        action='update',
                        source_path=source_info.path,
                        target_path=target_info.path,
                        reason=self._get_difference_reason(source_info, target_info)
                    ))

            # Files to delete (only in target, not in source)
            for rel_path, target_info in target_files.items():
                # Skip special files
                if self._should_skip(rel_path):
                    continue

                if rel_path not in source_files:
                    # File doesn't exist in source, delete it
                    differences.append(FileDifference(
                        action='delete',
                        source_path='',  # No source path for deletion
                        target_path=target_info.path,
                        reason='missing_in_source'
                    ))

            return differences

        except Exception as e:
            raise FileAccessError(f"Error finding differences: {str(e)}") from e

    def _scan_directory(self, storage) -> Dict[str, FileInfo]:
        """
        Scan a directory and collect file information.

        Args:
            storage: Storage backend to scan

        Returns:
            Dictionary mapping relative paths to FileInfo objects
        """
        files = {}

        for item in storage.list_all():
            # Get file info
            full_path = storage.get_full_path(item)
            stat_info = storage.get_stats(item)

            if stat_info.is_file:
                files[item] = FileInfo(
                    path=full_path,
                    size=stat_info.size,
                    mtime=stat_info.mtime
                )

        return files

    def _apply_filters(self, files: Dict[str, FileInfo], filters: List[Pattern]) -> Dict[str, FileInfo]:
        """
        Apply filters to a list of files.

        Args:
            files: Dictionary of files
            filters: List of filter patterns

        Returns:
            Filtered dictionary of files
        """
        filtered_files = {}

        for rel_path, file_info in files.items():
            include = True

            for pattern in filters:
                if pattern.matches(rel_path):
                    include = pattern.is_include()
                    # Last matching pattern takes precedence

            if include:
                filtered_files[rel_path] = file_info

        return filtered_files

    def _should_skip(self, rel_path: str) -> bool:
        """
        Determine if a file should be skipped.

        Args:
            rel_path: Relative path of the file

        Returns:
            True if the file should be skipped, False otherwise
        """
        # Skip versioning directory and temporary files
        skip_patterns = [
            '.versions/',  # Versioning directory
            '.~tmp~',      # Temporary files
            '.DS_Store',   # macOS system files
            'Thumbs.db'    # Windows thumbnail cache
        ]

        return any(pattern in rel_path for pattern in skip_patterns)

    def _files_differ(self, source_info: FileInfo, target_info: FileInfo) -> bool:
        """
        Determine if two files are different.

        Args:
            source_info: Source file information
            target_info: Target file information

        Returns:
            True if the files are different, False otherwise
        """
        # Quick check: size and modification time
        if source_info.size != target_info.size:
            return True

        # Skip checksum if modification times are the same and not forcing integrity check
        if abs(source_info.mtime - target_info.mtime) < 1 and not self.verify_integrity:
            return False

        # Calculate checksums if not already done
        if source_info.checksum is None:
            source_info.checksum = calculate_checksum(source_info.path)

        if target_info.checksum is None:
            target_info.checksum = calculate_checksum(target_info.path)

        # Compare checksums
        return source_info.checksum != target_info.checksum

    def _get_difference_reason(self, source_info: FileInfo, target_info: FileInfo) -> str:
        """Get the reason why two files are different."""
        if source_info.size != target_info.size:
            return 'size_mismatch'
        elif abs(source_info.mtime - target_info.mtime) >= 1:
            return 'time_mismatch'
        else:
            return 'content_mismatch'