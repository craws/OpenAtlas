# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from openatlas.test_base import TestBaseCase


class HierachyTest(TestBaseCase):

    def test_hierarchy(self):
        rv = self.app.get('/hierarchy')
        #assert 'Overview' in rv.data
