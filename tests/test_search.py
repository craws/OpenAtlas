from flask import url_for

from openatlas import app
from tests.base import TestBaseCase, insert


class SearchTest(TestBaseCase):
    def test_search(self) -> None:
        c = self.client
        with app.test_request_context():
            app.preprocess_request()
            person = insert('person', 'Waldo', begin_to='2018-01-01')
            person.link('P1', insert('alias', 'Waldo alias'))
            object_ = insert('place', 'Waldorf')
            object_.link('P1', insert('alias', 'Waldorf alias'))
            insert('person', 'Waldo without date')

        rv = c.post(url_for('search_index'), data={'global-term': ''})
        assert b'No entries' in rv.data

        rv = c.post(
            url_for('search_index'),
            data={
                'global-term': 'wal',
                'include_dateless': True,
                'begin_year': -100})
        assert b'Waldo' in rv.data

        rv = c.post(
            url_for('search_index'),
            data={'term': 'do', 'end_year': 3000, 'classes': 'person'})
        assert b'Waldo' in rv.data

        rv = c.post(
            url_for('search_index'),
            data={'term': 'do', 'classes': 'person'})
        assert b'Waldo' in rv.data

        rv = c.post(
            url_for('search_index'),
            data={'term': 'x', 'begin_year': 2, 'end_year': -1})
        assert b'cannot start after' in rv.data

        for invalid_data in [
            {'term': 'x', 'begin_month': 13},
            {'term': 'x', 'begin_month': 5},
            {'term': 'x', 'begin_year': 2020, 'begin_day': 5},
            {'term': 'x', 'begin_year': 2019, 'begin_month': 2,
             'begin_day': 29},
            {'term': 'x', 'end_month': 13},
            {'term': 'x', 'end_month': 5},
            {'term': 'x', 'end_year': 2020, 'end_day': 5},
            {'term': 'x', 'end_year': 2020, 'end_month': 2,
             'end_day': 30},
            {'term': 'x', 'end_year': 2019, 'end_month': 2,
             'end_day': 29}]:
            rv = c.post(url_for('search_index'), data=invalid_data)
            assert (
                b'id="search-date-feedback" class="col-12 small mt-1 '
                b'text-danger fw-semibold">Not a valid date</div>'
            ) in rv.data

        for valid_data in [
            {'term': 'x', 'begin_year': 2020},
            {'term': 'x', 'begin_year': 2020, 'begin_month': 2},
            {'term': 'x', 'begin_year': 2020, 'begin_month': 2,
             'begin_day': 29},
            {'term': 'x', 'end_year': 2020},
            {'term': 'x', 'end_year': 2020, 'end_month': 2},
            {'term': 'x', 'end_year': 2020, 'end_month': 2,
             'end_day': 29}]:
            rv = c.post(url_for('search_index'), data=valid_data)
            assert (
                b'id="search-date-feedback" class="col-12 small mt-1 d-none"'
                b'></div>'
            ) in rv.data, valid_data
