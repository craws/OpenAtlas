# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import url_for

from openatlas import SettingsMapper, app
from openatlas.test_base import TestBaseCase


class SettingsTests(TestBaseCase):

    def test_settings(self):
        with app.app_context():
            self.login()
            rv = self.app.get(url_for('settings_index'))
            assert b'Edit' in rv.data
            rv = self.app.get(url_for('settings_update'))
            assert b'Save' in rv.data
            form_data = {}
            for name in SettingsMapper.fields:
                form_data[name] = ''
            form_data['default_language'] = 'en'
            form_data['default_table_rows'] = '10'
            form_data['failed_login_forget_minutes'] = '10'
            form_data['failed_login_tries'] = '10'
            form_data['minimum_password_length'] = '10'
            form_data['random_password_length'] = '10'
            form_data['reset_confirm_hours'] = '10'
            form_data['log_level'] = '0'
            form_data['site_name'] = 'Nostromo'
            rv = self.app.post(url_for('settings_update'), data=form_data, follow_redirects=True)
            assert b'Nostromo' in rv.data
