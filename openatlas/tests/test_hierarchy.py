# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import url_for

from openatlas import app
from openatlas.test_base import TestBaseCase


class HierarchyTest(TestBaseCase):

    def test_hierarchy(self):
        self.login()
        with app.app_context():
            rv = self.app.get(url_for('hierarchy_insert'))
            assert b'+ Custom' in rv.data
            form_data = {
                'name': 'Geronimo',
                'multiple': True,
                'description': 'Very important!'}
            rv = self.app.post(url_for('hierarchy_insert'), data=form_data)
            hierarchy_id = rv.location.split('/')[-1].replace('node#tab-', '')
            rv = self.app.get(url_for('hierarchy_update', id_=hierarchy_id))
            assert b'Geronimo' in rv.data
            rv = self.app.post(
                url_for('hierarchy_update', id_=hierarchy_id),
                data=form_data,
                follow_redirects=True)
            assert b'Changes have been saved.' in rv.data
