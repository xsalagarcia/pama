import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

class FernetEncDecrypt:
    """
    Cypher class.
    """

    def __init__(self, key: bytes, salt: bytes) -> None:
        if len(key) not in {16, 24, 32} and len(salt) not in {16, 24, 32}:
            raise ValueError("Key and salt must be 16, 24 or 32 bytes long")

        kdf = Argon2id(salt=salt, length=32, iterations=1, lanes=4, memory_cost=2 ** 21)

        self.f = Fernet(base64.urlsafe_b64encode(kdf.derive(key)))

    def encrypt(self, plaintext: bytes) -> bytes:
        return self.f.encrypt(plaintext)

    def decrypt(self, data: bytes) -> bytes:
        return self.f.decrypt(data)

