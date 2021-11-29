from flask import g, url_for

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.type import Type
from tests.base import TestBaseCase


class TypeTest(TestBaseCase):

    def test_type(self) -> None:
        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                actor_type = Type.get_hierarchy('Actor actor relation')
                dimension_type = Type.get_hierarchy('Dimensions')
                sex_type = Type.get_hierarchy('Sex')
            rv = self.app.get(url_for('type_index'))
            assert b'Actor actor relation' in rv.data
            rv = self.app.get(
                url_for('insert', class_='type', origin_id=actor_type.id))
            assert b'Actor actor relation' in rv.data
            rv = self.app.post(
                url_for('insert', class_='type', origin_id=actor_type.id),
                data={'name_search': 'new'})
            assert b'Inverse' in rv.data
            data = {
                'name': 'My secret type',
                'name_inverse': 'Do I look inverse?',
                'description': 'Very important!'}
            rv = self.app.post(
                url_for('insert', class_='type', origin_id=actor_type.id),
                data=data)
            type_id = rv.location.split('/')[-1]
            rv = self.app.get(url_for('update', id_=type_id))
            assert b'My secret type' in rv.data and b'Super' in rv.data
            self.app.post(
                url_for('insert', class_='type', origin_id=sex_type.id),
                data=data)
            rv = self.app.post(
                url_for('update', id_=type_id),
                data=data,
                follow_redirects=True)
            assert b'Changes have been saved.' in rv.data

            # Insert an continue
            data['continue_'] = 'yes'
            rv = self.app.post(
                url_for('insert', class_='type', origin_id=actor_type.id),
                data=data,
                follow_redirects=True)
            assert b'An entry has been created' in rv.data
            data['continue_'] = ''

            # Forbidden system type
            rv = self.app.post(
                url_for('update', id_=actor_type.id),
                data=data,
                follow_redirects=True)
            assert b'Forbidden' in rv.data

            # Update with self as root
            data[str(actor_type.id)] = type_id
            rv = self.app.post(
                url_for('update', id_=type_id),
                data=data,
                follow_redirects=True)
            assert b'Type can&#39;t have itself as super' in rv.data

            # Update with sub as root
            rv = self.app.post(
                url_for('insert', class_='type', origin_id=actor_type.id),
                data=data)
            sub_type_id = rv.location.split('/')[-1].replace('type#tab-', '')
            data[str(actor_type.id)] = sub_type_id
            rv = self.app.post(
                url_for('update', id_=type_id),
                data=data,
                follow_redirects=True)
            assert b'Type can&#39;t have a sub as super' in rv.data

            # Custom type
            rv = self.app.get(
                url_for('view', id_=sex_type.id),
                follow_redirects=True)
            assert b'Male' in rv.data

            # Administrative unit
            rv = self.app.get(
                url_for(
                    'view',
                    id_=Type.get_hierarchy('Administrative unit').id),
                follow_redirects=True)
            assert b'Austria' in rv.data

            # Value type
            rv = self.app.get(
                url_for('view', id_=dimension_type.id),
                follow_redirects=True)
            assert b'Height' in rv.data
            rv = self.app.get(url_for('view', id_=dimension_type.subs[0]))
            assert b'Unit' in rv.data
            rv = self.app.get(url_for('update', id_=dimension_type.subs[0]))
            assert b'Dimensions' in rv.data

            # Untyped entities

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                actor = Entity.insert('person', 'Connor MacLeod')
            rv = self.app.get(url_for('show_untyped_entities', id_=sex_type.id))
            assert b'Connor MacLeod' in rv.data
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                actor.link('P2', g.types[sex_type.subs[0]])
            rv = self.app.get(url_for('show_untyped_entities', id_=sex_type.id))
            assert b'No entries' in rv.data

            # Delete
            rv = self.app.get(
                url_for('type_delete', id_=actor_type.id),
                follow_redirects=True)
            assert b'Forbidden' in rv.data
            rv = self.app.get(
                url_for('type_delete', id_=sub_type_id),
                follow_redirects=True)
            assert b'The entry has been deleted.' in rv.data
