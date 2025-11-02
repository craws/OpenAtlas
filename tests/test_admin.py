from pathlib import Path

from flask import g, url_for

from openatlas import app
from openatlas.database import entity as db
from openatlas.models.dates import form_to_datetime64
from openatlas.models.entity import Link
from openatlas.models.logger import Logger
from tests.base import TestBaseCase, get_hierarchy, insert


class AdminTests(TestBaseCase):

    def test_admin(self) -> None:
        c = self.client
        with app.test_request_context():
            app.preprocess_request()
            Logger.log('error', 'test', 'error log')
            Logger.log('info', 'test', 'info log')
            Logger.log('debug', 'test', 'debug log')
            person = insert('person', 'Oliver Twist')
            insert('person', 'Oliver Twist')
            insert('file', 'Forsaken file')
            insert('feature', 'Forsaken subunit')
            invalid = insert('artifact', 'Invalid linked entity')
            db.link({
                'property_code': 'P86',
                'domain_id': invalid.id,
                'range_id': invalid.id,
                'description': '',
                'type_id': None,
                'begin_from': None,
                'begin_to': None,
                'begin_comment': None,
                'end_from': None,
                'end_to': None,
                'end_comment': None})

        self.client.post(  # Login again after Logger statements above
            url_for('login'),
            data={'username': 'Alice', 'password': 'test'})
        assert b'Oliver Twist' in c.get(url_for('orphans')).data

        rv = c.get(url_for('log'))
        assert b'Login' in rv.data
        assert b'info log' in rv.data
        assert b'error log' in rv.data
        assert b'debug log' not in rv.data
        assert b'Login' not in c.get(url_for('log_delete')).data

        rv = c.get(url_for('check_dates'))
        assert b'Congratulations, everything looks fine!' in rv.data

        rv = c.get(url_for('check_links'))
        assert b'Invalid linked entity' in rv.data

        file_ = 'Test77.txt'
        file_path = Path(app.config['UPLOAD_PATH'] / file_)
        with open(file_path, 'w', encoding='utf8') as _:
            pass
        iiif_path = Path(Path(g.settings['iiif_path']) / file_)
        with open(iiif_path, 'w', encoding='utf8') as _:
            pass

        rv = c.get(
            url_for('admin_file_delete', filename=file_),
            follow_redirects=True)
        assert b'Test77.txt was deleted' in rv.data

        rv = c.get(
            url_for('admin_file_delete', filename=file_),
            follow_redirects=True)
        assert b'An error occurred when trying to delete' in rv.data

        rv = c.get(
            url_for('admin_file_iiif_delete', filename=file_),
            follow_redirects=True)
        assert b'Test77.txt was deleted' in rv.data

        rv = c.get(
            url_for('admin_file_iiif_delete', filename=file_),
            follow_redirects=True)
        assert b'An error occurred when trying to delete' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            event = insert('acquisition', 'Event Horizon')
            event.update(
                data={
                    'attributes':
                        {'begin_from': form_to_datetime64(2000, 1, 1)}})
            event2 = insert('activity', 'Event Impossible')
            event2.update(
                data={
                    'attributes':
                        {'begin_from': form_to_datetime64(1000, 1, 1)}})
            event2.link('P134', event)
            event.link('P9', event2)
            person.update({
                'attributes': {
                    'begin_from': '2018-01-31',
                    'begin_to': '2018-01-01'}})
            involvement = Link.get_by_id(
                event.link(
                    'P11',
                    person,
                    dates={
                        'begin_from': '2017-01-31',
                        'begin_to': '2017-01-01',
                        'begin_comment': None,
                        'end_from': '2017-01-01',
                        'end_to': None,
                        'end_comment': None})[0])
            #involvement.begin_from = form_to_datetime64(2017, 1, 31)
            #involvement.begin_to = form_to_datetime64(2017, 1, 1)
            #involvement.end_from = form_to_datetime64(2017, 1, 1)

            # Todo: continue tests - implement relations
            #involvement.update({})

            source = insert('source', 'Tha source')
            source.link('P67', event)
            source.link('P67', event)
            source_type = get_hierarchy('Source')
            source.link('P2', g.types[source_type.subs[0]])
            source.link('P2', g.types[source_type.subs[1]])

        rv = c.get(url_for('check_dates'))
        assert b'tab-counter' in rv.data

        rv = c.get(url_for('check_link_duplicates'))
        assert b'Event Horizon' in rv.data

        rv = c.get(
            url_for('check_link_duplicates', delete='delete'),
            follow_redirects=True)
        assert b'Remove' in rv.data

        rv = c.get(
            url_for(
                'delete_single_type_duplicate',
                entity_id=source.id,
                type_id=source_type.subs[0]),
            follow_redirects=True)
        assert b'Congratulations, everything looks fine!' in rv.data

        rv = c.post(
            url_for('check_similar'),
            data={'classes': 'person', 'ratio': 100},
            follow_redirects=True)
        assert b'Oliver Twist' in rv.data

        rv = c.get(url_for('settings', category='mail'))
        assert b'mail from' in rv.data

        rv = c.get(url_for('settings', category='general'))
        assert b'log level' in rv.data

        rv = c.get(url_for('settings', category='iiif'))
        assert b'on upload' in rv.data

        rv = c.get(url_for('settings', category='file'))
        assert b'file size in MB' in rv.data

        rv = c.post(
            url_for('admin_content', item='citation_example'),
            data={'en': 'cool citation'},
            follow_redirects=True)
        assert b'Changes have been saved' in rv.data

        rv = c.get(url_for('insert', class_='edition'))
        assert b'cool citation' in rv.data

        rv = c.get(url_for('admin_content', item='legal_notice'))
        assert b'Save' in rv.data

        rv = c.get(url_for('arche_index'))
        assert b'https://arche-curation.acdh-dev.oeaw.ac.at/' in rv.data

        rv = c.post(
            url_for('admin_content', item='legal_notice'),
            data={'en': 'My legal notice', 'de': 'German notice'},
            follow_redirects=True)
        assert b'My legal notice' in rv.data

        c.get('/index/setlocale/de')
        rv = c.get(url_for('index_content', item='legal_notice'))
        assert b'German notice' in rv.data
