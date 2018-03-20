from flask import url_for

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
            data = {
                'actor': '[' + str(related_id) + ']',
                relation_id: relation_id,
                'inverse': None,
                'date_begin_year': '-1949',
                'date_begin_month': '10',
                'date_begin_day': '8',
                'date_begin_year2': '-1948',
                'date_end_year': '2049',
                'date_end_year2': '2050'}
            rv = self.app.post(
                url_for('relation_insert', origin_id=actor_id), data=data, follow_redirects=True)
            assert b'The Kurgan' in rv.data
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
