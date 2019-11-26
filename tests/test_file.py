import os

from flask import url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from tests.base import TestBaseCase


class FileTest(TestBaseCase):

    def test_event(self) -> None:
        with app.app_context():
            self.login()

            # Create entities for file
            with app.test_request_context():
                app.preprocess_request()
                actor = EntityMapper.insert('E21', 'File keeper')
                reference = EntityMapper.insert('E31', 'Ancient Books', 'edition')

            # Insert
            rv = self.app.get(url_for('file_insert', origin_id=actor.id))
            assert b'+ File' in rv.data

            with open(os.path.dirname(__file__) + '/../openatlas/static/images/layout/logo.png',
                      'rb') as img:
                rv = self.app.post(url_for('file_insert', origin_id=actor.id),
                                   data={'name': 'OpenAtlas logo', 'file': img},
                                   follow_redirects=True)
            assert b'An entry has been created' in rv.data
            with open(os.path.dirname(__file__) + '/../openatlas/static/images/layout/logo.png',
                      'rb') as img:
                rv = self.app.post(url_for('file_insert', origin_id=reference.id),
                                   data={'name': 'OpenAtlas logo', 'file': img},
                                   follow_redirects=True)
            assert b'An entry has been created' in rv.data
            with app.test_request_context():
                app.preprocess_request()
                files = EntityMapper.get_by_system_type('file')
                file_id = files[0].id
                file_id2 = files[1].id

            # Logo
            rv = self.app.get(url_for('admin_logo'))
            assert b'Change logo' in rv.data
            rv = self.app.post(url_for('admin_logo'), data={'file': file_id}, follow_redirects=True)
            assert b'Remove logo' in rv.data
            with self.app.get(url_for('display_logo', filename=str(file_id) + '.png')):
                pass   # Calling with "with" to prevent unclosed files warning
            rv = self.app.get(url_for('admin_logo', action='remove'), follow_redirects=True)
            assert b'Change logo' in rv.data

            with open(os.path.dirname(__file__) + '/test_file.py', 'rb') as invalid_file:
                rv = self.app.post(url_for('file_insert', origin_id=actor.id),
                                   data={'name': 'Invalid file', 'file': invalid_file},
                                   follow_redirects=True)
            assert b'File type not allowed' in rv.data

            rv = self.app.post(url_for('file_insert', origin_id=actor.id), follow_redirects=True,
                               data={'name': 'This is not a file'})
            assert b'This field is required' in rv.data

            # View
            rv = self.app.get(url_for('entity_view', id_=file_id))
            assert b'OpenAtlas logo' in rv.data
            rv = self.app.get(url_for('entity_view', id_=file_id2))
            assert b'OpenAtlas logo' in rv.data

            with self.app.get(url_for('download_file', filename=str(file_id) + '.png')):
                pass  # Calling with "with" to prevent unclosed files warning
            with self.app.get(url_for('display_file', filename=str(file_id) + '.png')):
                pass  # Calling with "with" to prevent unclosed files warning

            # Index
            rv = self.app.get(url_for('file_index'))
            assert b'OpenAtlas logo' in rv.data

            # Set and unset as main image
            self.app.get(url_for('file_set_as_profile_image', id_=file_id, origin_id=actor.id),
                         follow_redirects=True)
            self.app.get(url_for('file_remove_profile_image', entity_id=actor.id))

            # Add to file
            rv = self.app.get(url_for('file_add_reference', id_=file_id))
            assert b'Add Reference' in rv.data
            rv = self.app.post(url_for('file_add_reference', id_=file_id),
                               data={'reference': reference.id, 'page': '777'},
                               follow_redirects=True)
            assert b'777' in rv.data

            # Update
            rv = self.app.get(url_for('file_update', id_=file_id))
            assert b'OpenAtlas logo' in rv.data
            rv = self.app.post(url_for('file_update', id_=file_id), data={'name': 'Updated file'},
                               follow_redirects=True)
            assert b'Changes have been saved' in rv.data and b'Updated file' in rv.data

            rv = self.app.get(url_for('file_add', id_=file_id, class_name='actor'))
            assert b'Add Actor' in rv.data
            rv = self.app.post(url_for('file_add', id_=file_id, class_name='actor'),
                               data={'checkbox_values': [actor.id]}, follow_redirects=True)
            assert b'File keeper' in rv.data

            # Delete
            rv = self.app.get(url_for('file_delete', id_=file_id), follow_redirects=True)
            assert b'The entry has been deleted' in rv.data
