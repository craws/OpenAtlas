import pathlib
import unittest
from typing import Optional

import psycopg2
from flask import g

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.type import Type


class TestBaseCase(unittest.TestCase):

    def setUp(self) -> None:
        app.testing = True
        app.config['SERVER_NAME'] = 'local.host'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_METHODS'] = []  # Disable CSRF in tests
        self.setup_database()
        self.app = app.test_client()
        self.login()  # Login on default because needed almost everywhere
        self.prepare_reference_system_form_data()

    def login(self) -> None:
        with app.app_context():
            self.app.post(
                '/login',
                data={'username': 'Alice', 'password': 'test'})

    def setup_database(self) -> None:
        connection = psycopg2.connect(
            database=app.config['DATABASE_NAME'],
            host=app.config['DATABASE_HOST'],
            user=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASS'],
            port=app.config['DATABASE_PORT'])
        connection.autocommit = True
        self.cursor = connection.cursor()
        for file_name in [
                '1_structure',
                '2_data_model',
                '3_data_web',
                '4_data_type',
                'data_test']:
            with open(
                    pathlib.Path(app.root_path).parent / 'install' /
                    f'{file_name}.sql',
                    encoding='utf8') as sql_file:
                self.cursor.execute(sql_file.read())

    def prepare_reference_system_form_data(self) -> None:
        with app.app_context():
            self.app.get('/')  # Needed to initialise g
            self.alice_id = 2
            self.precision_type = \
                Type.get_hierarchy('External reference match')
            self.geonames = \
                f'reference_system_id_{g.reference_system_geonames.id}'
            self.wikidata = \
                f'reference_system_id_{g.reference_system_wikidata.id}'


class ApiTestCase(TestBaseCase):

    def setUp(self) -> None:
        super().setUp()
        with open(
                pathlib.Path(app.root_path).parent / 'install' /
                'data_test_api.sql',
                encoding='utf8') as sql_file:
            self.cursor.execute(sql_file.read())


def insert_entity(
        name: str,
        class_: str,
        description: Optional[str] = None) -> Entity:
    entity = Entity.insert(class_, name, description)
    if class_ in ['artifact', 'feature', 'place', 'stratigraphic_unit']:
        entity.link(
            'P53',
            Entity.insert('object_location', f'Location of {name}'))
    return entity
