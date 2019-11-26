from flask import url_for

from openatlas import app
from tests.base import TestBaseCase


class ProfileTests(TestBaseCase):

    def test_profile(self) -> None:
        with app.app_context():
            self.login()

            # Profile update
            rv = self.app.get(url_for('profile_index'))
            assert b'alice@example.com' in rv.data
            rv = self.app.get(url_for('profile_update'))
            assert b'Newsletter' in rv.data
            data = {'name': 'Alice Abernathy',
                    'email': 'alice@umbrella.net',
                    'max_zoom': 20,
                    'module_geonames': '',
                    'module_notes': '',
                    'show_email': '',
                    'newsletter': '',
                    'language': 'en',
                    'table_rows': '100',
                    'table_show_aliases': 'off',
                    'layout': 'advanced'}
            rv = self.app.post(url_for('profile_update'), data=data, follow_redirects=True)
            assert b'saved' in rv.data
            assert b'Alice Abernathy' in rv.data

            # Change password
            rv = self.app.get(url_for('profile_password'))
            assert b'Old password' in rv.data
            new_pass = 'you_never_guess_this'
            data = {'password_old': 'test', 'password': new_pass, 'password2': new_pass}
            rv = self.app.post(url_for('profile_password'), data=data, follow_redirects=True)
            assert b'Your password has been updated' in rv.data
            data['password2'] = 'short'
            rv = self.app.post(url_for('profile_password'), data=data, follow_redirects=True)
            assert b'match' in rv.data
            data['password_old'] = new_pass
            rv = self.app.post(url_for('profile_password'), data=data, follow_redirects=True)
            assert b'New password is like old one' in rv.data
            data['password'] = 'short'
            rv = self.app.post(url_for('profile_password'), data=data, follow_redirects=True)
            assert b'too short' in rv.data
