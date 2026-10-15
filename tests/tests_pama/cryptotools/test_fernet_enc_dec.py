import hashlib
import os
import unittest

from cryptography.fernet import InvalidToken

from pama.cryptotools import fernet_enc_dec
from pama.exceptions.cryptotools import CryptoError


class TestFernetEncDec(unittest.TestCase):
    def test_encrypt_decrypt(self):
        salt = os.urandom(32)
        key_str = "some key"
        key_bytes = hashlib.sha256(key_str.encode("utf-8")).digest()

        enc_dec = fernet_enc_dec.FernetEncDecrypt(key=key_bytes, salt=salt)
        other_enc_dec = fernet_enc_dec.FernetEncDecrypt(key=b"other key", salt=salt)

        # Use fernet_enc_dec for encrypt.
        text = "Text to encrypt"
        cyphered = enc_dec.encrypt(text.encode("utf-8"))
        self.assertNotEqual(text, cyphered)

        # And use aes_cypher for decrypt
        self.assertEqual(enc_dec.decrypt(cyphered).decode("utf-8"), text)

        with self.assertRaises(CryptoError):
            other_enc_dec.decrypt(cyphered).decode("utf-8")


