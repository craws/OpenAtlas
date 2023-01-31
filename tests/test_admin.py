from pathlib import Path

from flask import g, url_for

from openatlas import app
from openatlas.database.link import Link as DbLink
from openatlas.models.link import Link
from tests.base import TestBaseCase, get_hierarchy, insert


class AdminTests(TestBaseCase):

    def test_admin(self) -> None:
        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                person = insert('person', 'Oliver Twist')
                insert('person', 'Oliver Twist')
                insert('file', 'Forsaken file')
                insert('feature', 'Forsaken subunit')
                invalid = insert('artifact', 'Invalid linked entity')
                DbLink.insert({
                    'property_code': 'P86',
                    'domain_id': invalid.id,
                    'range_id': invalid.id,
                    'description': '',
                    'type_id': None})

            rv = self.app.get(url_for('admin_orphans'))
            assert b'Oliver Twist' in rv.data
            assert b'Forsaken file' in rv.data
            assert b'Forsaken subunit' in rv.data

            rv = self.app.get(url_for('admin_log'))
            assert b'Login' in rv.data

            rv = self.app.get(url_for('admin_check_dates'))
            assert b'Congratulations, everything looks fine!' in rv.data

            rv = self.app.get(url_for('admin_log_delete'))
            assert b'Login' not in rv.data

            rv = self.app.get(url_for('admin_check_links'))
            assert b'Invalid linked entity' in rv.data

            file_ = 'Test77.txt'
            with open(Path(app.config['UPLOAD_DIR'] / file_), 'w') as _file:
                pass

            rv = self.app.get(
                url_for('admin_file_delete', filename=file_),
                follow_redirects=True)
            assert b'Test77.txt was deleted' in rv.data

            rv = self.app.get(
                url_for('admin_file_delete', filename=file_),
                follow_redirects=True)
            assert b'An error occurred when trying to delete' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                event = insert('acquisition', 'Event Horizon')
                person.update({
                    'attributes': {
                        'begin_from': '2018-01-31',
                        'begin_to': '2018-01-01'}})
                involvement = Link.get_by_id(event.link('P11', person)[0])
                involvement.begin_from = '2017-01-31'
                involvement.begin_to = '2017-01-01'
                involvement.end_from = '2017-01-01'
                involvement.update()
                source = insert('source', 'Tha source')
                source.link('P67', event)
                source.link('P67', event)
                source_type = get_hierarchy('Source')
                source.link('P2', g.types[source_type.subs[0]])
                source.link('P2', g.types[source_type.subs[1]])

            rv = self.app.get(url_for('admin_check_dates'))
            assert b'<span class="tab-counter">' in rv.data

            rv = self.app.get(url_for('admin_check_link_duplicates'))
            assert b'Event Horizon' in rv.data

            rv = self.app.get(
                url_for('admin_check_link_duplicates', delete='delete'),
                follow_redirects=True)
            assert b'Remove' in rv.data

            rv = self.app.get(
                url_for(
                    'admin_delete_single_type_duplicate',
                    entity_id=source.id,
                    type_id=source_type.subs[0]),
                follow_redirects=True)
            assert b'Congratulations, everything looks fine!' in rv.data

            rv = self.app.post(
                url_for('admin_check_similar'),
                data={'classes': 'person', 'ratio': 100},
                follow_redirects=True)
            assert b'Oliver Twist' in rv.data

            rv = self.app.get(url_for('admin_settings', category='mail'))
            assert b'recipients feedback' in rv.data

            rv = self.app.get(url_for('admin_settings', category='general'))
            assert b'log level' in rv.data

            rv = self.app.post(
                url_for('admin_content', item='citation_example'),
                data={'en': 'cool citation'},
                follow_redirects=True)
            assert b'Changes have been saved' in rv.data

            rv = self.app.get(url_for('insert', class_='edition'))
            assert b'cool citation' in rv.data

            rv = self.app.get(url_for('admin_content', item='legal_notice'))
            assert b'Save' in rv.data

            rv = self.app.get(url_for('arche_index'))
            assert b'https://arche-curation.acdh-dev.oeaw.ac.at/' in rv.data
            #
            # rv = self.app.get(url_for('arche_fetch'))
            # assert b'No entities to retrieve' in rv.data

            rv = self.app.post(
                url_for('admin_content', item='legal_notice'),
                data={'en': 'My legal notice', 'de': 'German notice'},
                follow_redirects=True)
            assert b'My legal notice' in rv.data

            self.app.get('/index/setlocale/de')
            rv = self.app.get(url_for('index_content', item='legal_notice'))
            assert b'German notice' in rv.data
