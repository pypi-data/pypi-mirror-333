"""
Local file system storage backend.
"""

import os
import shutil
import logging
from dataclasses import dataclass
from typing import BinaryIO, List, Optional, Iterator, Dict, Any, Tuple


@dataclass
class StatInfo:
    """File statistics information."""
    is_file: bool
    is_dir: bool
    size: int
    mtime: float


class LocalStorage:
    """
    Local file system storage backend.

    This class provides an interface for interacting with the local
    file system for file operations.
    """

    def __init__(self, base_path: str):
        """
        Initialize a LocalStorage instance.

        Args:
            base_path: Base directory path
        """
        self.base_path = os.path.abspath(base_path) if os.path.exists(base_path) else base_path
        self.logger = logging.getLogger("filesync_guardian.storage.local")

        # Create base path if it doesn't exist
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path, exist_ok=True)

    def get_full_path(self, rel_path: str) -> str:
        """
        Get the absolute path for a relative path.

        Args:
            rel_path: Relative path

        Returns:
            Absolute path
        """
        # Handle root path case
        if not rel_path:
            return self.base_path

        return os.path.join(self.base_path, rel_path)

    def get_relative_path(self, abs_path: str) -> str:
        """
        Get the relative path from an absolute path.

        Args:
            abs_path: Absolute path

        Returns:
            Relative path
        """
        return os.path.relpath(abs_path, self.base_path)

    def list_files(self, rel_path: str = "") -> List[str]:
        """
        List files in a directory.

        Args:
            rel_path: Relative path to the directory

        Returns:
            List of relative file paths (not including directories)
        """
        full_path = self.get_full_path(rel_path)
        if not os.path.exists(full_path) or not os.path.isdir(full_path):
            return []

        files = []
        entries = os.listdir(full_path)

        for entry in entries:
            entry_path = os.path.join(full_path, entry)
            if os.path.isfile(entry_path):
                if rel_path:
                    files.append(os.path.join(rel_path, entry))
                else:
                    files.append(entry)

        return files

    def list_dirs(self, rel_path: str = "") -> List[str]:
        """
        List subdirectories in a directory.

        Args:
            rel_path: Relative path to the directory

        Returns:
            List of relative directory paths
        """
        full_path = self.get_full_path(rel_path)
        if not os.path.exists(full_path) or not os.path.isdir(full_path):
            return []

        dirs = []
        entries = os.listdir(full_path)

        for entry in entries:
            entry_path = os.path.join(full_path, entry)
            if os.path.isdir(entry_path):
                if rel_path:
                    dirs.append(os.path.join(rel_path, entry))
                else:
                    dirs.append(entry)

        return dirs

    def list_all(self, rel_path: str = "") -> List[str]:
        """
        List all files and directories recursively.

        Args:
            rel_path: Relative path to start from

        Returns:
            List of all relative file paths
        """
        full_path = self.get_full_path(rel_path)
        if not os.path.exists(full_path) or not os.path.isdir(full_path):
            return []

        all_files = []
        for root, _, files in os.walk(full_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_file_path = self.get_relative_path(abs_path)
                all_files.append(rel_file_path)

        return all_files

    def exists(self, rel_path: str) -> bool:
        """
        Check if a file or directory exists.

        Args:
            rel_path: Relative path

        Returns:
            True if the path exists
        """
        return os.path.exists(self.get_full_path(rel_path))

    def is_file(self, rel_path: str) -> bool:
        """
        Check if a path is a file.

        Args:
            rel_path: Relative path

        Returns:
            True if the path is a file
        """
        full_path = self.get_full_path(rel_path)
        return os.path.exists(full_path) and os.path.isfile(full_path)

    def is_dir(self, rel_path: str) -> bool:
        """
        Check if a path is a directory.

        Args:
            rel_path: Relative path

        Returns:
            True if the path is a directory
        """
        full_path = self.get_full_path(rel_path)
        return os.path.exists(full_path) and os.path.isdir(full_path)

    def get_stats(self, rel_path: str) -> StatInfo:
        """
        Get statistics for a file or directory.

        Args:
            rel_path: Relative path

        Returns:
            StatInfo object
        """
        full_path = self.get_full_path(rel_path)
        if not os.path.exists(full_path):
            return StatInfo(False, False, 0, 0)

        is_file = os.path.isfile(full_path)
        is_dir = os.path.isdir(full_path)
        size = os.path.getsize(full_path) if is_file else 0
        mtime = os.path.getmtime(full_path)

        return StatInfo(is_file, is_dir, size, mtime)

    def ensure_directory(self, rel_path: str) -> bool:
        """
        Ensure a directory exists, creating it if necessary.

        Args:
            rel_path: Relative path to the directory

        Returns:
            True if the directory exists or was created successfully
        """
        full_path = self.get_full_path(rel_path)

        try:
            if not os.path.exists(full_path):
                os.makedirs(full_path, exist_ok=True)

            return os.path.isdir(full_path)
        except Exception as e:
            self.logger.error(f"Error creating directory {rel_path}: {str(e)}", exc_info=True)
            return False

    def open_file(self, rel_path: str, mode: str = 'rb') -> BinaryIO:
        """
        Open a file for reading or writing.

        Args:
            rel_path: Relative path to the file
            mode: File open mode

        Returns:
            File object
        """
        full_path = self.get_full_path(rel_path)

        # Create directory if needed for write modes
        if 'w' in mode or 'a' in mode:
            dir_path = os.path.dirname(full_path)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)

        return open(full_path, mode)

    def read_file(self, rel_path: str) -> bytes:
        """
        Read a file's contents.

        Args:
            rel_path: Relative path to the file

        Returns:
            File contents as bytes
        """
        with self.open_file(rel_path, 'rb') as f:
            return f.read()

    def write_file(self, rel_path: str, data: bytes) -> int:
        """
        Write data to a file.

        Args:
            rel_path: Relative path to the file
            data: Data to write

        Returns:
            Number of bytes written
        """
        with self.open_file(rel_path, 'wb') as f:
            return f.write(data)

    def delete(self, rel_path: str) -> bool:
        """
        Delete a file or directory.

        Args:
            rel_path: Relative path

        Returns:
            True if deletion was successful
        """
        full_path = self.get_full_path(rel_path)

        try:
            if not os.path.exists(full_path):
                return True

            if os.path.isfile(full_path):
                os.unlink(full_path)
            else:
                shutil.rmtree(full_path)

            return True
        except Exception as e:
            self.logger.error(f"Error deleting {rel_path}: {str(e)}", exc_info=True)
            return False

    def copy(self, src_path: str, dst_path: str) -> bool:
        """
        Copy a file or directory.

        Args:
            src_path: Source relative path
            dst_path: Destination relative path

        Returns:
            True if copy was successful
        """
        src_full = self.get_full_path(src_path)
        dst_full = self.get_full_path(dst_path)

        try:
            # Create destination directory if needed
            dst_dir = os.path.dirname(dst_full)
            if dst_dir and not os.path.exists(dst_dir):
                os.makedirs(dst_dir, exist_ok=True)

            if os.path.isfile(src_full):
                shutil.copy2(src_full, dst_full)
            else:
                shutil.copytree(src_full, dst_full)

            return True
        except Exception as e:
            self.logger.error(f"Error copying {src_path} to {dst_path}: {str(e)}", exc_info=True)
            return False

    def is_local(self) -> bool:
        """
        Check if this is a local storage backend.

        Returns:
            True for LocalStorage
        """
        return True