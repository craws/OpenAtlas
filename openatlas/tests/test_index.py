# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from openatlas.test_base import TestBaseCase


class IndexTests(TestBaseCase):

    def test_index(self):
        rv = self.app.get('/')
        assert b'Overview' in rv.data
        rv = self.app.get('/some_missing_site')
        assert b'404' in rv.data
        rv = self.app.get('/index/changelog')
        assert b'Version' in rv.data
        rv = self.app.get('/index/contact')
        assert b'Contact' in rv.data
        rv = self.app.get('/index/credits')
        assert b'Stefan Eichert' in rv.data
        rv = self.app.get('/index/faq')
        assert b'Faq' in rv.data
        self.app.get('/index/setlocale/en')
