# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import url_for

from openatlas import app, EntityMapper
from openatlas.test_base import TestBaseCase


class ContentTests(TestBaseCase):

    def test_content_and_newsletter(self):
        self.login()
        with app.app_context():
            self.app.post(url_for('actor_insert', code='E21'), data={'name': 'Oliver Twist'})
            with app.test_request_context():
                app.preprocess_request()
                EntityMapper.insert('E61', '2017-04-01')  # add orphaned date
            rv = self.app.get(url_for('admin_orphans'))
            assert b'Oliver Twist' in rv.data
            assert b'2017-04-01' in rv.data
            rv = self.app.get(url_for('admin_orphans', delete='orphans'))
            assert b'2017-04-01' not in rv.data
            rv = self.app.get(url_for('admin_newsletter'))
            assert b'Newsletter' in rv.data

    def test_logs(self):
        self.login()
        with app.app_context():
            rv = self.app.get(url_for('admin_log'))
            assert b'Login' in rv.data
            rv = self.app.get(url_for('admin_log_delete', follow_redirects=True))
            assert b'Login' not in rv.data
