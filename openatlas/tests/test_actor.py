from flask import g, url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.models.node import NodeMapper
from openatlas.test_base import TestBaseCase


class ActorTests(TestBaseCase):

    def test_actor(self):
        with app.app_context():
            self.login()
            rv = self.app.get(url_for('actor_index'))
            assert b'No entries' in rv.data

            # Create entities for actor
            rv = self.app.post(url_for('place_insert'), data={'name': 'Nostromos'})
            residence_id = rv.location.split('/')[-1]
            with app.test_request_context():
                app.preprocess_request()
                sex_node = NodeMapper.get_hierarchy_by_name('Sex')
                sex_node_sub_1 = g.nodes[sex_node.subs[0]]
                sex_node_sub_2 = g.nodes[sex_node.subs[1]]
                event = EntityMapper.insert('E8', 'Event Horizon')
                source = EntityMapper.insert('E33', 'Tha source')

            # Actor insert
            rv = self.app.get(url_for('actor_insert', code='E21'))
            assert b'+ Person' in rv.data
            self.app.get(url_for('actor_insert', code='E21', origin_id=residence_id))
            data = {sex_node.id: sex_node_sub_1.id,
                    'name': 'Sigourney Weaver',
                    'alias-1': 'Ripley',
                    'residence': residence_id,
                    'begins_in': residence_id,
                    'ends_in': residence_id,
                    'description': 'Susan Alexandra Weaver is an American actress.',
                    'begin_year_from': '-1949',
                    'begin_month_from': '10',
                    'begin_day_from': '8',
                    'begin_year_to': '-1948',
                    'end_year_from': '2049',
                    'end_year_to': '2050'}
            rv = self.app.post(url_for('actor_insert', code='E21', origin_id=residence_id),
                               data=data)
            actor_id = rv.location.split('/')[-1]

            # Test actor nodes
            rv = self.app.get(url_for('node_view', id_=sex_node_sub_1.id))
            assert b'Susan' in rv.data
            rv = self.app.get(url_for('node_move_entities', id_=sex_node_sub_1.id))
            assert b'Sigourney' in rv.data
            rv = self.app.post(url_for('node_move_entities', id_=sex_node_sub_1.id),
                               data={sex_node.id: sex_node_sub_2.id, 'selection': [actor_id]},
                               follow_redirects=True)
            assert b'Entities where updated' in rv.data
            rv = self.app.post(url_for('node_move_entities', id_=sex_node_sub_2.id),
                               data={sex_node.id: '', 'selection': [actor_id]},
                               follow_redirects=True)
            assert b'Entities where updated' in rv.data
            self.app.post(url_for('actor_insert', code='E21', origin_id=actor_id), data=data)
            self.app.post(url_for('actor_insert', code='E21', origin_id=event.id), data=data)
            self.app.post(url_for('actor_insert', code='E21', origin_id=source.id), data=data)
            rv = self.app.post(url_for('reference_insert', code='reference'), data={'name': 'Book'})
            reference_id = rv.location.split('/')[-1]
            rv = self.app.post(url_for('actor_insert', code='E21', origin_id=reference_id),
                               data=data, follow_redirects=True)
            assert b'An entry has been created' in rv.data
            data['continue_'] = 'yes'
            rv = self.app.post(url_for('actor_insert', code='E21'), data=data,
                               follow_redirects=True)
            assert b'An entry has been created' in rv.data
            rv = self.app.get(url_for('actor_index'))
            assert b'Sigourney Weaver' in rv.data

            # Actor update
            rv = self.app.get(url_for('actor_update', id_=actor_id))
            assert b'American actress' in rv.data
            data['name'] = 'Susan Alexandra Weaver'
            data['end_year_from'] = ''
            data['begin_year_to'] = '1950'
            data['begin_day_from'] = ''
            rv = self.app.post(url_for('actor_update', id_=actor_id), data=data,
                               follow_redirects=True)
            assert b'Susan Alexandra Weaver' in rv.data
            rv = self.app.post(url_for('ajax_bookmark'), data={'entity_id': actor_id},
                               follow_redirects=True)
            assert b'Remove bookmark' in rv.data
            rv = self.app.get('/')
            assert b'Weaver' in rv.data
            rv = self.app.post(url_for('ajax_bookmark'), data={'entity_id': actor_id},
                               follow_redirects=True)
            assert b'Bookmark' in rv.data
            rv = self.app.get(url_for('link_delete', origin_id=actor_id, id_=666),
                              follow_redirects=True)
            assert b'removed'in rv.data

            # Actor delete
            rv = self.app.get(url_for('actor_delete', id_=actor_id), follow_redirects=True)
            assert b'The entry has been deleted.' in rv.data
