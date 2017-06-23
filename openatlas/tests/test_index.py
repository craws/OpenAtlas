# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from openatlas.test_base import TestBaseCase


class IndexTests(TestBaseCase):

    def test_index(self):
        rv = self.app.get('/')
        assert 'Overview' in rv.data
        rv = self.app.get('/some_missing_site')
        assert '404' in rv.data
        rv = self.app.get('/index/changelog')
        assert 'Version' in rv.data
        rv = self.app.get('/index/contact')
        assert 'Contact' in rv.data
        rv = self.app.get('/index/credits')
        assert 'Stefan Eichert' in rv.data
        rv = self.app.get('/index/faq')
        assert 'Faq' in rv.data
        self.app.get('/index/setlocale/en')
