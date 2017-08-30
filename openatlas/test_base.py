# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import os
import unittest
from openatlas import app, get_cursor


class TestBaseCase(unittest.TestCase):
    @staticmethod
    def setup_database():
        for file_name in ['structure.sql', 'data_web.sql', 'data_model.sql', 'data_node.sql', 'data_test.sql']:
            with open(os.path.dirname(__file__) + '/../install/' + file_name, 'r') as sqlFile:
                sql = sqlFile.read()
                cursor = get_cursor()
                cursor.execute(sql)

    def setUp(self):
        app.config['LANGUAGE'] = 'en'
        app.config['WHITELISTED_DOMAINS'] = 'E61'
        app.config['WTF_CSRF_ENABLED'] = False
        self.setup_database()
        self.app = app.test_client()

    def tearDown(self):
        pass

    def login(self):
        self.app.post('/login', data={'username': 'Alice', 'password': 'test'})
