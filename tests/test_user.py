from typing import Any

from flask import g, url_for

from openatlas import app
from tests.base import TestBaseCase, insert_entity


class UserTests(TestBaseCase):

    def test_user(self) -> None:

        with app.app_context():
            rv: Any = self.app.get(url_for('user_insert'))
            assert b'+ User' in rv.data

            data = {
                'active': '',
                'username': 'Ripley',
                'email': 'ripley@nostromo.org',
                'password': 'you_never_guess_this',
                'password2': 'you_never_guess_this',
                'group': 'admin',
                'name': 'Ripley Weaver'}
            rv = self.app.post(url_for('user_insert'), data=data)
            user_id = rv.location.split('/')[-1]
            data['password'] = 'too short'
            rv = self.app.post(url_for('user_insert'), data=data)
            assert b'match' in rv.data

            rv = self.app.post(
                url_for('user_insert'),
                data={
                    'active': '',
                    'username': 'Newt',
                    'email': 'newt@nostromo.org',
                    'password': 'you_never_guess_this',
                    'password2': 'you_never_guess_this',
                    'group': 'admin',
                    'name': 'Newt',
                    'continue_': 'yes'},
                follow_redirects=True)
            assert b'Newt' not in rv.data

            rv = self.app.get(url_for('user_view', id_=user_id))
            assert b'Ripley' in rv.data

            rv = self.app.get(url_for('user_view', id_=666))
            assert b'404' in rv.data

            rv = self.app.get(url_for('user_update', id_=self.alice_id))
            assert b'Alice' in rv.data

            data['description'] = 'The warrant officer'
            rv = self.app.post(
                url_for('user_update', id_=user_id),
                data=data,
                follow_redirects=True)
            assert b'The warrant officer' in rv.data

            rv = self.app.post(url_for('user_update', id_=1234), data=data)
            assert b'404' in rv.data

            rv = self.app.get(
                url_for('admin_index', action='delete_user', id_=user_id))
            assert b'User deleted' in rv.data

            self.app.post(
                url_for('insert', class_='bibliography'),
                data={'name': 'test', 'description': 'test'})
            rv = self.app.get(url_for('user_activity'))
            assert b'Activity' in rv.data

            rv = self.app.post(
                url_for('user_activity', user_id=user_id),
                data={'limit': 100, 'user': 0, 'action': 'all'})
            assert b'Activity' in rv.data

            rv = self.app.get(
                url_for(
                    'admin_index',
                    action='delete_user',
                    id_=self.alice_id))
            assert b'403 - Forbidden' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                person = insert_entity('Hugo', 'person')

            self.app.get(url_for('logout'))
            rv = self.app.get(url_for('user_insert'), follow_redirects=True)
            assert b'Forgot your password?' not in rv.data

            self.app.post(
                '/login',
                data={'username': 'Editor', 'password': 'test'})
            rv = self.app.get(url_for('user_insert'))
            assert b'403 - Forbidden' in rv.data

            rv = self.app.post(url_for('insert', class_='reference_system'))
            assert b'403 - Forbidden' in rv.data

            rv = self.app.get(
                url_for(
                    'index',
                    view='actor',
                    delete_id=g.reference_system_wikidata.id))
            assert b'403 - Forbidden' in rv.data

            self.app.get(url_for('logout'))
            self.app.post(
                '/login',
                data={'username': 'Manager', 'password': 'test'})

            rv = self.app.get(url_for('admin_settings', category='mail'))
            assert b'403 - Forbidden' in rv.data

            rv = self.app.get(url_for('user_update', id_=self.alice_id))
            assert b'403 - Forbidden' in rv.data

            self.app.get(url_for('logout'))
            self.app.post(
                '/login',
                data={'username': 'Contributor', 'password': 'test'})

            rv = self.app.get(
                url_for('index', view='actor', delete_id=person.id))
            assert b'403 - Forbidden' in rv.data
