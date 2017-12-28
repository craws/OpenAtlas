# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import url_for
from openatlas import app, EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.test_base import TestBaseCase


class RelationTests(TestBaseCase):

    def test_relation(self):
        self.login()
        with app.app_context():
            actor_id = EntityMapper.insert('E21', 'Connor MacLeod').id
            related_id = EntityMapper.insert('E21', 'The Kurgan').id

            # add relationship
            rv = self.app.get(url_for('relation_insert', origin_id=actor_id))
            assert b'Actor Actor Relation' in rv.data
            data = {'actor': '[' + str(related_id) + ']', 'inverse': True}
            rv = self.app.post(
                url_for('relation_insert', origin_id=actor_id), data=data, follow_redirects=True)
            assert b'The Kurgan' in rv.data
            data = {'actor': '[' + str(related_id) + ']', 'continue_': 'yes'}
            rv = self.app.post(
                url_for('relation_insert', origin_id=actor_id), data=data, follow_redirects=True)
            assert b'The Kurgan' in rv.data
            rv = self.app.get(url_for('actor_view', id_=actor_id))
            assert b'The Kurgan' in rv.data

            # update relationship
            link_id = LinkMapper.get_links(actor_id, 'OA7')[0].id
            rv = self.app.get(url_for('relation_update', id_=link_id, origin_id=related_id))
            assert b'Connor' in rv.data
            rv = self.app.post(
                url_for('relation_update', id_=link_id, origin_id=actor_id),
                data={'description': 'There can be only one!', 'inverse': True},
                follow_redirects=True)
            assert b'only one' in rv.data
