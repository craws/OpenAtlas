from flask import url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.test_base import TestBaseCase


class SearchTest(TestBaseCase):

    def test_search(self):
        self.login()
        with app.test_request_context():
            app.preprocess_request()
            person = EntityMapper.insert('E21', 'Waldo')
            person.begin_to = '2018-01-01'
            person.update()
            person.link('P131', EntityMapper.insert('E82', 'Waldo alias'))
            object_ = EntityMapper.insert('E18', 'Waldorf', 'place')
            object_.link('P1', EntityMapper.insert('E41', 'Waldorf alias'))
            EntityMapper.insert('E21', 'Waldo without date')
        with app.app_context():
            self.app.post(url_for('search_index'), data={'global-term': ''})
            rv = self.app.post(url_for('search_index'), data={'global-term': 'wal',
                                                              'include_dateless': True,
                                                              'begin_year': -100, 'end_year': 3000})
            assert b'Waldo' in rv.data
            rv = self.app.post(url_for('search_index'), data={'term': 'wal', 'own': True})
            assert b'Waldo' not in rv.data
            data = {'term': 'do', 'classes': 'actor'}
            rv = self.app.post(url_for('search_index'), data=data)
            assert b'Waldo' in rv.data
            rv = self.app.post(url_for('search_index'), follow_redirects=True,
                               data={'term': 'x', 'begin_year': 2, 'end_year': -1})
            assert b'cannot start after' in rv.data
