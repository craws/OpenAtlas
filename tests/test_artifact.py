from typing import Any

from flask import url_for

from openatlas import app
from tests.base import TestBaseCase, insert


class ArtifactTest(TestBaseCase):

    def test_artifact(self) -> None:
        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                source = insert('source', 'Necronomicon')
                actor = insert('person', 'Conan')
                place = insert('place', 'Home')
                sub_artifact = insert('artifact', 'Sub artifact')

            rv: Any = self.app.get(
                url_for('insert', class_='artifact', origin_id=place.id))
            assert b'+&nbsp;<span' in rv.data

            rv = self.app.post(
                url_for('insert', class_='artifact'),
                data={
                    'name': 'Love-letter',
                    'actor': actor.id,
                    'artifact_super': place.id})
            artifact_id = rv.location.split('/')[-1]

            rv = self.app.get(url_for('add_subunit', super_id=place.id))
            assert b'Love-letter' not in rv.data

            rv = self.app.post(
                url_for('add_subunit', super_id=place.id),
                data={'checkbox_values': [sub_artifact.id]},
                follow_redirects=True)
            assert b'Sub artifact' in rv.data

            rv = self.app.get(url_for('index', view='artifact'))
            assert b'Love-letter' in rv.data

            rv = self.app.get(url_for('update', id_=artifact_id))
            assert b'Love-letter' in rv.data

            rv = self.app.post(
                url_for('update', id_=artifact_id),
                data={
                    'name': 'A little hate',
                    'description': 'makes nothing better',
                    'artifact_super': place.id},
                follow_redirects=True)
            assert b'Changes have been saved' in rv.data

            rv = self.app.get(url_for('entity_add_source', id_=artifact_id))
            assert b'link source' in rv.data

            rv = self.app.post(
                url_for('entity_add_source', id_=artifact_id),
                data={'checkbox_values': str([source.id])},
                follow_redirects=True)
            assert b'Necronomicon' in rv.data

            rv = self.app.get(
                url_for('insert', class_='move', origin_id=artifact_id))
            assert b'A little hate' in rv.data

            rv = self.app.post(
                url_for('insert', class_='move', origin_id=artifact_id),
                data={'name': 'Event Horizon', 'artifact': [artifact_id]},
                follow_redirects=True)
            assert b'Event Horizon' in rv.data

            rv = self.app.get(
                url_for('link_insert', id_=actor.id, view='artifact'))
            assert b'A little hate' in rv.data

            rv = self.app.post(
                url_for('link_insert', id_=actor.id, view='artifact'),
                data={'checkbox_values': [artifact_id]},
                follow_redirects=True)
            assert b'A little hate' in rv.data

            rv = self.app.get(
                url_for('insert', class_='artifact', origin_id=actor.id))
            assert b'Conan' in rv.data

            rv = self.app.get(
                url_for('delete', id_=artifact_id),
                follow_redirects=True)
            assert b'The entry has been deleted' in rv.data

            rv = self.app.get(url_for('user_view', id_=self.alice_id))
            assert b'<a href="/admin/user/entities/2">1</a>' in rv.data

            rv = self.app.post(
                url_for('insert', class_='artifact'),
                data={'name': 'This will be continued', 'continue_': 'yes'},
                follow_redirects=True)
            assert b'An entry has been created' in rv.data

            rv = self.app.get(url_for('user_view', id_=self.alice_id))
            assert b'<a href="/admin/user/entities/2">2</a>' in rv.data

            rv = self.app.get(url_for('user_entities', id_=self.alice_id))
            assert b'This will be continued' in rv.data
