from flask import url_for

from openatlas import app
from openatlas.models.entity import Entity
from tests.base import TestBaseCase, random_string


class EventTest(TestBaseCase):

    def test_event(self) -> None:
        with app.app_context():  # type: ignore
            # Create entities for event
            place_name = random_string()
            rv = self.app.post(url_for('place_insert'), data={'name': place_name})
            residence_id = rv.location.split('/')[-1]
            actor_name = random_string()
            event_name = random_string()
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                actor = Entity.insert('E21', actor_name)
                file = Entity.insert('E31', 'X-Files', 'file')
                source = Entity.insert('E33', 'Necronomicon', 'source content')
                carrier = Entity.insert('E84', 'I care for you', 'information carrier')
                reference = Entity.insert('E31', 'https://openatlas.eu', 'external reference')

            # Insert
            rv = self.app.get(url_for('event_insert', code='E7'))
            assert b'+ Activity' in rv.data
            data = {'name': event_name,
                    'place': residence_id}
            rv = self.app.post(url_for('event_insert', code='E7', origin_id=reference.id),
                               data=data, follow_redirects=True)
            assert bytes(event_name, 'utf-8') in rv.data
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                activity_id = Entity.get_by_menu_item('event')[0].id
            self.app.post(url_for('event_insert', code='E7', origin_id=actor.id), data=data)
            self.app.post(url_for('event_insert', code='E7', origin_id=file.id), data=data)
            self.app.post(url_for('event_insert', code='E7', origin_id=source.id), data=data)
            rv = self.app.get(url_for('event_insert', code='E7', origin_id=residence_id))
            assert b'Location' in rv.data
            rv = self.app.get(url_for('event_insert', code='E9', origin_id=residence_id))
            assert b'Location' not in rv.data

            # Acquisition
            event_name2 = random_string(8)
            rv = self.app.post(url_for('event_insert', code='E8'),
                               data={'name': event_name2,
                                     'given_place': [residence_id],
                                     'place': residence_id,
                                     'event': activity_id,
                                     'begin_year_from': '1949',
                                     'begin_month_from': '10',
                                     'begin_day_from': '8',
                                     'end_year_from': '1951'})
            event_id = rv.location.split('/')[-1]
            rv = self.app.get(url_for('entity_view', id_=event_id))
            assert bytes(event_name, 'utf-8') in rv.data

            # Move
            rv = self.app.post(url_for('event_insert', code='E9'),
                               data={'name': 'Keep it moving',
                                     'place_to': residence_id,
                                     'place_from': residence_id,
                                     'object': carrier.id,
                                     'person': actor.id})
            move_id = rv.location.split('/')[-1]
            rv = self.app.get(url_for('entity_view', id_=move_id))
            assert b'Keep it moving' in rv.data
            rv = self.app.get(url_for('event_update', id_=move_id))
            assert b'Keep it moving' in rv.data

            # Add another event and test if events are seen at place
            event_name3 = random_string()
            self.app.post(url_for('event_insert', code='E8'),
                          data={'name': event_name3, 'given_place': [residence_id]})
            rv = self.app.get(url_for('entity_view', id_=residence_id))
            assert bytes(place_name, 'utf-8') in rv.data
            rv = self.app.get(url_for('entity_view', id_=actor.id))
            assert bytes(actor_name, 'utf-8') in rv.data
            rv = self.app.post(url_for('event_insert', code='E8'), follow_redirects=True,
                               data={'name': event_name, 'continue_': 'yes'})
            assert b'An entry has been created' in rv.data
            rv = self.app.get(url_for('event_index'))
            assert b'Event' in rv.data
            self.app.get(url_for('entity_view', id_=activity_id))

            # Add to event
            rv = self.app.get(url_for('entity_add_file', id_=event_id))
            assert b'Link File' in rv.data
            rv = self.app.post(url_for('entity_add_file', id_=event_id),
                               data={'checkbox_values': str([file.id])}, follow_redirects=True)
            assert b'X-Files' in rv.data

            rv = self.app.get(url_for('entity_add_reference', id_=event_id))
            assert b'Link Reference' in rv.data
            rv = self.app.post(url_for('entity_add_reference', id_=event_id),
                               data={'reference': reference.id, 'page': '777'},
                               follow_redirects=True)
            assert b'777' in rv.data

            # Update
            rv = self.app.get(url_for('event_update', id_=activity_id))
            assert bytes(event_name, 'utf-8') in rv.data
            rv = self.app.get(url_for('event_update', id_=event_id))
            assert bytes(event_name, 'utf-8') in rv.data
            data = {'name': 'Event updated'}
            rv = self.app.post(url_for('event_update', id_=event_id),
                               data=data,
                               follow_redirects=True)
            assert b'Event updated' in rv.data

            # Test super event validation
            data = {'name': 'Event Horizon', 'event': event_id}
            rv = self.app.post(url_for('event_update', id_=event_id),
                               data=data,
                               follow_redirects=True)
            assert b'error' in rv.data

            # Delete
            rv = self.app.get(url_for('event_index', action='delete', id_=event_id))
            assert b'The entry has been deleted.' in rv.data
