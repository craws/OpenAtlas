from typing import Any

from flask import url_for

from openatlas import app
from tests.base import TestBaseCase


class UserTests(TestBaseCase):

    def test_user(self) -> None:
        data = {
            'active': '',
            'username': 'Ripley',
            'email': 'ripley@nostromo.org',
            'password': 'you_never_guess_this',
            'password2': 'you_never_guess_this',
            'group': 'admin',
            'name': 'Ripley Weaver',
            'description': '',
            'send_info': ''}
        data2 = {
            'active': '',
            'username': 'Newt',
            'email': 'newt@nostromo.org',
            'password': 'you_never_guess_this',
            'password2': 'you_never_guess_this',
            'group': 'admin',
            'name': 'Newt',
            'continue_': 'yes',
            'send_info': ''}
        with app.app_context():
            rv: Any = self.app.get(url_for('user_insert'))
            assert b'+ User' in rv.data

            rv = self.app.post(url_for('user_insert'), data=data)
            user_id = rv.location.split('/')[-1]
            data['password'] = 'too short'
            rv = self.app.post(url_for('user_insert'), data=data)
            assert b'match' in rv.data

            rv = self.app.post(
                url_for('user_insert'),
                follow_redirects=True, data=data2)
            assert b'Newt' not in rv.data

            rv = self.app.get(url_for('user_view', id_=user_id))
            assert b'Ripley' in rv.data

            rv = self.app.get(url_for('user_update', id_=self.alice_id))
            assert b'Alice' in rv.data

            data['description'] = 'The warrant officer'
            rv = self.app.post(
                url_for('user_update', id_=user_id),
                data=data,
                follow_redirects=True)
            assert b'The warrant officer' in rv.data

            rv = self.app.get(
                url_for('admin_index', action='delete_user', id_=user_id))
            assert b'User deleted' in rv.data

            self.app.post(
                url_for('insert', class_='bibliography'),
                data={'name': 'test', 'description': 'test'})
            rv = self.app.get(url_for('user_activity'))
            assert b'Activity' in rv.data

            rv = self.app.get(url_for('user_activity', user_id=user_id))
            assert b'Activity' in rv.data

            rv = self.app.post(
                url_for('user_activity'),
                data={'limit': 'all', 'action': 'all', 'user': 'all'})
            assert b'Activity' in rv.data

            rv = self.app.get(
                url_for(
                    'admin_index',
                    action='delete_user',
                    id_=self.alice_id))
            assert b'403 - Forbidden' in rv.data

            self.app.get(url_for('logout'))
            rv = self.app.get(url_for('user_insert'), follow_redirects=True)
            assert b'Forgot your password?' not in rv.data

            self.app.post(
                '/login',
                data={'username': 'Editor', 'password': 'test'})
            rv = self.app.get(url_for('user_insert'), follow_redirects=True)
            assert b'403 - Forbidden' in rv.data

            self.app.get(url_for('logout'))
            self.app.post(
                '/login',
                data={'username': 'Manager', 'password': 'test'})
            rv = self.app.get(
                url_for('admin_settings', category='mail'),
                follow_redirects=True)
            assert b'403 - Forbidden' in rv.data
