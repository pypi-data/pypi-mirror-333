"""
FileWatcher for monitoring file system changes.
"""

import os
import time
import logging
from threading import Thread, Event
from typing import Callable, Dict, List, Optional, Set

from filesync_guardian.exceptions import FileAccessError


class FileWatcher:
    """
    Watches for changes in a directory.

    This class monitors a directory for file changes and triggers
    callback functions when files are created, modified, or deleted.
    """

    def __init__(self, path: str, recursive: bool = True, polling_interval: float = 1.0):
        """
        Initialize a FileWatcher instance.

        Args:
            path: Directory path to watch
            recursive: Whether to watch subdirectories
            polling_interval: Seconds between polling checks
        """
        self.path = os.path.abspath(path)
        self.recursive = recursive
        self.polling_interval = polling_interval
        self.logger = logging.getLogger("filesync_guardian.watcher")

        # Last known state
        self.last_scan: Dict[str, float] = {}
        self.stop_event = Event()
        self.watch_thread: Optional[Thread] = None

        # Callbacks
        self.on_created: Optional[Callable[[str], None]] = None
        self.on_modified: Optional[Callable[[str], None]] = None
        self.on_deleted: Optional[Callable[[str], None]] = None

    def start(self) -> None:
        """
        Start watching for file changes.

        Raises:
            FileAccessError: If the watched path doesn't exist
        """
        if not os.path.exists(self.path):
            raise FileAccessError(f"Watch path does not exist: {self.path}")

        # Do initial scan
        self.last_scan = self._scan_directory()

        # Start watch thread
        self.stop_event.clear()
        self.watch_thread = Thread(target=self._watch_loop, daemon=True)
        self.watch_thread.start()

        self.logger.info(f"Started watching {self.path}")

    def stop(self) -> None:
        """Stop watching for file changes."""
        if self.watch_thread and self.watch_thread.is_alive():
            self.stop_event.set()
            self.watch_thread.join(timeout=2)
            self.logger.info(f"Stopped watching {self.path}")

    def _watch_loop(self) -> None:
        """Main watch loop that runs in a separate thread."""
        while not self.stop_event.is_set():
            try:
                # Scan the directory
                current_scan = self._scan_directory()

                # Compare with last scan
                self._detect_changes(current_scan)

                # Update last scan
                self.last_scan = current_scan

            except Exception as e:
                self.logger.error(f"Error in watch loop: {str(e)}", exc_info=True)

            # Wait for interval or until stopped
            self.stop_event.wait(self.polling_interval)

    def _scan_directory(self) -> Dict[str, float]:
        """
        Scan the watched directory and return file information.

        Returns:
            Dictionary mapping file paths to modification times
        """
        files = {}

        try:
            for dirpath, dirnames, filenames in os.walk(self.path):
                # Skip if not recursive and not in root
                if not self.recursive and dirpath != self.path:
                    continue

                # Process files
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(filepath, self.path)

                    try:
                        mtime = os.path.getmtime(filepath)
                        files[rel_path] = mtime
                    except Exception:
                        # Skip files we can't access
                        pass

        except Exception as e:
            self.logger.error(f"Error scanning directory: {str(e)}", exc_info=True)

        return files

    def _detect_changes(self, current_scan: Dict[str, float]) -> None:
        """
        Detect changes between current and previous scan.

        Args:
            current_scan: Current scan result
        """
        # Files in current but not in last scan (created)
        for filepath, mtime in current_scan.items():
            if filepath not in self.last_scan:
                if self.on_created:
                    self.on_created(filepath)
                    self.logger.debug(f"File created: {filepath}")
            elif abs(mtime - self.last_scan[filepath]) > 0.001:
                # Files with different modification time (modified)
                if self.on_modified:
                    self.on_modified(filepath)
                    self.logger.debug(f"File modified: {filepath}")

        # Files in last but not in current scan (deleted)
        for filepath in self.last_scan.keys():
            if filepath not in current_scan:
                if self.on_deleted:
                    self.on_deleted(filepath)
                    self.logger.debug(f"File deleted: {filepath}")

    def set_callbacks(
            self,
            on_created: Optional[Callable[[str], None]] = None,
            on_modified: Optional[Callable[[str], None]] = None,
            on_deleted: Optional[Callable[[str], None]] = None
    ) -> None:
        """
        Set callback functions for file events.

        Args:
            on_created: Called when a file is created
            on_modified: Called when a file is modified
            on_deleted: Called when a file is deleted
        """
        self.on_created = on_created
        self.on_modified = on_modified
        self.on_deleted = on_deleted