# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from openatlas.test_base import TestBaseCase


class HierarchyTest(TestBaseCase):

    def test_hierarchy(self):
        self.login()
        rv = self.app.get('/hierarchy')
        assert b'Overview' in rv.data
