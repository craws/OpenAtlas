from flask import url_for

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from tests.base import TestBaseCase


class MemberTests(TestBaseCase):

    def test_member(self) -> None:
        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                newt = Entity.insert('person', 'Newt')
                group = Entity.insert('group', 'LV-426 colony')

            rv = self.app.get(url_for('member_insert', origin_id=group.id))
            assert b'Actor function' in rv.data

            rv = self.app.post(
                url_for('member_insert', origin_id=newt.id, code='membership'),
                data={'group': str([group.id])},
                follow_redirects=True)
            assert b'LV-426 colony' in rv.data

            rv = self.app.post(
                url_for('member_insert', origin_id=newt.id, code='membership'),
                data={'group': str([group.id]), 'continue_': 'yes'},
                follow_redirects=True)
            assert b'LV-426 colony' in rv.data

            rv = self.app.post(
                url_for('member_insert', origin_id=group.id),
                data={'actor': str([newt.id])},
                follow_redirects=True)
            assert b'Newt' in rv.data

            rv = self.app.post(
                url_for('member_insert', origin_id=group.id),
                data={'actor': str([newt.id]), 'continue_': 'yes'},
                follow_redirects=True)
            assert b'Newt' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                link_id = Link.get_links(group.id, 'P107')[0].id
            rv = self.app.get(
                url_for('member_update', id_=link_id, origin_id=group.id))
            assert b'Newt' in rv.data

            rv = self.app.post(
                url_for('member_update', id_=link_id, origin_id=group.id),
                data={'description': 'We are here to help you.'},
                follow_redirects=True)
            assert b'here to help' in rv.data
