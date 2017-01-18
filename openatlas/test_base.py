import os
import unittest
from openatlas import app, get_cursor


class TestBaseCase(unittest.TestCase):
    @staticmethod
    def setup_database():
        with open(os.path.dirname(__file__) + '/../install/structure.sql', 'r') as sqlFile:
            sql = sqlFile.read()
            cursor = get_cursor()
            cursor.execute(sql)

    def setUp(self):
        self.setup_database()
        self.app = app.test_client()

    def tearDown(self):
        pass
