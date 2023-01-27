from pathlib import Path

from flask import url_for

from openatlas import app
from tests.base import TestBaseCase


class IndexTests(TestBaseCase):

    def test_index(self) -> None:
        with app.app_context():
            assert 'x00' in str(self.app.get('/static/favicon.ico').data)

            rv = self.app.get(url_for('index_changelog'))
            assert b'2.0.0' in rv.data
            assert b'is needed but current version is' not in rv.data

            rv = self.app.get(url_for('login'), follow_redirects=True)
            assert b'first' in rv.data

            # Can't use follow_redirects because would get into a loop
            self.app.get(url_for('set_locale', language='de'))

            rv = self.app.get('/')
            assert b'Quelle' in rv.data
            assert b'messages_de.js' in rv.data

            self.app.get(url_for('set_locale', language='en'))

            app.config['WRITABLE_DIRS'].append(Path(app.root_path) / 'error')
            app.config['DATABASE_VERSION'] = 'error'
            rv = self.app.get(url_for('view', id_=666), follow_redirects=True)
            assert b'teapot' in rv.data  # Id not found error
            assert b'OpenAtlas with default password is still' in rv.data
            assert b'Database version error is needed but current' in rv.data
            assert b'Directory not writable' in rv.data

            rv = self.app.get(url_for('logout'), follow_redirects=True)
            assert b'Password' in rv.data

            rv = self.app.get('/')
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
