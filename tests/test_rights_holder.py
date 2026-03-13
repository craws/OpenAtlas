from flask import url_for

from openatlas import app
from openatlas.models.rights_holder import RightsHolder
from tests.base import TestBaseCase, insert


class RightsHolderTests(TestBaseCase):

    def test_rights_holder(self) -> None:
        c = self.client
        c.post(
            url_for('login'),
            data={'username': 'Contributor', 'password': 'test'})

        # Insert
        data = {
            'name': 'Test Creator',
            'role': 'person',
            'description': 'A test creator'}
        rv = c.post(
            url_for('rights_holder_insert'),
            data=data,
            follow_redirects=True)
        assert b'An entry has been created' in rv.data
        assert b'Test Creator' in rv.data

        rv = c.post(url_for('rights_holder_insert'), data=data)
        assert b'Name-Role combination already exists' in rv.data

        data['confirm_duplicate'] = 'true'
        rv = c.post(
            url_for('rights_holder_insert'),
            data=data,
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            rights_holders = RightsHolder.get_rights_holder()
            rh_id = rights_holders[-1].id
            rh_name = rights_holders[-1].name
            person = insert('person', 'Nice person')

        rv = c.get(url_for('rights_holder_view', id_=rh_id))
        assert rh_name.encode() in rv.data

        rv = c.get(url_for('rights_holder_view', id_=9999))
        assert rv.status_code == 418
        assert b'418' in rv.data

        rv = c.post(
            url_for(
                'rights_holder_insert',
                origin_id=person.id,
                relation='creator'),
            data={
                'name': 'Test Creator 2',
                'role': 'person',
                'description': 'A second creator'},
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        rv = c.get(
            url_for('rights_holder_update', id_=rh_id),
            follow_redirects=True)
        assert b'Creator' in rv.data

        update_data = {
            'name': 'Updated Creator',
            'role': 'group',
            'description': 'An updated description'}
        rv = c.post(
            url_for('rights_holder_update', id_=rh_id),
            data=update_data,
            follow_redirects=True)
        assert b'Updated Creator' in rv.data

        rv = c.post(url_for('rights_holder_update', id_=999), data=update_data)
        assert b'404' in rv.data

        c.get(url_for('logout'))

        c.post(
            url_for('login'),
            data={'username': 'Contributor', 'password': 'test'})
        rv = c.get(url_for('rights_holder_delete', id_=rh_id))
        assert b'403 - Forbidden' in rv.data
        c.get(url_for('logout'))

        c.post(
            url_for('login'),
            data={'username': 'Editor', 'password': 'test'})
        rv = c.get(
            url_for('rights_holder_delete', id_=rh_id),
            follow_redirects=True)
        assert b'The entry has been deleted' in rv.data
