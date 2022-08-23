import pathlib
import unittest
from typing import Any, Optional, Union

import psycopg2

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.reference_system import ReferenceSystem


class TestBaseCase(unittest.TestCase):

    def setUp(self) -> None:
        app.testing = True
        app.config['SERVER_NAME'] = 'local.host'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_METHODS'] = []  # Disable CSRF in tests

        self.setup_database()
        self.app = app.test_client()
        self.login()  # Login on default because needed almost everywhere
        with app.app_context():
            self.app.get('/')  # Needed to initialise g
            self.precision_geonames = \
                'reference_system_precision_' + \
                str(ReferenceSystem.get_by_name('GeoNames').id)
            self.precision_wikidata = \
                'reference_system_precision_' + \
                str(ReferenceSystem.get_by_name('Wikidata').id)

    def login(self) -> None:
        with app.app_context():
            self.app.post(
                '/login',
                data={'username': 'Alice', 'password': 'test'})

    @staticmethod
    def setup_database() -> None:
        connection = psycopg2.connect(
            database=app.config['DATABASE_NAME'],
            host=app.config['DATABASE_HOST'],
            user=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASS'],
            port=app.config['DATABASE_PORT'])
        connection.autocommit = True
        cursor = connection.cursor()
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
                cursor.execute(sql_file.read())


def insert_entity(
        name: str,
        class_: str,
        description: Optional[str] = None,
        origin: Optional[Entity] = None) -> Entity:
    entity = Entity.insert(class_, name, description)
    if class_ in ['artifact', 'feature', 'place', 'stratigraphic_unit']:
        entity.link(
            'P53',
            Entity.insert('object_location', f'Location of {name}'))
        if origin:
            origin.link('P46', entity)
    return entity


def get_bool(
        data: dict[str, Any], key: str,
        value: Optional[Union[str, list[Any]]] = None) -> bool:
    return bool(data[key] == value) if value else bool(data[key])


def get_bool_inverse(data: dict[str, Any], key: str) -> bool:
    return bool(not data[key])


def get_no_key(data: dict[str, Any], key: str) -> bool:
    return bool(key not in data.keys())


def get_geom_properties(geom: dict[str, Any], key: str) -> bool:
    return bool(geom['features'][0]['properties'][key])


def get_class_mapping(data: list[dict[str, Any]]) -> bool:
    return bool(data[0]['systemClass']
                and data[0]['crmClass']
                and data[0]['view']
                and data[0]['icon']
                and data[0]['en'])
