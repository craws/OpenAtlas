from flask import url_for

from openatlas import app
from openatlas.models.settings import SettingsMapper
from openatlas.test_base import TestBaseCase


class SettingsTests(TestBaseCase):

    def test_settings(self):
        with app.app_context():
            self.login()
            rv = self.app.get(url_for('admin_index'))
            assert b'User' in rv.data
            rv = self.app.get(url_for('settings_index'))
            assert b'Edit' in rv.data
            rv = self.app.get(url_for('settings_update'))
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
            rv = self.app.post(url_for('settings_update'), data=data, follow_redirects=True)
            assert b'Nostromo' in rv.data
