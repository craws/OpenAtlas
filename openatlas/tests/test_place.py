# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from openatlas.test_base import TestBaseCase


class PlaceTest(TestBaseCase):

    def test_place(self):
        rv = self.app.get('/place')
        #assert 'Overview' in rv.data
