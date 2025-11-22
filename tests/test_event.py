from flask import g, url_for

from openatlas import app
from tests.base import TestBaseCase, insert


class EventTest(TestBaseCase):

    def test_event(self) -> None:
        c = self.client
        with app.test_request_context():
            app.preprocess_request()
            actor = insert('person', 'Captain Miller')
            file = insert('file', 'X-Files')
            artifact = insert('artifact', 'artifact new')
            residence = insert('place', 'Lewis and Clark')

        data = {'name': 'Event Horizon', 'location': residence.id}
        rv = c.post(url_for('insert', class_='activity'), data=data)
        activity_id = rv.location.split('/')[-1]

        rv = c.post(
            url_for('insert', class_='activity'),
            data=data,
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        rv = c.post(
            url_for('insert', class_='activity', origin_id=file.id),
            data=data,
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        rv = c.get(url_for('insert', class_='activity'))
        assert b'Location' in rv.data

        rv = c.get(url_for('insert', class_='move', origin_id=residence.id))
        assert b'Moved object' in rv.data

        rv = c.get(url_for('insert', class_='acquisition'))
        assert b'+ Acquisition' in rv.data

        data = {
            'name': 'Second event',
            'given_place': [residence.id],
            'given_artifact': '',
            'location': residence.id,
            'begin_year_from': '1949',
            'begin_month_from': '10',
            'begin_day_from': '8',
            'end_year_from': '1951',
            'preceding_event': '',
            'super': activity_id,
            'recipient': '',
            'donor': '',
            f'reference_system_id_{g.wikidata.id}':
                ['Q123', self.precision_type.subs[0]]}

        rv = c.post(url_for('insert', class_='acquisition'), data=data)
        event_id = rv.location.split('/')[-1]

        data['end_year_from'] = '7'
        rv = c.post(url_for('insert', class_='acquisition'), data=data)
        assert b'Begin dates cannot start after end dates' in rv.data

        rv = c.post(
            url_for('insert', class_='move'),
            data={
                'name': 'Keep it moving',
                'place_to': residence.id,
                'place_from': residence.id,
                'moved_object': artifact.id,
                'moved_person': actor.id})
        move_id = rv.location.split('/')[-1]

        rv = c.get(url_for('view', id_=move_id))
        assert b'Keep it moving' in rv.data

        rv = c.get(url_for('view', id_=artifact.id))
        assert b'Keep it moving' in rv.data

        rv = c.get(url_for('update', id_=move_id))
        assert b'Keep it moving' in rv.data

        rv = c.get(
            url_for('insert', class_='modification', origin_id=artifact.id))
        assert b'+ Modification' in rv.data

        rv = c.post(
            url_for('insert', class_='modification'),
            data={
                'name': 'A modification event',
                'modified_object': str([artifact.id]),
                'modified_place': residence.id})
        modification_id = rv.location.split('/')[-1]

        rv = c.get(url_for('view', id_=modification_id))
        assert b'artifact new' in rv.data

        rv = c.get(url_for('update', id_=modification_id))
        assert b'A modification event' in rv.data

        rv = c.post(
            url_for('insert', class_='production'),
            data={
                'name': 'A productive event',
                'produced_artifact': artifact.id})
        production_id = rv.location.split('/')[-1]
        rv = c.get(url_for('view', id_=production_id))

        assert b'artifact new' in rv.data

        rv = c.get(url_for('view', id_=artifact.id))
        assert b'A productive event' in rv.data

        rv = c.get(url_for('update', id_=production_id))
        assert b'A productive event' in rv.data

        rv = c.get(url_for('insert', class_='production'))
        assert b'+ Production' in rv.data

        rv = c.post(
            url_for('insert', class_='acquisition'),
            data={'name': 'Third event', 'given_place': [residence.id]},
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        rv = c.get(url_for('view', id_=residence.id))
        assert bytes('Lewis and Clark', 'utf-8') in rv.data

        rv = c.get(url_for('view', id_=actor.id))
        assert bytes('Captain Miller', 'utf-8') in rv.data

        rv = c.post(
            url_for('insert', class_='acquisition'),
            data={'name': 'Event Horizon', 'continue_': 'yes'},
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        rv = c.post(
            url_for('link_insert', origin_id=event_id, name='file'),
            data={'checkbox_values': str([file.id])},
            follow_redirects=True)
        assert b'X-Files' in rv.data

        rv = c.get(url_for('update', id_=activity_id))
        assert b'Event Horizon' in rv.data

        rv = c.get(url_for('update', id_=event_id))
        assert b'Event Horizon' in rv.data

        rv = c.post(
            url_for('update', id_=event_id),
            data={
                'name': 'Event with preceding',
                'preceding_event': activity_id,
                'event_id': event_id},
            follow_redirects=True)
        assert b'Event with preceding' in rv.data

        rv = c.get(url_for('update', id_=event_id))
        assert b'Event with preceding' in rv.data
