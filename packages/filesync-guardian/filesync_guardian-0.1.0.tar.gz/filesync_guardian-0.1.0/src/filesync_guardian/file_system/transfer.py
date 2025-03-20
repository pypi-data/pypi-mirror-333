"""
File transfer operations for moving files between storage backends.
"""

import os
import shutil
import tempfile
import logging
from typing import Optional, Tuple, BinaryIO

from filesync_guardian.exceptions import TransferError, IntegrityError
from filesync_guardian.utils.checksum import calculate_checksum


class FileTransfer:
    """
    Handles file transfer operations between different storage backends.

    This class is responsible for copying, moving, and verifying files
    between different storage locations.
    """

    def __init__(self, source_storage, target_storage, verify_integrity: bool = True):
        """
        Initialize a FileTransfer instance.

        Args:
            source_storage: Source storage backend
            target_storage: Target storage backend
            verify_integrity: Whether to verify file integrity after transfer
        """
        self.source_storage = source_storage
        self.target_storage = target_storage
        self.verify_integrity = verify_integrity
        self.logger = logging.getLogger("filesync_guardian.transfer")

        # Buffer size for file transfers (8 MB)
        self.buffer_size = 8 * 1024 * 1024

    def transfer_file(
        self,
        source_path: str,
        target_path: str,
        overwrite: bool = True
    ) -> bool:
        """
        Transfer a file from source to target.

        Args:
            source_path: Source file path
            target_path: Target file path
            overwrite: Whether to overwrite existing files

        Returns:
            True if transfer was successful

        Raises:
            TransferError: If there's an issue with the transfer
            IntegrityError: If integrity verification fails
        """
        self.logger.debug(f"Transferring {source_path} to {target_path}")

        # Check if target exists and overwrite is False
        if not overwrite and self.target_storage.exists(target_path):
            self.logger.debug(f"Target file exists and overwrite is False, skipping: {target_path}")
            return False

        try:
            # If both storages are local and on the same filesystem, use copy
            if (self.source_storage.is_local() and
                self.target_storage.is_local() and
                os.path.exists(source_path)):

                # Create target directory if it doesn't exist
                target_dir = os.path.dirname(target_path)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)

                # Copy the file
                shutil.copy2(source_path, target_path)

            else:
                # Stream the file between storage backends
                self._stream_transfer(source_path, target_path)

            # Verify integrity if enabled
            if self.verify_integrity:
                self._verify_integrity(source_path, target_path)

            return True

        except Exception as e:
            raise TransferError(f"Error transferring file: {str(e)}") from e

    def _stream_transfer(self, source_path: str, target_path: str) -> None:
        """
        Stream a file from source to target storage.

        Args:
            source_path: Source file path
            target_path: Target file path
        """
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            # Create target directory if needed
            target_dir = os.path.dirname(target_path)
            self.target_storage.ensure_directory(target_dir)

            # Stream from source to temp file
            with self.source_storage.open_file(source_path, 'rb') as src_file:
                with open(temp_path, 'wb') as tmp:
                    self._copy_stream(src_file, tmp)

            # Stream from temp file to target
            with open(temp_path, 'rb') as tmp:
                with self.target_storage.open_file(target_path, 'wb') as tgt_file:
                    self._copy_stream(tmp, tgt_file)

        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def _copy_stream(self, src_file: BinaryIO, dst_file: BinaryIO) -> None:
        """
        Copy data from one file stream to another.

        Args:
            src_file: Source file object
            dst_file: Destination file object
        """
        while True:
            buf = src_file.read(self.buffer_size)
            if not buf:
                break
            dst_file.write(buf)

    def _verify_integrity(self, source_path: str, target_path: str) -> None:
        """
        Verify file integrity by comparing checksums.

        Args:
            source_path: Source file path
            target_path: Target file path

        Raises:
            IntegrityError: If checksums don't match
        """
        self.logger.debug(f"Verifying integrity of {target_path}")

        # Calculate checksums
        source_checksum = calculate_checksum(source_path)
        target_checksum = calculate_checksum(target_path)

        # Compare checksums
        if source_checksum != target_checksum:
            error_msg = f"Integrity check failed for {target_path}: checksums don't match"
            self.logger.error(error_msg)

            # Try to delete the corrupted target file
            try:
                os.unlink(target_path)
            except Exception:
                pass

            raise IntegrityError(error_msg)

        self.logger.debug(f"Integrity verification successful for {target_path}")

    def move_file(self, source_path: str, target_path: str, overwrite: bool = True) -> bool:
        """
        Move a file from source to target.

        Args:
            source_path: Source file path
            target_path: Target file path
            overwrite: Whether to overwrite existing files

        Returns:
            True if move was successful

        Raises:
            TransferError: If there's an issue with the move
        """
        # First transfer the file
        if not self.transfer_file(source_path, target_path, overwrite):
            return False

        # Then delete the source
        try:
            self.source_storage.delete(source_path)
            return True
        except Exception as e:
            raise TransferError(f"Error deleting source file after move: {str(e)}") from e