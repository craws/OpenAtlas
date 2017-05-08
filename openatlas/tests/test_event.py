# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from openatlas.test_base import TestBaseCase


class EventTest(TestBaseCase):

    def test_event(self):
        response = self.app.get('/event')
        #assert 'Overview' in response.data
