
from flask import url_for

from openatlas import app
from openatlas.api.v03.resources.util import get_by_cidoc_classes
from tests.base import (
    ApiTestCase, get_bool, get_bool_inverse, get_class_mapping,
    get_geom_properties, get_no_key)


class Api02(ApiTestCase):

    def test_api_02(self) -> None:

        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                for entity in get_by_cidoc_classes(['all']):
                    if entity.name == 'Location of Shire':
                        location = entity
                    if entity.name == 'Shire':
                        place = entity
                    if entity.name == 'Boundary Mark':
                        boundary_mark = entity
                    if entity.name == 'Travel to Mordor':
                        event = entity
                    if entity.name == 'Travel to Mordor':
                        event = entity
                    if entity.name == 'Economical':
                        relation_sub = entity
                    if entity.name == 'Austria':
                        unit_node = entity
                    if entity.name == 'Frodo':
                        actor = entity
                    if entity.name == 'Sam':
                        actor2 = entity
                    if entity.name == 'Home of Baggins':
                        feature = entity
                    if entity.name == 'Sûza':
                        alias = entity
                    if entity.name == 'Height':
                        height = entity
                    if entity.name == 'Exchange':
                        exchange = entity

            # ---Content Endpoints---
            # ClassMapping
            rv = self.app.get(url_for('api_02.class_mapping')).get_json()
            assert get_class_mapping(rv)

            # Content
            rv = self.app.get(
                url_for('api_02.content', lang='de', download=True)).get_json()
            assert bool(rv['intro'] == 'Das ist Deutsch')
            rv = self.app.get(url_for('api_02.content')).get_json()
            assert bool(rv['intro'] == 'This is English')

            # geometric_entities/
            for rv in [
                self.app.get(url_for(
                    'api_02.geometric_entities')).get_json(),
                self.app.get(url_for(
                    'api_02.geometric_entities',
                    download=True)).get_json()]:
                assert bool(rv['features'][0]['geometry']['coordinates'])
                assert get_geom_properties(rv, 'id')
                assert get_geom_properties(rv, 'objectDescription')
                assert get_geom_properties(rv, 'objectId')
                assert get_geom_properties(rv, 'objectName')
                assert get_geom_properties(rv, 'shapeType')

            # system_class_count/
            rv = self.app.get(url_for('api_02.system_class_count')).get_json()
            assert bool(rv['person'])

            # overview_count/
            rv = self.app.get(url_for('api_02.overview_count')).get_json()
            assert bool(rv[0]['systemClass'])

            # ---Entity Endpoints---
            # /entity
            # Test Entity
            rv = self.app.get(
                url_for('api_02.entity', id_=place.id, download=True))
            rv = rv.get_json()['features'][0]
            assert get_bool(rv, '@id')
            assert get_bool(rv, 'type', 'Feature')
            assert get_bool(rv, 'crmClass', 'crm:E18 Physical Thing')
            assert get_bool(rv, 'systemClass', 'place')
            assert get_bool(rv['properties'], 'title')
            assert get_bool(
                rv['description'][0],
                'value',
                'The Shire was the homeland of the hobbits.')
            timespan = rv['when']['timespans'][0]
            assert get_bool(
                timespan['start'], 'earliest', '2018-01-31T00:00:00')
            assert get_bool(
                timespan['start'], 'latest', '2018-03-01T00:00:00')
            assert get_bool(
                timespan['end'], 'earliest', '2019-01-31T00:00:00')
            assert get_bool(
                timespan['end'], 'latest', '2019-03-01T00:00:00')
            assert get_bool(rv['types'][0], 'identifier')
            assert get_bool(rv['types'][0], 'label', 'Boundary Mark')
            rel = rv['relations']
            assert get_bool(rel[1], 'label', 'Height')
            assert get_bool(rel[0], 'relationTo')
            assert get_bool(rel[0], 'relationType', 'crm:P2 has type')
            assert get_bool(rel[0], 'relationSystemClass', 'type')
            assert get_bool(rel[1], 'relationDescription', '23.0')
            assert get_bool(rv['names'][0], 'alias', 'Sûza')
            assert get_bool(rv['links'][0], 'type', 'closeMatch')
            links = rv['links'][0]
            assert get_bool(
                links, 'identifier', 'https://www.geonames.org/2761369')
            assert get_bool(links, 'referenceSystem', 'GeoNames')
            assert get_bool(rv['geometry'], 'type', 'Point')
            assert get_bool(
                rv['geometry'], 'coordinates', [16.37069611, 48.208571233])
            assert get_bool(rv['depictions'][0], '@id')
            assert get_bool(
                rv['depictions'][0], 'title', 'Picture with a License')
            assert get_bool(rv['depictions'][0], 'license', 'Open license')
            assert get_bool(rv['depictions'][0], 'url')

            # Test entity in GeoJSON format
            rv = self.app.get(
                url_for('api_02.entity', id_=place.id, format='geojson'))
            rv = rv.get_json()['features'][0]
            assert get_bool(rv['geometry'], 'type')
            assert get_bool(rv['geometry'], 'coordinates')
            assert get_bool(rv['properties'], '@id')
            assert get_bool(rv['properties'], 'systemClass')
            assert get_bool(rv['properties'], 'name')
            assert get_bool(rv['properties'], 'description')
            assert get_bool(rv['properties'], 'begin_earliest')
            assert get_bool(rv['properties'], 'begin_latest')
            assert get_bool(rv['properties'], 'begin_comment')
            assert get_bool(rv['properties'], 'end_earliest')
            assert get_bool(rv['properties'], 'end_latest')
            assert get_bool(rv['properties'], 'end_comment')
            assert get_bool(rv['properties'], 'types')

            # Test Entity export and RDFS
            for rv in [
                self.app.get(
                    url_for('api_02.entity', id_=place.id, format='xml')),
                self.app.get(
                    url_for('api_02.entity', id_=place.id, export='csv')),
                self.app.get(
                    url_for('api_02.code', code='place', format='xml')),
                self.app.get(
                    url_for('api_02.code', code='place', export='csv')),
                self.app.get(url_for(
                    'api_02.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    export='csv')), ]:
                assert b'Shire' in rv.data

            # Test Entities endpoints
            for rv in [
                self.app.get(url_for('api_02.class', class_code='E21')),
                self.app.get(url_for(
                    'api_02.code', code='place', type_id=boundary_mark.id)),
                self.app.get(url_for('api_02.latest', latest=2)),
                self.app.get(
                    url_for('api_02.system_class', system_class='artifact')),
                self.app.get(
                    url_for('api_02.entities_linked_to_entity', id_=event.id)),
                self.app.get(
                    url_for('api_02.type_entities', id_=boundary_mark.id)),
                self.app.get(
                    url_for('api_02.type_entities', id_=relation_sub.id)),
                self.app.get(
                    url_for('api_02.type_entities_all', id_=unit_node.id)),
                self.app.get(
                    url_for('api_02.type_entities_all', id_=relation_sub.id)),
                self.app.get(url_for(
                    'api_02.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    last=actor.id)),
                self.app.get(url_for(
                    'api_02.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    filter='and|name|like|Shire',
                    sort='desc',
                    column='id',
                    download=True)),
                self.app.get(url_for(
                    'api_02.code',
                    code='place',
                    filter=f"and|id|eq|{place.id}")),
                self.app.get(url_for(
                    'api_02.code',
                    code='place',
                    filter=f"and|begin_from|eq|2018-01-31"))]:
                rv_results = rv.get_json()['results'][0]['features'][0]
                rv_page = rv.get_json()['pagination']
                assert get_bool(rv_results, '@id')
                assert get_bool(rv_page, 'entities')
                assert get_bool(rv_page, 'entitiesPerPage')
                assert get_bool(rv_page, 'index')
                assert get_bool(rv_page, 'totalPages')

            # Test Entities with show=none
            rv = self.app.get(
                url_for('api_02.class', class_code='E21', show='none'))
            rv = rv.get_json()['results'][0]['features'][0]
            assert get_bool_inverse(rv, 'geometry')
            assert get_no_key(rv, 'depictions')
            assert get_no_key(rv, 'links')
            assert get_no_key(rv, 'types')

            # Test Entities limit
            rv = self.app.get(url_for(
                'api_02.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                limit=1,
                first=actor2.id)).get_json()
            assert bool(len(rv['results']) == 1)

            # Test if Query returns enough entities
            rv = self.app.get(url_for(
                'api_02.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                limit=1,
                first=actor2.id)).get_json()
            assert bool(rv['pagination']['entities'] == 8)

            # Test page parameter
            rv = self.app.get(url_for(
                'api_02.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                limit=1,
                page=8)).get_json()
            properties = rv['results'][0]['features'][0]['properties']
            assert bool(properties['title'] == place.name)

            # Test Entities count
            rv = self.app.get(url_for(
                'api_02.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                count=True))
            assert bool(rv.get_json() == 8)

            # Test Entities count
            rv = self.app.get(url_for('api_02.geometric_entities', count=True))
            assert bool(rv.get_json() == 1)

            # Test entities with GeoJSON Format
            rv = self.app.get(url_for(
                'api_02.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                format='geojson')).get_json()
            rv = rv['results'][0]['features'][0]
            assert get_bool(rv['properties'], '@id')
            assert get_bool(rv['properties'], 'systemClass')

            # ---Type Endpoints---

            # Test Type Entities
            rv = self.app.get(url_for(
                'api_02.node_entities', id_=unit_node.id, download=True))
            assert get_bool(rv.get_json()['nodes'][0], 'label')

            # Test type entities all
            rv = self.app.get(url_for(
                'api_02.node_entities_all', id_=unit_node.id)).get_json()
            assert bool([True for i in rv['nodes'] if i['label'] == 'Wien'])

            # Test type entities count
            rv = self.app.get(url_for(
                'api_02.node_entities', id_=unit_node.id, count=True))
            assert bool(rv.get_json() == 3)

            # Test type overview
            rv = self.app.get(url_for('api_02.node_overview', download=True))
            rv = rv.get_json()['types'][0]['place']['Administrative unit']
            assert bool([True for i in rv if i['label'] == 'Austria'])

            rv = self.app.get(url_for('api_02.node_overview'))
            rv = rv.get_json()['types'][0]['place']['Administrative unit']
            assert bool([True for i in rv if i['label'] == 'Austria'])

            # Test type tree
            rv = self.app.get(url_for('api_02.type_tree'))
            assert bool(rv.get_json()['typeTree'][0])
            rv = self.app.get(url_for('api_02.type_tree', download=True))
            assert bool(rv.get_json()['typeTree'][0])

            # subunit/
            rv = self.app.get(
                url_for('api_02.subunit', id_=place.id)).get_json()
            assert bool(rv['nodes'][0]['label'] == 'Home of Baggins')

            # subunit_hierarchy/
            rv = self.app.get(url_for(
                'api_02.subunit_hierarchy', id_=place.id)).get_json()
            assert bool(rv['nodes'][1]['label'] == 'Bar')
