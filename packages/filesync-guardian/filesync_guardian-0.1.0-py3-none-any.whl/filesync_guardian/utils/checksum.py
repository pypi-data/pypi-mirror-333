"""
Checksum utilities for file integrity verification.
"""

import os
import hashlib
from typing import Optional


def calculate_checksum(file_path: str, algorithm: str = 'sha256', buffer_size: int = 65536) -> str:
    """
    Calculate the checksum of a file.

    Args:
        file_path: Path to the file
        algorithm: Hash algorithm to use ('md5', 'sha1', 'sha256', or 'sha512')
        buffer_size: Buffer size for reading the file

    Returns:
        Checksum hash as a hexadecimal string

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the algorithm is not supported
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if algorithm == 'md5':
        hash_obj = hashlib.md5()
    elif algorithm == 'sha1':
        hash_obj = hashlib.sha1()
    elif algorithm == 'sha256':
        hash_obj = hashlib.sha256()
    elif algorithm == 'sha512':
        hash_obj = hashlib.sha512()
    else:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            hash_obj.update(data)

    return hash_obj.hexdigest()


def verify_checksum(file_path: str, expected_checksum: str, algorithm: str = 'sha256') -> bool:
    """
    Verify that a file matches the expected checksum.

    Args:
        file_path: Path to the file
        expected_checksum: Expected checksum value
        algorithm: Hash algorithm to use

    Returns:
        True if the checksum matches, False otherwise
    """
    try:
        actual_checksum = calculate_checksum(file_path, algorithm)
        return actual_checksum == expected_checksum
    except Exception:
        return False