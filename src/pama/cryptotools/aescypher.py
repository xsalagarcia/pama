import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class AESCypher:
    """
    Cypher class.
    """
    def __init__(self, key: bytes):
        """
        :param key: Some bytes (hash is recommended) for using encrypt-decrypt AES-GCM protocol.
        """
        if len(key) not in {16, 24, 32}:
            raise ValueError("Key must be 16, 24 or 32 bytes long")
        self.key = key
        self.aes_gcm = AESGCM(self.key)

    def encrypt(self, plaintext: bytes, associated_data: bytes | None = None) -> bytes:
        """
        Encrypt some plain text.
        :param plaintext:
        :param associated_data: Associated data can be used as unencrypted data for integrity or context.
        :return:
        """
        nonce = os.urandom(12)  # Number used once to ensure that each message is unique. This must be random.
        return nonce + self.aes_gcm.encrypt(nonce, plaintext, associated_data=associated_data)

    def decrypt(self, data: bytes, associated_data: bytes | None = None) -> bytes:
        """
        Decrypt bytes to plaintext.
        :param data:
        :param associated_data: If associated data was used for encrypt, use the same.
        :return:
        """
        nonce = data[:12]  # First 12 bytes are nonce (see encrypt function).
        ciphertext = data[12:]
        return self.aes_gcm.decrypt(nonce, ciphertext, associated_data=associated_data)
