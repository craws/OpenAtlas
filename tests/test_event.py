from typing import Any

from flask import g, url_for

from openatlas import app
from tests.base import TestBaseCase, insert


class EventTest(TestBaseCase):

    def test_event(self) -> None:
        with app.test_request_context():
            app.preprocess_request()
            actor = insert('person', 'Captain Miller')
            file = insert('file', 'X-Files')
            artifact = insert('artifact', 'artifact')
            residence = insert('place', 'Lewis and Clark')
            reference = insert('external_reference', 'https://d-nb.info')

        data = {'name': 'Event Horizon', 'location': residence.id}
        rv: Any = self.app.post(
            url_for('insert', class_='activity'),
            data=data)
        activity_id = rv.location.split('/')[-1]

        rv = self.app.post(
            url_for('insert', class_='activity', origin_id=actor.id),
            data=data,
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        rv = self.app.post(
            url_for('insert', class_='activity', origin_id=file.id),
            data=data,
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        rv = self.app.get(
            url_for('insert', class_='activity', origin_id=residence.id))
        assert b'location' in rv.data

        rv = self.app.get(
            url_for('insert', class_='move', origin_id=residence.id))
        assert b'Moved artifact' in rv.data

        data = {
            'name': 'Second event',
            'given_place': [residence.id],
            'given_artifact': '',
            'location': residence.id,
            'sub_event_of': activity_id,
            'begin_year_from': '1949',
            'begin_month_from': '10',
            'begin_day_from': '8',
            'end_year_from': '1951',
            'event_preceding': '',
            f'reference_system_id_{g.wikidata.id}':
                ['Q123', self.precision_type.subs[0]]}

        rv = self.app.post(url_for('insert', class_='acquisition'), data=data)
        event_id = rv.location.split('/')[-1]

        data['end_year_from'] = '7'
        rv = self.app.post(url_for('insert', class_='acquisition'), data=data)
        assert b'Begin dates cannot start after end dates' in rv.data

        rv = self.app.post(
            url_for('insert', class_='move'),
            data={
                'name': 'Keep it moving',
                'place_to': residence.id,
                'place_from': residence.id,
                'moved_artifact': artifact.id,
                'moved_person': actor.id})
        move_id = rv.location.split('/')[-1]

        rv = self.app.get(url_for('view', id_=move_id))
        assert b'Keep it moving' in rv.data

        rv = self.app.get(url_for('view', id_=artifact.id))
        assert b'Keep it moving' in rv.data

        rv = self.app.get(url_for('update', id_=move_id))
        assert b'Keep it moving' in rv.data

        rv = self.app.get(
            url_for('insert', class_='creation', origin_id=file.id))
        assert b'+ Creation' in rv.data

        rv = self.app.post(
            url_for('insert', class_='creation'),
            data={'name': 'A creation event', 'file': file.id})
        creation_id = rv.location.split('/')[-1]

        rv = self.app.get(url_for('view', id_=creation_id, origin_id=file.id))
        assert b'File' in rv.data

        rv = self.app.get(url_for('update', id_=creation_id))
        assert b'A creation event' in rv.data

        rv = self.app.post(
            url_for('insert', class_='modification'),
            data={
                'name': 'A modification event',
                'artifact': artifact.id,
                'modified_place': residence.id})
        modification_id = rv.location.split('/')[-1]

        rv = self.app.get(url_for('view', id_=modification_id))
        assert b'A modification event' in rv.data

        rv = self.app.get(url_for('update', id_=modification_id))
        assert b'A modification event' in rv.data

        rv = self.app.post(
            url_for('insert', class_='production'),
            data={'name': 'A productive event', 'artifact': artifact.id})
        production_id = rv.location.split('/')[-1]

        rv = self.app.get(url_for('view', id_=production_id))
        assert b'artifact' in rv.data

        rv = self.app.get(url_for('view', id_=artifact.id))
        assert b'A productive event' in rv.data

        rv = self.app.get(url_for('update', id_=production_id))
        assert b'A productive event' in rv.data

        rv = self.app.post(
            url_for('insert', class_='acquisition'),
            data={'name': 'Third event', 'given_place': [residence.id]},
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        rv = self.app.get(url_for('view', id_=residence.id))
        assert bytes('Lewis and Clark', 'utf-8') in rv.data

        rv = self.app.get(url_for('view', id_=actor.id))
        assert bytes('Captain Miller', 'utf-8') in rv.data

        rv = self.app.post(
            url_for('insert', class_='acquisition'),
            data={'name': 'Event Horizon', 'continue_': 'yes'},
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        rv = self.app.get(url_for('view', id_=activity_id))
        assert b'1949' in rv.data

        rv = self.app.get(url_for('entity_add_file', id_=event_id))
        assert b'link file' in rv.data

        rv = self.app.post(
            url_for('entity_add_file', id_=event_id),
            data={'checkbox_values': str([file.id])},
            follow_redirects=True)
        assert b'X-Files' in rv.data

        rv = self.app.post(
            url_for('entity_add_reference', id_=event_id),
            data={'reference': reference.id, 'page': '777'},
            follow_redirects=True)
        assert b'777' in rv.data

        rv = self.app.get(url_for('update', id_=activity_id))
        assert b'Event Horizon' in rv.data

        rv = self.app.get(url_for('update', id_=event_id))
        assert b'Event Horizon' in rv.data

        rv = self.app.post(
            url_for('update', id_=event_id),
            data={
                'name': 'Event with preceding',
                'event_preceding': activity_id,
                'event_id': event_id},
            follow_redirects=True)
        assert b'Event with preceding' in rv.data

        rv = self.app.get(url_for('update', id_=event_id))
        assert b'Event with preceding' in rv.data
