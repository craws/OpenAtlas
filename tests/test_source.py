from flask import url_for

from openatlas import app
from openatlas.models.entity import Entity
from tests.base import TestBaseCase


class SourceTest(TestBaseCase):

    def test_source(self) -> None:
        with app.app_context():  # type: ignore
            self.login()

            # Source insert
            rv = self.app.get(url_for('source_insert'))
            assert b'+ Source' in rv.data
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                origin = Entity.insert('E21', 'David Duchovny')
                actor = Entity.insert('E21', 'Gillian Anderson Gillian Anderson ')
                carrier = Entity.insert('E84', 'I care for you', 'information carrier')
                file = Entity.insert('E31', 'X-Files', 'file')
                reference = Entity.insert('E31', 'https://openatlas.eu', 'external reference')

            rv = self.app.post(url_for('source_insert', origin_id=origin.id),
                               data={'name': 'Test source'}, follow_redirects=True)
            assert b'An entry has been created' in rv.data
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                source = Entity.get_by_codes('source')[0]
            rv = self.app.post(url_for('source_insert', origin_id=reference.id),
                               data={'name': 'Test source'}, follow_redirects=True)
            assert b'https://openatlas.eu' in rv.data
            rv = self.app.post(url_for('source_insert', origin_id=file.id),
                               data={'name': 'Test source'}, follow_redirects=True)
            assert b'An entry has been created' in rv.data and b'X-Files' in rv.data
            data = {'name': 'Test source', 'continue_': 'yes'}
            rv = self.app.post(url_for('source_insert'), data=data, follow_redirects=True)
            assert b'An entry has been created' in rv.data

            rv = self.app.get(url_for('source_insert', origin_id=carrier.id))
            assert b'I care for you' in rv.data
            rv = self.app.post(url_for('source_insert', origin_id=carrier.id),
                               data={'name': 'Necronomicon', 'information_carrier': [carrier.id]},
                               follow_redirects=True)
            assert b'I care for you' in rv.data

            rv = self.app.get(url_for('source_index'))
            assert b'Test source' in rv.data

            # Link source
            rv = self.app.post(url_for('reference_insert', code='external reference',
                                       origin_id=source.id),
                               data={'name': 'https://openatlas.eu'},
                               follow_redirects=True)
            assert b'Test source' in rv.data

            self.app.get(url_for('source_add', id_=source.id, origin_id=actor.id,
                                 class_name='actor'))
            rv = self.app.post(url_for('source_add', id_=source.id, class_name='actor'),
                               data={'checkbox_values': [actor.id]}, follow_redirects=True)
            assert b'Gillian Anderson' in rv.data
            rv = self.app.get(url_for('entity_view', id_=source.id))
            assert b'Gillian Anderson' in rv.data
            rv = self.app.get(url_for('source_add', id_=source.id, class_name='place'))
            assert b'Add Place' in rv.data

            # Update source
            rv = self.app.get(url_for('source_update', id_=source.id))
            assert b'Test source' in rv.data
            data = {'name': 'Source updated', 'description': 'some description'}
            rv = self.app.post(url_for('source_update', id_=source.id), data=data,
                               follow_redirects=True)
            assert b'Source updated' in rv.data
            rv = self.app.get(url_for('entity_view', id_=source.id))
            assert b'some description' in rv.data

            # Add to source
            rv = self.app.get(url_for('source_add_reference', id_=source.id))
            assert b'Add Reference' in rv.data
            rv = self.app.post(url_for('source_add_reference', id_=source.id),
                               data={'reference': reference.id, 'page': '777'},
                               follow_redirects=True)
            assert b'777' in rv.data

            # Delete source
            rv = self.app.get(url_for('source_index', action='delete', id_=source.id))
            assert b'The entry has been deleted.' in rv.data
