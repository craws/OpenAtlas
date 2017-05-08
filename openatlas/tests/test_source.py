# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from openatlas.test_base import TestBaseCase


class SourceTest(TestBaseCase):

    def test_source(self):
        response = self.app.get('/source')
        #assert 'Overview' in response.data
