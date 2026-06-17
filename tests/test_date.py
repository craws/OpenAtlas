from flask import url_for

from openatlas import app
from tests.base import TestBaseCase

from openatlas.display.util import format_entity_date
from openatlas.models.dates import Dates


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

            # An end date inside the begin span is rejected
            data['begin_year_to'] = 7
            data['begin_year_from'] = 5
            data['end_year_from'] = 6
            data['end_year_to'] = ''
            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'Begin dates cannot start after end dates' in rv.data

            # A standalone *_to date (without *_from) is now allowed
            data['begin_year_from'] = ''
            data['begin_year_to'] = ''
            data['end_year_from'] = ''
            data['end_year_to'] = ''
            rv = c.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'Date place' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            dates_with_only_to = Dates({
                'begin_to': '1500-12-31 00:00:00',
                'begin_comment': 'Test Comment'})
            formatted_only_to_date = format_entity_date(
                dates_with_only_to,
                'begin',
                with_comment=True)
            assert formatted_only_to_date == 'by 1500-12-31 (Test Comment)'

            dates_with_only_from = Dates({
                'begin_from': '1400-01-01 00:00:00'})
            formatted_only_from_date = format_entity_date(
                dates_with_only_from,
                'begin')
            assert formatted_only_from_date == 'from 1400-01-01'

            dates_with_both_from_and_to = Dates({
                'begin_from': '1400-01-01 00:00:00',
                'begin_to': '1500-12-31 00:00:00'})
            formatted_between_date = format_entity_date(
                dates_with_both_from_and_to,
                'begin')
            assert formatted_between_date == \
                   'between 1400-01-01 and 1500-12-31'
