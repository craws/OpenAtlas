from flask import url_for

from openatlas import app
from tests.base import TestBaseCase, get_hierarchy, insert


class RelationTests(TestBaseCase):
    def test_relation(self) -> None:
        c = self.client
        with app.test_request_context():
            app.preprocess_request()
            actor = insert('person', 'Connor MacLeod')
            related = insert('person', 'The Kurgan')

        rv = c.get(
            url_for('link_insert_detail', origin_id=actor.id, name='relative'))
        assert b'Actor relation' in rv.data

        relation = get_hierarchy('Actor relation')
        sub_id = relation.subs[0]
        data = {
            'actor': actor.id,
            'relative': related.id,
            relation.id: sub_id,
            'inverse': None,
            'begin_year_from': '-1949',
            'begin_month_from': '10',
            'begin_day_from': '8',
            'begin_year_to': '-1948',
            'end_year_from': '2049',
            'end_year_to': '2050'}
        rv = c.post(
            url_for('link_insert_detail', origin_id=actor.id, name='relative'),
            data=data,
            follow_redirects=True)
        assert b'The Kurgan' in rv.data

        data['relative'] = actor.id
        data['actor'] = related.id
        rv = c.post(
            url_for(
                'link_insert_detail',
                origin_id=related.id,
                name='relative'),
            data=data,
            follow_redirects=True)
        assert b'Connor' in rv.data

        rv = c.get(url_for('view', id_=sub_id))
        assert b'Connor' in rv.data

        rv = c.get(url_for('change_type', id_=sub_id))
        assert b'The Kurgan' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            link_ = actor.get_links('OA7')[0]

        rv = c.post(
            url_for('change_type', id_=sub_id),
            data={
                relation.id: relation.subs[1],
                'selection': [link_.id],
                'checkbox_values': str([link_.id])},
            follow_redirects=True)
        assert b'Entities were updated' in rv.data

        rv = c.post(
            url_for('change_type', id_=relation.subs[1]),
            data={
                relation.id: '',
                'selection': [link_.id],
                'checkbox_values': str([link_.id])},
            follow_redirects=True)
        assert b'Entities were updated' in rv.data

        rv = c.get(
            url_for(
                'link_update',
                id_=link_.id,
                origin_id=related.id,
                name='relative'))
        assert b'Connor' in rv.data

        rv = c.post(
            url_for(
                'link_update',
                id_=link_.id,
                origin_id=actor.id,
                name='relative'),
            data={'description': 'There can be only one', 'inverse': True},
            follow_redirects=True)
        assert b'only one' in rv.data

        data['relative'] = actor.id
        data['actor'] = actor.id
        rv = c.post(
            url_for(
                'link_insert_detail',
                origin_id=actor.id,
                name='relative'),
            data=data,
            follow_redirects=True)
        assert b'link to itself' in rv.data
