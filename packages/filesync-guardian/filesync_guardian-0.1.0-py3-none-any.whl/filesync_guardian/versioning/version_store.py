"""
VersionStore for managing file versions.
"""

import os
import json
import shutil
import logging
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from filesync_guardian.exceptions import VersioningError


class VersionStore:
    """
    Manages file versioning.

    This class handles creating, storing, and retrieving file versions,
    allowing users to restore previous versions of files.
    """

    def __init__(self, version_dir: str, max_versions: int = 5):
        """
        Initialize a VersionStore instance.

        Args:
            version_dir: Directory to store versions
            max_versions: Maximum number of versions to keep per file
        """
        self.version_dir = version_dir
        self.max_versions = max_versions
        self.logger = logging.getLogger("filesync_guardian.versioning")

        # Create version directory if it doesn't exist
        if not os.path.exists(version_dir):
            os.makedirs(version_dir, exist_ok=True)

        # Path to metadata file
        self.metadata_path = os.path.join(version_dir, 'version_metadata.json')

        # Load metadata if it exists
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict:
        """
        Load version metadata from file.

        Returns:
            Dictionary with version metadata
        """
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading version metadata: {str(e)}", exc_info=True)

        # Default empty metadata
        return {"files": {}}

    def _save_metadata(self) -> None:
        """Save version metadata to file."""
        try:
            with open(self.metadata_path, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving version metadata: {str(e)}", exc_info=True)

    def add_version(self, file_path: str) -> str:
        """
        Add a new version of a file.

        Args:
            file_path: Path to the file to version

        Returns:
            Version ID

        Raises:
            VersioningError: If there's an issue creating the version
        """
        if not os.path.exists(file_path):
            raise VersioningError(f"File does not exist: {file_path}")

        try:
            # Generate a unique version ID
            timestamp = int(time.time())
            file_hash = hashlib.md5(file_path.encode()).hexdigest()[:8]
            version_id = f"{timestamp}_{file_hash}"

            # Create version directory if needed
            rel_path = os.path.basename(file_path)
            version_subdir = os.path.join(self.version_dir, rel_path)
            os.makedirs(version_subdir, exist_ok=True)

            # Copy the file to the version directory
            version_path = os.path.join(version_subdir, version_id)
            shutil.copy2(file_path, version_path)

            # Update metadata
            if rel_path not in self.metadata["files"]:
                self.metadata["files"][rel_path] = []

            # Add version info
            self.metadata["files"][rel_path].append({
                "id": version_id,
                "timestamp": timestamp,
                "size": os.path.getsize(file_path),
                "path": version_path
            })

            # Sort versions by timestamp (newest first)
            self.metadata["files"][rel_path].sort(
                key=lambda v: v["timestamp"],
                reverse=True
            )

            # Prune old versions if needed
            if len(self.metadata["files"][rel_path]) > self.max_versions:
                self._prune_old_versions(rel_path)

            # Save metadata
            self._save_metadata()

            self.logger.debug(f"Created version {version_id} for {file_path}")
            return version_id

        except Exception as e:
            raise VersioningError(f"Error creating version: {str(e)}") from e

    def _prune_old_versions(self, rel_path: str) -> None:
        """
        Remove old versions to stay within max_versions limit.

        Args:
            rel_path: Relative path of the file
        """
        versions = self.metadata["files"][rel_path]
        if len(versions) <= self.max_versions:
            return

        # Get versions to delete
        to_delete = versions[self.max_versions:]
        versions = versions[:self.max_versions]

        # Update metadata
        self.metadata["files"][rel_path] = versions

        # Delete files
        for version in to_delete:
            try:
                if os.path.exists(version["path"]):
                    os.unlink(version["path"])
            except Exception as e:
                self.logger.error(f"Error deleting old version: {str(e)}", exc_info=True)

    def get_versions(self, file_path: str) -> List[Dict]:
        """
        Get all versions of a file.

        Args:
            file_path: Path to the file

        Returns:
            List of version information dictionaries
        """
        rel_path = os.path.basename(file_path)
        return self.metadata["files"].get(rel_path, [])

    def restore_version(self, file_path: str, version_id: Optional[str] = None) -> bool:
        """
        Restore a specific version of a file.

        Args:
            file_path: Path to the file to restore
            version_id: Version ID to restore (latest if None)

        Returns:
            True if restore was successful

        Raises:
            VersioningError: If there's an issue restoring the version
        """
        rel_path = os.path.basename(file_path)
        versions = self.metadata["files"].get(rel_path, [])

        if not versions:
            raise VersioningError(f"No versions found for {file_path}")

        # Find the version to restore
        version_to_restore = None
        if version_id:
            for version in versions:
                if version["id"] == version_id:
                    version_to_restore = version
                    break

            if not version_to_restore:
                raise VersioningError(f"Version {version_id} not found for {file_path}")
        else:
            # Use the latest version
            version_to_restore = versions[0]

        try:
            # Create a new version of the current file if it exists
            if os.path.exists(file_path):
                self.add_version(file_path)

            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Copy the version to the original location
            shutil.copy2(version_to_restore["path"], file_path)

            self.logger.info(f"Restored version {version_to_restore['id']} of {file_path}")
            return True

        except Exception as e:
            raise VersioningError(f"Error restoring version: {str(e)}") from e

    def delete_version(self, file_path: str, version_id: str) -> bool:
        """
        Delete a specific version of a file.

        Args:
            file_path: Path to the file
            version_id: Version ID to delete

        Returns:
            True if deletion was successful

        Raises:
            VersioningError: If there's an issue deleting the version
        """
        rel_path = os.path.basename(file_path)
        versions = self.metadata["files"].get(rel_path, [])

        if not versions:
            raise VersioningError(f"No versions found for {file_path}")

        # Find the version to delete
        version_to_delete = None
        for i, version in enumerate(versions):
            if version["id"] == version_id:
                version_to_delete = version
                del versions[i]
                break

        if not version_to_delete:
            raise VersioningError(f"Version {version_id} not found for {file_path}")

        try:
            # Delete the version file
            if os.path.exists(version_to_delete["path"]):
                os.unlink(version_to_delete["path"])

            # Update metadata
            self.metadata["files"][rel_path] = versions
            self._save_metadata()

            self.logger.info(f"Deleted version {version_id} of {file_path}")
            return True

        except Exception as e:
            raise VersioningError(f"Error deleting version: {str(e)}") from e

    def cleanup(self) -> None:
        """
        Clean up orphaned version files.

        This method scans the version directory and removes any files
        not referenced in the metadata.
        """
        # Get all paths in the metadata
        referenced_paths = set()
        for file_info in self.metadata["files"].values():
            for version in file_info:
                referenced_paths.add(version["path"])

        # Scan version directory
        for root, _, files in os.walk(self.version_dir):
            for file in files:
                if file == 'version_metadata.json':
                    continue

                file_path = os.path.join(root, file)
                if file_path not in referenced_paths:
                    try:
                        os.unlink(file_path)
                        self.logger.debug(f"Removed orphaned version file: {file_path}")
                    except Exception as e:
                        self.logger.error(f"Error removing orphaned file: {str(e)}", exc_info=True)