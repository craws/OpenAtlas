from flask import url_for

from openatlas import app
from openatlas.models.node import NodeMapper
from tests.base import TestBaseCase


class NodeTest(TestBaseCase):

    def test_node(self) -> None:
        with app.app_context():  # type: ignore
            self.login()
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                actor_node = NodeMapper.get_hierarchy_by_name('Actor Actor Relation')
                dimension_node = NodeMapper.get_hierarchy_by_name('Dimensions')
                sex_node = NodeMapper.get_hierarchy_by_name('Sex')
            rv = self.app.get(url_for('node_index'))
            assert b'Actor Actor Relation' in rv.data
            rv = self.app.get(url_for('node_insert', root_id=actor_node.id, super_id=actor_node.id))
            assert b'Actor Actor Relation' in rv.data
            rv = self.app.post(url_for('node_insert', root_id=actor_node.id),
                               data={'name_search': 'new'})
            assert b'Inverse' in rv.data
            data = {'name': 'My secret node', 'name_inverse': 'Do I look inverse?',
                    'description': 'Very important!'}
            rv = self.app.post(url_for('node_insert', root_id=actor_node.id), data=data)
            node_id = rv.location.split('/')[-1].replace('node#tab-', '')
            rv = self.app.get(url_for('node_update', id_=node_id))
            assert b'My secret node' in rv.data and b'Super' in rv.data
            self.app.post(url_for('node_insert', root_id=sex_node.id), data=data)
            rv = self.app.post(url_for('node_update', id_=node_id), data=data,
                               follow_redirects=True)
            assert b'Changes have been saved.' in rv.data

            # Test insert an continue
            data['continue_'] = 'yes'
            rv = self.app.post(url_for('node_insert', root_id=actor_node.id), data=data,
                               follow_redirects=True)
            assert b'An entry has been created' in rv.data
            data['continue_'] = ''

            # Test forbidden system node
            rv = self.app.post(url_for('node_update', id_=actor_node.id), data=data,
                               follow_redirects=True)
            assert b'Forbidden' in rv.data

            # Test update with self as root
            data[str(actor_node.id)] = node_id
            rv = self.app.post(url_for('node_update', id_=node_id), data=data,
                               follow_redirects=True)
            assert b'Type can&#39;t have itself as super.' in rv.data

            # Test update with a child as root
            rv = self.app.post(url_for('node_insert', root_id=actor_node.id), data=data)
            child_node_id = rv.location.split('/')[-1].replace('node#tab-', '')
            data[str(actor_node.id)] = child_node_id
            rv = self.app.post(url_for('node_update', id_=node_id), data=data,
                               follow_redirects=True)
            assert b'Type can&#39;t have a sub as super.' in rv.data

            # Test value type
            rv = self.app.get(url_for('node_update', id_=dimension_node.subs[0]),
                              follow_redirects=True)
            assert b'Dimensions' in rv.data

            # Test delete system node
            rv = self.app.get(url_for('node_delete', id_=actor_node.id), follow_redirects=True)
            assert b'Forbidden' in rv.data
            rv = self.app.get(url_for('node_delete', id_=child_node_id), follow_redirects=True)
            assert b'The entry has been deleted.' in rv.data
