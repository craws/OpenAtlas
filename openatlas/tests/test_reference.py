from flask import url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.test_base import TestBaseCase


class ReferenceTest(TestBaseCase):

    def test_reference(self):

        with app.app_context():
            self.login()

            # Reference insert
            rv = self.app.get(url_for('reference_insert', code='bibliography'))
            assert b'+ Bibliography' in rv.data
            rv = self.app.get(url_for('reference_insert', code='edition'))
            assert b'+ Edition' in rv.data
            rv = self.app.get(url_for('reference_insert', code='carrier'))
            assert b'+ Carrier' in rv.data
            data = {'name': 'Test reference', 'description': 'Reference description'}
            rv = self.app.post(url_for('reference_insert', code='bibliography'), data=data)
            bibliography_id = rv.location.split('/')[-1]
            data['continue_'] = 'yes'
            rv = self.app.post(
                url_for('reference_insert', code='carrier'), data=data, follow_redirects=True)
            assert b'An entry has been created' in rv.data
            rv = self.app.get(url_for('reference_index'))

            # Reference update
            assert b'Test reference' in rv.data
            rv = self.app.get(url_for('reference_update', id_=bibliography_id))
            assert b'Test reference' in rv.data
            data['name'] = 'Test reference updated'
            rv = self.app.post(
                url_for('reference_update', id_=bibliography_id), data=data, follow_redirects=True)
            assert b'Test reference updated' in rv.data

            # Reference link
            with app.test_request_context():
                app.preprocess_request()
                batman = EntityMapper.insert('E21', 'Batman')
            rv = self.app.get(url_for('reference_add', origin_id=batman.id))
            assert b'Batman' in rv.data
            rv = self.app.post(
                url_for('reference_add', origin_id=batman.id),
                data={'reference': bibliography_id},
                follow_redirects=True)
            assert b'Test reference updated' in rv.data

            rv = self.app.get(
                url_for('reference_add2', reference_id=bibliography_id, class_name='actor'))
            assert b'Batman' in rv.data
            rv = self.app.post(
                url_for('reference_add2', reference_id=bibliography_id, class_name='actor'),
                data={'actor': batman.id},
                follow_redirects=True)
            assert b'Test reference updated' in rv.data

            # Reference link update
            with app.test_request_context():
                app.preprocess_request()
                link_id = batman.get_links('P67', True)[0].id
                file_id = EntityMapper.insert('E31', 'The X-Files', 'file').id
                LinkMapper.insert(file_id, 'P67', int(bibliography_id))
            rv = self.app.post(url_for(
                'reference_link_update',
                link_id=link_id,
                origin_id=bibliography_id), data={'page': '666'}, follow_redirects=True)
            assert b'Changes have been saved' in rv.data

            # Reference unlink
            rv = self.app.get(url_for('reference_view', id_=bibliography_id, unlink_id=batman.id))
            assert b'removed'in rv.data and b'The X-Files' in rv.data

            # Reference delete
            rv = self.app.get(
                url_for('reference_delete', id_=bibliography_id), follow_redirects=True)
            assert b'The entry has been deleted.' in rv.data
