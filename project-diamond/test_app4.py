# Project: app unittest
# Purpose Details: tests all methods of app4
# Course: IST 411
# Date Developed: 12/4/2018
# Last Date Changed: 12/4/2018
# Rev:
# ----------------------------
import unittest

from app4 import AESDecrypt
from app4 import AESEncrypt


class TestApp4(unittest.TestCase):

    def test_decrypt(self):
        cipher = b'z\x03\xc9O\xc9\xa4\xa4\x80q\xf2\xec\x96\x03\n\xda\xe4'
        # in bytes
        key = b'This is a key123'
        IV = b'This is an IV123'

        # instantiation
        decryptObj = AESDecrypt(key, IV)
        decrypted_message = str(decryptObj.decrypt(cipher), 'utf-8').strip()
        expected_message = '411 Project'
        # test
        self.assertEqual(expected_message, decrypted_message)

    def test_encrypted(self):
        """ Test will pass if below message returns proper cipher"""

        message = '411 Project'
        # in bytes
        key = b'This is a key123'
        IV = b'This is an IV123'

        # instantiation
        encryptObj = AESEncrypt(key, IV)
        check_cipher = encryptObj.encrypt(message)
        expected_cipher = b'z\x03\xc9O\xc9\xa4\xa4\x80q\xf2\xec\x96\x03\n\xda\xe4'
        # test
        self.assertEqual(expected_cipher, check_cipher)
