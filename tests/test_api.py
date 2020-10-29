import pathlib

from flask import url_for, g

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.node import Node
from tests.base import TestBaseCase


class ApiTests(TestBaseCase):

    def test_api(self) -> None:
        with app.app_context():  # type: ignore
            rv = self.app.post(url_for('place_insert'),
                               data={'name': 'Nostromos', 'begin_year_from': -1949,
                                     'begin_month_from': 2, 'begin_day_from': 8,
                                     'begin_year_to': -1948, 'end_year_from': 1996,
                                     'end_year_to': 1996, 'end_comment': 'end year',
                                     'begin_comment': 'begin year',
                                     'gis_points': """[{
                                             "type":"Feature",
                                             "geometry":{"type":"Point","coordinates":[9,17]},
                                             "properties":{"name":"Valhalla","description":"",
                                             "shapeType":"centerpoint"}}]""",
                                     })
            place_id = rv.location.split('/')[-1]
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                event = Entity.insert('E8', 'Event Horizon')
                event.link('P7', Entity.get_by_id(place_id))
                place_node = Node.get_hierarchy('Place')
                place = Entity.get_by_id(place_id)
                place.link("P2", place_node)
                reference = Entity.insert('E31', 'https://openatlas.eu', 'external reference')
                source = Entity.insert('E33', 'Necronomicon')
                unit_node = Node.get_hierarchy('Administrative Unit')
                unit_sub1 = g.nodes[unit_node.subs[0]]
                unit_sub2 = g.nodes[unit_node.subs[1]]
                # stratigraphic_node = Node.get_hierarchy('Stratigraphic Unit')
                # stratigraphic_sub = g.nodes[stratigraphic_node.subs[0]]

            # Data for geometric results
            data = {'name': 'Asgard', 'geonames_id': '123', 'geonames_precision': True,
                    'geonames_description': "Alexander",
                    unit_node.id: str([unit_sub1.id, unit_sub2.id]),
                    'gis_points': """[{
                            "type":"Feature",
                            "geometry":{"type":"Point","coordinates":[9,17]},
                            "properties":{"name":"Valhalla","description":"",
                            "shapeType":"centerpoint"}}]""",
                    'gis_lines': """[{
                            "type":"Feature",
                            "geometry":{
                                "type":"LineString",
                                "coordinates":[[9.75307425847859,17.8111792731339],
                                [9.75315472474904,17.8110005175436],
                                [9.75333711496205,17.8110873417098]]},
                            "properties":{"name":"","description":"nice Test","shapeType":"line"}}]""",
                    'gis_polygons': """[{
                            "type":"Feature",
                            "geometry":{
                                "type":"Polygon",
                                "coordinates":[[[9.75307425847859,17.8111792731339],
                                [9.75315472474904,17.8110005175436],
                                [9.75333711496205,17.8110873417098],
                                [9.75307425847859,17.8111792731339]]]},
                            "properties":{"name":"","description":"","shapeType":"shape"}}]""",
                    'alias-1': 'Val-hall'}
            rv = self.app.post(url_for('place_insert', origin_id=reference.id),
                               data=data,
                               follow_redirects=True)
            assert b'Asgard' in rv.data
            rv = self.app.post(url_for('place_insert', origin_id=source.id),
                               data=data,
                               follow_redirects=True)
            assert b'Asgard' in rv.data
            rv = self.app.post(url_for('place_insert', origin_id=source.id),
                               data=data,
                               follow_redirects=True)
            assert b'Necronomicon' in rv.data

            # Path Tests
            rv = self.app.get(url_for('api_index'))
            assert b'Test API' in rv.data
            rv = self.app.get(url_for('api_get_latest', limit=10))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('api_entity', id_=place_id))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('api_download_entity', id_=place_id))
            assert b'@context"' in rv.data
            rv = self.app.get(url_for('api_get_by_menu_item', code='reference'))
            assert b'openatlas' in rv.data
            rv = self.app.get(url_for('api_get_by_class', class_code='E33'))
            assert b'Necronomicon' in rv.data
            rv = self.app.get(url_for('api_get_by_class', class_code='E31'))
            assert b'https://openatlas.eu' in rv.data
            rv = self.app.get(url_for('api_node_entities', id_=unit_node.id))
            assert b'Austria' in rv.data
            rv = self.app.get(url_for('api_node_entities_all', id_=unit_node.id))
            assert b'Austria' in rv.data
            rv = self.app.get(
                url_for('api_get_query', entities=place_id, classes='E18', items='place'))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('api_content', lang='de'))
            assert b'intro' in rv.data

            # Path test with download
            rv = self.app.get(url_for('api_entity', id_=place_id, download=True))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('api_get_latest', limit=10, download=True))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('api_get_by_menu_item', code='reference', download=True))
            assert b'openatlas' in rv.data
            rv = self.app.get(url_for('api_get_by_class', class_code='E33', download=True))
            assert b'Necronomicon' in rv.data
            rv = self.app.get(url_for('api_node_entities', id_=unit_node.id, download=True))
            assert b'Austria' in rv.data
            rv = self.app.get(url_for('api_node_entities_all', id_=unit_node.id, download=True))
            assert b'Austria' in rv.data
            rv = self.app.get(url_for('api_get_query', entities=place_id, download=True))
            assert b'106' in rv.data
            rv = self.app.get(url_for('api_content', lang='de', download=True))
            assert b'intro' in rv.data

            # Testing Subunit
            rv = self.app.post(url_for('place_insert', origin_id=place_id), data={'name': "Item"})
            feature_id = rv.location.split('/')[-1]
            self.app.post(url_for('place_insert', origin_id=feature_id), data={'name': "Pot"})
            rv = self.app.get(url_for('api_subunit', id_=place_id))
            assert b'Item' in rv.data and b'Pot' not in rv.data
            rv = self.app.get(url_for('api_subunit', id_=place_id, download=True))
            assert b'Item' in rv.data and b'Pot' not in rv.data
            rv = self.app.get(url_for('api_subunit', id_=place_id, count=True))
            assert b'1' in rv.data
            rv = self.app.get(url_for('api_subunit_hierarchy', id_=place_id))
            assert b'Pot' in rv.data
            rv = self.app.get(url_for('api_subunit_hierarchy', id_=place_id, download=True))
            assert b'Pot' in rv.data
            rv = self.app.get(url_for('api_subunit_hierarchy', id_=place_id, count=True))
            assert b'2' in rv.data

            # Parameter: filter
            rv = self.app.get(url_for('api_get_by_menu_item',
                                      code='place',
                                      limit=10,
                                      sort='desc',
                                      column='name',
                                      filter='or|name|like|Nostromos'))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('api_get_by_menu_item', code='reference'))
            assert b'openatlas' in rv.data
            rv = self.app.get(url_for('api_get_by_class',
                                      class_code='E18',
                                      filter='or|name|like|Nostr'))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('api_get_by_class',
                                      class_code='E18',
                                      filter='or|created|gt|'))
            assert b'404i' in rv.data
            rv = self.app.get(url_for('api_get_by_class',
                                      class_code='E18',
                                      filter='or|created|Wrong|2000-01-01'))
            assert b'404j' in rv.data
            rv = self.app.get(url_for('api_get_by_class',
                                      class_code='E18',
                                      filter='or|created|gt|2000-01-623'))
            assert b'404k' in rv.data
            rv = self.app.get(url_for('api_get_by_class',
                                      class_code='E18',
                                      filter='or|id|gt|String'))
            assert b'404l' in rv.data


            # Parameter: last
            rv = self.app.get(url_for('api_get_by_class', class_code='E18', last=place_id))
            assert b'entities' in rv.data
            # Parameter: first
            rv = self.app.get(url_for('api_get_by_class', class_code='E18', first=place_id))
            assert b'entities' in rv.data

            # Parameter: show
            rv = self.app.get(url_for('api_get_by_class', class_code='E33', show='types'))
            assert b'Necronomicon' in rv.data
            rv = self.app.get(url_for('api_get_by_class', class_code='E33', show='when'))
            assert b'Necronomicon' in rv.data
            rv = self.app.get(url_for('api_get_by_class', class_code='E33', show='none'))
            assert b'Necronomicon' in rv.data

            # Parameter: count
            rv = self.app.get(url_for('api_get_by_class', class_code='E33', count=True))
            assert b'1' in rv.data
            rv = self.app.get(url_for('api_get_by_menu_item', code='reference', count=True))
            assert b'2' in rv.data  # Assert can vary, to get around use \n
            rv = self.app.get(
                url_for('api_get_query', ntities=place_id, classes='E18', items='place',
                        count=True))
            assert b'1' in rv.data
            rv = self.app.get(url_for('api_node_entities', id_=unit_node.id, count=True))
            assert b'6' in rv.data
            rv = self.app.get(url_for('api_node_entities_all', id_=unit_node.id, count=True))
            assert b'14' in rv.data

            # Error Codes
            rv = self.app.get(url_for('api_entity', id_=99999999))
            assert b'404a' in rv.data
            rv = self.app.get(url_for('api_get_by_class', class_code='E18', last=1231223121321))
            assert b'404a' in rv.data
            rv = self.app.get(url_for('api_entity', id_="Hello"))
            assert b'404b' in rv.data
            rv = self.app.get(url_for('api_get_latest', limit=99999))
            assert b'404e' in rv.data
            rv = self.app.get(url_for('api_get_latest', limit='wrong'))
            assert b'404e' in rv.data
            rv = self.app.get(url_for('api_get_by_class', class_code='E99999'))
            assert b'404' in rv.data
            rv = self.app.get(url_for('api_get_by_menu_item', code='Hello'))
            assert b'404c' in rv.data
            rv = self.app.get(url_for('api_get_query'))
            assert b'404h' in rv.data

            # rv = self.app.get(url_for('api_get_by_menu_item',
            #                           code='place',
            #                           limit=10,
            #                           sort='desc',
            #                           column='name',
            #                           filter='or|name|wrong|Nostromos'))
            # assert b'404f' in rv.data
            rv = self.app.get(url_for('api_node_entities', id_='Hello'))
            assert b'404b' in rv.data
            rv = self.app.get(url_for('api_node_entities_all', id_='Hello'))
            assert b'404b' in rv.data
            rv = self.app.get(url_for('api_subunit', id_='Hello'))
            assert b'404b' in rv.data
            rv = self.app.get(url_for('api_subunit_hierarchy', id_='Hello'))
            assert b'404b' in rv.data
            rv = self.app.get(url_for('api_node_entities', id_=9999999))
            assert b'404g' in rv.data
            rv = self.app.get(url_for('api_node_entities_all', id_=9999999))
            assert b'404g' in rv.data
            rv = self.app.get(url_for('api_subunit', id_=99999999))
            assert b'404a' in rv.data
            rv = self.app.get(url_for('api_subunit_hierarchy', id_=9999999))
            assert b'404a' in rv.data
            rv = self.app.get(url_for('api_subunit_hierarchy', id_=event.id))
            assert b'404g' in rv.data
            # rv = self.app.get(url_for('api_subunit', id_=source.id))
            # assert b'404a' in rv.data
            # rv = self.app.post(url_for('api_get_entities_by_json'))
            # assert b'405' in rv.data
            self.app.get(url_for('logout'), follow_redirects=True)
            # rv = self.app.get(url_for('api_entity', id_=place_id))
            # assert b'403' in rv.data
