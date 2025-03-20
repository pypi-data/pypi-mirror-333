"""
Pattern matching for file filtering.
"""

import re
import fnmatch
from typing import List, Optional, Set, Tuple


class Pattern:
    """
    File pattern matcher for include/exclude rules.

    This class handles file pattern matching for filtering files
    during synchronization operations.
    """

    def __init__(self, pattern: str):
        """
        Initialize a Pattern instance.

        Args:
            pattern: Pattern string, with optional prefix:
                    - '+:' or '': Include pattern
                    - '-:': Exclude pattern

        Examples:
            - '*.txt': Include all text files
            - '-:*.tmp': Exclude all tmp files
            - '+:backup/*.zip': Include all zip files in backup directory
        """
        # Parse pattern type and actual pattern
        if pattern.startswith('+:'):
            self.include = True
            self.pattern = pattern[2:]
        elif pattern.startswith('-:'):
            self.include = False
            self.pattern = pattern[2:]
        else:
            self.include = True
            self.pattern = pattern

        # Convert glob pattern to regex
        if '*' in self.pattern or '?' in self.pattern or '[' in self.pattern:
            self.is_glob = True
            regex_pattern = fnmatch.translate(self.pattern)
            # Remove the end of string marker ($) to match anywhere in path
            if regex_pattern.endswith('\\Z'):
                regex_pattern = regex_pattern[:-3] + '.*\\Z'
            self.regex = re.compile(regex_pattern)
        else:
            self.is_glob = False

    def matches(self, path: str) -> bool:
        """
        Check if a path matches this pattern.

        Args:
            path: The path to check

        Returns:
            True if the path matches the pattern, False otherwise
        """
        # For glob patterns, use regex matching
        if self.is_glob:
            return bool(self.regex.match(path))

        # For directory patterns ending with slash
        if self.pattern.endswith('/'):
            return path.startswith(self.pattern) or path + '/' == self.pattern

        # For exact matches
        return path == self.pattern

    def is_include(self) -> bool:
        """
        Check if this is an include pattern.

        Returns:
            True if this is an include pattern, False if it's an exclude pattern
        """
        return self.include

    def __str__(self) -> str:
        """Get string representation of the pattern."""
        prefix = '+:' if self.include else '-:'
        return f"{prefix}{self.pattern}"


class PatternSet:
    """
    A set of patterns for filtering files.

    This class manages multiple patterns and provides methods
    for checking if files should be included or excluded.
    """

    def __init__(self, patterns: Optional[List[str]] = None):
        """
        Initialize a PatternSet instance.

        Args:
            patterns: List of pattern strings
        """
        self.patterns: List[Pattern] = []

        if patterns:
            for pattern in patterns:
                self.add_pattern(pattern)

    def add_pattern(self, pattern: str) -> None:
        """
        Add a pattern to the set.

        Args:
            pattern: Pattern string
        """
        self.patterns.append(Pattern(pattern))

    def should_include(self, path: str) -> bool:
        """
        Check if a path should be included based on the pattern set.

        Args:
            path: The path to check

        Returns:
            True if the path should be included, False otherwise
        """
        # Default to include if no patterns
        if not self.patterns:
            return True

        # Start with default (exclude)
        include = False

        for pattern in self.patterns:
            if pattern.matches(path):
                include = pattern.is_include()
                # Last matching pattern takes precedence

        return include

    def filter_paths(self, paths: List[str]) -> List[str]:
        """
        Filter a list of paths based on the pattern set.

        Args:
            paths: List of paths to filter

        Returns:
            Filtered list of paths
        """
        return [path for path in paths if self.should_include(path)]