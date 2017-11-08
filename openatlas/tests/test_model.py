# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import url_for, current_app

from openatlas import app, PropertyMapper, EntityMapper
from openatlas.models.classObject import ClassMapper
from openatlas.models.link import LinkMapper
from openatlas.test_base import TestBaseCase


class ModelTests(TestBaseCase):

    def test_model(self):
        with app.app_context():
            rv = self.app.get(url_for('model_index'))
            assert b'Browse' in rv.data
            rv = self.app.get(url_for('class_index'))
            assert b'E1' in rv.data
            rv = self.app.get(url_for('class_view', class_id=ClassMapper.get_by_code('E2').id))
            assert b'E2' in rv.data
            rv = self.app.get(url_for('property_index'))
            assert b'P1' in rv.data
            rv = self.app.get(
                url_for('property_view', property_id=PropertyMapper.get_by_code('P68').id))
            assert b'P68' in rv.data
            form_data = {
                'domain': ClassMapper.get_by_code('E1').id,
                'range': ClassMapper.get_by_code('E1').id,
                'property': PropertyMapper.get_by_code('P1').id}
            rv = self.app.post(url_for('model_index'), data=form_data)
            assert b'Wrong' in rv.data
            self.login()
            # insert some data for network
            actor = EntityMapper.insert('E21', 'King Arthur')
            event = EntityMapper.insert('E7', 'Battle of Camlann')
            prop_object = EntityMapper.insert('E89', 'Propositional Object')
            with current_app.test_request_context():
                LinkMapper.insert(actor, 'P11', event)
                LinkMapper.insert(actor, 'P67', prop_object)
            rv = self.app.get(url_for('model_network'))
            assert b'Orphans' in rv.data
            rv = self.app.post(
                url_for('model_network'),
                data={'orphans': True, 'width': 100, 'height': 40, 'distance': -666, 'charge': 500})
            assert b'666' in rv.data
