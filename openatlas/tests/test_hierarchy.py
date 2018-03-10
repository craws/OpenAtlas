from flask import url_for

from openatlas import app
from openatlas.models.node import NodeMapper
from openatlas.test_base import TestBaseCase


class HierarchyTest(TestBaseCase):

    def test_hierarchy(self):
        with app.app_context():
            self.login()
            rv = self.app.get(url_for('hierarchy_insert'))
            assert b'+ Custom' in rv.data
            data = {'name': 'Geronimo', 'multiple': True, 'description': 'Very important!'}
            rv = self.app.post(url_for('hierarchy_insert'), data=data)
            hierarchy_id = rv.location.split('/')[-1].replace('types#tab-', '')
            rv = self.app.get(url_for('hierarchy_update', id_=hierarchy_id))
            assert b'Geronimo' in rv.data
            rv = self.app.post(
                url_for('hierarchy_update', id_=hierarchy_id), data=data, follow_redirects=True)
            assert b'Changes have been saved.' in rv.data
            data['name'] = 'Actor Actor Relation'
            rv = self.app.post(
                url_for('hierarchy_update', id_=hierarchy_id), data=data, follow_redirects=True)
            assert b'The name is already in use' in rv.data
            rv = self.app.post(url_for('hierarchy_delete', id_=hierarchy_id), follow_redirects=True)
            assert b'deleted' in rv.data

            # Test checks
            actor_node = NodeMapper.get_hierarchy_by_name('Actor Actor Relation')
            rv = self.app.get(url_for('hierarchy_update', id_=actor_node.id), follow_redirects=True)
            assert b'Forbidden' in rv.data
            rv = self.app.get(url_for('hierarchy_delete', id_=actor_node.id), follow_redirects=True)
            assert b'Forbidden' in rv.data
            rv = self.app.post(url_for('hierarchy_insert'), data=data)
            assert b'The name is already in use' in rv.data
