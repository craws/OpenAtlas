# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from openatlas.test_base import TestBaseCase


class ReferenceTest(TestBaseCase):

    def test_reference(self):
        response = self.app.get('/reference')
        #assert 'Overview' in response.data
