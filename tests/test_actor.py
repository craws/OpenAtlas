from typing import Any

from flask import g, url_for

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.type import Type
from tests.base import TestBaseCase


class ActorTests(TestBaseCase):

    def test_actor(self) -> None:
        with app.app_context():
            rv: Any = self.app.get(url_for('index', view='actor'))
            assert b'No entries' in rv.data

            rv = self.app.post(url_for('insert', class_='place'), data={
                'name': 'Captain Miller',
                })
            residence_id = rv.location.split('/')[-1]
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                sex_type = Type.get_hierarchy('Sex')
                sex_type_sub_1 = g.types[sex_type.subs[0]]
                sex_type_sub_2 = g.types[sex_type.subs[1]]
                event = Entity.insert('acquisition', 'Event Horizon')
                source = Entity.insert('source', 'Necronomicon')
                artifact_type_id = Type.get_hierarchy('Artifact').id

            rv = self.app.get(url_for('insert', class_='person'))
            assert b'+ Person' in rv.data

            self.app.get(
                url_for('insert', class_='person', origin_id=residence_id))
            data = {
                sex_type.id: sex_type_sub_1.id,
                'name': 'Sigourney Weaver',
                'alias-1': 'Ripley',
                'residence': residence_id,
                'begins_in': residence_id,
                'ends_in': residence_id,
                'description': 'Susan Alexandra Weaver is an American actress',
                'begin_year_from': '-1949',
                'begin_month_from': '10',
                'begin_day_from': '8',
                'begin_hour_from': '13',
                'begin_minute_from': '33',
                'begin_second_from': '37',
                'begin_year_to': '-1948',
                'begin_hour_to': '13',
                'begin_minute_to': '33',
                'begin_second_to': '37',
                'end_year_from': '2049',
                'end_hour_from': '13',
                'end_minute_from': '33',
                'end_second_from': '37',
                'end_year_to': '2050',
                'end_hour_to': '13',
                'end_minute_to': '33',
                'end_second_to': '37',
                }
            rv = self.app.post(url_for('insert', class_='person'), data=data)
            actor_id = rv.location.split('/')[-1]
            self.app.post(url_for('insert', class_='group'), data=data)
            rv = self.app.post(
                url_for('insert', class_='person', origin_id=residence_id),
                data=data,
                follow_redirects=True)
            assert b'An entry has been created' in rv.data

            rv = self.app.get(url_for('view', id_=sex_type_sub_1.id))
            assert b'Susan' in rv.data

            rv = self.app.get(
                url_for('type_move_entities', id_=sex_type_sub_1.id))
            assert b'Sigourney' in rv.data

            rv = self.app.post(
                url_for('type_move_entities', id_=sex_type_sub_1.id),
                follow_redirects=True,
                data={
                    sex_type.id: sex_type_sub_2.id,
                    'selection': [actor_id],
                    'checkbox_values': str([actor_id])})
            assert b'Entities were updated' in rv.data

            rv = self.app.post(
                url_for('type_move_entities', id_=sex_type_sub_2.id),
                follow_redirects=True,
                data={
                    sex_type.id: '',
                    'selection': [actor_id],
                    'checkbox_values': str([actor_id])})
            assert b'Entities were updated' in rv.data

            rv = self.app.get(
                url_for('remove_class', id_=sex_type.id, name='person'))
            assert b'403' in rv.data

            self.app.post(
                url_for('insert', class_='person', origin_id=actor_id),
                data=data)
            self.app.post(
                url_for('insert', class_='person', origin_id=event.id),
                data=data)
            self.app.post(
                url_for('insert', class_='person', origin_id=source.id),
                data=data)
            rv = self.app.post(
                url_for('insert', class_='external_reference'),
                data={'name': 'https://openatlas.eu'})
            reference_id = rv.location.split('/')[-1]
            rv = self.app.post(
                url_for('insert', class_='person', origin_id=reference_id),
                data=data,
                follow_redirects=True)
            assert b'An entry has been created' in rv.data

            data['continue_'] = 'yes'
            rv = self.app.post(
                url_for('insert', class_='person'),
                data=data,
                follow_redirects=True)
            assert b'An entry has been created' in rv.data

            rv = self.app.get(url_for('index', view='actor'))
            assert b'Sigourney Weaver' in rv.data

            rv = self.app.get(url_for('entity_add_source', id_=actor_id))
            assert b'Link source' in rv.data

            rv = self.app.post(
                url_for('entity_add_source', id_=actor_id),
                data={'checkbox_values': str([source.id])},
                follow_redirects=True)
            assert b'Necronomicon' in rv.data

            rv = self.app.get(url_for('entity_add_reference', id_=actor_id))
            assert b'Link reference' in rv.data

            rv = self.app.post(
                url_for('entity_add_reference', id_=actor_id),
                data={'reference': reference_id, 'page': '777'},
                follow_redirects=True)
            assert b'777' in rv.data

            self.login('manager')
            rv = self.app.get(url_for('update', id_=actor_id))
            assert b'American actress' in rv.data

            data['name'] = 'Susan Alexandra Weaver'
            data['alias-1'] = 'Ripley1'
            data['end_year_from'] = ''
            data['end_year_to'] = ''
            data['begin_year_to'] = '1950'
            data['begin_day_from'] = ''
            rv = self.app.post(
                url_for('update', id_=actor_id),
                data=data,
                follow_redirects=True)
            assert b'Changes have been saved' in rv.data

            rv = self.app.post(
                url_for('ajax_bookmark'),
                data={'entity_id': actor_id})
            assert b'Remove bookmark' in rv.data

            rv = self.app.post(
                url_for('ajax_create_entity'),
                data={
                    'entityName': 'artifact',
                    'name': 'Bishop',
                    'standardType': artifact_type_id,
                    'description': 'AI'})
            assert rv.data.isdigit()

            rv = self.app.post(
                url_for('ajax_get_entity_table', content_domain='artifact'),
                data={'filterIds': str([])})
            assert b'Bishop' in rv.data

            rv = self.app.get('/')
            assert b'Weaver' in rv.data

            rv = self.app.post(
                url_for('ajax_bookmark'),
                data={'entity_id': actor_id})
            assert b'Bookmark' in rv.data

            rv = self.app.get(
                url_for('link_delete', origin_id=actor_id, id_=666),
                follow_redirects=True)
            assert b'removed' in rv.data

            rv = self.app.get(
                url_for('index', view='actor', delete_id=actor_id))
            assert b'The entry has been deleted.' in rv.data
