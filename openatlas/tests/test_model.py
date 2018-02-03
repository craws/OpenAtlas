# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import url_for

from openatlas import app, EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.test_base import TestBaseCase


class ModelTests(TestBaseCase):

    def test_model(self):
        with app.app_context():
            rv = self.app.get(url_for('model_index'))
            assert b'Browse' in rv.data
            rv = self.app.get(url_for('class_index'))
            assert b'E1' in rv.data
            rv = self.app.get(url_for('class_view', code='E2'))
            assert b'E2' in rv.data
            rv = self.app.get(url_for('property_index'))
            assert b'P1' in rv.data
            rv = self.app.get(url_for('property_view', code='P68'))
            assert b'P68' in rv.data
            data = {'domain': 'E1', 'range': 'E1', 'property': 'P1'}
            rv = self.app.post(url_for('model_index'), data=data)
            assert b'Wrong' in rv.data
            self.login()
            # insert some data for network
            actor = EntityMapper.insert('E21', 'King Arthur')
            event = EntityMapper.insert('E7', 'Battle of Camlann')
            prop_object = EntityMapper.insert('E89', 'Propositional Object')
            with app.test_request_context():
                LinkMapper.insert(actor, 'P11', event)
                LinkMapper.insert(actor, 'P67', prop_object)
            rv = self.app.get(url_for('model_network'))
            assert b'Orphans' in rv.data
            rv = self.app.post(
                url_for('model_network'),
                data={'orphans': True, 'width': 100, 'height': 40, 'distance': -666, 'charge': 500})
            assert b'666' in rv.data
