from typing import Any

from flask import url_for

from openatlas import app
from tests.base import TestBaseCase, insert


class SourceTest(TestBaseCase):

    def test_source(self) -> None:
        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                gillian = insert('person', 'Gillian Anderson Gillian Anderson')
                artifact = insert('artifact', 'Artifact with inscription')
                reference = insert('external_reference', 'https://d-nb.info')

            rv: Any = self.app.post(
                url_for('insert', class_='source'),
                data={'name': 'Necronomicon'})
            source_id = rv.location.split('/')[-1]

            rv = self.app.get(
                url_for('insert', class_='source', origin_id=artifact.id))
            assert b'Artifact with inscription' in rv.data

            rv = self.app.get(
                url_for('link_insert', id_=source_id, view='actor'),
                data={'checkbox_values': [gillian.id]})
            assert b'Gillian' in rv.data

            rv = self.app.get(url_for('update', id_=source_id))
            assert b'Necronomicon' in rv.data

            rv = self.app.post(
                url_for('update', id_=source_id),
                data={
                    'name': 'Source updated',
                    'description': 'some description',
                    'artifact': [artifact.id]},
                follow_redirects=True)
            assert b'Source updated' in rv.data

            rv = self.app.get(url_for('entity_add_reference', id_=source_id))
            assert b'link reference' in rv.data

            rv = self.app.post(
                url_for('entity_add_reference', id_=source_id),
                data={'reference': reference.id, 'page': '777'},
                follow_redirects=True)
            assert b'777' in rv.data

            rv = self.app.get(
                url_for(
                    'insert',
                    class_='source_translation',
                    origin_id=source_id))
            assert b'+&nbsp;<span' in rv.data

            rv = self.app.post(
                url_for(
                    'insert',
                    class_='source_translation',
                    origin_id=source_id),
                data={'name': 'Translation continued', 'continue_': 'yes'},
                follow_redirects=True)
            assert b'+' in rv.data

            rv = self.app.post(
                url_for(
                    'insert',
                    class_='source_translation',
                    origin_id=source_id),
                data={'name': 'Test translation'})
            translation_id = rv.location.split('/')[-1]

            rv = self.app.get(url_for('update', id_=translation_id))
            assert b'Test translation' in rv.data

            rv = self.app.post(
                url_for('update', id_=translation_id),
                data={'name': 'Translation updated'},
                follow_redirects=True)
            assert b'Translation updated' in rv.data

            rv = self.app.get(
                url_for(
                    'index',
                    view='source_translation',
                    delete_id=translation_id),
                follow_redirects=True)
            assert b'The entry has been deleted' in rv.data
