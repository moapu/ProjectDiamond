# Project: app2 unittest
# Purpose Details: tests all methods of app2
# Course: IST 411
# Date Developed: 10/3/2018
# Last Date Changed: 10/24/2018
# Rev:
# ----------------------------
import unittest

from app2 import App2


class TestApp2(unittest.TestCase):

    def test_hash_data(self):
        """ Test will succeed if it returns True """

        # in bytes
        json_msg = b'{"GeeksforGeeks":"dsda"}'

        # instantiation
        app2 = App2()
        hash_returned = app2.hash_data(json_msg)

        # test
        self.assertTrue(hash_returned)

    def test_save_hash_to_disk(self):
        """ Test will succeed if it returns True """

        import os
        import hmac
        import hashlib

        # in bytes
        json_msg = b'{"name": "mo"}'
        key = b'team4_secret_key'

        # hash
        sha256 = hmac.new(key, json_msg, hashlib.sha256).hexdigest()

        # instantiation
        app2 = App2()
        return_value = app2.save_file(json_msg, sha256)

        # test
        exists = os.path.isfile('group4_payload_hash.json')
        self.assertTrue(exists)

    def test_send_to_app3(self):
        """ Test will fail if it returns 'error' """

        # instantiation
        app2 = App2()
        return_value = app2.send_to_app3()
        self.assertFalse(str(return_value).__contains__("error"))
