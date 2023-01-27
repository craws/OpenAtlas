from flask import url_for

from openatlas import app
from tests.base import TestBaseCase, insert


class ModelTests(TestBaseCase):

    def test_model(self) -> None:
        with app.app_context():

            rv = self.app.get(url_for('openatlas_class_index'))
            assert b'Involvement' in rv.data

            rv = self.app.get(url_for('cidoc_class_index'))
            assert b'E1' in rv.data

            rv = self.app.get(url_for('property_index'))
            assert b'P1' in rv.data

            rv = self.app.post(
                url_for('model_index'),
                data={
                    'cidoc_domain': 'E1',
                    'cidoc_range': 'E1',
                    'cidoc_property': 'P13'})
            assert b'Wrong domain' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                actor = insert('person', 'King Arthur')
                event = insert('activity', 'Battle of Camlann')
                source = insert('source', 'The source')
                event.link('P11', actor)
                source.link('P67', event)

            rv = self.app.get(url_for('model_network', dimensions=2))
            assert b'Show orphans' in rv.data

            rv = self.app.get(url_for('model_network'))
            assert b'Show orphans' in rv.data

            rv = self.app.post(
                url_for('model_network'),
                data={
                    'orphans': True,
                    'width': 100,
                    'height': 40,
                    'distance': -666,
                    'charge': 500})
            assert b'666' in rv.data

            rv = self.app.get(url_for('class_entities', code='E21'))
            assert b'King Arthur' in rv.data

            self.app.get('/index/setlocale/de')

            rv = self.app.get(url_for('cidoc_class_view', code='E18'))
            assert b'Materielles' in rv.data

            rv = self.app.get(url_for('property_view', code='P166'))
            assert b'was a presence of' in rv.data
