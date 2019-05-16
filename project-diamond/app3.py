# Project: Email Server
# Purpose Details: To create a Server to send and receive JSON payloads over SMTP
# Course: IST-411-001
# Date Developed: 10.09.18
# Last Date Changed: 11.07.18
# Rev: 1.0.3
# ===========================
import hashlib
import hmac
import json
import logging
import smtplib
import threading
from email.mime.text import MIMEText

import Pyro4
import time
import zlib
from log4mongo.handlers import MongoHandler

# === PYTHON LOGGER ===
logger = logging.getLogger("app2")
handler = MongoHandler(host='localhost', database_name='db_group4', collection='log_group4', port=27017)
logger.addHandler(handler)
FORMAT = '[%(asctime)s][%(levelname)s][%(module)s][%(funcName)s][line:%(lineno)d] %(message)s'
datestr = "%m/%d/%Y %I:%M:%S %p"
logging.basicConfig(format=FORMAT, datefmt=datestr, level=logging.DEBUG)


class App3:

    def __init__(self):
        self.__from_address = '411fa18team4@psu.edu'
        self.__to_addresses = ['something@psu.edu']
        self.__subject = 'TEAM 4'

    def email_payload(self, i, body, subject, to_address, from_address):
        """
        Build the message header

        :param i:
        :param body: body of the email
        :param subject: subject of the email
        :param to_address: address to send the email to
        :param from_address: where the email is sent from
        :rtype: object
        """

        msg = MIMEText(body)
        msg['Subject'] = ('Project Diamond: %s' % subject)
        msg['From'] = from_address
        msg['To'] = to_address
        return msg

    def server_thread(self, to_address, payload, i):
        """
        sends msg to the group members

        :param to_address: address to send the email to
        :param payload: payload that will be sent
        :param i:
        """

        logger.info("starting EmailServer Thread# %s" % to_address)

        try:
            # Connect to the SMTP_SSL server
            s = smtplib.SMTP_SSL('authsmtp.psu.edu', 465)

            # msg body
            payloadFormatter = json.dumps(payload, indent=4)
            msg = self.email_payload(i, payloadFormatter, self.__subject, to_address,
                                     self.__from_address)
            s.sendmail(self.__from_address, [to_address], str(msg))

            logger.info("Hurray we sent a message! %s on thread# %d" % (to_address, i))

        except Exception as e:
            logger.debug("server socket.timeout: %s" % e.args[0])

        # sleeps
        time.sleep(5)
        logger.info("Fin EmailServer Thread# %s" % to_address)

    def thread_changing(self, payload):
        """
        retrieve the threads change number

        :param payload: payload that will be sent
        :rtype: object
        """

        logger.info("thread changing")

        i = 0
        for to_address in self.__to_addresses:
            t = threading.Thread(target=self.server_thread(to_address, payload, i))
            t.start()
            i += 1

    def return_payload_and_hash(self):
        """ open & retrieve the json data """

        file = open('group4_payload_hash.json', 'r')
        json_data = json.load(file)
        file_hash = json_data.pop('sha256')
        file.close()
        return json_data, file_hash

    def transform_payload_to_bytes(self, payload_from_file):
        """
        transforms file json to bytes

        :param payload_from_file: retrieved payload from the file
        :rtype: bytes
        """

        str_payload = str(payload_from_file)
        byte_payload = bytes(str_payload, 'utf-8')
        return byte_payload

    def computed_hash(self, bytes_json):
        """
        computes the new hash

        :param bytes_json: json data in bytes form
        :rtype: str
        """

        key = b'team4_secret_key'
        sha256 = hmac.new(key, bytes_json, hashlib.sha256)
        hash = sha256.hexdigest()
        return hash

    def verify_hash(self, a, b):
        """
        compares the hash

        :param a: first hash
        :param b: second hash
        :rtype: str
        """

        return hmac.compare_digest(a, b)

    def compress(self, data):
        """
        uses compression to compress the json object

        :param data :
        :rtype: bytes

        """
        logger.info("size of data before compression" + str(len(data)))
        compress_data = zlib.compress(data)
        logger.info("size of data after compression" + str(len(compress_data)))
        return compress_data

    def pyro_send(self, jsonObj):
        """
        uses Pyro4 to send payload to app4

        :param jsonObj:
        :rtype: object
        """

        try:
            obj = json.dumps(jsonObj)
            compress_obj = self.compress(str.encode(obj))
            s = Pyro4.Proxy("PYRONAME:ist411.group4")
            logger.info(s.get_message(obj))

        except Exception as e:
            logger.debug("Execution exception: %s" % e.args[0])

    def main(self):
        """
        Launches main hashing calls and dispatches email threads
        :rtype: object
        """

        logger.info("getting payload and hash")
        (payload, file_hash) = self.return_payload_and_hash()

        logger.info("transforming payload to bytes")
        bytes_payload = self.transform_payload_to_bytes(payload)

        logger.info("computing the new hash")
        computed_hash = self.computed_hash(bytes_payload)

        logger.info("verifying hash")
        is_match = self.verify_hash(file_hash, computed_hash)

        logger.info("From file: %s" % file_hash)
        logger.info("Computed:  %s" % computed_hash)

        if is_match:
            logger.info("HASH Check: %s" % '\n*** MATCH ***')
        else:
            logger.info("HASH Check: %s" % '\n*** NO MATCH ***')

        logger.info("verifying hash")
        self.thread_changing(payload)

        logger.info("sending to app4 thru Pyro")
        self.pyro_send(payload)


if __name__ == "__main__":
    app3 = App3()
    app3.main()
