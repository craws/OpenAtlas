from typing import Any

from flask import url_for

from openatlas import app
from openatlas.models.entity import Entity
from tests.base import TestBaseCase


class ReferenceTest(TestBaseCase):

    def test_reference(self) -> None:
        with app.app_context():
            rv: Any = self.app.get(url_for('insert', class_='bibliography'))
            assert b'+ Bibliography' in rv.data

            rv = self.app.get(url_for('insert', class_='edition'))
            assert b'+ Edition' in rv.data

            data = {
                'name': 'https://openatlas.eu',
                'description': 'Reference description'}
            rv = self.app.post(
                url_for('insert', class_='external_reference'),
                data=data)
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                reference = Entity.get_by_id(rv.location.split('/')[-1])
            data['continue_'] = 'yes'
            rv = self.app.post(
                url_for('insert', class_='external_reference'),
                data=data,
                follow_redirects=True)
            assert b'An entry has been created' in rv.data

            rv = self.app.get(url_for('index', view='reference'))
            assert b'https://openatlas.eu' in rv.data

            rv = self.app.get(url_for('update', id_=reference.id))
            assert b'https://openatlas.eu' in rv.data

            data['name'] = 'https://updated.openatlas.eu'
            rv = self.app.post(
                url_for('update', id_=reference.id),
                data=data,
                follow_redirects=True)
            assert b'https://updated.openatlas.eu' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                batman = Entity.insert('person', 'Batman')
            rv = self.app.get(
                url_for('reference_add', id_=reference.id, view='actor'))
            assert b'Batman' in rv.data

            rv = self.app.post(
                url_for('reference_add', id_=reference.id, view='actor'),
                data={'actor': batman.id},
                follow_redirects=True)
            assert b'https://updated.openatlas.eu' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                link_id = batman.get_links('P67', True)[0].id
                file = Entity.insert('file', 'The X-Files')
                file.link('P67', reference)
            rv = self.app.post(
                url_for('link_update', id_=link_id, origin_id=reference.id),
                data={'page': '666'}, follow_redirects=True)
            assert b'Changes have been saved' in rv.data

            rv = self.app.get(
                url_for('index', view='reference', delete_id=reference.id))
            assert b'The entry has been deleted.' in rv.data
