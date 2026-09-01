import hashlib
import unittest

from pama.cryptotools.aescypher import AESCypher


class TestAESCypher(unittest.TestCase):

    def test_encrypt_and_decrypt(self):
        # Create the cypher using a hash of some bytes. With digest() we'll get the hash in 32-bytes binary format.
        aes_cypher = AESCypher(hashlib.sha256(b"some key").digest())

        # Use aes_cypher for encrypt.
        text = "Text to encrypt"
        cyphered = aes_cypher.encrypt(text.encode("utf-8"))
        self.assertNotEqual(text, cyphered)

        # And use aes_cypher for decrypt
        self.assertEqual(aes_cypher.decrypt(cyphered).decode("utf-8"), text)


