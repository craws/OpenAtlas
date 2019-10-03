from flask import url_for

from openatlas import app
from openatlas.test_base import TestBaseCase


class SqlTest(TestBaseCase):

    def test_sql(self):
        with app.app_context():
            self.login()
            rv = self.app.get(url_for('sql_index'))
            assert b'Warning' in rv.data
            rv = self.app.get(url_for('sql_execute'))
            assert b'Execute' in rv.data
            rv = self.app.post(url_for('sql_execute'), data={'statement': 'SELECT * FROM web.user'})
            assert b'Alice' in rv.data
            rv = self.app.post(url_for('sql_execute'), data={'statement': 'SELECT * FROM fail;'})
            assert b'relation "fail" does not exist' in rv.data
