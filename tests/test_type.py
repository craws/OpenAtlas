from typing import Any

from flask import g, url_for

from openatlas import app
from tests.base import TestBaseCase, get_hierarchy, insert


class TypeTest(TestBaseCase):

    def test_type(self) -> None:
        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()
                actor_type = get_hierarchy('Actor relation')
                dimension_type = get_hierarchy('Dimensions')
                historical_type = get_hierarchy('Historical place')
                place = insert('place', 'Home')
                place.link('P2', g.types[dimension_type.subs[0]], '46')
                location = place.get_linked_entity_safe('P53')
                location.link('P89', g.types[historical_type.subs[0]])

            rv: Any = self.app.get(
                url_for('view', id_=historical_type.subs[0]))
            assert b'Historical place' in rv.data

            rv = self.app.get(
                url_for('insert', class_='type', origin_id=actor_type.id))
            assert b'Actor relation' in rv.data

            data = {
                'name': 'My secret type',
                'name_inverse': 'Do I look inverse?',
                'description': 'Very important!',
                actor_type.id: actor_type.subs[0]}
            rv = self.app.post(
                url_for('insert', class_='type', origin_id=actor_type.id),
                data=data)
            type_id = rv.location.split('/')[-1]

            rv = self.app.get(url_for('update', id_=type_id))
            assert b'My secret type' in rv.data
            assert b'super' in rv.data

            rv = self.app.get(url_for('update', id_=dimension_type.subs[0]))
            assert b'unit' in rv.data

            rv = self.app.post(
                url_for('update', id_=type_id),
                data=data,
                follow_redirects=True)
            assert b'Changes have been saved' in rv.data

            data['continue_'] = 'yes'
            rv = self.app.post(
                url_for('insert', class_='type', origin_id=actor_type.id),
                data=data,
                follow_redirects=True)
            assert b'An entry has been created' in rv.data

            rv = self.app.post(
                url_for('ajax_add_type'),
                data={
                    'name': 'New dynamic',
                    'description': 'Hello',
                    'superType': actor_type.id})
            assert rv.data.isdigit()

            rv = self.app.get(
                url_for('ajax_get_type_tree', root_id=actor_type.id))
            assert b'New dynamic' in rv.data

            rv = self.app.post(
                url_for('update', id_=actor_type.id),
                data=data)
            assert b'Forbidden' in rv.data

            admin_unit = get_hierarchy('Administrative unit')
            rv = self.app.post(
                url_for(
                    'insert',
                    class_='administrative_unit',
                    origin_id=admin_unit.subs[0]),
                data={'name': 'admin unit'},
                follow_redirects=True)
            assert b'An entry has been created' in rv.data

            rv = self.app.get(url_for('update', id_=admin_unit.subs[0]))
            assert b'admin unit' in rv.data

            rv = self.app.get(url_for('view', id_=dimension_type.subs[0]))
            assert b'Unit' in rv.data

            sex = get_hierarchy('Sex')
            sex_sub = g.types[sex.subs[0]]

            rv = self.app.get(
                url_for('type_unset_selectable', id_=sex_sub.id),
                follow_redirects=True)
            assert b'set selectable' in rv.data

            rv: Any = self.app.get(url_for('insert', class_='person'))
            assert b'sex' in rv.data

            rv: Any = self.app.get(url_for('type_index'))
            assert b'sex' in rv.data

            rv = self.app.get(
                url_for('type_set_selectable', id_=sex_sub.id),
                follow_redirects=True)
            assert b'set unselectable' in rv.data

            with app.test_request_context():
                app.preprocess_request()
                actor = insert('person', 'Connor MacLeod')
                actor.link('P2', sex_sub)

            rv = self.app.get(url_for('show_untyped_entities', id_=sex.id))
            assert b'no entries' in rv.data

            rv = self.app.get(
                url_for('show_untyped_entities', id_=admin_unit.id))
            assert b'Home' in rv.data

            rv = self.app.get(
                url_for('type_delete', id_=actor_type.id),
                follow_redirects=True)
            assert b'Forbidden' in rv.data

            with app.test_request_context():
                app.preprocess_request()
                actor.link('P2', g.types[sex.subs[1]])

            rv = self.app.get(url_for('update', id_=actor.id))
            assert b'422' in rv.data

            rv = self.app.post(
                url_for('type_move_entities', id_=dimension_type.subs[0]))
            assert b'403' in rv.data

            rv = self.app.get(
                url_for('show_multiple_linked_entities', id_=sex.id))
            assert b'Connor' in rv.data

            self.app.post(
                url_for('hierarchy_update', id_=sex.id),
                data={'multiple': True})
            rv = self.app.get(url_for('hierarchy_update', id_=sex.id))
            assert b'disabled="disabled" id="multiple"' in rv.data

            rv = self.app.get(
                url_for('hierarchy_delete', id_=sex.id),
                follow_redirects=True)
            assert b'Warning' in rv.data

            with app.test_request_context():
                app.preprocess_request()
                actor.link('P74', location, type_id=actor_type.subs[0])

            rv = self.app.get(
                url_for('type_delete_recursive', id_=actor_type.subs[0]))
            assert b'Warning' in rv.data

            rv = self.app.post(
                url_for('type_delete_recursive', id_=sex.id),
                data={'confirm_delete': True},
                follow_redirects=True)
            assert b'Types deleted' in rv.data

            rv = self.app.post(
                url_for('type_delete_recursive', id_=actor_type.id),
                data={'confirm_delete': True})
            assert b'403 - Forbidden' in rv.data
