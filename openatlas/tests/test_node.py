# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import url_for

from openatlas import app, NodeMapper
from openatlas.test_base import TestBaseCase


class NodeTest(TestBaseCase):

    def test_node(self):
        self.login()
        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()
                actor_node = NodeMapper.get_hierarchy_by_name('Actor Actor Relation')
                sex_node = NodeMapper.get_hierarchy_by_name('Sex')
            rv = self.app.get(url_for('node_index'))
            assert b'Actor Actor Relation' in rv.data
            rv = self.app.post(
                url_for('node_insert', root_id=actor_node.id), data={'name_search': 'new'})
            assert b'Inverse' in rv.data
            data = {
                'name': 'My secret node',
                'name_inverse': 'Do I look inverse?',
                'description': 'Very important!'}
            rv = self.app.post(url_for('node_insert', root_id=actor_node.id), data=data)
            node_id = rv.location.split('/')[-1].replace('node#tab-', '')
            rv = self.app.get(url_for('node_update', id_=node_id))
            assert b'My secret node' in rv.data
            self.app.post(url_for('node_insert', root_id=sex_node.id), data=data)
            rv = self.app.post(
                url_for('node_update', id_=node_id), data=data, follow_redirects=True)
            assert b'Changes have been saved.' in rv.data

            # test forbidden system node
            rv = self.app.post(
                url_for('node_update', id_=actor_node.id), data=data, follow_redirects=True)
            assert b'Forbidden' in rv.data

            # test update with self as root
            data[str(actor_node.id)] = node_id
            rv = self.app.post(
                url_for('node_update', id_=node_id), data=data, follow_redirects=True)
            assert b'super' in rv.data

            #  test delete system node
            rv = self.app.get(url_for('node_delete', id_=actor_node.id), follow_redirects=True)
            assert b'Forbidden' in rv.data
            rv = self.app.get(url_for('node_delete', id_=node_id), follow_redirects=True)
            assert b'The entry has been deleted.' in rv.data
