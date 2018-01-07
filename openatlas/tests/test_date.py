# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import url_for

from openatlas import app
from openatlas.test_base import TestBaseCase


class DateTest(TestBaseCase):

    def test_date(self):
        self.login()
        with app.app_context():

            # dates insert
            data = {
                'name': 'Date place',
                'date_begin_year': -1949,
                'date_begin_month': 2,
                'date_begin_day': 8,
                'date_begin_year2': -1948,
                'date_end_year': 2040,
                'date_end_year2': 2050,
                'date_birth': True,
                'date_death': True}
            rv = self.app.post(url_for('place_insert'), data=data, follow_redirects=True)
            assert b'Date place' in rv.data

            data['date_begin_day'] = 31  # test invalid dates
            rv = self.app.post(url_for('place_insert'), data=data, follow_redirects=True)
            assert b'Not a valid date' in rv.data

            data['date_begin_day'] = 5
            data['date_begin_year'] = 20  # test invalid time span (first after second date)
            rv = self.app.post(url_for('place_insert'), data=data, follow_redirects=True)
            assert b'First date cannot be after second' in rv.data

            data['date_begin_year'] = -1949
            data['date_end_year'] = -2000  # test invalid begin dates which are after end dates
            rv = self.app.post(url_for('place_insert'), data=data, follow_redirects=True)
            assert b'Begin dates cannot start after end dates' in rv.data
            data['date_end_year2'] = ''
            rv = self.app.post(url_for('place_insert'), data=data, follow_redirects=True)
            assert b'Begin dates cannot start after end dates' in rv.data
