from pathlib import Path

from flask import url_for

from openatlas import app
from tests.base import TestBaseCase


class IndexTests(TestBaseCase):

    def test_index(self) -> None:
        with app.app_context():

            assert b'not found' in self.app.get('/404').data
            assert b'0' in self.app.get('/').data
            assert b'Thank you' in self.app.get(url_for('index_feedback')).data
            assert 'x00' in str(self.app.get('/static/favicon.ico').data)

            rv = self.app.get(url_for('index_changelog'))
            assert b'2.0.0' in rv.data
            assert b'is needed but current version is' not in rv.data

            self.app.get(url_for('index_content', item='contact'))
            self.app.get(url_for('set_locale', language='en'))
            rv = self.app.get(url_for('reset_password'))
            assert b'Forgot your password?' not in rv.data

            rv = self.app.get(url_for('login'), follow_redirects=True)
            assert b'first' in rv.data

            self.app.get(url_for('set_locale', language='de'))
            assert b'Quelle' in self.app.get('/').data

            self.app.get(url_for('set_locale', language='en'))
            assert b'Source' in self.app.get('/').data

            rv = self.app.get(url_for('view', id_=666), follow_redirects=True)
            assert b'teapot' in rv.data  # Id not found error

            app.config['WRITABLE_DIRS'].append(Path(app.root_path) / 'error')
            app.config['DATABASE_VERSION'] = 'error'
            rv = self.app.get('/')
            assert b'OpenAtlas with default password is still' in rv.data
            assert b'Database version error is needed but current' in rv.data
            assert b'Directory not writable' in rv.data

            rv = self.app.get(url_for('logout'), follow_redirects=True)
            assert b'Password' in rv.data

            rv = self.app.get(url_for('reset_password'))
            assert b'Forgot your password?' in rv.data

            rv = self.app.get(url_for('reset_confirm', code='1234'))
            assert b'404' in rv.data

            rv = self.app.get(url_for('index_unsubscribe', code='1234'))
            assert b'invalid' in rv.data

            rv = self.app.get('/')  # Test intro when not logged in
            assert b'Overview' in rv.data

            rv = self.app.get(url_for('login'))
            assert b'Password' in rv.data

            rv = self.app.post(
                url_for('login'),
                data={'username': 'Never', 'password': 'wrong'})
            assert b'No user with this name found' in rv.data

            rv = self.app.post(
                url_for('login'),
                data={'username': 'Alice', 'password': 'wrong'})
            assert b'Wrong Password' in rv.data

            rv = self.app.post(
                url_for('login'),
                data={'username': 'inactive', 'password': 'test'})
            assert b'This user is not activated' in rv.data

            for _i in range(4):
                rv = self.app.post(
                    url_for('login'),
                    data={'username': 'inactive', 'password': '?'})
            assert b'Too many login attempts' in rv.data
