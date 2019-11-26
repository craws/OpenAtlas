from flask import url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from tests.base import TestBaseCase


class MemberTests(TestBaseCase):

    def test_member(self) -> None:
        with app.app_context():
            self.login()
            with app.test_request_context():
                app.preprocess_request()
                actor = EntityMapper.insert('E21', 'Ripley')
                group = EntityMapper.insert('E74', 'Space Marines')

            # Add membership
            rv = self.app.get(url_for('member_insert', origin_id=group.id))
            assert b'Actor Function' in rv.data
            data = {'group': str([group.id])}
            rv = self.app.post(
                url_for('membership_insert', origin_id=actor.id), data=data, follow_redirects=True)
            assert b'Space Marines' in rv.data
            data = {'group': str([group.id]), 'continue_': 'yes'}
            rv = self.app.post(
                url_for('membership_insert', origin_id=actor.id), data=data, follow_redirects=True)
            assert b'Space Marines' in rv.data

            rv = self.app.post(
                url_for('membership_insert', origin_id=group.id), data=data, follow_redirects=True)
            assert b"Can't link to itself" in rv.data
            rv = self.app.post(url_for('member_insert', origin_id=actor.id),
                               data={'actor': str([actor.id])}, follow_redirects=True)
            assert b"Can't link to itself" in rv.data

            # Add member to group
            data = {'actor': str([actor.id])}
            rv = self.app.post(
                url_for('member_insert', origin_id=group.id), data=data, follow_redirects=True)
            assert b'Ripley' in rv.data
            data['continue_'] = 'yes'
            rv = self.app.post(
                url_for('member_insert', origin_id=group.id), data=data, follow_redirects=True)
            assert b'Ripley' in rv.data

            # Update
            with app.test_request_context():
                app.preprocess_request()
                link_id = LinkMapper.get_links(group.id, 'P107')[0].id
            rv = self.app.get(url_for('member_update', id_=link_id, origin_id=group.id))
            assert b'Ripley' in rv.data
            rv = self.app.post(
                url_for('member_update', id_=link_id, origin_id=group.id),
                data={'description': 'We are here to help you.'},
                follow_redirects=True)
            assert b'here to help' in rv.data
