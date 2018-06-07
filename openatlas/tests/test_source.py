from flask import url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.test_base import TestBaseCase


class SourceTest(TestBaseCase):

    def test_source(self):
        with app.app_context():
            self.login()

            # Source insert
            rv = self.app.get(url_for('source_insert'))
            assert b'+ Source' in rv.data
            with app.test_request_context():
                app.preprocess_request()
                origin_id = EntityMapper.insert('E21', 'David Duchovny').id
                actor_id = EntityMapper.insert('E21', 'Gillian Anderson').id
                reference_id = EntityMapper.insert('E84', 'Ancient Books', 'information carrier').id
                file_id = EntityMapper.insert('E31', 'The X-Files', 'file').id

            rv = self.app.post(url_for('source_insert', origin_id=origin_id),
                               data={'name': 'Test source'}, follow_redirects=True)
            assert b'An entry has been created' in rv.data
            with app.test_request_context():
                app.preprocess_request()
                source_id = EntityMapper.get_by_codes('source')[0].id
            rv = self.app.post(url_for('source_insert', origin_id=reference_id),
                               data={'name': 'Test source'}, follow_redirects=True)
            assert b'Ancient Books' in rv.data
            rv = self.app.post(url_for('source_insert', origin_id=file_id),
                               data={'name': 'Test source'}, follow_redirects=True)
            assert b'An entry has been created' in rv.data and b'The X-Files' in rv.data
            data = {'name': 'Test source', 'continue_': 'yes'}
            rv = self.app.post(url_for('source_insert'), data=data, follow_redirects=True)
            assert b'An entry has been created' in rv.data
            rv = self.app.get(url_for('source_index'))
            assert b'Test source' in rv.data

            # Link source
            rv = self.app.post(
                url_for('reference_insert', code='edition', origin_id=source_id),
                data={'name': 'Test reference'},
                follow_redirects=True)
            assert b'Test source' in rv.data
            self.app.get(url_for('source_add', origin_id=actor_id))
            data = {'values': source_id}
            rv = self.app.post(
                url_for('source_add', origin_id=actor_id), data=data, follow_redirects=True)
            assert b'Gillian Anderson' in rv.data

            with app.test_request_context():
                app.preprocess_request()
                link_id = LinkMapper.get_links(source_id, 'P67')[0].id
            rv = self.app.get(url_for('source_view', id_=source_id, unlink_id=link_id))
            assert b'removed'in rv.data

            self.app.get(
                url_for('source_add2', origin_id=actor_id, id_=source_id, class_name='actor'))
            rv = self.app.post(
                url_for('source_add2', id_=source_id, class_name='actor'),
                data={'values': actor_id}, follow_redirects=True)
            assert b'Gillian Anderson' in rv.data
            rv = self.app.get(url_for('source_view', id_=source_id))
            assert b'Gillian Anderson' in rv.data

            # Update source
            rv = self.app.get(url_for('source_update', id_=source_id))
            assert b'Test source' in rv.data
            data = {'name': 'Source updated', 'description': 'some description'}
            rv = self.app.post(
                url_for('source_update', id_=source_id), data=data, follow_redirects=True)
            assert b'Source updated' in rv.data
            rv = self.app.get(url_for('source_view', id_=source_id))
            assert b'some description' in rv.data

            # Delete source
            rv = self.app.get(url_for('source_delete', id_=source_id), follow_redirects=True)
            assert b'The entry has been deleted.' in rv.data
