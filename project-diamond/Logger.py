# Project: app1 implementation
# Purpose Details:
#       app2will receive the secure payload from app1 using TLS.
#       All workflow actions pass or fail will be logged into
#       the activity MongoDB NoSQL database with a timestamp.
#       Unit tests will confirm all methods are functional.
# Course: IST 411
# Date Developed: 10/3/2018
# Last Date Changed: 10/3/2018
# Rev:
# ----------------------------
import sys

from pymongo import MongoClient


class Logger:

    def __init__(self):
        # connect to mongoDB
        self.__client = MongoClient('localhost', 27017)
        self.__db = self.__client.db_group4
        self.__collection = self.__db.log_group4

    def display_log(self):
        """
        displays the log file in MongoDB
        """

        try:
            cursor = self.__collection.find({})
            for document in cursor:
                print(f"{document['timestamp']} "
                      f"[{document['level']}]"
                      f"[{document['fileName']}]"
                      f"[{document['method']}]"
                      f"[Line:{document['lineNumber']}]"
                      f" {document['message']} ")

        except:
            e = sys.exc_info()[0]
            print("error: %s" % e)


if __name__ == '__main__':
    logger = Logger()
    logger.display_log()
