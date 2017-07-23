# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from openatlas.test_base import TestBaseCase


class PlaceTest(TestBaseCase):

    def test_place(self):
        rv = self.app.get('/place/insert/E18')
        assert b'+ Place' in rv.data
        form_data = {'name': 'Test place'}
        rv = self.app.post('/place/insert/E18', data=form_data)
        place_id = rv.location.split('/')[-1]
        form_data['continue_'] = 'yes'
        rv = self.app.post('/place/insert/E21', data=form_data, follow_redirects=True)
        assert b'Entity created' in rv.data
        rv = self.app.get('/place')
        assert b'Test place' in rv.data
        rv = self.app.get('/place/update/' + place_id)
        assert b'Test place' in rv.data
        form_data['name'] = 'Test place updated'
        rv = self.app.post('/place/update/' + place_id, data=form_data, follow_redirects=True)
        assert b'Test place updated' in rv.data
        rv = self.app.get('/place/delete/' + place_id, follow_redirects=True)
        assert b'Entity deleted' in rv.data
