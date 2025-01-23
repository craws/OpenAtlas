from pathlib import Path

from flask import g, url_for

from openatlas import app
from openatlas.database import entity as db
from openatlas.forms.util import form_to_datetime64
from openatlas.models.entity import Link
from tests.base import TestBaseCase, get_hierarchy, insert


class TokenTests(TestBaseCase):
    def test_token(self) -> None:
        c = self.client
        with app.test_request_context():
            app.preprocess_request()


        rv = c.get(url_for('api_token'))
        assert b'Token' in rv.data

        rv = c.get(url_for('generate_token'))
        assert b'Generate token' in rv.data

        rv = c.post(url_for('generate_token'))
        assert b'Generate token' in rv.data
