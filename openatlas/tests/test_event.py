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
                reference_id = EntityMapper.insert('E31', 'https://openatlas.eu',
                                                   'external reference').id

            # Insert
            rv = self.app.get(url_for('event_insert', code='E7'))
            assert b'+ Activity' in rv.data
            data = {'name': 'First event ever First event ever First event ever First event ever',
                    'place': residence_id}
            rv = self.app.post(url_for('event_insert', code='E7', origin_id=reference_id),
                               data=data, follow_redirects=True)
            assert b'First event ever' in rv.data
            with app.test_request_context():
                app.preprocess_request()
                activity_id = EntityMapper.get_by_codes('event')[0].id
            self.app.post(url_for('event_insert', code='E7', origin_id=actor_id), data=data)
            self.app.post(url_for('event_insert', code='E7', origin_id=file_id), data=data)
            self.app.post(url_for('event_insert', code='E7', origin_id=source_id), data=data)

            # Acquisition
            rv = self.app.post(url_for('event_insert', code='E8'),
                               data={'name': 'Test event',
                                     'given_place': '[' + str(residence_id) + ']',
                                     'place': residence_id,
                                     'event': activity_id,
                                     'begin_year_from': '1949',
                                     'begin_month_from': '10',
                                     'begin_day_from': '8',
                                     'end_year_from': '1951'})
            event_id = rv.location.split('/')[-1]
            rv = self.app.get(url_for('event_view', id_=event_id))
            assert b'Test event' in rv.data

            # Move
            rv = self.app.post(url_for('event_insert', code='E9'),
                               data={'name': 'Keep it moving', 'place_to': residence_id,
                                     'place_from': residence_id})
            move_id = rv.location.split('/')[-1]
            rv = self.app.get(url_for('event_view', id_=move_id))
            assert b'Keep it moving' in rv.data
            rv = self.app.get(url_for('event_update', id_=move_id))
            assert b'Keep it moving' in rv.data

            # Add another event and test if events are seen at place
            self.app.post(url_for('event_insert', code='E8'),
                          data={'name': 'Dusk', 'given_place': '[' + str(residence_id) + ']'})
            rv = self.app.get(url_for('place_view', id_=residence_id))
            assert b'Test event' in rv.data
            rv = self.app.get(url_for('actor_view', id_=actor_id))
            assert b'Game master' in rv.data
            rv = self.app.post(url_for('event_insert', code='E8'), follow_redirects=True,
                               data={'name': 'Test event', 'continue_': 'yes'})
            assert b'An entry has been created' in rv.data
            rv = self.app.get(url_for('event_index'))
            assert b'Test event' in rv.data
            self.app.get(url_for('event_view', id_=activity_id))

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
