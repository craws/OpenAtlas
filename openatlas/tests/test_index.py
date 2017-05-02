# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from openatlas.test_base import TestBaseCase


class IndexTestCase(TestBaseCase):

    def test_index(self):
        response = self.app.get('/')
        assert 'Overview' in response.data
        response = self.app.get('/some_missing_site')
        assert '404' in response.data
        response = self.app.get('/index/changelog')
        assert 'Version' in response.data
        response = self.app.get('/index/contact')
        assert 'Contact' in response.data
        response = self.app.get('/index/credits')
        assert 'Stefan Eichert' in response.data
        response = self.app.get('/index/faq')
        assert 'Faq' in response.data
        self.app.get('/index/setlocale/en')
