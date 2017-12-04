# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import url_for

from openatlas import app
from openatlas.test_base import TestBaseCase


class EventTest(TestBaseCase):

    def test_event(self):
        with app.app_context():
            self.login()
            rv = self.app.get(url_for('event_insert', code='E7'))
            assert b'+ Activity' in rv.data
            form_data = {'name': 'Test event', 'description': 'Event description'}
            rv = self.app.post(url_for('event_insert', code='E7'), data=form_data)
            event_id = rv.location.split('/')[-1]
            form_data['continue_'] = 'yes'
            rv = self.app.post(
                url_for('event_insert', code='E8'),
                data=form_data,
                follow_redirects=True)
            assert b'An entry has been created' in rv.data
            rv = self.app.get(url_for('event_index'))
            assert b'Test event' in rv.data
            rv = self.app.get(url_for('event_update', id_=event_id))
            assert b'Test event' in rv.data
            form_data['name'] = 'Test event updated'
            rv = self.app.post(
                url_for('event_update', id_=event_id),
                data=form_data,
                follow_redirects=True)
            assert b'Test event updated' in rv.data
            rv = self.app.get(url_for('involvement_insert', origin_id=event_id))
            assert b'+ Involvement' in rv.data
            rv = self.app.get(url_for('event_delete', id_=event_id), follow_redirects=True)
            assert b'The entry has been deleted.' in rv.data
