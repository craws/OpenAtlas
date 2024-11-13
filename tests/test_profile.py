from flask import url_for

from openatlas import app
from openatlas.database.user import get_tokens
from tests.base import ProfileTestCase


class ProfileTests(ProfileTestCase):

    def test_profile(self) -> None:
        with app.app_context():
            rv = self.app.get(url_for('profile_settings', category='profile'))
            assert b'alice@example.com' in rv.data

            rv = self.app.post(
                url_for('profile_settings', category='profile'),
                data={
                    'name': 'Alice Abernathy',
                    'email': 'alice@umbrella.net',
                    'show_email': ''},
                follow_redirects=True)
            assert b'saved' in rv.data and b'Alice Abernathy' in rv.data

            rv = self.app.post(
                url_for('profile_settings', category='display'),
                data={
                    'language': 'en',
                    'table_rows': 10,
                    'map_zoom_default': 10,
                    'map_zoom_max': 10},
                follow_redirects=True)
            assert b'saved' in rv.data

            rv = self.app.get(url_for('profile_password'))
            assert b'old password' in rv.data

            new_pass = 'you_never_guess_this'
            data = {
                'password_old': 'test',
                'password': new_pass,
                'password2': new_pass}
            rv = self.app.post(
                url_for('profile_password'),
                data=data,
                follow_redirects=True)
            assert b'Your password has been updated' in rv.data

            data['password2'] = 'short'
            rv = self.app.post(
                url_for('profile_password'),
                data=data,
                follow_redirects=True)
            assert b'match' in rv.data

            data['password_old'] = new_pass
            rv = self.app.post(
                url_for('profile_password'),
                data=data,
                follow_redirects=True)
            assert b'New password is like old one' in rv.data

            data['password'] = 'short'
            rv = self.app.post(
                url_for('profile_password'),
                data=data,
                follow_redirects=True)
            assert b'too short' in rv.data

            tokens = [
                {'expiration': 0, 'token_name': 'one day token'},
                {'expiration': 1, 'token_name': '90 days token'},
                {'expiration': 2, 'token_name': 'indefinite token'}]
            for token in tokens:
                rv = self.app.post(
                    url_for('generate_token'),
                    data=token,
                    follow_redirects=True)
                assert b'Token stored' in rv.data

            # This should get the token table, which will not be generated
            rv = self.app.get(url_for('profile_index'))
            assert b'Generate' in rv.data

            with app.app_context():
                with app.test_request_context():
                    app.preprocess_request()
                    token_id = get_tokens(self.alice_id)[0]['id']

            rv = self.app.get(
                url_for('delete_token', id_=token_id),
                follow_redirects=True)
            assert b'Token deleted' in rv.data

            rv = self.app.get(
                url_for('delete_all_tokens'),
                follow_redirects=True)
            assert b'All tokens deleted' in rv.data
