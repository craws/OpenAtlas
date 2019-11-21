from typing import Union, Dict

from flask import url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.models.node import NodeMapper
from openatlas.models.settings import SettingsMapper
from openatlas.test_base import TestBaseCase


class ContentTests(TestBaseCase):

    def test_content_and_newsletter(self) -> None:
        with app.app_context():
            self.login()
            self.app.post(url_for('actor_insert', code='E21'), data={'name': 'Oliver Twist'})
            with app.test_request_context():
                app.preprocess_request()
                EntityMapper.insert('E31', 'One forsaken file entity', 'file')  # Add orphaned file
            rv = self.app.get(url_for('admin_orphans'))
            assert all(x in rv.data for x in [b'Oliver Twist', b'forsaken'])
            rv = self.app.get(url_for('admin_orphans_delete', parameter='orphans'))
            assert b'Oliver Twist' not in rv.data
            self.app.get(url_for('admin_orphans_delete', parameter='unlinked'))
            self.app.get(url_for('admin_orphans_delete', parameter='types'))
            self.app.get(url_for('admin_orphans_delete', parameter='whatever bogus string'))
            rv = self.app.get(url_for('admin_newsletter'))
            assert b'Newsletter' in rv.data

    def test_logs(self) -> None:
        self.login()
        with app.app_context():
            rv = self.app.get(url_for('admin_log'))
            assert b'Login' in rv.data
            rv = self.app.get(url_for('admin_log_delete', follow_redirects=True))
            assert b'Login' not in rv.data

    def test_links(self) -> None:
        self.login()
        with app.app_context():
            rv = self.app.get(url_for('admin_check_links', check='check'))
            assert b'Invalid linked entity' in rv.data

    def test_dates(self) -> None:
        self.login()
        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()
                # Create invalid dates for an actor and a relation link
                person = EntityMapper.insert('E21', 'Person')
                event = EntityMapper.insert('E7', 'Event')
                person.begin_from = '2018-01-31'
                person.begin_to = '2018-01-01'
                person.update()
                involvement = LinkMapper.get_by_id(event.link('P11', person))
                involvement.begin_from = '2017-01-31'
                involvement.begin_to = '2017-01-01'
                involvement.end_from = '2017-01-01'
                involvement.update()
            rv = self.app.get(url_for('admin_check_dates'))
            assert b'Invalid dates <span class="tab-counter">1' in rv.data
            assert b'Invalid link dates <span class="tab-counter">1' in rv.data
            assert b'Invalid involvement dates <span class="tab-counter">1' in rv.data

    def test_admin(self) -> None:
        with app.app_context():
            self.login()
            rv = self.app.get(url_for('admin_mail'))
            assert b'Email from' in rv.data
            rv = self.app.get(url_for('admin_index'))
            assert b'User' in rv.data
            rv = self.app.get(url_for('admin_general'))
            assert b'Edit' in rv.data
            rv = self.app.get(url_for('admin_general_update'))
            assert b'Save' in rv.data
            rv = self.app.get(url_for('admin_map'))
            assert b'MaxClusterRadius' in rv.data
            rv = self.app.post(url_for('admin_map'), follow_redirects=True, data={
                'map_cluster_enabled': True, 'map_cluster_max_radius': 2,
                'map_cluster_disable_at_zoom': 5})
            assert b'Changes have been saved.' in rv.data

            # Check link duplicates and multi use of single nodes
            with app.test_request_context():
                app.preprocess_request()
                event = EntityMapper.insert('E8', 'Event Horizon')
                source = EntityMapper.insert('E33', 'Tha source')
                source.link('P67', event)
                source.link('P67', event)
                source_node = NodeMapper.get_hierarchy_by_name('Source')
                source.link('P2', source_node.subs[0])
                source.link('P2', source_node.subs[1])
            rv = self.app.get(url_for('admin_check_link_duplicates'))
            assert b'Event Horizon' in rv.data
            rv = self.app.get(url_for('admin_check_link_duplicates', delete='delete'),
                              follow_redirects=True)
            assert b'Remove' in rv.data
            rv = self.app.get(url_for('admin_delete_single_type_duplicate', entity_id=source.id,
                                      node_id=source_node.subs[0]), follow_redirects=True)
            assert b'Congratulations, everything looks fine!' in rv.data

            # Check similar names
            with app.test_request_context():
                app.preprocess_request()
                EntityMapper.insert('E21', 'I have the same name!')
                EntityMapper.insert('E21', 'I have the same name!')
            rv = self.app.post(url_for('admin_check_similar'), follow_redirects=True,
                               data={'classes': 'actor', 'ratio': 100})
            assert b'I have the same name!' in rv.data
            rv = self.app.post(url_for('admin_check_similar'), follow_redirects=True,
                               data={'classes': 'file', 'ratio': 100})
            assert b'No entries' in rv.data

            data: Dict[str, Union[str, int]] = {name: '' for name in SettingsMapper.fields}
            data['default_language'] = 'en'
            data['default_table_rows'] = '10'
            data['failed_login_forget_minutes'] = '10'
            data['failed_login_tries'] = '10'
            data['minimum_password_length'] = '10'
            data['random_password_length'] = '10'
            data['reset_confirm_hours'] = '10'
            data['log_level'] = '0'
            data['site_name'] = 'Nostromo'
            data['minimum_jstree_search'] = 3
            data['minimum_tablesorter_search'] = 4
            rv = self.app.post(url_for('admin_general_update'), data=data, follow_redirects=True)
            assert b'Nostromo' in rv.data
            rv = self.app.get(url_for('admin_mail_update'))
            assert b'Mail transport port' in rv.data
            data = {'mail': True,
                    'mail_transport_username': 'whatever',
                    'mail_transport_host': 'localhost',
                    'mail_transport_port': '23',
                    'mail_from_email': 'max@example.com',
                    'mail_from_name': 'Max Headroom',
                    'mail_recipients_feedback': 'headroom@example.com'}
            rv = self.app.post(url_for('admin_mail_update'), data=data, follow_redirects=True)
            assert b'Max Headroom' in rv.data
            rv = self.app.get(url_for('admin_file'))
            assert b'jpg' in rv.data
            rv = self.app.post(url_for('admin_file'),
                               data={'file_upload_max_size': 20, 'profile_image_width': 20},
                               follow_redirects=True)
            assert b'Changes have been saved.' in rv.data
