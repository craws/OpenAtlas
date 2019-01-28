from flask import url_for, g

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.models.node import NodeMapper
from openatlas.test_base import TestBaseCase


class RelationTests(TestBaseCase):

    def test_relation(self):
        with app.app_context():
            self.login()
            with app.test_request_context():
                app.preprocess_request()
                actor_id = EntityMapper.insert('E21', 'Connor MacLeod').id
                related_id = EntityMapper.insert('E21', 'The Kurgan').id

            # Add relationship
            rv = self.app.get(url_for('relation_insert', origin_id=actor_id))
            assert b'Actor Actor Relation' in rv.data
            relation_id = NodeMapper.get_hierarchy_by_name('Actor Actor Relation').id
            relation_sub_id = g.nodes[relation_id].subs[0]
            data = {'actor': '[' + str(related_id) + ']',
                    relation_id: relation_sub_id,
                    'inverse': None,
                    'begin_year_from': '-1949',
                    'begin_month_from': '10',
                    'begin_day_from': '8',
                    'begin_year_to': '-1948',
                    'end_year_from': '2049',
                    'end_year_to': '2050'}
            rv = self.app.post(
                url_for('relation_insert', origin_id=actor_id), data=data, follow_redirects=True)
            assert b'The Kurgan' in rv.data
            rv = self.app.get(url_for('node_view', id_=relation_sub_id))
            assert b'Connor' in rv.data
            data['continue_'] = 'yes'
            data['inverse'] = True
            rv = self.app.post(
                url_for('relation_insert', origin_id=actor_id), data=data, follow_redirects=True)
            assert b'The Kurgan' in rv.data
            rv = self.app.get(url_for('actor_view', id_=actor_id))
            assert b'The Kurgan' in rv.data

            rv = self.app.post(
                url_for('relation_insert', origin_id=related_id), data=data, follow_redirects=True)
            assert b"Can't link to itself." in rv.data

            # Relation types
            rv = self.app.get(url_for('node_move_entities', id_=relation_sub_id))
            assert b'The Kurgan' in rv.data

            # Update relationship
            with app.test_request_context():
                app.preprocess_request()
                link_id = LinkMapper.get_links(actor_id, 'OA7')[0].id
                link_id2 = LinkMapper.get_links(actor_id, 'OA7', True)[0].id
            rv = self.app.get(url_for('relation_update', id_=link_id, origin_id=related_id))
            assert b'Connor' in rv.data
            rv = self.app.post(
                url_for('relation_update', id_=link_id, origin_id=actor_id),
                data={'description': 'There can be only one!', 'inverse': True},
                follow_redirects=True)
            assert b'only one' in rv.data
            rv = self.app.post(
                url_for('relation_update', id_=link_id2, origin_id=actor_id),
                data={'description': 'There can be only one!', 'inverse': None},
                follow_redirects=True)
            assert b'only one' in rv.data
