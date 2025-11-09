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
            data={'name': 'https://openatlas.eu'})
        reference_id = rv.location.split('/')[-1]

        rv = c.get(url_for('update', id_=reference_id))
        assert b'https://openatlas.eu' in rv.data

        rv = c.post(
            url_for('update', id_=reference_id),
            data={'name': 'https://d-nb.info'},
            follow_redirects=True)
        assert b'https://d-nb.info' in rv.data

        rv = c.post(
            url_for(
                'link_insert_detail',
                origin_id=reference_id,
                relation_name='actor'),
            data={'actor': batman.id},
            follow_redirects=True)
        assert b'https://d-nb.info' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            links = batman.get_links('P67', ['external_reference'], True)

        rv = c.post(
            url_for(
                'link_update',
                id_=links[0].id,
                origin_id=reference_id,
                relation='actor'),
            data={'page': '666'},
            follow_redirects=True)
        assert b'Changes have been saved' in rv.data

        rv = c.post(
            url_for('update', id_=reference_id, copy='copy_'),
            data={'name': 'https://openatlas.eu'},
            follow_redirects=True)
        assert b'An entry has been created' in rv.data
