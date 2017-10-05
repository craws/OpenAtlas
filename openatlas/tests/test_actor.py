# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from openatlas.test_base import TestBaseCase


class ActorTests(TestBaseCase):

    def test_actor(self):
        self.login()
        rv = self.app.get('/actor/insert/E21')
        assert b'+ Person' in rv.data
        form_data = {
            'name': 'Sigourney Weaver',
            'description': 'Susan Alexandra Weaver is an American actress.',
            'date_begin_year': '1949',
            'date_begin_month': '10',
            'date_begin_day': '8',
            'date_end_year': '2049',
            'date_birth': True,
            'date_death': True}
        rv = self.app.post('/actor/insert/E21', data=form_data)
        actor_id = rv.location.split('/')[-1]
        form_data['continue_'] = 'yes'
        rv = self.app.post('/actor/insert/E21', data=form_data, follow_redirects=True)
        assert b'An entry has been created' in rv.data
        rv = self.app.get('/actor')
        assert b'Sigourney Weaver' in rv.data
        rv = self.app.get('/actor/update/' + actor_id)
        assert b'American actress' in rv.data
        form_data['name'] = 'Susan Alexandra Weaver'
        form_data['date_end_year'] = ''
        form_data['date_begin_year2'] = '1950'
        form_data['date_begin_day'] = ''
        rv = self.app.post('/actor/update/' + actor_id, data=form_data, follow_redirects=True)
        assert b'Susan Alexandra Weaver' in rv.data
        rv = self.app.post('/ajax/bookmark', data={'entity_id': actor_id}, follow_redirects=True)
        assert b'Remove bookmark' in rv.data
        rv = self.app.get('/')
        assert b'Weaver' in rv.data
        rv = self.app.post('/ajax/bookmark', data={'entity_id': actor_id}, follow_redirects=True)
        assert b'Bookmark' in rv.data
        rv = self.app.get('/actor/delete/' + actor_id, follow_redirects=True)
        assert b'The entry has been deleted.' in rv.data
