"""
Progress reporting utilities for long-running operations.
"""

import time
from typing import Callable, Optional, Dict, List, Tuple


class ProgressReporter:
    """
    Reports progress for long-running operations.

    This class keeps track of progress during operations like
    synchronization and provides ETA and speed estimates.
    """

    def __init__(self):
        """Initialize a ProgressReporter instance."""
        self.start_time = None
        self.current_progress = 0.0
        self.current_stage = "Initializing"
        self.on_progress: Optional[Callable[[float], None]] = None
        self.history: List[Tuple[float, float]] = []  # (timestamp, progress)

    def reset(self):
        """Reset the progress reporter."""
        self.start_time = time.time()
        self.current_progress = 0.0
        self.current_stage = "Initializing"
        self.history = []
        self._record_history()

    def update(self, progress: float):
        """
        Update progress value.

        Args:
            progress: Progress value (0-100)
        """
        self.current_progress = max(0.0, min(100.0, progress))
        self._record_history()

        if self.on_progress:
            self.on_progress(self.current_progress)

    def update_stage(self, stage: str, progress: Optional[float] = None):
        """
        Update the current stage and optionally the progress.

        Args:
            stage: Current operation stage
            progress: Optional progress value
        """
        self.current_stage = stage
        if progress is not None:
            self.update(progress)

    def _record_history(self):
        """Record the current progress in history."""
        if not self.start_time:
            self.start_time = time.time()

        self.history.append((time.time(), self.current_progress))

        # Keep only the last 10 entries to avoid unbounded growth
        if len(self.history) > 10:
            self.history = self.history[-10:]

    def get_progress(self) -> float:
        """
        Get the current progress percentage.

        Returns:
            Progress value (0-100)
        """
        return self.current_progress

    def get_eta(self) -> Optional[float]:
        """
        Estimate time remaining until completion.

        Returns:
            Estimated seconds remaining or None if cannot be calculated
        """
        if not self.history or len(self.history) < 2 or self.current_progress >= 100:
            return None

        # Calculate speed based on recent history
        recent_history = self.history[-5:]  # Use last 5 entries
        if len(recent_history) < 2:
            return None

        first_time, first_progress = recent_history[0]
        last_time, last_progress = recent_history[-1]

        time_diff = last_time - first_time
        progress_diff = last_progress - first_progress

        if time_diff <= 0 or progress_diff <= 0:
            return None

        # Calculate speed in progress units per second
        speed = progress_diff / time_diff

        # Calculate remaining progress and time
        remaining_progress = 100.0 - last_progress
        eta = remaining_progress / speed if speed > 0 else None

        return eta

    def get_speed(self) -> Optional[float]:
        """
        Get the current progress speed.

        Returns:
            Speed in progress units per second or None if cannot be calculated
        """
        if not self.history or len(self.history) < 2:
            return None

        # Calculate speed based on recent history
        recent_history = self.history[-5:]  # Use last 5 entries
        if len(recent_history) < 2:
            return None

        first_time, first_progress = recent_history[0]
        last_time, last_progress = recent_history[-1]

        time_diff = last_time - first_time
        progress_diff = last_progress - first_progress

        if time_diff <= 0:
            return None

        return progress_diff / time_diff

    def get_elapsed_time(self) -> float:
        """
        Get the elapsed time since starting.

        Returns:
            Elapsed time in seconds
        """
        if not self.start_time:
            return 0.0

        return time.time() - self.start_time

    def get_status(self) -> Dict:
        """
        Get the current status.

        Returns:
            Dictionary with status information
        """
        eta = self.get_eta()
        speed = self.get_speed()
        elapsed = self.get_elapsed_time()

        return {
            "progress": self.current_progress,
            "stage": self.current_stage,
            "elapsed": elapsed,
            "eta": eta,
            "speed": speed,
            "estimated_total": elapsed + (eta or 0)
        }

    def format_status(self) -> str:
        """
        Format the current status as a string.

        Returns:
            Formatted status string
        """
        status = self.get_status()

        progress_str = f"{status['progress']:.1f}%"
        stage_str = status['stage']
        elapsed_str = self._format_time(status['elapsed'])

        parts = [f"{stage_str}: {progress_str}", f"Elapsed: {elapsed_str}"]

        if status['eta'] is not None:
            eta_str = self._format_time(status['eta'])
            parts.append(f"ETA: {eta_str}")

        return " | ".join(parts)

    @staticmethod
    def _format_time(seconds: float) -> str:
        """Format time in seconds as h:m:s."""
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"