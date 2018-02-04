# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import url_for

from openatlas import app, EntityMapper
from openatlas.test_base import TestBaseCase


class ActorTests(TestBaseCase):

    def test_actor(self):
        self.login()
        with app.app_context():
            rv = self.app.get(url_for('actor_index'))
            assert b'No entries' in rv.data

            # create a residence for actor
            rv = self.app.post(url_for('place_insert'), data={'name': 'Nostromos'})
            residence_id = rv.location.split('/')[-1]

            # actor insert
            rv = self.app.get(url_for('actor_insert', code='E21'))
            assert b'+ Person' in rv.data
            data = {
                'name': 'Sigourney Weaver',
                'alias-1': 'Ripley',
                'residence': residence_id,
                'appears_first': residence_id,
                'appears_last': residence_id,
                'description': 'Susan Alexandra Weaver is an American actress.',
                'date_begin_year': '-1949',
                'date_begin_month': '10',
                'date_begin_day': '8',
                'date_begin_year2': '-1948',
                'date_end_year': '2049',
                'date_end_year2': '2050',
                'date_birth': True,
                'date_death': True}
            rv = self.app.post(url_for('actor_insert', code='E21'), data=data)
            actor_id = rv.location.split('/')[-1]
            rv = self.app.post(url_for('reference_insert', code='reference'), data={'name': 'Book'})
            reference_id = rv.location.split('/')[-1]
            rv = self.app.post(
                url_for('actor_insert', code='E21', origin_id=reference_id),
                data=data,
                follow_redirects=True)
            assert b'An entry has been created' in rv.data
            data['continue_'] = 'yes'
            rv = self.app.post(
                url_for('actor_insert', code='E21'), data=data, follow_redirects=True)
            assert b'An entry has been created' in rv.data
            rv = self.app.get(url_for('actor_index'))
            assert b'Sigourney Weaver' in rv.data

            # actor update
            rv = self.app.get(url_for('actor_update', id_=actor_id))
            assert b'American actress' in rv.data
            data['name'] = 'Susan Alexandra Weaver'
            data['date_end_year'] = ''
            data['date_begin_year2'] = '1950'
            data['date_begin_day'] = ''
            rv = self.app.post(
                url_for('actor_update', id_=actor_id), data=data, follow_redirects=True)
            assert b'Susan Alexandra Weaver' in rv.data
            rv = self.app.post(
                url_for('ajax_bookmark'), data={'entity_id': actor_id}, follow_redirects=True)
            assert b'Remove bookmark' in rv.data
            rv = self.app.get('/')
            assert b'Weaver' in rv.data
            rv = self.app.post(
                url_for('ajax_bookmark'), data={'entity_id': actor_id}, follow_redirects=True)
            assert b'Bookmark' in rv.data
            rv = self.app.get(
                url_for('actor_view', id_=actor_id, unlink_id=666), follow_redirects=True)
            assert b'removed'in rv.data

            # actor delete
            rv = self.app.get(url_for('actor_delete', id_=actor_id), follow_redirects=True)
            assert b'The entry has been deleted.' in rv.data
