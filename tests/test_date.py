from flask import url_for

from openatlas import app
from openatlas.display.util import format_entity_date
from openatlas.models.dates import Dates
from tests.base import TestBaseCase


class DateTest(TestBaseCase):
    def test_date(self) -> None:
        c = self.client
        with app.app_context():
            data = {  # Don't change year values, needed for leap years
                'name': 'Date place',
                'begin_year_from': -1949,
                'begin_month_from': 2,
                'begin_day_from': 8,
                'begin_comment': 'it was a sunny day',
                'begin_year_to': -1948,
                'end_year_from': 1996,
                'end_year_to': 1996}

            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'Date place' in rv.data

            data['begin_year_from'] = ''
            data['begin_month_from'] = ''
            data['begin_day_from'] = ''
            data['begin_year_to'] = ''
            data['end_year_from'] = ''
            data['end_year_to'] = 1220
            data['end_month_to'] = 10
            data['end_day_to'] = 4
            data['end_comment'] = 'latest end bound'
            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'Date place' in rv.data
            assert b'by 1220-10-04' in rv.data
            place_id = int(rv.request.path.split('/')[-1])
            rv = c.get(url_for('update', id_=place_id))
            assert b'>Hide<' in rv.data

            data['begin_year_to'] = 1300
            data['begin_month_to'] = ''
            data['begin_day_to'] = ''
            data['end_year_to'] = 1200
            data['end_month_to'] = ''
            data['end_day_to'] = ''
            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'Begin dates cannot start after end dates' in rv.data

            data['begin_year_from'] = 1100
            data['begin_month_from'] = ''
            data['begin_day_from'] = ''
            data['begin_year_to'] = ''
            data['end_year_from'] = ''
            data['end_year_to'] = 1200
            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'Date place' in rv.data

            data['begin_month_from'] = 2
            data['begin_day_from'] = 31
            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'not a valid date' in rv.data

            data['begin_day_from'] = 5
            data['begin_year_from'] = 20
            data['begin_year_to'] = 10
            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'First date cannot be after second' in rv.data

            data['begin_year_from'] = -1949
            data['end_year_from'] = -2000
            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'Begin dates cannot start after end dates' in rv.data

            data['end_year_to'] = ''
            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'Begin dates cannot start after end dates' in rv.data

            data['begin_year_to'] = 7
            data['begin_year_from'] = 5
            data['end_year_from'] = ''
            data['end_year_to'] = 4
            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'Begin dates cannot start after end dates' in rv.data

            data['end_year_from'] = 6
            data['end_year_to'] = 8
            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'Date place' in rv.data
            assert rv.request.path.startswith('/entity/')

            data['begin_year_from'] = 1400
            data['begin_month_from'] = 5
            data['begin_day_from'] = 5
            data['begin_year_to'] = 1400
            data['begin_month_to'] = 5
            data['begin_day_to'] = 5
            data['end_year_from'] = 1400
            data['end_month_from'] = 5
            data['end_day_from'] = 5
            data['end_year_to'] = 1400
            data['end_month_to'] = 5
            data['end_day_to'] = 5
            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'Date place' in rv.data
            assert rv.request.path.startswith('/entity/')

            rv = c.post(
                url_for('insert', class_='place'),
                data={
                    'name': 'Date place',
                    'begin_year_from': 1500,
                    'end_year_to': 1400},
                follow_redirects=True)
            assert b'Begin dates cannot start after end dates' in rv.data

            data['begin_year_from'] = ''
            data['begin_month_from'] = ''
            data['begin_day_from'] = ''
            data['begin_year_to'] = ''
            data['begin_month_to'] = ''
            data['begin_day_to'] = ''
            data['end_year_from'] = ''
            data['end_month_from'] = ''
            data['end_day_from'] = ''
            data['end_year_to'] = ''
            data['end_month_to'] = ''
            data['end_day_to'] = ''
            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'Date place' in rv.data

