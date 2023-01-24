from flask import url_for

from openatlas import app
from tests.base import TestBaseCase


class ArcheTest(TestBaseCase):

    def test_export(self) -> None:
        with app.app_context():
            rv = self.app.get(url_for('arche_index'))
            assert b'https://arche-curation.acdh-dev.oeaw.ac.at/' in rv.data

            rv = self.app.get(url_for('arche_fetch'))
            assert b'No entities to retrieve' in rv.data


