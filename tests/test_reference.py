from flask import url_for

from openatlas import app
from tests.base import TestBaseCase, insert


class ReferenceTest(TestBaseCase):

    def test_reference(self) -> None:
        c = self.client
        with app.test_request_context():
            app.preprocess_request()
            batman = insert('person', 'Batman')

        rv = c.post(
            url_for('insert', class_='external_reference'),
            data={'name': 'https://openatlas.eu',  'description': 'No'})
        reference_id = rv.location.split('/')[-1]

        rv = c.get(url_for('update', id_=reference_id))
        assert b'https://openatlas.eu' in rv.data

        rv = c.post(
            url_for('update', id_=reference_id),
            data={'name': 'https://d-nb.info',  'description': 'No'},
            follow_redirects=True)
        assert b'https://d-nb.info' in rv.data

        return  # Todo: continue tests

        rv = c.post(
            url_for('reference_add', id_=reference_id, view='actor'),
            data={'actor': batman.id},
            follow_redirects=True)
        assert b'https://d-nb.info' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            link_id = batman.get_links('P67', True)[0].id

        rv = c.post(
            url_for('link_update', id_=link_id, origin_id=reference_id),
            data={'page': '666'},
            follow_redirects=True)
        assert b'Changes have been saved' in rv.data
