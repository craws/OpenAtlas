from flask import url_for

from openatlas import app
from tests.base import TestBaseCase, get_hierarchy, insert


class ActorTests(TestBaseCase):

    def test_actor(self) -> None:
        c = self.client
        with app.test_request_context():
            app.preprocess_request()
            place = insert('place', 'Vienna')
            event = insert('acquisition', 'Event Horizon')
            group = insert('group', 'LV-426 colony')

        rv = c.get(url_for('insert', class_='person'))
        assert b'Vienna' in rv.data

        sex = get_hierarchy('Sex')
        data = {
            sex.id: sex.subs[0],
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
        rv = c.post(url_for('insert', class_='person'), data=data)
        actor_id = rv.location.split('/')[-1]

        rv = c.post(
            url_for('insert', class_='group'),
            data=data,
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        data["name"] = '<h1 class="test">Sigourney Weaver</h1>with HTML'
        rv = c.post(
            url_for('insert', class_='person'),
            data=data,
            follow_redirects=True)
        assert b'<h1 class="test">Sigourney Weaver</h1>' not in rv.data
        assert b'Sigourney Weaver' in rv.data

        rv = c.post(
            url_for('insert', class_='person'),
            data=data,
            follow_redirects=True)
        print(url_for('insert', class_='person', origin_id=place.id))
        assert b'An entry has been created' in rv.data

        rv = c.post(
            url_for('type_move_entities', id_=sex.subs[0]),
            data={
                sex.id: sex.subs[1],
                'selection': [actor_id],
                'checkbox_values': str([actor_id])},
            follow_redirects=True)
        assert b'Entities were updated' in rv.data

        rv = c.get(url_for('remove_class', id_=sex.id, name='person'))
        assert b'403' in rv.data

        rv = c.post(
            url_for('insert', class_='person'),
            data=data,
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        rv = c.post(
            url_for('insert', class_='person', origin_id=event.id),
            data=data,
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        c.get(url_for('logout'))
        c.post(
            url_for('login'),
            data={'username': 'Manager', 'password': 'test'})
        rv = c.get(url_for('update', id_=actor_id))
        assert b'American actress' in rv.data

        data.update({
            'name': 'Susan Alexandra Weaver',
            'alias-1': 'Ripley1',
            'end_year_from': '',
            'end_year_to': '',
            'begin_year_to': '1950',
            'begin_day_from': ''})

        rv = c.post(
            url_for('update', id_=actor_id),
            data=data,
            follow_redirects=True)
        assert b'Changes have been saved' in rv.data

        rv = c.post(
            url_for('ajax_create_entity'),
            data={
                'entityName': 'artifact',
                'name': 'Bishop',
                'standardType': get_hierarchy('Artifact').id,
                'description': 'AI'})
        assert rv.data.isdigit()

        rv = c.get(
            url_for('link_delete', origin_id=actor_id, id_=666),
            follow_redirects=True)
        assert b'removed' in rv.data

        rv = c.get(
            url_for('link_insert_detail', origin_id=group.id, name='member'))
        assert b'Actor function' in rv.data

        rv = c.post(
            url_for(
                'link_insert_detail',
                origin_id=actor_id,
                name='member_of'),
            data={'member_of': [group.id]},
            follow_redirects=True)
        assert b'LV-426 colony' in rv.data

        rv = c.post(
            url_for('link_insert_detail', origin_id=group.id, name='member'),
            data={'member': [actor_id]},
            follow_redirects=True)
        assert b'LV-426 colony' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            link_ = group.get_links('P107')[0]

        rv = c.post(
            url_for(
                'link_update', id_=link_.id,
                origin_id=group.id,
                name="member"),
            data={'description': 'We are here to help you'},
            follow_redirects=True)
        assert b'We are here to help you' in rv.data
