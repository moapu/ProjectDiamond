# Project: app2 implementation
# Purpose Details: receive the secure payload from app1 using TLS.
# Course: IST 411
# Date Developed: 10/3/2018
# Last Date Changed: 10/28/2018
# Rev:
# ----------------------------
import hashlib
import hmac
import json
import logging
import socket
import ssl

import pysftp
from log4mongo.handlers import MongoHandler

# === PYTHON LOGGER ===
logger = logging.getLogger("app2")
handler = MongoHandler(host='localhost', database_name='db_group4', collection='log_group4', port=27017)
logger.addHandler(handler)
FORMAT = '[%(asctime)s][%(levelname)s][%(module)s][%(funcName)s][line:%(lineno)d] %(message)s'
datestr = "%m/%d/%Y %I:%M:%S %p"
logging.basicConfig(format=FORMAT, datefmt=datestr, level=logging.DEBUG)


class App2:

    def __init__(self, host='localhost', port=9091):
        self.__host = host
        self.__port = port
        self.__file = 'group4_payload_hash.json'

    def start_listening(self):
        """ returns the socket and ssl_sock """

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = ssl.wrap_socket(s, server_side=True, certfile="server.crt", keyfile="server.key")
        ssl_sock.bind((self.__host, self.__port))
        ssl_sock.listen(5)
        return s, ssl_sock

    def send_to_app3(self):
        """ send file to sftp """

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        cinfo = {'cnopts': cnopts,
                 'host': 'oz-ist-linux-fa18-411',
                 'username': 'ftpuser',
                 'password': 'test1234',
                 'port': 103}

        try:
            with pysftp.Connection(**cinfo) as sftp:
                logger.info("SFTP connection made")
                try:
                    logger.info("sending the json file...")
                    sftp.put(self.__file)

                    logger.info("getting the json file...")
                    sftp.get(self.__file)

                    logger.info("Sent file to sftp")

                except Exception as e:
                    logger.debug("Execution exception: %s" % e.args[0])
                    return 'error'

        except Exception as e:
            logger.debug("Execution exception: %s" % e.args[0])
            return 'error'

    def save_file(self, data, hashed):
        """ save file to current directory """

        # add hash to data
        data_with_hash = json.loads(data.decode('utf-8'))
        data_with_hash['sha256'] = hashed

        # save to file
        outfile = open(self.__file, 'w')
        json.dump(data_with_hash, outfile)
        outfile.close()

    def hash_data(self, json_data):
        """ returns the hash in str """

        bytes_json = bytes(str(json.loads(json_data)), 'utf-8')
        key = b'team4_secret_key'
        sha256 = hmac.new(key, bytes_json, hashlib.sha256)
        return sha256.hexdigest()

    def server(self):
        """
        receives the payload
        sends the payload to app3 with hash appended
        """

        try:
            logger.info("server listening")
            (s, ssl_sock) = self.start_listening()

            while True:
                logger.info("receiving data")
                (client_socket, address) = ssl_sock.accept()
                data = client_socket.recv(4096)

                logger.info("Data received")

                # breaks if 'data' is empty
                if not data: break

                logger.info("hashing payload")
                hashed = self.hash_data(data)

                logger.info("saving hash to disk")
                self.save_file(data, hashed)

                logger.info("sending to app3")
                self.send_to_app3()

            s.close()

        except Exception as e:
            logger.debug("Execution exception: %s" % e.args[0])


if __name__ == '__main__':
    app2 = App2()
    app2.server()
