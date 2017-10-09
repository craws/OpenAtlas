# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from openatlas.test_base import TestBaseCase


class SourceTest(TestBaseCase):

    def test_source(self):
        self.login()
        rv = self.app.get('/source/insert')
        assert b'+ Source' in rv.data
        form_data = {'name': 'Test source'}
        rv = self.app.post('/source/insert', data=form_data)
        source_id = rv.location.split('/')[-1]
        form_data['continue_'] = 'yes'
        rv = self.app.post('/source/insert', data=form_data, follow_redirects=True)
        assert b'An entry has been created' in rv.data
        rv = self.app.get('/source')
        assert b'Test source' in rv.data
        rv = self.app.get('/source/update/' + source_id)
        assert b'Test source' in rv.data
        form_data['name'] = 'Test source updated'
        rv = self.app.post('/source/update/' + source_id, data=form_data, follow_redirects=True)
        assert b'Test source updated' in rv.data
        rv = self.app.get('/source/delete/' + source_id, follow_redirects=True)
        assert b'The entry has been deleted.' in rv.data
