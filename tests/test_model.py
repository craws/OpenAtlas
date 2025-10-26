from flask import url_for

from openatlas import app
from tests.base import TestBaseCase, insert


class ModelTests(TestBaseCase):

    def test_model(self) -> None:

        return  # Todo: continue tests

        c = self.client
        rv = c.get(url_for('openatlas_class_index'))
        assert b'Involvement' in rv.data

        rv = c.get(url_for('cidoc_class_index'))
        assert b'E1' in rv.data

        rv = c.get(url_for('property_index'))
        assert b'P1' in rv.data

        rv = c.post(
            url_for('model_index'),
            data={'domain': 'E1', 'range': 'E1', 'property': 'P13'})
        assert b'Wrong domain' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            actor = insert('person', 'King Arthur')
            event = insert('activity', 'Battle of Camlann')
            event.link('P11', actor)
            source = insert('source', 'The source')
            source.link('P67', event)
            place = insert('place', 'Camelot')
            actor.link('P74', place.get_linked_entity_safe('P53'))

        rv = c.get(url_for('network', dimensions=0, id_=place.id))
        assert b'Depth' in rv.data

        rv = c.get(url_for('network', dimensions=2))
        assert b'Show orphans' in rv.data

        rv = c.get(url_for('network', dimensions=0))
        assert b'Show orphans' in rv.data

        rv = c.post(
            url_for('network', dimensions=0),
            data={
                'orphans': True,
                'width': 100,
                'height': 40,
                'distance': -666,
                'charge': 500})
        assert b'666' in rv.data

        rv = c.get(url_for('class_entities', code='E21'))
        assert b'King Arthur' in rv.data

        c.get('/index/setlocale/de')
        rv = c.get(url_for('cidoc_class_view', code='E18'))
        assert b'Materielles' in rv.data

        rv = c.get(url_for('property_view', code='P166'))
        assert b'was a presence of' in rv.data
