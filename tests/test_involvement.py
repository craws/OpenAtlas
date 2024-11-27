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
                'insert_relation',
                type_='involvement',
                origin_id=actor.id),
            data={
                'event': str([event.id]),
                'activity': 'P11',
                'begin_year_from': '950',
                'end_year_from': '1950'},
            follow_redirects=True)
        assert b'Event Horizon' in rv.data

        rv = c.post(
            url_for(
                'insert_relation',
                type_='involvement',
                origin_id=event.id),
            data={
                'actor': str([actor.id]),
                'continue_': 'yes',
                'activity': 'P22'},
            follow_redirects=True)
        assert b'Event Horizon' in rv.data

        rv = c.get(url_for('view', id_=event.id))
        assert b'Event Horizon' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            link_ = event.get_links('P22')[0]

        rv = c.post(
            url_for('link_update', id_=link_.id, origin_id=actor.id),
            data={
                'description': 'Infinite Space - Infinite Terror',
                'activity': 'P23'},
            follow_redirects=True)
        assert b'Infinite Space - Infinite Terror' in rv.data
