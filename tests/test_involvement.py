from flask import url_for

from openatlas import app
from tests.base import TestBaseCase, insert


class InvolvementTests(TestBaseCase):

    def test_involvement(self) -> None:
        c = self.client
        with app.test_request_context():
            app.preprocess_request()
            actor = insert('person', 'Captain Miller')
            event = insert('acquisition', 'Event Horizon')

        rv = c.post(
            url_for('update', id_=event.id),
            data={
                 'name': 'Event Horizon',
                 'begin_year_from': '949',
                 'begin_month_from': '10',
                 'begin_day_from': '8',
                 'end_year_from': '1951'},
            follow_redirects=True)
        assert b'Event Horizon' in rv.data

        rv = c.post(
            url_for(
                'link_insert_detail',
                origin_id=actor.id,
                name='participated'),
            data={
                'participated': event.id,
                'begin_year_from': '',
                'end_year_from': ''},
            follow_redirects=True)
        assert b'Event Horizon' in rv.data

        rv = c.post(
            url_for(
                'link_insert_detail',
                origin_id=actor.id,
                name='participated'),
            data={
                'participated': event.id,
                'begin_year_from': '948',
                'end_year_from': '1952'},
            follow_redirects=True)
        assert b'Event Horizon' in rv.data

        rv = c.post(
            url_for(
                'link_insert_detail',
                origin_id=event.id,
                name='recipient'),
            data={'recipient': actor.id, 'continue_': 'yes'},
            follow_redirects=True)
        assert b'Event Horizon' in rv.data

        rv = c.get(url_for('view', id_=event.id))
        assert b'Event Horizon' in rv.data
