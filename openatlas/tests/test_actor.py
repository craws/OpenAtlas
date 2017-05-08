# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from openatlas.test_base import TestBaseCase


class ActorTests(TestBaseCase):

    def test_actor(self):
        response = self.app.get('/actor')
        #assert 'Overview' in response.data
