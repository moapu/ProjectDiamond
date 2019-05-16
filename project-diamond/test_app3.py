# Project: app3 unittest
# Purpose Details: tests all methods of app3
# Course: IST 411
# Date Developed: 10/3/2018
# Last Date Changed: 10/28/2018
# Rev:
# ----------------------------

import unittest

from app3 import App3


# import example
# from mock import patch, call


class TestApp3(unittest.TestCase):

    def test_returnPayloadAndHash(self):
        """ tests if the return value is a tuple """

        app3 = App3()
        returnType = type(app3.return_payload_and_hash())
        self.assertEqual(returnType, tuple)

    def test_transformPayloadToBytes(self):
        """ tests if the bytes returned is same """

        dictPayload = {'name': 'apu'}
        bytePayload = bytes(str(dictPayload), 'utf-8')

        # test
        app3 = App3()
        returnAsByte = app3.transform_payload_to_bytes(dictPayload)
        self.assertEqual(returnAsByte, bytePayload)

    def test_computedHash(self):
        """  tests if returned hash is same as computed hash """

        import hmac
        import hashlib
        key = b'team4_secret_key'
        data = b'data'
        sha256 = hmac.new(key, data, hashlib.sha256).hexdigest()

        # test
        app3 = App3()
        returnHash = app3.computed_hash(data)
        self.assertEqual(returnHash, sha256)

    def test_verifyHash(self):
        """  tests if both hash matches """

        import hmac
        import hashlib
        key = b'team4_secret_key'
        data = b'data'
        a = hmac.new(key, data, hashlib.sha256).hexdigest()
        b = hmac.new(key, data, hashlib.sha256).hexdigest()

        # test
        app3 = App3()
        returnValue = app3.verify_hash(a, b)
        self.assertTrue(returnValue)

    # def build_message(sender, recipients, subject, body):
    #     msg = MIMEText(body)
    #     msg['Subject'] = subject
    #     msg['From'] = sender
    #     msg['To'] = ",".join(recipients)
    #
    #     return msg
    #
    # def send_message(msg):
    #     s = smtplib.SMTP("smtp.mydomain.com")
    #     result = s.sendmail(msg["From"], msg["To"].split(","), msg.as_string())
    #     s.quit()
    #
    #     return result
    #
    # def test_emailPayload(self):
    #     thread_num = 44
    #     body = 'this is a test 123'
    #     subject = 'this is a test 123'
    #     fromAddr = 'thdh@aol.com'
    #     toAddr = 'addr@aol.com'
    #     test_payload = ''
    #
    #     msg = MIMEText(body)
    #     msg['Subject'] = ('Project Diamond: %s %d' % (subject, thread_num))
    #     msg['From'] = fromAddr
    #     msg['To'] = toAddr
    #
    #     # Call App3 email_payload method
    #     sendmail = App3().email_payload(thread_num, body, subject, toAddr, fromAddr)
    #
    #     # self.assertEqual(msg, sendmail)
    #     self.assertEqual('Project Diamond: ' + subject + ' ' + str(thread_num), sendmail['subject'])
    #     self.assertEqual(fromAddr, sendmail['From'])
    #     self.assertEqual(toAddr, sendmail['To'])

    # def test_send_email(self):
    #     # Mock 'smtplib.SMTP' class
    #     with patch("smtplib.SMTP") as mock_smtp:
    #         # Build test message
    #         from_address = "from@domain.com"
    #         to_address = "to@domain.com"
    #
    #         msg = example.build_message(
    #             from_address, [to_address], "subject", "message")
    #
    #         # Send message
    #         example.send_message(msg)

# if __name__ == '__main__':
#     SendEmailTests().test_emailPayload()
#     # SendEmailTests().test_send_email()
