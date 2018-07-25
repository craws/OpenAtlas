from flask import url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.test_base import TestBaseCase


class SearchTest(TestBaseCase):

    def test_search(self):
        self.login()
        with app.test_request_context():
            app.preprocess_request()
            LinkMapper.insert(
                EntityMapper.insert('E21', 'Waldo'),
                'P131',
                EntityMapper.insert('E82', 'Waldo alias'))
            LinkMapper.insert(
                EntityMapper.insert('E18', 'Waldorf'),
                'P1',
                EntityMapper.insert('E41', 'Waldorf alias'))

        with app.app_context():
            rv = self.app.post(url_for('index_search'), data={'global-term': 'wal'})
            assert b'Waldo' in rv.data
            rv = self.app.post(url_for('index_search'), data={'global-term': 'wal', 'own': True})
            assert b'Waldo' not in rv.data
            data = {'term': 'do', 'classes': 'actor'}
            rv = self.app.post(url_for('index_search'), data=data)
            assert b'Waldo' in rv.data
