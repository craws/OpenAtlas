# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from openatlas import SettingsMapper
from openatlas.test_base import TestBaseCase


class SettingsTests(TestBaseCase):

    def test_settings(self):
        rv = self.app.get('/settings')
        assert b'Edit' in rv.data
        rv = self.app.get('/settings/update')
        assert b'Save' in rv.data
        form_data = {}
        for name in SettingsMapper.fields:
            form_data[name] = ''
        form_data['default_language'] = 'en'
        form_data['default_table_rows'] = '10'
        form_data['log_level'] = '0'
        rv = self.app.post('/settings/update', data=form_data, follow_redirects=True)
        assert b'Edit' in rv.data
