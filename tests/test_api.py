from flask import url_for
from nose.tools import raises

from openatlas import app
from openatlas.api.v02.resources.error import EntityDoesNotExistError
from openatlas.models.node import Node
from tests.base import TestBaseCase, insert_entity


class ApiTests(TestBaseCase):

    def test_api(self) -> None:
        with app.app_context():  # type: ignore
            with app.test_request_context():
                app.preprocess_request()
                place = insert_entity('Nostromos', 'place')
                external_reference = insert_entity('https://openatlas.eu', 'external_reference')
                feature = insert_entity('Feature', 'feature', place)
                strati = insert_entity('Strato', 'stratigraphic_unit', feature)

                unit_node = Node.get_hierarchy('Administrative Unit')

            # Path Tests
            rv = self.app.get(url_for('usage'))
            assert b'message' in rv.data
            rv = self.app.get(url_for('latest', latest=10))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('latest', count=True, latest=1))
            assert b'1' in rv.data
            rv = self.app.get(url_for('entity', id_=place.id))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('code', code='reference'))
            assert b'openatlas' in rv.data
            # rv = self.app.get(url_for('class', class_code='E33'))
            # assert b'Necronomicon' in rv.data
            rv = self.app.get(url_for('class', class_code='E31'))
            assert b'https://openatlas.eu' in rv.data
            rv = self.app.get(url_for('node_entities', id_=unit_node.id))
            assert b'Austria' in rv.data
            rv = self.app.get(url_for('node_entities_all', id_=unit_node.id))
            assert b'Austria' in rv.data
            # Todo: Expected Nostromos too, only get Asgard
            rv = self.app.get(
                url_for('query', entities=place.id, classes='E18', items='place'))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('content', lang='de'))
            assert b'intro' in rv.data

            # Path test with download
            rv = self.app.get(url_for('entity', id_=place.id, download=True))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('latest', latest=10, download=True))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('code', code='reference', download=True))
            assert b'https://openatlas.eu' in rv.data
            rv = self.app.get(url_for('class', class_code='E31', download=True))
            assert b'https://openatlas.eu' in rv.data
            rv = self.app.get(url_for('node_entities', id_=unit_node.id, download=True))
            assert b'Austria' in rv.data
            rv = self.app.get(url_for('node_entities_all', id_=unit_node.id, download=True))
            assert b'Austria' in rv.data
            rv = self.app.get(url_for('query', classes='E31', download=True))
            assert b'https://openatlas.eu' in rv.data
            rv = self.app.get(url_for('content', lang='de', download=True))
            assert b'intro' in rv.data

            # Testing Subunit

            rv = self.app.get(url_for('subunit', id_=place.id))
            assert b'Feature' in rv.data and b'Strato' not in rv.data
            rv = self.app.get(url_for('subunit', id_=place.id, download=True))
            assert b'Feature' in rv.data and b'Strato' not in rv.data
            rv = self.app.get(url_for('subunit', id_=place.id, count=True))
            assert b'1' in rv.data
            rv = self.app.get(url_for('subunit_hierarchy', id_=place.id))
            assert b'Strato' in rv.data
            rv = self.app.get(url_for('subunit_hierarchy', id_=place.id, download=True))
            assert b'Strato' in rv.data
            rv = self.app.get(url_for('subunit_hierarchy', id_=place.id, count=True))
            assert b'2' in rv.data

            # Parameter: filter
            rv = self.app.get(url_for('code',
                                      code='place',
                                      limit=10,
                                      sort='desc',
                                      column='name',
                                      filter='or|name|like|Nostromos'))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('code', code='reference'))
            assert b'openatlas' in rv.data
            rv = self.app.get(url_for('class',
                                      class_code='E18',
                                      filter='or|name|like|Nostr'))
            assert b'Nostromos' in rv.data
            # rv = self.app.get(url_for('class',
            #                           class_code='E18',
            #                           filter='or|created|gt|'))
            # assert b'404' in rv.data
            # rv = self.app.get(url_for('class',
            #                           class_code='E18',
            #                           filter='or|created|Wrong|2000-01-01'))
            # assert b'404' in rv.data
            # rv = self.app.get(url_for('class',
            #                           class_code='E18',
            #                           filter='or|created|gt|2000-01-623'))
            # assert b'404' in rv.data
            # rv = self.app.get(url_for('class',
            #                           class_code='E18',
            #                           filter='or|id|gt|String'))
            # assert b'404' in rv.data

            # Parameter: last
            rv = self.app.get(url_for('class', class_code='E18', last=place.id))
            assert b'entities' in rv.data
            # Parameter: first
            rv = self.app.get(url_for('class', class_code='E18', first=place.id))
            assert b'entities' in rv.data

            # Parameter: show
            rv = self.app.get(url_for('class', class_code='E31', show='types'))
            assert b'https://openatlas.eu' in rv.data
            rv = self.app.get(url_for('class', class_code='E31', show='when'))
            assert b'https://openatlas.eu' in rv.data
            rv = self.app.get(url_for('class', class_code='E31', show='none'))
            assert b'https://openatlas.eu' in rv.data

            # Parameter: count
            rv = self.app.get(url_for('class', class_code='E31', count=True))
            assert b'1' in rv.data

            # Todo: adapt for new external reference systems
            # rv = self.app.get(url_for('code', code='reference', count=True))
            # assert b'2' in rv.data  # Assert can vary, to get around use \n
            rv = self.app.get(
                url_for('query', entities=place.id, classes='E18', codes='place'))
            assert b'Nostromos' in rv.data
            rv = self.app.get(
                url_for('query', entities=place.id, classes='E18', codes='place', count=True))
            assert b'7' in rv.data
            rv = self.app.get(url_for('node_entities', id_=unit_node.id, count=True))
            assert b'6' in rv.data
            rv = self.app.get(url_for('node_entities_all', id_=unit_node.id, count=True))
            assert b'8' in rv.data

    @raises(EntityDoesNotExistError)
    def error_test(self):
        with app.app_context():  # type: ignore
            self.app.get(url_for('class', class_code='E18', last=1231223121321))
        # rv = self.app.get(url_for('entity', id_="Hello"))
        # assert b'404' in rv.data
        # rv = self.app.get(url_for('latest', latest=99999))
        # assert b'404' in rv.data
        # rv = self.app.get(url_for('latest', latest='wrong'))
        # assert b'404' in rv.data
        # rv = self.app.get(url_for('class', class_code='E99999'))
        # assert b'404' in rv.data
        # rv = self.app.get(url_for('code', code='Hello'))
        # assert b'404' in rv.data
        # rv = self.app.get(url_for('query'))
        # assert b'404' in rv.data
        #
        # rv = self.app.get(url_for('api_get_by_menu_item',
        #                           code='place',
        #                           limit=10,
        #                           sort='desc',
        #                           column='name',
        #                           filter='or|name|wrong|Nostromos'))
        # assert b'404f' in rv.data
        # rv = self.app.get(url_for('node_entities', id_='Hello'))
        # assert b'404' in rv.data
        # rv = self.app.get(url_for('node_entities_all', id_='Hello'))
        # assert b'404' in rv.data
        # rv = self.app.get(url_for('subunit', id_='Hello'))
        # assert b'404' in rv.data
        # rv = self.app.get(url_for('subunit_hierarchy', id_='Hello'))
        # assert b'404' in rv.data
        # rv = self.app.get(url_for('node_entities', id_=9999999))
        # assert b'404' in rv.data
        # rv = self.app.get(url_for('node_entities_all', id_=9999999))
        # assert b'404' in rv.data
        # rv = self.app.get(url_for('subunit', id_=99999999))
        # assert b'404' in rv.data
        # rv = self.app.get(url_for('subunit_hierarchy', id_=9999999))
        # assert b'404' in rv.data
        # # rv = self.app.get(url_for('subunit_hierarchy', id_=place.id))
        # # assert b'404' in rv.data
        # # rv = self.app.get(url_for('api_subunit', id_=plac.id))
        # # assert b'404a' in rv.data
        # # rv = self.app.post(url_for('api_get_entities_by_json'))
        # # assert b'405' in rv.data
        # # self.app.get(url_for('logout'), follow_redirects=True)
        # # rv = self.app.get(url_for('entity', id_=place.id))
        # # assert b'403' in rv.data
