# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import url_for
from openatlas import app, EntityMapper
from openatlas.test_base import TestBaseCase


class EventTest(TestBaseCase):

    def test_event(self):
        self.login()
        with app.app_context():

            # event insert
            rv = self.app.get(url_for('event_insert', code='E7'))
            assert b'+ Activity' in rv.data
            actor_id = EntityMapper.insert('E21', 'Hansi').id
            rv = self.app.post(
                url_for('event_insert', code='E8', origin_id=actor_id),
                data={'name': 'Test event'},
                follow_redirects=True)
            assert b'An entry has been created' in rv.data
            event_id = EntityMapper.get_by_codes('event')[0].id
            rv = self.app.post(
                url_for('event_insert', code='E8'),
                data={'name': 'Test event', 'continue_': 'yes'},
                follow_redirects=True)
            assert b'An entry has been created' in rv.data
            rv = self.app.get(url_for('event_index'))
            assert b'Test event' in rv.data

            # event update
            rv = self.app.get(url_for('event_update', id_=event_id))
            assert b'Test event' in rv.data
            rv = self.app.post(
                url_for('event_update', id_=event_id),
                data={'name': 'Event updated'},
                follow_redirects=True)
            assert b'Event updated' in rv.data

            # test super event validation
            rv = self.app.post(
                url_for('event_update', id_=event_id),
                data={'name': 'Event Horizon', 'event': event_id},
                follow_redirects=True)
            assert b'error' in rv.data

            # delete event
            rv = self.app.get(url_for('event_delete', id_=event_id), follow_redirects=True)
            assert b'The entry has been deleted.' in rv.data
