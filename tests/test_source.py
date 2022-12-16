from typing import Any

from flask import url_for

from openatlas import app
from openatlas.models.entity import Entity
from tests.base import TestBaseCase, insert_entity


class SourceTest(TestBaseCase):

    def test_source(self) -> None:
        with app.app_context():
            rv: Any = self.app.get(url_for('insert', class_='source'))
            assert b'+ Source' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                origin = Entity.insert('person', 'David Duchovny', 'person')
                actor = Entity.insert(
                    'person',
                    'Gillian Anderson Gillian Anderson',
                    'person')
                artifact = insert_entity('I care for you', 'artifact')
                inscribed_artifact = Entity.insert(
                    'artifact',
                    'Artifact with text')
                file = Entity.insert('file', 'X-Files')
                reference = Entity.insert(
                    'external_reference',
                    'https://openatlas.eu')

            rv = self.app.post(
                url_for('insert', class_='source', origin_id=origin.id),
                data={'name': 'Test source'},
                follow_redirects=True)
            assert b'An entry has been created' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                source = Entity.get_by_view('source')[0]
            rv = self.app.post(
                url_for('insert', class_='source', origin_id=reference.id),
                data={'name': 'Test source'},
                follow_redirects=True)
            assert b'https://openatlas.eu' in rv.data

            rv = self.app.post(
                url_for('insert', class_='source', origin_id=file.id),
                data={'name': 'Test source'},
                follow_redirects=True)
            assert b'X-Files' in rv.data and b'An entry has been' in rv.data

            data = {'name': 'Test source', 'continue_': 'yes'}
            rv = self.app.post(
                url_for('insert', class_='source'),
                data=data,
                follow_redirects=True)
            assert b'An entry has been created' in rv.data

            rv = self.app.get(
                url_for('insert', class_='source', origin_id=artifact.id))
            assert b'I care for you' in rv.data

            rv = self.app.post(
                url_for('insert', class_='source', origin_id=artifact.id),
                data={'name': 'Necronomicon', 'artifact': [artifact.id]},
                follow_redirects=True)
            assert b'I care for you' in rv.data

            rv = self.app.get(url_for('index', view='source'))
            assert b'Test source' in rv.data

            rv = self.app.post(
                url_for(
                    'insert',
                    class_='external_reference',
                    origin_id=source.id),
                data={'name': 'https://openatlas.eu'},
                follow_redirects=True)
            assert b'Test source' in rv.data

            self.app.get(
                url_for(
                    'link_insert',
                    id_=source.id,
                    origin_id=actor.id,
                    view='actor'))
            rv = self.app.post(
                url_for('link_insert', id_=source.id, view='actor'),
                data={'checkbox_values': [actor.id]},
                follow_redirects=True)
            assert b'Gillian Anderson' in rv.data

            rv = self.app.get(url_for('view', id_=source.id))
            assert b'Gillian Anderson' in rv.data

            rv = self.app.get(
                url_for('link_insert', id_=source.id, view='place'))
            assert b'Place' in rv.data

            rv = self.app.get(url_for('update', id_=source.id))
            assert b'Test source' in rv.data

            data = {
                'name': 'Source updated',
                'description': 'some description',
                'artifact': str([inscribed_artifact.id])}
            rv = self.app.post(
                url_for('update', id_=source.id),
                data=data,
                follow_redirects=True)
            assert b'Source updated' in rv.data and b'Artifact with' in rv.data

            rv = self.app.get(url_for('view', id_=source.id))
            assert b'some description' in rv.data

            # Add to source
            rv = self.app.get(url_for('entity_add_reference', id_=source.id))
            assert b'Link reference' in rv.data

            rv = self.app.post(
                url_for('entity_add_reference', id_=source.id),
                data={'reference': reference.id, 'page': '777'},
                follow_redirects=True)
            # Todo: fix page display at reference tab of source
            print(rv.data)
            assert b'777' in rv.data

            rv = self.app.get(url_for(
                'insert',
                class_='source_translation',
                origin_id=source.id))
            assert b'+ Source translation' in rv.data

            rv = self.app.post(
                url_for(
                    'insert',
                    class_='source_translation',
                    origin_id=source.id),
                follow_redirects=True,
                data={'name': 'Translation continued', 'continue_': 'yes'})
            assert b'+ Source translation' in rv.data

            rv = self.app.post(
                url_for(
                    'insert',
                    class_='source_translation',
                    origin_id=source.id),
                data={'name': 'Test translation'})
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                translation_id = rv.location.split('/')[-1]
            rv = self.app.get(url_for('view', id_=source.id))
            assert b'Test translation' in rv.data

            self.app.get(url_for('update', id_=translation_id))
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
            assert b'The entry has been deleted.' in rv.data

            rv = self.app.get(
                url_for('index', view='source', delete_id=source.id))
            assert b'The entry has been deleted.' in rv.data
