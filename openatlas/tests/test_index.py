# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
# -*- coding: utf-8 -*-
from openatlas.test_base import TestBaseCase


class IndexTestCase(TestBaseCase):

    def test_index(self):
        response = self.app.get('/')
        assert b'Overview' in response.data
        # response = self.app.get('/some_missing_site')
        # assert b'404' in response.data
        response = self.app.get('/index/changelog')
        assert b'Version' in response.data
        response = self.app.get('/index/contact')
        assert b'Contact' in response.data  # needs better assertion
        response = self.app.get('/index/credits')
        assert b'Stefan Eichert' in response.data
        response = self.app.get('/index/faq')
        assert b'Faq' in response.data  # needs better assertion
        self.app.get('/index/setlocale/de')  # needs assertion
