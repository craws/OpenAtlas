from typing import Any

from flask import url_for

from openatlas import app
from openatlas.models.entity import Entity
from tests.base import TestBaseCase, insert_entity


class EventTest(TestBaseCase):

    def test_event(self) -> None:
        with app.app_context():
            place_name = 'Lewis and Clark'
            rv: Any = self.app.post(
                url_for('insert', class_='place'),
                data={
                    'name': place_name,
                    })
            residence_id = rv.location.split('/')[-1]
            actor_name = 'Captain Miller'
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                actor = Entity.insert('person', actor_name)
                file = Entity.insert('file', 'X-Files')
                source = Entity.insert('source', 'Necronomicon')
                artifact = insert_entity('artifact', 'artifact')
                reference = Entity.insert(
                    'external_reference',
                    'https://openatlas.eu')

            rv = self.app.get(url_for('insert', class_='activity'))
            assert b'+ Activity' in rv.data

            data = {
                'name': 'Event Horizon',
                'place': residence_id,
                }
            rv = self.app.post(
                url_for('insert', class_='activity', origin_id=reference.id),
                data=data,
                follow_redirects=True)
            assert bytes('Event Horizon', 'utf-8') in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                activity_id = Entity.get_by_view('event')[0].id
            self.app.post(
                url_for('insert', class_='activity', origin_id=actor.id),
                data=data)
            self.app.post(
                url_for('insert', class_='activity', origin_id=file.id),
                data=data)
            self.app.post(
                url_for('insert', class_='activity', origin_id=source.id),
                data=data)
            rv = self.app.get(
                url_for('insert', class_='activity', origin_id=residence_id))
            assert b'Location' in rv.data

            rv = self.app.get(
                url_for('insert', class_='move', origin_id=residence_id))
            assert b'Location' not in rv.data

            event_name2 = 'Second event'
            rv = self.app.post(
                url_for('insert', class_='acquisition'),
                data={
                    'name': event_name2,
                    'given_place': [residence_id],
                    'place': residence_id,
                    'event': activity_id,
                    'begin_year_from': '1949',
                    'begin_month_from': '10',
                    'begin_day_from': '8',
                    'end_year_from': '1951',
                    self.wikidata: ['Q123', self.precision_type.subs[0]]
                })
            event_id = rv.location.split('/')[-1]

            rv = self.app.get(url_for('view', id_=event_id))
            assert b'Event Horizon' in rv.data

            rv = self.app.post(
                url_for('insert', class_='move'),
                data={
                    'name': 'Keep it moving',
                    'place_to': residence_id,
                    'place_from': residence_id,
                    'artifact': artifact.id,
                    'person': actor.id,
                    })
            move_id = rv.location.split('/')[-1]

            rv = self.app.get(url_for('view', id_=move_id))
            assert b'Keep it moving' in rv.data

            rv = self.app.get(url_for('view', id_=artifact.id))
            assert b'Keep it moving' in rv.data

            rv = self.app.get(url_for('update', id_=move_id))
            assert b'Keep it moving' in rv.data

            rv = self.app.post(
                url_for('insert', class_='production'),
                data={
                    'name': 'A very productive event',
                    'artifact': artifact.id,
                    })
            production_id = rv.location.split('/')[-1]
            rv = self.app.get(url_for('view', id_=production_id))
            assert b'Artifact' in rv.data

            rv = self.app.get(url_for('view', id_=artifact.id))
            assert b'A very productive event' in rv.data

            rv = self.app.get(url_for('update', id_=production_id))
            assert b'A very productive event' in rv.data

            event_name3 = 'Third event'
            self.app.post(url_for('insert', class_='acquisition'), data={
                'name': event_name3,
                'given_place': [residence_id],
                })
            rv = self.app.get(url_for('view', id_=residence_id))
            assert bytes(place_name, 'utf-8') in rv.data

            rv = self.app.get(url_for('view', id_=actor.id))
            assert bytes(actor_name, 'utf-8') in rv.data

            rv = self.app.post(
                url_for('insert', class_='acquisition'),
                follow_redirects=True,
                data={
                    'name': 'Event Horizon',
                    'continue_': 'yes',
                    })
            assert b'An entry has been created' in rv.data

            rv = self.app.get(url_for('index', view='event'))
            assert b'Event' in rv.data

            rv = self.app.get(url_for('view', id_=activity_id))
            assert b'1949' in rv.data

            rv = self.app.get(url_for('entity_add_file', id_=event_id))
            assert b'Link file' in rv.data

            rv = self.app.post(
                url_for('entity_add_file', id_=event_id),
                data={'checkbox_values': str([file.id])},
                follow_redirects=True)
            assert b'X-Files' in rv.data

            rv = self.app.get(url_for('entity_add_reference', id_=event_id))
            assert b'Link reference' in rv.data

            rv = self.app.post(
                url_for('entity_add_reference', id_=event_id),
                data={'reference': reference.id, 'page': '777'},
                follow_redirects=True)
            assert b'777' in rv.data

            rv = self.app.get(url_for('update', id_=activity_id))
            assert b'Event Horizon' in rv.data

            rv = self.app.get(url_for('update', id_=event_id))
            assert b'Event Horizon' in rv.data

            data['name'] = 'Event updated'
            rv = self.app.post(
                url_for('update', id_=event_id),
                data=data,
                follow_redirects=True)
            assert b'Changes have been saved' in rv.data

            rv = self.app.post(
                url_for('update', id_=event_id),
                data={
                    'name': 'Event with preceding',
                    'event_preceding': activity_id,
                    'event_id': event_id},
                follow_redirects=True)
            assert b'Event with preceding' in rv.data

            rv = self.app.get(url_for('view', id_=activity_id))
            assert b'Event with preceding' in rv.data

            rv = self.app.get(url_for('update', id_=event_id))
            assert b'Event with preceding' in rv.data

            rv = self.app.get(
                url_for('index', view='event', delete_id=event_id))
            assert b'The entry has been deleted.' in rv.data
