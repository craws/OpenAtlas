from flask import url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.test_base import TestBaseCase


class ReferenceTest(TestBaseCase):

    def test_reference(self) -> None:

        with app.app_context():
            self.login()

            # Reference insert
            rv = self.app.get(url_for('reference_insert', code='bibliography'))
            assert b'+ Bibliography' in rv.data
            rv = self.app.get(url_for('reference_insert', code='edition'))
            assert b'+ Edition' in rv.data
            data = {'name': 'https://openatlas.eu', 'description': 'Reference description'}
            rv = self.app.post(url_for('reference_insert', code='external_reference'), data=data)
            with app.test_request_context():
                app.preprocess_request()
                reference = EntityMapper.get_by_id(rv.location.split('/')[-1])
            data['continue_'] = 'yes'
            rv = self.app.post(url_for('reference_insert', code='external_reference'),
                               data=data, follow_redirects=True)
            assert b'An entry has been created' in rv.data
            rv = self.app.get(url_for('reference_index'))
            assert b'https://openatlas.eu' in rv.data

            # Reference update
            rv = self.app.get(url_for('reference_update', id_=reference.id))
            assert b'https://openatlas.eu' in rv.data
            data['name'] = 'http://updated.openatlas.eu'
            rv = self.app.post(url_for('reference_update', id_=reference.id), data=data,
                               follow_redirects=True)
            assert b'http://updated.openatlas.eu' in rv.data

            # Reference link
            with app.test_request_context():
                app.preprocess_request()
                batman = EntityMapper.insert('E21', 'Batman')
            rv = self.app.get(url_for('reference_add', id_=reference.id, class_name='actor'))
            assert b'Batman' in rv.data
            rv = self.app.post(url_for('reference_add', id_=reference.id, class_name='actor'),
                               data={'actor': batman.id}, follow_redirects=True)
            assert b'http://updated.openatlas.eu' in rv.data

            # Reference link update
            with app.test_request_context():
                app.preprocess_request()
                link_id = batman.get_links('P67', True)[0].id
                file = EntityMapper.insert('E31', 'The X-Files', 'file')
                file.link('P67', reference)
            rv = self.app.post(
                url_for('reference_link_update', link_id=link_id, origin_id=reference.id),
                data={'page': '666'}, follow_redirects=True)
            assert b'Changes have been saved' in rv.data

            # Reference delete
            rv = self.app.get(url_for('reference_delete', id_=reference.id),
                              follow_redirects=True)
            assert b'The entry has been deleted.' in rv.data
