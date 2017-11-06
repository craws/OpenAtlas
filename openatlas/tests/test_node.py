# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import url_for

from openatlas import app
from openatlas.test_base import TestBaseCase


class NodeTest(TestBaseCase):

    def test_node(self):
        self.login()
        with app.app_context():
            rv = self.app.get(url_for('node_index'))
            assert b'Actor Actor Relation' in rv.data
