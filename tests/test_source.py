import json

from flask import url_for

from openatlas import app
from openatlas.models.annotation import AnnotationText
from openatlas.models.entity import Entity
from tests.base import TestBaseCase, insert


class SourceTest(TestBaseCase):
    def test_source(self) -> None:
        c = self.client
        with app.test_request_context():
            app.preprocess_request()
            gillian = insert('person', 'Gillian Anderson Gillian Anderson')
            artifact = insert('artifact', 'Artifact with inscription')

        annotation_data = {
            'annotation_id': 'c27',
            'comment': 'whatever',
            'entityId': artifact.id}
        rv = c.post(
            url_for('insert', class_='source'),
            data={
                'name': 'Necronomicon',
                'description':
                    f'The <mark meta="{json.dumps(annotation_data)}">'
                    'Necronomicon</mark>, the Book of the Dead.'})
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

        del annotation_data['entityId']
        rv = c.post(
            url_for('update', id_=source_id),
            data={
                'name': 'Source updated',
                'description':
                    f'The <mark meta="{json.dumps(annotation_data)}">'
                    'Necronomicon</mark>, the Book of the Dead.',
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

        with app.test_request_context():
            app.preprocess_request()
            source = Entity.get_by_id(int(source_id))
            translation_2 = insert(
                'source_translation',
                'new translation',
                ('The <mark meta="{"annotationId":"c27",'
                 f'"entityId":{artifact.id},'
                 '"comment":"nice"}">Bible</mark>,'
                 ' also referred to as the Book of the living'))
            source.link('P73', translation_2)
            source.delete_links('P67', ['artifact'])

        rv = c.get(url_for('orphans'))
        assert b'/annotation/text/relink' in rv.data

        rv = c.get(
            url_for(
                'annotation_text_relink',
                origin_id=source.id,
                entity_id=artifact.id),
            follow_redirects=True)
        assert b'Entities relinked' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            annotation_id = AnnotationText.get_by_source_id(
                translation_2.id)[0].id
            source.delete_links('P67', ['artifact'])

        rv = c.get(
            url_for(
                'annotation_text_remove_entity',
                annotation_id=annotation_id,
                entity_id=artifact.id),
            follow_redirects=True)
        assert b'Entity removed from annotation' in rv.data

        rv = c.get(
            url_for('annotation_text_delete', id_=source.id),
            follow_redirects=True)
        assert b'Annotation deleted' in rv.data

        rv = c.get(
            url_for('delete', id_=translation_id),
            follow_redirects=True)
        assert b'The entry has been deleted' in rv.data
