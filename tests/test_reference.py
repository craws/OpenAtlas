from typing import Any

from flask import url_for

from openatlas import app
from openatlas.models.entity import Entity
from tests.base import TestBaseCase, insert


class ReferenceTest(TestBaseCase):

    def test_reference(self) -> None:
        with app.app_context():
            rv: Any = self.app.post(
                url_for('insert', class_='external_reference'),
                data={'name': 'https://openatlas.eu',  'description': 'No'})
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                reference = Entity.get_by_id(rv.location.split('/')[-1])
                batman = insert('person', 'Batman')

            rv = self.app.get(url_for('update', id_=reference.id))
            assert b'https://openatlas.eu' in rv.data

            rv = self.app.post(
                url_for('update', id_=reference.id),
                data={'name': 'https://d-nb.info',  'description': 'No'},
                follow_redirects=True)
            assert b'https://d-nb.info' in rv.data

            rv = self.app.post(
                url_for('reference_add', id_=reference.id, view='actor'),
                data={'actor': batman.id},
                follow_redirects=True)
            assert b'https://d-nb.info' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                link_id = batman.get_links('P67', True)[0].id
            rv = self.app.post(
                url_for('link_update', id_=link_id, origin_id=reference.id),
                data={'page': '666'}, follow_redirects=True)
            assert b'Changes have been saved' in rv.data
