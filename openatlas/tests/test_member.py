from flask import url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.test_base import TestBaseCase


class MemberTests(TestBaseCase):

    def test_member(self):
        with app.app_context():
            self.login()
            with app.test_request_context():
                app.preprocess_request()
                actor_id = EntityMapper.insert('E21', 'Ripley').id
                group_id = EntityMapper.insert('E74', 'Space Marines').id

            # add membership
            rv = self.app.get(url_for('member_insert', origin_id=group_id))
            assert b'Actor Function' in rv.data
            data = {'group': '[' + str(group_id) + ']'}
            rv = self.app.post(
                url_for('membership_insert', origin_id=actor_id), data=data, follow_redirects=True)
            assert b'Space Marines' in rv.data
            data = {'group': '[' + str(group_id) + ']', 'continue_': 'yes'}
            rv = self.app.post(
                url_for('membership_insert', origin_id=actor_id), data=data, follow_redirects=True)
            assert b'Space Marines' in rv.data

            # add member to group
            data = {'actor': '[' + str(actor_id) + ']'}
            rv = self.app.post(
                url_for('member_insert', origin_id=group_id), data=data, follow_redirects=True)
            assert b'Ripley' in rv.data
            data['continue_'] = 'yes'
            rv = self.app.post(
                url_for('member_insert', origin_id=group_id), data=data, follow_redirects=True)
            assert b'Ripley' in rv.data

            # update member
            with app.test_request_context():
                app.preprocess_request()
                link_id = LinkMapper.get_links(group_id, 'P107')[0].id
            rv = self.app.get(url_for('member_update', id_=link_id, origin_id=group_id))
            assert b'Ripley' in rv.data
            rv = self.app.post(
                url_for('member_update', id_=link_id, origin_id=group_id),
                data={'description': 'We are here to help you.'},
                follow_redirects=True)
            assert b'here to help' in rv.data
