import os
from flask import url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.test_base import TestBaseCase


class FileTest(TestBaseCase):

    def test_event(self):
        with app.app_context():
            self.login()

            # Create entities for file
            with app.test_request_context():
                app.preprocess_request()
                actor_id = EntityMapper.insert('E21', 'File keeper').id
                reference_id = EntityMapper.insert('E31', 'Ancient Books', 'edition').id

            # Insert
            rv = self.app.get(url_for('file_insert', origin_id=actor_id))
            assert b'+ File' in rv.data

            with open(os.path.dirname(__file__) + '/../static/images/layout/logo.png', 'rb') as img:
                rv = self.app.post(
                    url_for('file_insert', code='E7', origin_id=actor_id),
                    data={'name': 'OpenAtlas logo', 'file': img}, follow_redirects=True)
            assert b'An entry has been created' in rv.data
            with open(os.path.dirname(__file__) + '/../static/images/layout/logo.png', 'rb') as img:
                rv = self.app.post(
                    url_for('file_insert', code='E7', origin_id=reference_id),
                    data={'name': 'OpenAtlas logo', 'file': img}, follow_redirects=True)
            assert b'An entry has been created' in rv.data
            with app.test_request_context():
                app.preprocess_request()
                files = EntityMapper.get_by_system_type('file')
                file_id = files[0].id
                file_id2 = files[1].id

            with open(os.path.dirname(__file__) + '/test_file.py', 'rb') as invalid_file:
                rv = self.app.post(
                    url_for('file_insert', code='E7', origin_id=actor_id),
                    data={'name': 'Invalid file', 'file': invalid_file}, follow_redirects=True)
            assert b'File type not allowed' in rv.data

            rv = self.app.post(
                url_for('file_insert', code='E7', origin_id=actor_id),
                data={'name': 'This is not a file'}, follow_redirects=True)
            assert b'This field is required' in rv.data

            # View
            rv = self.app.get(url_for('file_view', id_=file_id))
            assert b'OpenAtlas logo' in rv.data
            rv = self.app.get(url_for('file_view', id_=file_id2))
            assert b'OpenAtlas logo' in rv.data

            # Calling download, display urls with "with to prevent unclosed files warning
            with self.app.get(url_for('download_file', filename=str(file_id) + '.png')) as image:
                pass
            with self.app.get(url_for('display_file', filename=str(file_id) + '.png')) as image:
                pass

            # Index
            rv = self.app.get(url_for('file_index'))
            assert b'OpenAtlas logo' in rv.data

            # Add
            rv = self.app.get(url_for('file_add', origin_id=actor_id))
            assert b'Add File' in rv.data
            rv = self.app.post(
                url_for('file_add', origin_id=actor_id),
                data={'values': file_id}, follow_redirects=True)
            assert b'OpenAtlas logo' in rv.data

            # Update
            rv = self.app.get(url_for('file_update', id_=file_id))
            assert b'OpenAtlas logo' in rv.data
            rv = self.app.post(
                url_for('file_update', id_=file_id), data={'name': 'Updated file'},
                follow_redirects=True)
            assert b'Changes have been saved' in rv.data and b'Updated file' in rv.data

            # Unlink
            rv = self.app.get(url_for('file_view', id_=file_id, unlink_id=actor_id))
            assert b'Link removed' in rv.data

            rv = self.app.get(url_for('file_add2', id_=file_id, class_name='actor'))
            assert b'Add Actor' in rv.data
            rv = self.app.post(
                url_for('file_add2', id_=file_id, class_name='actor'),
                data={'values': actor_id}, follow_redirects=True)
            assert b'File keeper' in rv.data

            # Delete
            rv = self.app.get(url_for('file_delete', id_=file_id), follow_redirects=True)
            assert b'The entry has been deleted' in rv.data
