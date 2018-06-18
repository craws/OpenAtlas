from flask import url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.test_base import TestBaseCase


class EventTest(TestBaseCase):

    def test_event(self):
        with app.app_context():
            self.login()

            # Create entities for event
            rv = self.app.post(url_for('place_insert'), data={'name': 'My house'})
            residence_id = rv.location.split('/')[-1]
            with app.test_request_context():
                app.preprocess_request()
                actor_id = EntityMapper.insert('E21', 'Game master').id
                file_id = EntityMapper.insert('E31', 'One forsaken file entity', 'file').id
                source_id = EntityMapper.insert('E33', 'Necronomicon', 'source content').id
                reference_id = EntityMapper.insert('E31', 'Ancient Books', 'edition').id

            # Insert
            rv = self.app.get(url_for('event_insert', code='E7'))
            assert b'+ Activity' in rv.data
            data = {'name': 'First event ever', 'place': residence_id}

            rv = self.app.post(url_for('event_insert', code='E7', origin_id=reference_id),
                               data=data, follow_redirects=True)
            assert b'First event ever' in rv.data
            with app.test_request_context():
                app.preprocess_request()
                activity_id = EntityMapper.get_by_codes('event')[0].id

            self.app.post(url_for('event_insert', code='E7', origin_id=actor_id), data=data)
            self.app.post(url_for('event_insert', code='E7', origin_id=file_id), data=data)
            self.app.post(url_for('event_insert', code='E7', origin_id=source_id), data=data)

            rv = self.app.post(
                url_for('event_insert', code='E8'),
                data={
                    'name': 'Test event',
                    'given_place': '[' + str(residence_id) + ']',
                    'place': residence_id,
                    'event': activity_id,
                    'date_begin_year': '1949',
                    'date_begin_month': '10',
                    'date_begin_day': '8',
                    'date_end_year': '1951'})
            event_id = rv.location.split('/')[-1]
            rv = self.app.get(url_for('event_view', id_=event_id))
            assert b'Test event' in rv.data
            rv = self.app.get(url_for('actor_view', id_=actor_id))
            assert b'Game master' in rv.data
            rv = self.app.post(
                url_for('event_insert', code='E8'),
                data={'name': 'Test event', 'continue_': 'yes'},
                follow_redirects=True)
            assert b'An entry has been created' in rv.data
            rv = self.app.get(url_for('event_index'))
            assert b'Test event' in rv.data
            self.app.get(url_for('event_view', id_=activity_id))
            rv = self.app.get(
                url_for('event_view', id_=actor_id, unlink_id=666), follow_redirects=True)
            assert b'removed' in rv.data

            # Update
            rv = self.app.get(url_for('event_update', id_=activity_id))
            assert b'Test event' in rv.data
            rv = self.app.get(url_for('event_update', id_=event_id))
            assert b'First event ever' in rv.data
            data = {'name': 'Event updated'}
            rv = self.app.post(
                url_for('event_update', id_=event_id), data=data, follow_redirects=True)
            assert b'Event updated' in rv.data

            # Test super event validation
            data = {'name': 'Event Horizon', 'event': event_id}
            rv = self.app.post(
                url_for('event_update', id_=event_id), data=data, follow_redirects=True)
            assert b'error' in rv.data

            # Delete
            rv = self.app.get(url_for('event_delete', id_=event_id), follow_redirects=True)
            assert b'The entry has been deleted.' in rv.data
