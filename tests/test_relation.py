from flask import url_for

from openatlas import app
from openatlas.models.link import Link
from tests.base import TestBaseCase, get_hierarchy, insert


class RelationTests(TestBaseCase):

    def test_relation(self) -> None:
        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                actor = insert('person', 'Connor MacLeod')
                related = insert('person', 'The Kurgan')

            rv = self.app.get(
                url_for(
                    'insert_relation',
                    origin_id=actor.id,
                    type_='actor_relation'))
            assert b'Actor relation' in rv.data

            relation = get_hierarchy('Actor relation')
            sub_id = relation.subs[0]
            data = {
                'actor': str([related.id]),
                relation.id: sub_id,
                'inverse': None,
                'begin_year_from': '-1949',
                'begin_month_from': '10',
                'begin_day_from': '8',
                'begin_year_to': '-1948',
                'end_year_from': '2049',
                'end_year_to': '2050'}
            rv = self.app.post(
                url_for(
                    'insert_relation',
                    origin_id=actor.id,
                    type_='actor_relation'),
                data=data,
                follow_redirects=True)
            assert b'The Kurgan' in rv.data

            rv = self.app.get(url_for('view', id_=sub_id))
            assert b'Connor' in rv.data

            rv = self.app.get(url_for('type_move_entities', id_=sub_id))
            assert b'The Kurgan' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                link_ = Link.get_links(actor.id, 'OA7')[0]

            rv = self.app.post(
                url_for('type_move_entities', id_=sub_id),
                data={
                    relation.id: relation.subs[1],
                    'selection': [link_.id],
                    'checkbox_values': str([link_.id])},
                follow_redirects=True)
            assert b'Entities were updated' in rv.data

            rv = self.app.post(
                url_for('type_move_entities', id_=relation.subs[1]),
                data={
                    relation.id: '',
                    'selection': [link_.id],
                    'checkbox_values': str([link_.id])},
                follow_redirects=True)
            assert b'Entities were updated' in rv.data

            rv = self.app.get(
                url_for('link_update', id_=link_.id, origin_id=related.id))
            assert b'Connor' in rv.data

            rv = self.app.post(
                url_for('link_update', id_=link_.id, origin_id=actor.id),
                data={'description': 'There can be only one', 'inverse': True},
                follow_redirects=True)
            assert b'only one' in rv.data
