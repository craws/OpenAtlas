from flask import url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.models.settings import SettingsMapper
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
            assert b'Invalid linked entity' in rv.data

    def test_admin(self):
        with app.app_context():
            self.login()
            rv = self.app.get(url_for('admin_mail'))
            assert b'Email from' in rv.data
            rv = self.app.get(url_for('admin_index'))
            assert b'User' in rv.data
            rv = self.app.get(url_for('admin_general'))
            assert b'Edit' in rv.data
            rv = self.app.get(url_for('admin_general_update'))
            assert b'Save' in rv.data
            data = {}
            for name in SettingsMapper.fields:
                data[name] = ''
            data['default_language'] = 'en'
            data['default_table_rows'] = '10'
            data['failed_login_forget_minutes'] = '10'
            data['failed_login_tries'] = '10'
            data['minimum_password_length'] = '10'
            data['random_password_length'] = '10'
            data['reset_confirm_hours'] = '10'
            data['log_level'] = '0'
            data['site_name'] = 'Nostromo'
            rv = self.app.post(url_for('admin_general_update'), data=data, follow_redirects=True)
            assert b'Nostromo' in rv.data
            rv = self.app.get(url_for('admin_mail_update'))
            assert b'Mail transport port' in rv.data
            rv = self.app.post(url_for('admin_mail_update'), data=data, follow_redirects=True)
            assert b'Email from' in rv.data
            rv = self.app.get(url_for('admin_file'))
            assert b'jpg' in rv.data
            rv = self.app.post(
                url_for('admin_file'), data={'file_upload_max_size': 20}, follow_redirects=True)
            assert b'Changes have been saved.' in rv.data
