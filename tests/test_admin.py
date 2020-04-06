from flask import g, url_for

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.node import Node
from tests.base import TestBaseCase


class ContentTests(TestBaseCase):

    def test_content_and_newsletter(self) -> None:
        with app.app_context():  # type: ignore
            self.app.post(url_for('actor_insert', code='E21'), data={'name': 'Oliver Twist'})
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                Entity.insert('E31', 'One forsaken file entity', 'file')  # Add orphaned file
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
        with app.app_context():  # type: ignore
            rv = self.app.get(url_for('admin_log'))
            assert b'Login' in rv.data
            rv = self.app.get(url_for('admin_log_delete', follow_redirects=True))
            assert b'Login' not in rv.data

    def test_links(self) -> None:
        with app.app_context():  # type: ignore
            rv = self.app.get(url_for('admin_check_links', check='check'))
            assert b'Invalid linked entity' in rv.data

    def test_dates(self) -> None:
        with app.app_context():  # type: ignore
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                # Create invalid dates for an actor and a relation link
                person = Entity.insert('E21', 'Person')
                event = Entity.insert('E7', 'Event')
                person.begin_from = '2018-01-31'
                person.begin_to = '2018-01-01'
                person.update()
                involvement = Link.get_by_id(event.link('P11', person)[0])
                involvement.begin_from = '2017-01-31'
                involvement.begin_to = '2017-01-01'
                involvement.end_from = '2017-01-01'
                involvement.update()
            rv = self.app.get(url_for('admin_check_dates'))
            assert b'Invalid dates <span class="tab-counter">1' in rv.data
            assert b'Invalid link dates <span class="tab-counter">1' in rv.data
            assert b'Invalid involvement dates <span class="tab-counter">1' in rv.data

    def test_duplicates(self) -> None:
        with app.app_context():  # type: ignore
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                event = Entity.insert('E8', 'Event Horizon')
                source = Entity.insert('E33', 'Tha source')
                source.link('P67', event)
                source.link('P67', event)
                source_node = Node.get_hierarchy('Source')
                source.link('P2', g.nodes[source_node.subs[0]])
                source.link('P2', g.nodes[source_node.subs[1]])
            rv = self.app.get(url_for('admin_check_link_duplicates'))
            assert b'Event Horizon' in rv.data
            rv = self.app.get(url_for('admin_check_link_duplicates', delete='delete'),
                              follow_redirects=True)
            assert b'Remove' in rv.data
            rv = self.app.get(url_for('admin_delete_single_type_duplicate',
                                      entity_id=source.id,
                                      node_id=source_node.subs[0]),
                              follow_redirects=True)
            assert b'Congratulations, everything looks fine!' in rv.data

    def test_similar(self) -> None:
        with app.app_context():  # type: ignore
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                Entity.insert('E21', 'I have the same name!')
                Entity.insert('E21', 'I have the same name!')
            rv = self.app.post(url_for('admin_check_similar'),
                               follow_redirects=True,
                               data={'classes': 'actor', 'ratio': 100})
            assert b'I have the same name!' in rv.data
            rv = self.app.post(url_for('admin_check_similar'),
                               follow_redirects=True,
                               data={'classes': 'file', 'ratio': 100})
            assert b'No entries' in rv.data

    def test_settings(self) -> None:
        with app.app_context():  # type: ignore
            rv = self.app.get(url_for('admin_index'))
            assert b'User' in rv.data

            # Map
            rv = self.app.get(url_for('admin_map'))
            assert b'Max cluster radius' in rv.data
            rv = self.app.post(url_for('admin_map'),
                               follow_redirects=True,
                               data={'map_cluster_max_radius': 2, 'map_cluster_disable_at_zoom': 5})
            assert b'Changes have been saved.' in rv.data

            # General
            rv = self.app.get(url_for('admin_general'))
            assert b'Save' in rv.data
            data = {'default_language': 'en',
                    'default_table_rows': '10',
                    'failed_login_forget_minutes': '10',
                    'failed_login_tries': '10',
                    'minimum_password_length': '10',
                    'random_password_length': '10',
                    'reset_confirm_hours': '10',
                    'log_level': '0',
                    'site_name': 'Nostromo',
                    'minimum_jstree_search': 3}
            rv = self.app.post(url_for('admin_general'), data=data, follow_redirects=True)
            assert b'Nostromo' in rv.data

            # Mail
            rv = self.app.get(url_for('admin_mail'))
            assert b'Recipients feedback' in rv.data
            data = {'mail': True,
                    'mail_transport_username': 'whatever',
                    'mail_transport_host': 'localhost',
                    'mail_transport_port': '23',
                    'mail_from_email': 'max@example.com',
                    'mail_from_name': 'Max Headroom',
                    'mail_recipients_feedback': 'headroom@example.com'}
            rv = self.app.post(url_for('admin_mail'), data=data, follow_redirects=True)
            assert b'Max Headroom' in rv.data

            # File
            rv = self.app.get(url_for('admin_file'))
            assert b'jpg' in rv.data
            rv = self.app.post(url_for('admin_file'),
                               data={'file_upload_max_size': 20, 'profile_image_width': 20},
                               follow_redirects=True)
            assert b'Changes have been saved.' in rv.data

            # API
            rv = self.app.get(url_for('admin_api'))
            assert b'public' in rv.data
            rv = self.app.post(url_for('admin_api'), data={'public': True}, follow_redirects=True)
            assert b'Changes have been saved' in rv.data
