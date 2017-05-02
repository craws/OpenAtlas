# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from openatlas import SettingsMapper
from openatlas.test_base import TestBaseCase


class SettingsTestCase(TestBaseCase):

    def test_settings(self):
        response = self.app.get('/settings')
        assert 'Edit' in response.data
        response = self.app.get('/settings/update')
        assert 'Save' in response.data
        form_data = {}
        for name in SettingsMapper.fields:
            form_data[name] = ''
        form_data['default_language'] = 'en'
        form_data['default_table_rows'] = '10'
        form_data['log_level'] = '0'

        response = self.app.post('/settings/update', data=form_data, follow_redirects=True)
        assert 'Edit' in response.data
