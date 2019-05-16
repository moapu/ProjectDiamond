# Project: Pyro Server
# Purpose Details: Will receive Python object from app3 using Pyro
# Course: IST-411-001
# Date Developed: 10.26.18
# Last Date Changed: 10.26.18
# Rev:1.0.3
# ===========================


import Pyro4
import pika
from Crypto.Cipher import AES


class AESEncrypt:
    def __init__(self, key, some_string):
        self.__key = key
        self.__some_string = some_string

    def encrypt(self, payload):
        pad = b' '
        plaintext = str(payload).encode('utf-8')
        length = 16 - (len(plaintext) % 16)
        plaintext += length * pad

        aes = AES.new(self.__key, AES.MODE_CBC, self.__some_string)
        cipher = aes.encrypt(plaintext)
        return cipher


class AESDecrypt:

    def __init__(self, key, iv_string):
        self.__key = key
        self.__iv_string = iv_string

    # I do not think we need to write to a file

    def get_file(self):
        with open('encryptedfile.aes', 'rb') as f:
            data = f.read()
            return data

    def decrypt(self, cipher_text):
        aes = AES.new(self.__key, AES.MODE_CBC, self.__iv_string)
        plaintext = aes.decrypt(cipher_text)
        return plaintext


@Pyro4.expose
class App4(object):

    def get_message(self, pyObj):
        """This method recieves object from app3"""
        self.rabbit_send(pyObj)
        return pyObj

    def rabbit_send(self, pyObj):
        try:
            key = b'This is a key 23'
            some_string = b'This is an iv456'
            print("Connecting to Localhost Queue")
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            print("Channel Connected")
            channel.queue_declare(queue='diamond')
            aes_encrypt = AESEncrypt(key, some_string)
            encrypted_py_obj = aes_encrypt.encrypt(pyObj)
            rabbit_payload = encrypted_py_obj
            # rabbit_payload = json.dumps(pyObj)

            decrypt = AESDecrypt(key, some_string)
            decrypted_data = decrypt.decrypt(rabbit_payload)
            print(" [x] decrypt payload to app1 using RabbitMQ %s" % decrypted_data)

            # Send json as string in the body.
            channel.basic_publish(exchange="", routing_key='diamond', body=rabbit_payload)
            print(" [x] Sent payload to app1 using RabbitMQ")
            connection.close()

        except Exception as e:
            print(e)


if __name__ == '__main__':
    try:
        # make a Pyro daemon
        daemon = Pyro4.Daemon()
        ns = Pyro4.locateNS()
        uri = daemon.register(App4)
        ns.register("ist411.group4", uri)

        print("Ready to send object using Pyro")
        daemon.requestLoop()

    except Exception as e:
        print(e)
