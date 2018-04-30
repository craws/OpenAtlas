from flask import url_for

from openatlas import app
from openatlas.test_base import TestBaseCase


class ContentTests(TestBaseCase):

    def test_content(self):
        with app.app_context():
            self.login()
            rv = self.app.get(url_for('content_view', item='legal'))
            assert b'Edit' in rv.data
            rv = self.app.get(url_for('content_update', item='legal'))
            assert b'Save' in rv.data
            data = {'en': 'Legal notice', 'de': 'Impressum'}
            rv = self.app.post(
                url_for('content_update', item='legal'), data=data, follow_redirects=True)
            assert b'Impressum' in rv.data
            rv = self.app.get(url_for('content_index'))
            assert b'Text' in rv.data
            self.app.get('/index/setlocale/de')
            rv = self.app.get('/', follow_redirects=True)
            assert b'Impressum' in rv.data
