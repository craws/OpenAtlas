from flask import url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.test_base import TestBaseCase


class ContentTests(TestBaseCase):

    def test_content_and_newsletter(self):
        with app.app_context():
            self.login()
            self.app.post(url_for('actor_insert', code='E21'), data={'name': 'Oliver Twist'})
            with app.test_request_context():
                app.preprocess_request()
                EntityMapper.insert('E61', '2017-04-01')  # add orphaned date
                EntityMapper.insert('E31', 'One forsaken file entity', 'file')  # add orphaned file
            rv = self.app.get(url_for('admin_orphans'))
            assert all(x in rv.data for x in [b'Oliver Twist', b'2017-04-01', b'forsaken'])
            rv = self.app.get(url_for('admin_orphans', delete='orphans'))
            assert b'2017-04-01' not in rv.data
            self.app.get(url_for('admin_orphans', delete='unlinked'))
            self.app.get(url_for('admin_orphans', delete='types'))
            self.app.get(url_for('admin_orphans', delete='something completely different'))
            rv = self.app.get(url_for('admin_newsletter'))
            assert b'Newsletter' in rv.data

    def test_logs(self):
        self.login()
        with app.app_context():
            rv = self.app.get(url_for('admin_log'))
            assert b'Login' in rv.data
            rv = self.app.get(url_for('admin_log_delete', follow_redirects=True))
            assert b'Login' not in rv.data

    def test_links(self):
        self.login()
        with app.app_context():
            rv = self.app.get(url_for('admin_check_links', check='check'))
            assert b'No entries' in rv.data

