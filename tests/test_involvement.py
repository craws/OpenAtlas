from typing import Any

from flask import url_for

from openatlas import app
from openatlas.models.link import Link
from tests.base import TestBaseCase, insert_entity


class InvolvementTests(TestBaseCase):

    def test_involvement(self) -> None:
        with app.app_context():
            rv: Any = self.app.post(
                url_for('insert', class_='acquisition'),
                data={
                    'name': 'Event Horizon',
                    'begin_year_from': '949',
                    'begin_month_from': '10',
                    'begin_day_from': '8',
                    'end_year_from': '1951'})
            event_id = int(rv.location.split('/')[-1])

            actor = insert_entity('person', 'Captain Miller')
            rv = self.app.post(
                url_for(
                    'insert_relation',
                    type_='involvement',
                    origin_id=actor.id),
                data={
                    'event': str([event_id]),
                    'activity': 'P11',
                    'begin_year_from': '950',
                    'end_year_from': '1950'},
                follow_redirects=True)
            assert b'Event Horizon' in rv.data

            rv = self.app.post(
                url_for(
                    'insert_relation',
                    type_='involvement',
                    origin_id=event_id),
                data={
                    'actor': str([actor.id]),
                    'continue_': 'yes',
                    'activity': 'P22'},
                follow_redirects=True)
            assert b'Event Horizon' in rv.data

            rv = self.app.get(url_for('view', id_=event_id))
            assert b'Event Horizon' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                link_ = Link.get_links(event_id, 'P22')[0]

            rv = self.app.post(
                url_for('link_update', id_=link_.id, origin_id=actor.id),
                data={
                    'description': 'Infinite Space - Infinite Terror',
                    'activity': 'P23'},
                follow_redirects=True)
            assert b'Infinite Space - Infinite Terror' in rv.data
