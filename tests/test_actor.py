from typing import Any

from flask import g, url_for

from openatlas import app
from tests.base import TestBaseCase, get_hierarchy, insert_entity


class ActorTests(TestBaseCase):

    def test_actor(self) -> None:
        with app.app_context():
            place = insert_entity('place', 'Vienna')
            event = insert_entity('acquisition', 'Event Horizon')
            with app.app_context():
                with app.test_request_context():
                    app.preprocess_request()  # type: ignore
                sex = get_hierarchy('Sex')
                sex_sub_1 = g.types[sex.subs[0]]
                sex_sub_2 = g.types[sex.subs[1]]

            print(app.config['SERVER_NAME'])
            print(app.config['DATABASE_NAME'])
            print(app.config['DATABASE_USER'])
            print(app.config['DATABASE_HOST'])
            print(app.config['DATABASE_PORT'])
            print(app.config['DATABASE_PASS'])
            print(app.config['MAIL_PASSWORD'])
            print(app.config['SECRET_KEY'])
            print(app.config['DEBUG'])
            print(app.config['WTF_CSRF_ENABLED'])
            print(app.config['WTF_CSRF_METHODS'])

            rv: Any = self.app.get(
                url_for('insert', class_='person', origin_id=place.id))
            assert b'Vienna' in rv.data

            data = {
                sex.id: sex_sub_1.id,
                'name': 'Sigourney Weaver',
                'alias-1': 'Ripley',
                'residence': place.id,
                'begins_in': place.id,
                'ends_in': place.id,
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
                'end_second_to': '37'}
            rv = self.app.post(url_for('insert', class_='person'), data=data)
            actor_id = rv.location.split('/')[-1]

            rv = self.app.post(
                url_for('insert', class_='group'),
                data=data,
                follow_redirects=True)
            assert b'An entry has been created' in rv.data

            rv = self.app.post(
                url_for('insert', class_='person', origin_id=place.id),
                data=data,
                follow_redirects=True)
            assert b'An entry has been created' in rv.data

            rv = self.app.post(
                url_for('type_move_entities', id_=sex_sub_1.id),
                data={
                    sex.id: sex_sub_2.id,
                    'selection': [actor_id],
                    'checkbox_values': str([actor_id])},
                follow_redirects=True)
            assert b'Entities were updated' in rv.data

            rv = self.app.get(
                url_for('remove_class', id_=sex.id, name='person'))
            assert b'403' in rv.data

            rv = self.app.post(
                url_for('insert', class_='person', origin_id=actor_id),
                data=data,
                follow_redirects=True)
            assert b'An entry has been created' in rv.data

            rv = self.app.post(
                url_for('insert', class_='person', origin_id=event.id),
                data=data,
                follow_redirects=True)
            assert b'An entry has been created' in rv.data

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
                url_for('ajax_create_entity'),
                data={
                    'entityName': 'artifact',
                    'name': 'Bishop',
                    'standardType': get_hierarchy('Artifact').id,
                    'description': 'AI'})
            assert rv.data.isdigit()

            rv = self.app.post(
                url_for('ajax_get_entity_table', content_domain='artifact'),
                data={'filterIds': str([])})
            assert b'Bishop' in rv.data

            rv = self.app.get(
                url_for('link_delete', origin_id=actor_id, id_=666),
                follow_redirects=True)
            assert b'removed' in rv.data
