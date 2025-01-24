from flask import url_for
from flask_jwt_extended import decode_token

from database.token import get_tokens
from models.user import User
from openatlas import app, check_incoming_tokens
from tests.base import TestBaseCase


class TokenTests(TestBaseCase):
    def test_token(self) -> None:
        c = self.client
        with app.test_request_context():
            app.preprocess_request()
            print([(user.username, user.id) for user in User.get_all()])

        rv = c.get(url_for('api_token'))
        assert b'Token' in rv.data

        rv = c.get(url_for('generate_token'))
        assert b'generate token' in rv.data

        generating_tokens = [
            {'expiration': 1, 'token_name': 'one day token', 'user': 2},
            {'expiration': 20, 'token_name': '20 day token', 'user': 5},
            {'expiration': 90, 'token_name': '90 day token', 'user': 4},
            {'expiration': 30, 'token_name': '30 day token', 'user': 3},
            {'expiration': 0, 'token_name': 'indefinite token', 'user': 1}]

        jwt_token_strings = []

        for token in generating_tokens:
            rv = c.post(
                url_for('generate_token'),
                data=token)
            for part in rv.headers['Set-Cookie'].split(';'):
                if 'jwt_token=' in part:
                    jwt_token_strings.append(
                        part.replace('jwt_token=', '').strip())
                    break

        for token in generating_tokens:
            rv = c.post(
                url_for('generate_token'),
                data=token,
                follow_redirects=True)
            assert b'Token stored' in rv.data

        rv = c.post(
            url_for('api_token'),
            data={'user_id': 1, 'revoked': 'all', 'valid': 'all'})
        assert b'indefinite token' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            tokens = get_tokens(0, 'all', 'all')

        rv = c.get(
            url_for('revoke_token', id_=tokens[0]['id']),
            follow_redirects=True)
        assert b'Token revoked' in rv.data

        rv = c.get(
            url_for('authorize_token', id_=tokens[0]['id']),
            follow_redirects=True)
        assert b'Token authorized' in rv.data

        rv = c.get(url_for('revoke_all_tokens'), follow_redirects=True)
        assert b'All tokens revoked' in rv.data

        rv = c.get(url_for('authorize_all_tokens'), follow_redirects=True)
        assert b'All tokens authorize' in rv.data

        rv = c.get(
            url_for('revoke_token', id_=tokens[0]['id']),
            follow_redirects=True)
        assert b'Token revoked' in rv.data

        with app.test_request_context():
            app.preprocess_request()

            for token in jwt_token_strings:
                decoded = decode_token(token)
                #check = check_incoming_tokens({'typ': 'JWT'}, decoded)
                #assert check is True if decoded['sub'] in ['Alice', 'Inactive'] else False

                # should fail if check_incoming_tokens checks for user active
                rv = c.get(
                    url_for('api_04.class_mapping', locale='de'),
                    headers={'Authorization': f'Bearer {token}'})
                assert b'results' in rv.data

            assert check_incoming_tokens({'typ': 'Unknown'}, decoded) is True

        rv = c.get(url_for('delete_revoked_tokens'), follow_redirects=True)
        assert b'All revoked tokens deleted' in rv.data

        rv = c.get(url_for('delete_invalid_tokens'), follow_redirects=True)
        assert b'All invalid tokens deleted' in rv.data

        rv = c.get(
            url_for('delete_token', id_=tokens[-1]['id']),
            follow_redirects=True)
        assert b'Token deleted' in rv.data

