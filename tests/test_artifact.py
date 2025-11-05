from flask import url_for

from openatlas import app
from tests.base import TestBaseCase, insert


class ArtifactTest(TestBaseCase):

    def test_artifact(self) -> None:
        c = self.client
        with app.test_request_context():
            app.preprocess_request()
            source = insert('source', 'Necronomicon')
            actor = insert('person', 'Conan')
            place = insert('place', 'Home')
            sub_artifact = insert('artifact', 'Sub artifact')

        rv = c.get(url_for('insert', class_='artifact', origin_id=place.id))
        assert b'+ Artifact' in rv.data

        rv = c.post(
            url_for('insert', class_='artifact'),
            data={
                'name': 'Love-letter',
                'actor': actor.id,
                'super': place.id})
        artifact_id = rv.location.split('/')[-1]

        rv = c.get(url_for('view', id_=actor.id))
        assert b'Love-letter' in rv.data

        rv = c.get(
            url_for(
                'link_insert',
                origin_id=place.id,
                relation_name='artifact'))
        assert b'Love-letter' not in rv.data

        rv = c.post(
            url_for(
                'link_insert',
                origin_id=place.id,
                relation_name='artifact'),
            data={'checkbox_values': [sub_artifact.id]},
            follow_redirects=True)
        assert b'Sub artifact' in rv.data

        rv = c.get(url_for('index', group='artifact'))
        assert b'Love-letter' in rv.data

        rv = c.get(url_for('update', id_=artifact_id))
        assert b'Love-letter' in rv.data

        rv = c.post(
            url_for('update', id_=artifact_id),
            data={
                'name': 'A little hate',
                'description': 'makes nothing better',
                'super': place.id},
            follow_redirects=True)
        assert b'Changes have been saved' in rv.data

        rv = c.get(
            url_for(
                'link_insert',
                origin_id=artifact_id,
                relation_name='source'))
        assert b'Source' in rv.data

        rv = c.post(
            url_for(
                'link_insert',
                origin_id=artifact_id,
                relation_name='source'),
            data={'checkbox_values': str([source.id])},
            follow_redirects=True)
        assert b'Necronomicon' in rv.data

        rv = c.get(url_for('insert', class_='move', origin_id=artifact_id))
        assert b'A little hate' in rv.data

        rv = c.post(
            url_for('insert', class_='move', origin_id=artifact_id),
            data={'name': 'Event Zero', 'moved_artifact': [artifact_id]},
            follow_redirects=True)
        assert b'Event Zero' in rv.data

        rv = c.get(url_for('insert', class_='artifact', origin_id=actor.id))
        assert b'Conan' in rv.data

        rv = c.get(
            url_for('delete', id_=artifact_id),
            follow_redirects=True)
        assert b'The entry has been deleted' in rv.data

        rv = c.get(url_for('user_view', id_=self.alice_id))
        assert b'<a href="/user/entities/1">1</a>' in rv.data

        rv = c.get(url_for('admin_index'))
        assert b'>1</a>' in rv.data

        rv = c.post(
            url_for('insert', class_='artifact'),
            data={'name': 'This will be continued', 'continue_': 'yes'},
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        rv = c.get(url_for('user_view', id_=self.alice_id))
        assert b'<a href="/user/entities/1">2</a>' in rv.data

        rv = c.get(url_for('user_entities', id_=self.alice_id))
        assert b'This will be continued' in rv.data
