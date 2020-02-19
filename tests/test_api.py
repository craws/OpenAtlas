from flask import url_for

from openatlas import app
from tests.base import TestBaseCase


class ApiTests(TestBaseCase):

    def test_api(self) -> None:
        with app.app_context():  # type: ignore
            self.login()
            rv = self.app.post(url_for('place_insert'),
                               data={'name': 'Nostromos',
                                     'description': 'In space, no one can hears you scream'})
            place_id = rv.location.split('/')[-1]

            rv = self.app.get(url_for('api_index'))
            assert b'Test API' in rv.data
            rv = self.app.get(url_for('api_entity', id_=place_id))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('api_get_by_code', code='place'))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('api_get_by_class', class_code='E18'))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('api_get_latest', limit=10))
            assert b'Nostromos' in rv.data
