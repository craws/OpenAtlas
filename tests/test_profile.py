from flask import url_for
from flask_jwt_extended import decode_token

from openatlas import app, check_if_token_revoked
from openatlas.database.token import get_tokens
from tests.base import ProfileTestCase


class ProfileTests(ProfileTestCase):

    def test_profile(self) -> None:
        c = self.client
        rv = c.get(url_for('profile_settings', category='profile'))
        assert b'alice@example.com' in rv.data

        rv = c.post(
            url_for('profile_settings', category='profile'),
            data={
                'name': 'Alice Abernathy',
                'email': 'alice@umbrella.net',
                'show_email': ''},
            follow_redirects=True)
        assert b'saved' in rv.data and b'Alice Abernathy' in rv.data

        rv = c.post(
            url_for('profile_settings', category='display'),
            data={
                'language': 'en',
                'table_rows': 10,
                'map_zoom_default': 10,
                'map_zoom_max': 10},
            follow_redirects=True)
        assert b'saved' in rv.data

        rv = c.get(url_for('profile_password'))
        assert b'old password' in rv.data

        new_pass = 'you_never_guess_this'
        data = {
            'password_old': 'test',
            'password': new_pass,
            'password2': new_pass}
        rv = c.post(
            url_for('profile_password'),
            data=data,
            follow_redirects=True)
        assert b'Your password has been updated' in rv.data

        data['password2'] = 'short'
        rv = c.post(
            url_for('profile_password'),
            data=data,
            follow_redirects=True)
        assert b'match' in rv.data

        data['password_old'] = new_pass
        rv = c.post(
            url_for('profile_password'),
            data=data,
            follow_redirects=True)
        assert b'New password is like old one' in rv.data

        data['password'] = 'short'
        rv = c.post(
            url_for('profile_password'),
            data=data,
            follow_redirects=True)
        assert b'too short' in rv.data

        expire_dates = [
            {'expiration': 0, 'token_name': 'one day token'},
            {'expiration': 1, 'token_name': '90 days token'},
            {'expiration': 2, 'token_name': 'indefinite token'}]
        for expire_date in expire_dates:
            rv = c.post(
                url_for('generate_token'),
                data=expire_date,
                follow_redirects=True)
            assert b'Token stored' in rv.data

        # This should get the token table, which will not be generated
        rv = c.get(url_for('profile_index'))
        assert b'Generate' in rv.data

        # Getting valid JWT token
        jwt_token = ''
        rv = c.post(
            url_for('generate_token'),
            data={'expiration': 0, 'token_name': 'one day token'})
        for part in rv.headers['Set-Cookie'].split(';'):
            if 'jwt_token=' in part:
                jwt_token = part.replace('jwt_token=', '').strip()
                break

        with app.test_request_context():
            app.preprocess_request()
            decoded = decode_token(jwt_token)
            check = check_if_token_revoked({'typ': 'JWT'}, decoded)
            assert check is False

            check = check_if_token_revoked({'typ': 'Unknown'}, decoded)
            assert check is True

            tokens = get_tokens(self.alice_id)
            token_id = tokens[0]['id']
            token_to_be_revoked_id = 0
            for token in tokens:
                if token['jti'] == decoded['jti']:
                    token_to_be_revoked_id = token['id']
                    break

        rv = c.get(
            url_for('api_04.class_mapping', locale='de'),
            headers={'Authorization': f'Bearer {jwt_token}'})
        assert b'results' in rv.data

        rv = c.get(
            url_for('revoke_token', id_=token_to_be_revoked_id),
            follow_redirects=True)
        assert b'Token revoked' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            check = check_if_token_revoked({'typ': 'JWT'}, decoded)
            assert check is True

        rv = c.get(
            url_for('authorize_token', id_=token_id),
            follow_redirects=True)
        assert b'Token authorized' in rv.data

        rv = c.get(url_for('revoke_all_tokens'), follow_redirects=True)
        assert b'All tokens revoked' in rv.data

        rv = c.get(
            url_for('delete_all_tokens'),
            follow_redirects=True)
        assert b'All revoked tokens deleted' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            check = check_if_token_revoked({'typ': 'JWT'}, decoded)
            assert check is True
