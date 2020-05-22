from flask import url_for

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.node import Node
from tests.base import TestBaseCase


class ApiTests(TestBaseCase):

    def test_api(self) -> None:
        with app.app_context():  # type: ignore
            rv = self.app.post(url_for('place_insert'),
                               data={'name': 'Nostromos',
                                     'description': 'In space, no one can hears you scream'})
            place_id = rv.location.split('/')[-1]
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                event = Entity.insert('E8', 'Event Horizon')
                event.link('P7', Entity.get_by_id(place_id))
                place_node = Node.get_hierarchy('Place')
                place = Entity.get_by_id(place_id)
                place.link("P2", place_node)

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
            rv = self.app.get(url_for('api_entity', id_=99999999))
            assert b'not found' in rv.data
            self.app.get(url_for('logout'), follow_redirects=True)
            rv = self.app.get(url_for('api_entity', id_=place_id))
            assert b'forbidden' in rv.data


