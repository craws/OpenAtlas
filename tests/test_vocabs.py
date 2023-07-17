from flask import url_for

from openatlas import app
from tests.base import TestBaseCase


class ExportImportTest(TestBaseCase):

    def test_vocabs(self) -> None:
        with app.app_context():
            rv = self.app.get(url_for('vocabs_index'))
            assert b'https://vocabs.acdh.oeaw.ac.at/' in rv.data

            rv = self.app.get(url_for('vocabs_update'))
            assert b'https://vocabs.acdh.oeaw.ac.at/' in rv.data

            self.login('Manager')
            rv = self.app.post(
                url_for('vocabs_update'),
                follow_redirects=True,
                data={
                    'base_url': 'https://vocabs.acdh.oeaw.ac.at/',
                    'endpoint': 'rest/v1/',
                    'vocabs_user': 'test'})
            assert b'test' in rv.data

            # rv = self.app.get(url_for('show_vocabularies'))
            # assert b'Backbone Thesaurus' in rv.data

            rv = self.app.get(url_for('vocabulary_import_view', id_='bbt'))
            assert b'Backbone Thesaurus' in rv.data

            rv = self.app.post(
                url_for('vocabulary_import_view', id_='bbt'),
                follow_redirects=True,
                data={
                    'confirm_import': True,
                    'concepts':
                        ['https://vocabs.dariah.eu/bbt/Concept/0000049'],
                    'classes': 'place',
                    'multiple': True,
                    'language': 'en'})
            assert b'Import of: 1' in rv.data

            rv = self.app.post(
                url_for('vocabulary_import_view', id_='bbt'),
                follow_redirects=True,
                data={
                    'confirm_import': True,
                    'concepts':
                        ['https://vocabs.dariah.eu/bbt/Concept/0000049'],
                    'classes': 'place',
                    'multiple': True,
                    'language': 'en'})
            assert b'Check log for not imported concepts' in rv.data

            # Test below is commented because of time out issues
            rv = self.app.post(
               url_for('vocabulary_import_view', id_='dyas'),
               follow_redirects=True,
               data={
                   'confirm_import': True,
                   'concepts':
                       ['https://humanitiesthesaurus.academyofathens.gr'
                        '/dyas-resource/Concept/22'],
                   'classes': 'place',
                   'multiple': True,
                   'language': 'en'})
            assert b'Import of: 1' in rv.data
