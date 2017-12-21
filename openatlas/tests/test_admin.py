# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import url_for

from openatlas import app, EntityMapper
from openatlas.test_base import TestBaseCase


class ContentTests(TestBaseCase):

    def test_content(self):
        self.login()
        EntityMapper.insert('E21', 'Oliver Twist')  # add unlinked person
        EntityMapper.insert('E61', '2017-04-01')  # add orphaned date
        with app.app_context():
            rv = self.app.get(url_for('admin_orphans'))
            assert b'Oliver Twist' in rv.data
            rv = self.app.get(url_for('admin_orphans', delete='orphans'))
            assert b'2017-04-01' not in rv.data

    def test_logs(self):
        self.login()
        with app.app_context():
            rv = self.app.get(url_for('admin_log'))
            assert b'Login' in rv.data
            rv = self.app.get(url_for('admin_log_delete', follow_redirects=True))
            assert b'Login' not in rv.data
