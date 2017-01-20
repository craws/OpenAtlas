# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
import os
import unittest
from openatlas import app, get_cursor


class TestBaseCase(unittest.TestCase):
    @staticmethod
    def setup_database():
        for file_name in ['structure.sql', 'data_web.sql']:
            with open(os.path.dirname(__file__) + '/../install/' + file_name, 'r') as sqlFile:
                sql = sqlFile.read()
                cursor = get_cursor()
                cursor.execute(sql)

    def setUp(self):
        app.config['language'] = 'en'
        self.setup_database()
        self.app = app.test_client()

    def tearDown(self):
        pass
