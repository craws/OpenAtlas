from flask import url_for

from openatlas import app
from openatlas.models.entity import Entity
from tests.base import TestBaseCase


class ObjectTest(TestBaseCase):

    def test_object(self) -> None:
        with app.app_context():  # type: ignore
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                source = Entity.insert('E33', 'Necronomicon')

            rv = self.app.get(url_for('object_insert'))
            assert b'+ Information Carrier' in rv.data
            rv = self.app.post(url_for('object_insert'), data={'name': 'Love-letter'},
                               follow_redirects=True)
            assert b'Love-letter' in rv.data
            rv = self.app.get(url_for('object_index'))
            assert b'Love-letter' in rv.data
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                object_ = Entity.get_by_menu_item('object')[0]
            rv = self.app.get(url_for('object_update', id_=object_.id))
            assert b'Love-letter' in rv.data
            rv = self.app.post(url_for('object_update', id_=object_.id), follow_redirects=True,
                               data={'name': 'A little hate',
                                     'description': 'makes nothing better'})
            assert b'Changes have been saved' in rv.data

            # Add to object
            rv = self.app.get(url_for('entity_add_source', id_=object_.id))
            assert b'Add Source' in rv.data
            rv = self.app.post(url_for('entity_add_source', id_=object_.id),
                               data={'checkbox_values': str([source.id])}, follow_redirects=True)
            assert b'Necronomicon' in rv.data

            # Add to event
            rv = self.app.get(url_for('event_insert', code='E9', origin_id=object_.id))
            assert b'A little hate' in rv.data
            rv = self.app.post(url_for('event_insert', code='E9', origin_id=object_.id),
                               data={'name': 'Event Horizon', 'object': [object_.id]},
                               follow_redirects=True)
            assert b'Event Horizon' in rv.data

            rv = self.app.get(url_for('object_index', action='delete', id_=object_.id))
            assert b'has been deleted' in rv.data
