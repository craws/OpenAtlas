from pathlib import Path

from flask import g, url_for

from openatlas import app
from tests.base import TestBaseCase


class IndexTests(TestBaseCase):

    def test_index(self) -> None:
        c = self.client
        assert 'x00' in str(c.get('/static/favicon.ico').data)

        rv = c.get(url_for('index_changelog'))
        assert b'is needed but current version is' not in rv.data

        with app.app_context():
            rv = c.get(url_for('login'), follow_redirects=True)
            assert b'first' in rv.data

        rv = c.get(
            url_for('set_locale', language='non_existing_locale'),
            follow_redirects=True)
        assert b'Source' in rv.data

        rv = c.get(url_for('set_locale', language='de'), follow_redirects=True)
        assert b'Quelle' in rv.data
        assert b'messages_de.js' in rv.data

        c.get(url_for('set_locale', language='en'))

        g.writable_paths.append(Path(app.root_path) / 'error')
        app.config['DATABASE_VERSION'] = 'error'
        app.config['EXPORT_PATH'] = Path('error')
        rv = c.get(url_for('view', id_=666), follow_redirects=True)
        assert b'teapot' in rv.data
        assert b'Database version error is needed but current' in rv.data
        assert b'directory not writable' in rv.data

        rv = c.get('/static/non_existing_file.js')
        assert b'The site does not exist.' in rv.data

        rv = c.get(url_for('logout'), follow_redirects=True)
        assert b'Password' in rv.data

        rv = c.get('/')
        assert b'overview' in rv.data

        rv = c.get(url_for('login'))
        assert b'Password' in rv.data

        rv = c.post(url_for('login'), data={'username': '-', 'password': '?'})
        assert b'No user with this name found' in rv.data

        rv = c.post(
            url_for('login'),
            data={'username': 'Alice', 'password': 'wrong'})
        assert b'Wrong Password' in rv.data

        rv = c.post(
            url_for('login'),
            data={'username': 'inactive', 'password': 'test'})
        assert b'This user is not activated' in rv.data

        for _i in range(4):
            rv = c.post(
                url_for('login'),
                data={'username': 'inactive', 'password': '?'})
        assert b'Too many login attempts' in rv.data
