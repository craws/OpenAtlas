# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from openatlas.test_base import TestBaseCase


class NodeTest(TestBaseCase):

    def test_node(self):
        self.login()
        rv = self.app.get('/node')
        assert b'Overview' in rv.data
