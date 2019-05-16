# Project: app1 implementation
# Purpose Details: sends a payload to app2 gathered from the internet
# Course: IST 411
# Date Developed: 10/3/2018
# Last Date Changed: 10/3/2018
# Rev:
# ----------------------------
import json
import logging
import socket
import ssl
import urllib.error
import urllib.parse
import urllib.request

import pika
from Crypto.Cipher import AES
from log4mongo.handlers import MongoHandler

# === PYTHON LOGGER ===
logger = logging.getLogger("app2")
handler = MongoHandler(host='localhost', database_name='db_group4', collection='log_group4', port=27017)
logger.addHandler(handler)
FORMAT = '[%(asctime)s][%(levelname)s][%(module)s][%(funcName)s][line:%(lineno)d] %(message)s'
datestr = "%m/%d/%Y %I:%M:%S %p"
logging.basicConfig(format=FORMAT, datefmt=datestr, level=logging.DEBUG)

"""Key and IV if needed"""
key = b'This is a key 23'
some_string = b'This is an iv456'


class AesDecrypt:

    def __init__(self, key, iv_string):
        self.__key = key
        self.__iv_string = iv_string

    # I do not think we need to write to a file

    def get_file(self):
        with open('encryptedfile.aes', 'rb') as f:
            data = f.read()
            return data

    def decrypt(self, ciphertext):
        aes = AES.new(self.__key, AES.MODE_CBC, self.__iv_string)
        plaintext = aes.decrypt(ciphertext)
        return plaintext


class App1:

    def __init__(self, host='localhost', port=9091):
        self.__host = host
        self.__port = port
        self.__url = "https://jsonplaceholder.typicode.com"
        self.__param = "/posts/1"

    def get_payload(self):
        """ Gets a payload from the url and returns it """

        response = urllib.request.urlopen(self.__url + self.__param)
        payload = response.read()
        return payload

    def write_payload(self, payload):
        """ writes the payload to a file """

        decoded_payload = json.loads(payload.decode('utf-8'))
        with open('serverSentInfo', 'w') as outFile:
            outFile.write(json.dumps(decoded_payload))
            return True

    def rabbit_receive(self):
        """connects to a queue using RabbitMQ and waits for message from app4"""

        try:
            print("Connecting to Localhost Queue")
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()
            print("Queue diamond created")
            channel.queue_declare(queue='diamond')

            def callback(ch, method, properties, body):

                print("STUFF: ", len(body) % 16)
                print(" [x] Received %r" % body)
                received_value_to_bytes = body
                decrypt = AesDecrypt(key, some_string)
                decrypted_data = decrypt.decrypt(received_value_to_bytes)
                print(decrypted_data)

            channel.basic_consume(callback, queue='diamond', no_ack=True)
            print(' [*] Waiting for message from app4. To exit press CTRL+C')
            channel.start_consuming()
            connection.close()


        except Exception as e:
            print(e)

    def main(self):
        """ MAIN """

        try:
            logger.info("setting up socket")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_sock = ssl.wrap_socket(client_socket, ca_certs="server.crt", cert_reqs=ssl.CERT_REQUIRED)
            ssl_sock.connect((self.__host, self.__port))

            logger.info("Getting a payload from URL")
            client_json = self.get_payload()

            logger.info("sending data")
            ssl_sock.sendall(client_json)

            logger.info("saving to file")
            self.write_payload(client_json)
            client_socket.close()

        except Exception as e:
            logger.debug("Execution exception: %s" % e.args[0])


if __name__ == '__main__':
    app1 = App1()
    app1.main()
    app1.rabbit_receive()
