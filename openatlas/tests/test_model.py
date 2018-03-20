from flask import url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.test_base import TestBaseCase


class ModelTests(TestBaseCase):

    def test_model(self):
        with app.app_context():
            rv = self.app.get(url_for('model_index'))
            assert b'Browse' in rv.data
            rv = self.app.get(url_for('class_index'))
            assert b'E1' in rv.data
            rv = self.app.get(url_for('class_view', code='E4'))
            assert b'Domain for' in rv.data
            rv = self.app.get(url_for('property_index'))
            assert b'P1' in rv.data
            rv = self.app.get(url_for('property_view', code='P68'))
            assert b'P68' in rv.data
            data = {'domain': 'E1', 'range': 'E1', 'property': 'P13'}
            rv = self.app.post(url_for('model_index'), data=data)
            assert b'Wrong domain' in rv.data

            self.login()
            with app.test_request_context():  # Insert data to display in network view
                app.preprocess_request()
                actor = EntityMapper.insert('E21', 'King Arthur')
                event = EntityMapper.insert('E7', 'Battle of Camlann')
                prop_object = EntityMapper.insert('E89', 'Propositional Object')
                LinkMapper.insert(actor, 'P11', event)
                LinkMapper.insert(actor, 'P67', prop_object)
            rv = self.app.get(url_for('model_network'))
            assert b'Orphans' in rv.data
            rv = self.app.post(
                url_for('model_network'),
                data={'orphans': True, 'width': 100, 'height': 40, 'distance': -666, 'charge': 500})
            assert b'666' in rv.data
