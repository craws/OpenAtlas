# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from openatlas.test_base import TestBaseCase


class ReferenceTest(TestBaseCase):

    def test_reference(self):
        rv = self.app.get('/reference/insert/bibliography')
        assert b'+ Bibliography' in rv.data
        rv = self.app.get('/reference/insert/edition')
        assert b'+ Edition' in rv.data
        rv = self.app.get('/reference/insert/carrier')
        assert b'+ Carrier' in rv.data
        form_data = {'name': 'Test reference', 'description': 'Reference description'}
        rv = self.app.post('/reference/insert/bibliography', data=form_data)
        bibliography_id = rv.location.split('/')[-1]
        form_data['continue_'] = 'yes'
        rv = self.app.post('/reference/insert/carrier', data=form_data, follow_redirects=True)
        assert b'Entity created' in rv.data
        rv = self.app.get('/reference')
        assert b'Test reference' in rv.data
        rv = self.app.get('/reference/update/' + bibliography_id)
        assert b'Test reference' in rv.data
        form_data['name'] = 'Test reference updated'
        rv = self.app.post('/reference/update/' + bibliography_id, data=form_data, follow_redirects=True)
        assert b'Test reference updated' in rv.data
        rv = self.app.get('/reference/delete/' + bibliography_id, follow_redirects=True)
        assert b'Entity deleted' in rv.data
