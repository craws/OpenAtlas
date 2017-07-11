# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from openatlas.test_base import TestBaseCase


class ActorTests(TestBaseCase):

    def test_actor(self):
        rv = self.app.get('/actor/insert/E21')
        assert '+ Person' in rv.data
        form_data = {'name': 'Test actor', 'description': 'Actor description'}
        rv = self.app.post('/actor/insert/E21', data=form_data)
        actor_id = rv.location.split('/')[-1]
        form_data['continue_'] = 'yes'
        rv = self.app.post('/actor/insert/E21', data=form_data, follow_redirects=True)
        assert 'Entity created' in rv.data
        rv = self.app.get('/actor')
        assert 'Test actor' in rv.data
        rv = self.app.get('/actor/update/' + actor_id)
        assert 'Test actor' in rv.data
        form_data['name'] = 'Test actor updated'
        rv = self.app.post('/actor/update/' + actor_id, data=form_data, follow_redirects=True)
        assert 'Test actor updated' in rv.data
        rv = self.app.get('/actor/delete/' + actor_id, follow_redirects=True)
        assert 'Entity deleted' in rv.data
