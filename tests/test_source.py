from flask import url_for

from openatlas import app
from tests.base import TestBaseCase, insert


class SourceTest(TestBaseCase):

    def test_source(self) -> None:
        c = self.client
        with app.test_request_context():
            app.preprocess_request()
            gillian = insert('person', 'Gillian Anderson Gillian Anderson')
            artifact = insert('artifact', 'Artifact with inscription')

        rv = c.post(
            url_for('insert', class_='source'),
            data={
                'name': 'Necronomicon',
                'description': (
                    'The <mark meta="{"annotationId":"c27",'
                    f'"entityId":{artifact.id},'
                    '"comment":"asdf"}">Necronomicon</mark>,'
                    ' also referred to as the Book of the Dead')})
        source_id = rv.location.split('/')[-1]

        rv = c.get(url_for('insert', class_='source'))
        assert b'Artifact with inscription' in rv.data

        rv = c.get(url_for('link_insert', origin_id=source_id, name='actor'))
        assert b'Gillian' in rv.data

        rv = c.post(
            url_for('link_insert', origin_id=source_id, name='actor'),
            data={'checkbox_values': [gillian.id]},
            follow_redirects=True)
        assert b'Gillian' in rv.data

        rv = c.get(url_for('update', id_=source_id))
        assert b'Necronomicon' in rv.data

        rv = c.post(
            url_for('update', id_=source_id),
            data={
                'name': 'Source updated',
                'description': (
                    'The <mark meta="{"annotationId":"c27",'
                    '"comment":"asdf"}">Necronomicon</mark>,'
                    ' also referred to as the Book of the Dead'),
                'artifact': [artifact.id]},
            follow_redirects=True)
        assert b'Source updated' in rv.data

        rv = c.get(url_for('insert', class_='source_translation'))
        assert b'+ Source translation' in rv.data

        rv = c.post(
            url_for(
                'insert',
                class_='source_translation',
                origin_id=source_id,
                relation='text'),
            data={'name': 'continue', 'source': source_id, 'continue_': 'yes'},
            follow_redirects=True)
        assert b'+' in rv.data

        rv = c.post(
            url_for(
                'insert',
                class_='source_translation',
                relation='text'),
            data={'name': 'Test translation', 'source': source_id})
        translation_id = rv.location.split('/')[-1]

        rv = c.get(url_for('update', id_=translation_id))
        assert b'Test translation' in rv.data

        rv = c.post(
            url_for('update', id_=translation_id),
            data={
                'name': 'Translation updated',
                'source': source_id,
                'opened': '9999999999'},
            follow_redirects=True)
        assert b'Changes have been saved' in rv.data

        rv = c.post(
            url_for('update', id_=translation_id),
            data={
                'name': 'Translation updated',
                'source': source_id,
                'opened': '1000000000'},
            follow_redirects=True)
        assert b'because it has been modified' in rv.data

        rv = c.get(
            url_for('delete', id_=translation_id),
            follow_redirects=True)
        assert b'The entry has been deleted' in rv.data
