from flask import url_for

from openatlas import app
from tests.base import TestBaseCase, insert


class SearchTest(TestBaseCase):

    def test_search(self) -> None:
        c = self.client
        with app.test_request_context():
            app.preprocess_request()
            person = insert('person', 'Waldo')
            person.update({'attributes': {'begin_to': '2018-01-01'}})
            person.link('P1', insert('appellation', 'Waldo alias'))
            object_ = insert('place', 'Waldorf')
            object_.link('P1', insert('appellation', 'Waldorf alias'))
            insert('person', 'Waldo without date')

        rv = c.post(url_for('search_index'), data={'global-term': ''})
        assert b'no entries' in rv.data

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
