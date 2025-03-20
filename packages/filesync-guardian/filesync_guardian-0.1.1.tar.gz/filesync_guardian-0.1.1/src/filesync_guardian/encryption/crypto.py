"""
Encryption utilities for secure file storage.
"""

import os
import hashlib
import tempfile
import base64
import logging
from typing import Optional, Tuple

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

from filesync_guardian.exceptions import EncryptionError


class Crypto:
    """
    Handles file encryption and decryption.

    This class provides methods for securely encrypting and decrypting
    files using the Fernet symmetric encryption algorithm.
    """

    def __init__(self, key: Optional[str] = None, salt: Optional[bytes] = None):
        """
        Initialize a Crypto instance.

        Args:
            key: Encryption key (password) or None to generate a random key
            salt: Salt for key derivation or None to use a default salt
        """
        self.logger = logging.getLogger("filesync_guardian.encryption")

        # Use provided key or generate one
        if key is None:
            self.key = Fernet.generate_key()
            self.logger.info("Generated new encryption key")
        else:
            # Derive a key from the password
            salt = salt or b'FileSync-Guardian-Salt'
            self.key = self._derive_key(key, salt)
            self.logger.info("Using provided encryption key")

        # Initialize Fernet cipher
        self.cipher = Fernet(self.key)

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Derive an encryption key from a password.

        Args:
            password: User-provided password
            salt: Salt for key derivation

        Returns:
            Derived encryption key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        # Derive the key and encode it for Fernet
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def encrypt_file(self, file_path: str) -> str:
        """
        Encrypt a file.

        Args:
            file_path: Path to the file to encrypt

        Returns:
            Path to the encrypted file (temporary)

        Raises:
            EncryptionError: If there's an issue with encryption
        """
        if not os.path.exists(file_path):
            raise EncryptionError(f"File does not exist: {file_path}")

        try:
            # Create a temporary file for the encrypted data
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_path = temp_file.name

            # Read the file and encrypt it
            with open(file_path, 'rb') as f:
                data = f.read()

            encrypted_data = self.cipher.encrypt(data)

            # Write the encrypted data to the temporary file
            with open(temp_path, 'wb') as f:
                f.write(encrypted_data)

            self.logger.debug(f"Encrypted {file_path} to {temp_path}")
            return temp_path

        except Exception as e:
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
            raise EncryptionError(f"Error encrypting file: {str(e)}") from e

    def decrypt_file(self, encrypted_path: str) -> str:
        """
        Decrypt a file.

        Args:
            encrypted_path: Path to the encrypted file

        Returns:
            Path to the decrypted file (temporary)

        Raises:
            EncryptionError: If there's an issue with decryption
        """
        if not os.path.exists(encrypted_path):
            raise EncryptionError(f"File does not exist: {encrypted_path}")

        try:
            # Create a temporary file for the decrypted data
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_path = temp_file.name

            # Read the encrypted file
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()

            # Decrypt the data
            decrypted_data = self.cipher.decrypt(encrypted_data)

            # Write the decrypted data to the temporary file
            with open(temp_path, 'wb') as f:
                f.write(decrypted_data)

            self.logger.debug(f"Decrypted {encrypted_path} to {temp_path}")
            return temp_path

        except Exception as e:
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
            raise EncryptionError(f"Error decrypting file: {str(e)}") from e

    def encrypt_data(self, data: bytes) -> bytes:
        """
        Encrypt raw data.

        Args:
            data: Data to encrypt

        Returns:
            Encrypted data
        """
        return self.cipher.encrypt(data)

    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """
        Decrypt raw data.

        Args:
            encrypted_data: Data to decrypt

        Returns:
            Decrypted data
        """
        return self.cipher.decrypt(encrypted_data)

    def get_key_string(self) -> str:
        """
        Get the encryption key as a string.

        Returns:
            Base64-encoded key string
        """
        return self.key.decode()