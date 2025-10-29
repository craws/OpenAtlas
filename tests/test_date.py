from flask import url_for

from openatlas import app
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
                'begin_year_to': -1948,
                'end_year_from': 1996,
                'end_year_to': 1996}

            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)

            return  # Todo: continue tests

            assert b'Date place' in rv.data

            data['begin_day_from'] = 31
            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'not a valid date' in rv.data

            data['begin_day_from'] = 5
            data['begin_year_from'] = 20
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

            data['begin_year_from'] = ''
            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'Required for time span' in rv.data
