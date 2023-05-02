import unittest
from mongoengine import connect, disconnect
import mongomock


class TestDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        connect(
            "DefiOS",
            host="mongodb://localhost",
            mongo_client_class=mongomock.MongoClient,
        )

    @classmethod
    def tearDownClass(cls):
        disconnect()
