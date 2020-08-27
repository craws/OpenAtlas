import unittest
from typing import Optional

import psycopg2
import random

from openatlas import app


def random_string(length: Optional[int] = None) -> str:
    # The idea is to test all/many unicode characters, this still needs work. One problem is that
    # strings in tables aren't found, also special chars like ' and " should be tested more often.
    # See test_event where tests for string in e.g. index table view were deactivated
    length = length if length else random.randint(1, 64)
    return ''.join(chr(random.randint(1, 10000)) for i in range(length))


class TestBaseCase(unittest.TestCase):

    def setUp(self) -> None:
        app.testing = True
        app.config['SERVER_NAME'] = 'local.host'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_METHODS'] = []  # This is the magic to disable CSRF for tests
        self.setup_database()
        self.app = app.test_client()
        self.login()  # login on default because needed almost everywhere

    def login(self) -> None:
        with app.app_context():  # type: ignore
            self.app.post('/login', data={'username': 'Alice', 'password': 'test'})

    @staticmethod
    def setup_database() -> None:
        connection = psycopg2.connect(database=app.config['DATABASE_NAME'],
                                      host=app.config['DATABASE_HOST'],
                                      user=app.config['DATABASE_USER'],
                                      password=app.config['DATABASE_PASS'],
                                      port=app.config['DATABASE_PORT'])
        connection.autocommit = True
        cursor = connection.cursor()
        for file_name in ['1_structure.sql', '2_data_web.sql', '3_data_model.sql',
                          '4_data_node.sql', 'data_test.sql']:
            path = app.config['ROOT_PATH'].joinpath('..', 'install', file_name)
            with open(path, encoding='utf8') as sqlFile:
                cursor.execute(sqlFile.read())
