# Project: app1 testing
# Purpose Details: app1 unittest
# Course: IST 411
# Date Developed: 10/3/2018
# Last Date Changed: 10/3/2018
# Rev:
# ----------------------------

import unittest
import urllib.request

from app1 import AesDecrypt
from app1 import App1


class TestApp1(unittest.TestCase):

    def test_send_payload(self):
        """
        Test the send_payload method from App1
        returns a byte-type object
        """

        # instance of App1
        app1_instance = App1()
        app1_json = app1_instance.get_payload()

        # retrieve json from url
        url = "https://jsonplaceholder.typicode.com/posts/1"
        response = urllib.request.urlopen(url)
        payload = response.read()

        # test
        self.assertEqual(app1_json, payload)

    def test_write_payload(self):
        """
        Test the write_payload method from App1
        """

        # retrieve json from url
        url = "https://jsonplaceholder.typicode.com/posts/1"
        response = urllib.request.urlopen(url)
        payload = response.read()

        # instance of App1
        app1_instance = App1()
        bool_result = app1_instance.write_payload(payload)

        # test that the file was written
        self.assertTrue(bool_result)

    def test_decrypt(self):
        """
        Passes if cipher returns proper message
        """

        cipher = b'z\x03\xc9O\xc9\xa4\xa4\x80q\xf2\xec\x96\x03\n\xda\xe4'
        # in bytes
        key = b'This is a key123'
        IV = b'This is an IV123'

        # instantiation
        decryptObj = AesDecrypt(key, IV)
        decrypted_message = str(decryptObj.decrypt(cipher), 'utf-8').strip()
        expected_message = '411 Project'
        # test
        self.assertEqual(expected_message, decrypted_message)
