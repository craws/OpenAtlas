import json
from typing import Any, Optional

from flask import url_for

from openatlas import app
from openatlas.api.resources.api_entity import ApiEntity
from tests.base import ApiTestCase


class Api(ApiTestCase):

    @staticmethod
    def get_bool(
            data: dict[str, Any],
            key: str,
            value: Optional[str | list[Any]] = None) -> bool:
        return bool(data[key] == value) if value else bool(data[key])

    @staticmethod
    def get_bool_inverse(data: dict[str, Any], key: str) -> bool:
        return bool(not data[key])

    @staticmethod
    def get_no_key(data: dict[str, Any], key: str) -> bool:
        return bool(key not in data.keys())

    @staticmethod
    def get_geom_properties(geom: dict[str, Any], key: str) -> bool:
        return bool(geom['features'][0]['properties'][key])

    @staticmethod
    def get_classes(data: list[dict[str, Any]]) -> bool:
        return bool(
            data[0]['systemClass']
            and data[0]['crmClass']
            and data[0]['view']
            and data[0]['icon']
            and data[0]['en'])

    @staticmethod
    def get_class_mapping(data: dict[str, Any], locale: str) -> bool:
        return bool(
            data['locale'] == locale
            and data['results'][0]['systemClass']
            and data['results'][0]['crmClass']
            and data['results'][0]['view']
            and data['results'][0]['icon']
            and data['results'][0]['label'])

    def test_api(self) -> None:

        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()
                for entity in  ApiEntity.get_by_cidoc_classes(['all']):
                    match entity.name:
                        case 'Location of Shire':
                            location = entity
                        case 'Shire':
                            place = entity
                        case 'Boundary Mark':
                            boundary_mark = entity
                        case 'Travel to Mordor':
                            event = entity
                        case 'Economical':
                            relation_sub = entity
                        case 'Austria':
                            unit_node = entity
                        case 'Frodo':
                            actor = entity
                        case 'Sam':
                            actor2 = entity
                        case 'Home of Baggins':
                            feature = entity
                        case 'Location of Home of Baggins':
                            feature_location = entity
                        case 'Sûza':
                            alias = entity
                        case 'Height':
                            height = entity
                        case 'Change of Property':
                            change_of_property = entity
                        case 'File without license':
                            file_without_licences = entity
                        case 'File without file':
                            file_without_file = entity

            # Test Swagger UI
            if app.config['OPENAPI_INSTANCE_FILE'].exists():
                app.config['OPENAPI_INSTANCE_FILE'].unlink()
            rv: Any = self.app.get(url_for('flasgger.apidocs'))
            assert b'Flasgger' in rv.data
            with app.config['OPENAPI_INSTANCE_FILE'].open(mode='r+') as f:
                data = json.load(f)
                data['servers'][0]['description'] = 'Wrong description'
                f.seek(0)
                json.dump(data, f)
                f.truncate()
            rv = self.app.get(url_for('flasgger.apidocs'))
            assert b'Flasgger' in rv.data
            with app.config['OPENAPI_INSTANCE_FILE'].open(mode='r+') as f:
                data = json.load(f)
                data['info']['version'] = '9.9.9'
                f.seek(0)
                json.dump(data, f)
                f.truncate()
            rv = self.app.get(url_for('flasgger.apidocs'))
            assert b'Flasgger' in rv.data

            # ---Content Endpoints---
            rv = self.app.get(url_for('api_04.classes')).get_json()
            assert self.get_classes(rv)

            rv = self.app.get(
                url_for('api_04.class_mapping', locale='de')).get_json()
            assert self.get_class_mapping(rv, 'de')

            rv = self.app.get(url_for(
                'api_04.class_mapping', locale='ca', download=True)).get_json()
            assert self.get_class_mapping(rv, 'ca')

            rv = self.app.get(url_for('api_04.backend_details')).get_json()
            assert bool(rv['version'] == app.config['VERSION'])
            rv = self.app.get(
                url_for('api_04.backend_details', download=True)).get_json()
            assert bool(rv['version'] == app.config['VERSION'])

            rv = self.app.get(url_for('api_04.system_class_count')).get_json()
            assert bool(rv['person'])

            rv = self.app.get(url_for('api.licensed_file_overview'))
            assert bool(len(rv.get_json().keys()) == 3)

            for rv in [
                self.app.get(url_for('api_04.geometric_entities')),
                self.app.get(
                    url_for('api_04.geometric_entities', download=True))]:
                rv = rv.get_json()
                assert bool(rv['features'][0]['geometry']['coordinates'])
                assert self.get_geom_properties(rv, 'id')
                assert self.get_geom_properties(rv, 'objectDescription')
                assert self.get_geom_properties(rv, 'objectId')
                assert self.get_geom_properties(rv, 'objectName')
                assert self.get_geom_properties(rv, 'shapeType')

            rv = self.app.get(
                url_for('api_04.export_database', format_='xml'))
            assert b'Shire' in rv.data
            assert 'application/xml' in rv.headers.get('Content-Type')

            rv = self.app.get(
                url_for('api_04.export_database', format_='json'))
            assert b'Shire' in rv.data
            assert 'application/json' in rv.headers.get('Content-Type')

            rv = self.app.get(url_for('api_04.export_database', format_='csv'))
            assert b'Shire' in rv.data
            assert 'application/zip' in rv.headers.get('Content-Type')

            # ---Entity Endpoints---
            # Test Entity
            rv = self.app.get(
                url_for('api_04.entity', id_=place.id, download=True))
            assert 'application/json' in rv.headers.get('Content-Type')
            rv = rv.get_json()['features'][0]
            assert self.get_bool(rv, '@id')
            assert self.get_bool(rv, 'type', 'Feature')
            assert self.get_bool(rv, 'crmClass', 'crm:E18 Physical Thing')
            assert self.get_bool(rv, 'systemClass', 'place')
            assert self.get_bool(rv['properties'], 'title')
            desc = rv['descriptions'][0]
            assert self.get_bool(
                desc, 'value', 'The Shire was the homeland of the hobbits.')
            timespan = rv['when']['timespans'][0]
            assert self.get_bool(
                timespan['start'], 'earliest', '2018-01-31T00:00:00')
            assert self.get_bool(
                timespan['start'], 'latest', '2018-03-01T00:00:00')
            assert self.get_bool(
                timespan['end'], 'earliest', '2019-01-31T00:00:00')
            assert self.get_bool(
                timespan['end'], 'latest', '2019-03-01T00:00:00')
            assert self.get_bool(rv['types'][0], 'identifier')
            assert self.get_bool(rv['types'][0], 'label', 'Boundary Mark')
            rel = rv['relations']
            assert self.get_bool(rel[1], 'label', 'Height')
            assert self.get_bool(rel[1], 'relationDescription', '23.0')
            assert self.get_bool(rel[0], 'relationTo')
            assert self.get_bool(rel[0], 'relationType', 'crm:P2 has type')
            assert self.get_bool(rel[0], 'relationSystemClass', 'type')
            assert self.get_bool(rv['names'][0], 'alias', 'Sûza')
            links = rv['links'][0]
            assert self.get_bool(links, 'type', 'closeMatch')
            assert self.get_bool(
                links, 'identifier', 'https://www.geonames.org/2761369')
            assert self.get_bool(links, 'referenceSystem', 'GeoNames')
            assert self.get_bool(rv['geometry'], 'type', 'GeometryCollection')
            assert self.get_bool(
                rv['geometry']['geometries'][1],
                'coordinates',
                [16.37069611, 48.208571233])
            assert self.get_bool(rv['depictions'][0], '@id')
            assert self.get_bool(
                rv['depictions'][0], 'title', 'Picture with a License')
            assert self.get_bool(
                rv['depictions'][0], 'license', 'Open license')
            assert self.get_bool(rv['depictions'][0], 'url')

            rv = self.app.get(url_for(
                'api_04.entity', id_=place.id, format='lpx', locale='de'))
            assert 'application/json' in rv.headers.get('Content-Type')
            rv = rv.get_json()['features'][0]
            rel = rv['relations']
            assert self.get_bool(rel[1], 'label', 'Height')
            assert self.get_bool(rel[1], 'relationDescription', '23.0')
            assert self.get_bool(rel[0], 'relationTo')
            assert self.get_bool(rel[0], 'relationType', 'crm:P2_has_type')
            assert self.get_bool(rel[0], 'relationTypeLabel', 'hat den Typus')

            geojson_checklist = [
                '@id', 'systemClass', 'name', 'description', 'begin_earliest',
                'begin_latest', 'begin_comment', 'end_earliest', 'end_latest',
                'end_comment', 'types']
            # Test entity in GeoJSON format
            rv = self.app.get(url_for(
                'api_04.entity', id_=place.id, format='geojson'))
            assert 'application/json' in rv.headers.get('Content-Type')
            rv = rv.get_json()['features'][0]
            assert self.get_bool(rv['geometry'], 'type')
            assert self.get_bool(rv['geometry'], 'coordinates')
            for key in geojson_checklist:
                assert self.get_bool(rv['properties'], key)

            rv = self.app.get(url_for(
                'api_04.entity', id_=place.id, format='geojson-v2'))
            assert 'application/json' in rv.headers.get('Content-Type')
            rv = rv.get_json()['features'][0]
            assert self.get_bool(rv['geometry'], 'type')
            assert self.get_bool(
                rv['geometry']['geometries'][0], 'coordinates')
            for key in geojson_checklist:
                assert self.get_bool(rv['properties'], key)

            # Test entity in Linked Open Usable Data
            rv = self.app.get(
                url_for('api_04.entity', id_=place.id, format='loud'))
            assert 'application/json' in rv.headers.get('Content-Type')
            rv = rv.get_json()
            assert bool(rv['type'] == 'PhysicalThing')
            assert bool(rv['_label'] == 'Shire')
            assert bool(rv['content']
                        == 'The Shire was the homeland of the hobbits.')
            assert bool(rv['timespan']['begin_of_the_begin']
                        == '2018-01-31T00:00:00')
            assert bool(rv['identified_by'][0]['_label'] == 'Sûza')
            assert bool(rv['classified_as'][0]['_label'] == 'Boundary Mark')
            assert bool(rv['former_or_current_location'][0]['_label']
                        == 'Location of Shire')
            assert bool(rv['former_or_current_location'][0]['defined_by']
                        == 'POLYGON((28.9389559878606 41.0290525580955,'
                           '28.9409293485759 41.0273124142771,28.941969652866 '
                           '41.0284940983463,28.9399641177912 41.0297647897435'
                           ',28.9389559878606 41.0290525580955))')

            # Problems because of
            # issue 130 https://github.com/RDFLib/rdflib/issues/130
            # or GitHub Actions connection issues
            # for rv in [
            #     self.app.get(
            #         url_for('api_04.entity', id_=place.id, format='n3')),
            #     self.app.get(url_for(
            #         'api_04.view_class',
            #         view_class='place',
            #         format='n3'))]:
            #     assert b'Shire' in rv.data

            # Test Entity export and RDFS
            for rv in [
                self.app.get(
                    url_for('api_04.entity', id_=place.id, export='csv')),
                self.app.get(url_for(
                    'api_04.query',
                    entities=location.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    export='csv'))]:
                assert b'Shire' in rv.data
                assert 'text/csv' in rv.headers.get('Content-Type')

            for rv in [
                self.app.get(url_for(
                    'api_04.entity', id_=place.id, export='csvNetwork')),
                self.app.get(url_for(
                    'api_04.query',
                    entities=location.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    export='csvNetwork'))]:
                assert b'Shire' in rv.data
                assert 'application/zip' in rv.headers.get('Content-Type')

            # Test Entities endpoints
            for rv in [
                self.app.get(url_for('api_04.cidoc_class', cidoc_class='E21')),
                self.app.get(url_for(
                    'api_04.view_class',
                    view_class='place',
                    sort='desc',
                    column='id',
                    relation_type='P2',
                    type_id=boundary_mark.id)),
                self.app.get(url_for(
                    'api_04.view_class',
                    view_class='place',
                    sort='desc',
                    column='begin_from',
                    relation_type='P2',
                    type_id=boundary_mark.id)),
                self.app.get(url_for('api_04.latest', limit=2)),
                self.app.get(
                    url_for('api_04.system_class', system_class='artifact')),
                self.app.get(
                    url_for('api_04.entities_linked_to_entity', id_=event.id)),
                self.app.get(
                    url_for('api_04.type_entities', id_=boundary_mark.id)),
                self.app.get(
                    url_for('api_04.type_entities', id_=relation_sub.id)),
                self.app.get(
                    url_for('api_04.type_entities_all', id_=unit_node.id)),
                self.app.get(
                    url_for('api_04.type_entities_all', id_=relation_sub.id)),
                self.app.get(url_for(
                    'api_04.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    sort='desc',
                    column='cidoc_class',
                    system_classes='person',
                    download=True,
                    last=actor.id)),
                self.app.get(url_for(
                    'api_04.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    linked_entities=place.id,
                    sort='desc',
                    column='system_class',
                    download=True,
                    actor=place.id))]:
                assert 'application/json' in rv.headers.get('Content-Type')
                rv = rv.get_json()
                rv_results = rv['results'][0]['features'][0]
                rv_page = rv['pagination']
                assert self.get_bool(rv_results, '@id')
                assert self.get_bool(rv_page, 'entities')
                assert self.get_bool(rv_page, 'entitiesPerPage')
                assert self.get_bool(rv_page, 'index')
                assert self.get_bool(rv_page, 'totalPages')

            # Test Entities with show=none
            rv = self.app.get(url_for(
                'api_04.cidoc_class', cidoc_class='E21', show='none'))
            rv = rv.get_json()['results'][0]['features'][0]
            assert self.get_bool_inverse(rv, 'geometry')
            assert self.get_no_key(rv, 'depictions')
            assert self.get_no_key(rv, 'links')
            assert self.get_no_key(rv, 'types')

            # Test if Query returns enough entities
            rv = self.app.get(url_for(
                'api_04.query',
                entities=location.id,
                cidoc_classes='E18',
                view_classes='artifact',
                system_classes='person',
                limit=0,
                first=actor2.id)).get_json()
            assert bool(rv['pagination']['entities'] == 8)

            # Test page parameter
            rv = self.app.get(url_for(
                'api_04.query',
                entities=location.id,
                cidoc_classes='E18',
                view_classes='artifact',
                system_classes='person',
                limit=1,
                page=7)).get_json()
            properties = rv['results'][0]['features'][0]['properties']
            assert bool(properties['title'] == place.name)
            assert bool(len(rv['results']) == 1)

            # Test Entities count
            rv = self.app.get(url_for(
                'api_04.query',
                entities=location.id,
                cidoc_classes='E18',
                view_classes='artifact',
                system_classes='person',
                count=True))
            assert bool(rv.get_json() == 8)

            rv = self.app.get(url_for('api_04.geometric_entities', count=True))
            assert bool(rv.get_json() == 6)

            # Test entities with GeoJSON Format
            for rv in [
                self.app.get(url_for(
                    'api_04.query',
                    entities=location.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='geojson')),
                self.app.get(url_for(
                    'api_04.query',
                    entities=location.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='geojson-v2'))]:
                rv = rv.get_json()['results'][0]['features'][0]
                assert self.get_bool(rv['properties'], '@id')
                assert self.get_bool(rv['properties'], 'systemClass')

            # Test entities with Linked Open Usable Data Format
            rv = self.app.get(url_for(
                'api_04.query',
                entities=location.id,
                cidoc_classes=['E18', 'E53'],
                view_classes='artifact',
                system_classes=['person', 'type'],
                format='loud',
                limit=0))
            rv = rv.get_json()['results'][0]
            assert bool(rv['type'] == 'Type')
            assert bool(rv['_label'] == 'Abbot')

            # ---Type Endpoints---
            for rv in [
                self.app.get(url_for('api_04.type_overview')),
                self.app.get(
                    url_for('api_04.type_overview', download=True))]:
                found = False
                for item in rv.get_json()['place']:
                    if found:
                        break
                    if item['name'] == 'Administrative unit':
                        for children in item['children']:
                            if children['label'] == 'Austria':
                                found = True
                                break
                assert found

            for rv in [
                self.app.get(url_for('api_04.type_by_view_class')),
                self.app.get(
                    url_for('api_04.type_by_view_class', download=True))]:
                found = False
                for item in rv.get_json()['place']:
                    if item['name'] == 'Place':
                        for children in item['children']:
                            if children['label'] == 'Boundary Mark':
                                found = True
                                break
                assert found

            rv = self.app.get(url_for('api_04.type_tree'))
            assert bool(rv.get_json()['typeTree'])
            rv = self.app.get(url_for('api_04.type_tree', download=True))
            assert bool(rv.get_json()['typeTree'])
            rv = self.app.get(url_for('api_04.type_tree', count=True))
            assert rv.get_json() > 0

            for rv in [
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"entityCidocClass":[{"operator":"equal",
                        "values":["E21"],"logicalOperator":"and"}]}""")),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"entitySystemClass":[{"operator":"equal",
                        "values":["person"],"logicalOperator":"and"}]}""")),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='activity',
                    format='lp',
                    search=f'{{"typeIDWithSubs":[{{"operator":"equal",'
                           f'"values":[{boundary_mark.id},'
                           f'{height.id},'
                           f'{change_of_property.id}],'
                           f'"logicalOperator":"or"}}]}}')),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search='{"entityDescription":[{"operator":"like",'
                           '"values":["FrOdO", "sam"],'
                           '"logicalOperator":"or"}]}'))]:
                assert bool(rv.get_json()['pagination']['entities'] == 2)

            # Test search parameter
            for rv in [
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    classes='E18',
                    codes='place',
                    system_classes='person',
                    format='lp',
                    search=f'{{"valueTypeID":[{{"operator":"equal",'
                           f'"values":[({height.id},23.0)]}}]}}')),
                self.app.get(url_for(
                    'api_04.query',
                    system_classes='place',
                    search="""{"entityName":[{"operator":"notEqual",
                        "values":["Mordor"],"logicalOperator":"or"}]}""")),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"typeName":[{"operator":"equal",
                        "values":["Boundary Mark", "Height"],
                        "logicalOperator":"and"}]}""")),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search=f'{{"relationToID":[{{"operator":"equal",'
                           f'"values":[{place.id}],'
                           f'"logicalOperator":"or"}}]}}')),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"beginFrom":[{"operator":"lesserThan",
                        "values":["2020-1-1"],"logicalOperator":"and"}]}""")),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"beginFrom":[{"operator":"lesserThan",
                        "values":["2020-1-1"],"logicalOperator":"or"}]}""")),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"beginTo":[{"operator":"lesserThanEqual",
                        "values":["2018-3-01"],"logicalOperator":"and"}]}""")),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"beginTo":[{"operator":"lesserThanEqual",
                        "values":["2018-3-01"],"logicalOperator":"or"}]}""")),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"endFrom":[{"operator":"greaterThan",
                        "values":["2013-2-1"],"logicalOperator":"and"}]}""")),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"endFrom":[{"operator":"greaterThan",
                        "values":["2013-2-1"],"logicalOperator":"or"}]}""")),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search='{"endTo":[{"operator":"greaterThanEqual", '
                           '"values":["2019-03-01"],"logicalOperator":"and"}]}'
                )),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"endTo":[{"operator":"greaterThanEqual",
                    "values":["2019-03-01"],"logicalOperator":"or"}]}""")),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='all',
                    system_classes='all',
                    format='lp',
                    search='{"entityDescription":[{"operator":"equal",'
                           '"values":["the shirE Was the Homeland of the'
                           ' hobbits.", "homeland"],'
                           '"logicalOperator":"or"}]}')),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search='{"entityName":[{"operator":"like",'
                           '"values":["Fr"],'
                           '"logicalOperator":"or"}]}')),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search='{"entityAliases":[{"operator":"like",'
                           '"values":["S"],'
                           '"logicalOperator":"or"}]}')),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search='{"typeName": [{"operator": "like",'
                           '"values": ["Oun", "HeI"],'
                           '"logicalOperator": "and"}]}')),
                self.app.get(url_for(
                    'api_04.query',
                    system_classes='place',
                    view_classes='artifact',
                    format='lp',
                    search=f'{{"typeIDWithSubs":[{{"operator":"notEqual",'
                           f'"values":[{boundary_mark.id}],'
                           f'"logicalOperator":"and"}}]}}')),
                self.app.get(url_for(
                    'api_04.query',
                    system_classes='place',
                    search="""{"entityName":[{"operator":"notEqual",
                                "values":["Mordor"],
                                "logicalOperator":"or"}]}"""))]:
                assert bool(rv.get_json()['pagination']['entities'] == 1)

            for rv in [
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search=f'{{"typeID":[{{"operator":"equal",'
                           f'"values":[{boundary_mark.id},'
                           f'{height.id}],'
                           f'"logicalOperator":"or"}}]}}')),
                self.app.get(url_for(
                    'api_04.query',
                    system_classes='place',
                    view_classes='artifact',
                    format='lp',
                    search=f'{{"typeIDWithSubs":[{{"operator":"equal",'
                           f'"values":[{boundary_mark.id}],'
                           f'"logicalOperator":"and"}}]}}')),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search=f'{{"typeIDWithSubs":[{{"operator":"equal",'
                           f'"values":[{boundary_mark.id},'
                           f'{height.id}],'
                           f'"logicalOperator":"or"}}]}}'))]:
                assert bool(rv.get_json()['pagination']['entities'] == 2)

            for rv in [
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"typeName":[{"operator":"notEqual",
                        "values":["Boundary Mark", "Height"],
                        "logicalOperator":"and"}]}""")),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search=f'{{"entityID":[{{"operator":"notEqual",'
                           f'"values":[{place.id}],'
                           f'"logicalOperator":"and"}}]}}')),
                self.app.get(url_for(
                    'api_04.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"entityAliases":[{"operator":"notEqual",
                        "values":["Sûza"],"logicalOperator":"and"}]}"""))]:
                assert bool(rv.get_json()['pagination']['entities'] == 6)

            for rv in [
                self.app.get(url_for('api_04.subunits', id_=place.id)),
                self.app.get(
                    url_for('api_04.subunits', id_=place.id, download=True))]:
                assert 'application/json' in rv.headers.get('Content-Type')
                rv = rv.get_json()[str(place.id)]
                for item in rv:
                    if item['id'] == place.id:
                        assert bool(item['id'] == place.id)
                        assert bool(item['openatlasClassName'] == "place")
                        assert bool(item['children'] == [feature.id])
                        item = item['properties']
                        assert bool(item['name'] == place.name)
                        assert bool(item['description'] == place.description)
                        assert bool(item['aliases'] == [alias.name])
                        assert bool(item['externalReferences'])
                        assert bool(item['timespan'])
                        assert bool(item['standardType'])
                        assert bool(item['files'])
                        assert bool(item['types'])

            rv = self.app.get(
                url_for('api_04.subunits', id_=place.id, count=True))
            assert b'3' in rv.data

            for rv in [
                self.app.get(
                    url_for('api_04.subunits', id_=place.id, format='xml')),
                self.app.get(url_for(
                    'api_04.subunits',
                    id_=place.id,
                    format='xml',
                    download=True))]:
                assert b'Shire' in rv.data

            # Test centroid
            for rv in [
                self.app.get(url_for(
                    'api_04.entity', id_=feature.id, centroid=True)),
                self.app.get(url_for(
                    'api_04.entity',
                    id_=feature.id,
                    format='geojson',
                    centroid=True)),
                self.app.get(url_for(
                    'api_04.entity',
                    id_=feature_location.id,
                    format='geojson',
                    centroid=True)),
                self.app.get(url_for(
                    'api_04.entity',
                    id_=feature.id,
                    format='geojson-v2',
                    centroid=True)),
                self.app.get(url_for(
                    'api_04.entity',
                    id_=feature_location.id,
                    format='geojson-v2',
                    centroid=True)),
                self.app.get(url_for(
                    'api_04.subunits',
                    id_=place.id,
                    centroid=True)),
                self.app.get(url_for(
                    'api_04.view_class',
                    view_class='all',
                    centroid=True,
                    limit=0))]:
                assert b'(autogenerated)' in rv.data
                assert 'application/json' in rv.headers.get('Content-Type')

            # Test Error Handling
            for rv in [
                self.app.get(url_for('api_04.entity', id_=233423424)),
                self.app.get(url_for(
                    'api_04.cidoc_class', cidoc_class='E18', last=1231))]:
                rv = rv.get_json()
                assert 'Entity does not exist' in rv['title']

            rv = self.app.get(url_for('api_04.subunits', id_=actor.id))
            assert 'ID is not a valid place' in rv.get_json()['title']

            rv = self.app.get(
                url_for(
                    'api_04.query',
                    entities=location.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    sort='desc',
                    column='id',
                    download=True,
                    last=place.id))
            assert 'ID is last entity' in rv.get_json()['title']

            rv = self.app.get(
                url_for(
                    'api_04.query',
                    system_classes='person',
                    type_id=boundary_mark.id))
            assert 'One entity ID is not a type' in rv.get_json()['title']

            rv = self.app.get(
                url_for('api_04.system_class', system_class='Wrong'))
            assert 'Invalid system_classes value' in rv.get_json()['title']

            rv = self.app.get(url_for('api_04.query'))
            assert 'No query parameters given' in rv.get_json()['title']

            rv = self.app.get(
                url_for('api_04.cidoc_class', cidoc_class='e99999999'))
            assert 'Invalid cidoc_classes value' in rv.get_json()['title']

            rv = self.app.get(
                url_for('api_04.view_class', view_class='Invalid'))
            assert 'Invalid view_classes value' in rv.get_json()['title']

            rv = self.app.get(url_for('api_04.latest', limit='99999999'))
            assert 'Invalid limit value' in rv.get_json()['title']

            rv = self.app.get(url_for(
                'api_04.view_class',
                view_class='place',
                search='{"typeID":[{"operator":"equal",'
                       '"values":["Boundary Mark", "Height", "Dimension"],'
                       '"logicalOperator":"and"}]}'))
            assert 'Invalid search value' in rv.get_json()['title']

            rv = self.app.get(url_for(
                'api_04.view_class',
                view_class='place',
                search='{"All":[{"operator":"notEqual",'
                       '"values":["Boundary Mark", "Height"],'
                       '"logicalOperator":"or"}]}'))
            assert 'Invalid search category' in rv.get_json()['title']

            rv = self.app.get(url_for(
                'api_04.view_class',
                view_class='place',
                search='{"typeName":[{"operator":"notEqual",'
                       '"values":[],'
                       '"logicalOperator":"or"}]}'))
            assert 'No search values' in rv.get_json()['title']

            rv = self.app.get(url_for(
                'api_04.view_class',
                view_class='place',
                search='"beginFrom":[{"operator":"lesserThan",'
                       '"values":["2000-1-1"],'
                       '"logicalOperator":"or"}]}'))
            assert 'Invalid search syntax' in rv.get_json()['title']

            rv = self.app.get(url_for('api_04.type_entities', id_=1234))
            assert 'Entity is not a type' in rv.get_json()['title']

            rv = self.app.get(url_for('api_04.type_entities_all', id_=1234))
            assert 'Entity is not a type' in rv.get_json()['title']

            rv = self.app.get(url_for(
                'api_04.view_class',
                view_class='place',
                search='{"typeName":[{"operator":"notEqualT",'
                       '"values":["Boundary Mark", "Height"],'
                       '"logicalOperator":"and"}]}'))
            assert 'Invalid compare operator' in rv.get_json()['title']

            rv = self.app.get(url_for(
                'api_04.view_class',
                view_class='place',
                search='{"typeName":[{"operator":"notEqual",'
                       '"values":["Boundary Mark", "Height"],'
                       '"logicalOperator":"xor"}]}'))
            assert 'Invalid logical operator' in rv.get_json()['title']

            rv = self.app.get(url_for(
                'api_04.display',
                filename=f'{file_without_licences.id}'))
            assert 'No license' in rv.get_json()['title']

            rv = self.app.get(url_for(
                'api_04.display',
                filename=f'{file_without_file.id}'))
            assert 'File not found' in rv.get_json()['title']

            assert b'Endpoint not found' in self.app.get('/api/entity2').data

            self.app.get(url_for('logout'))
            app.config['ALLOWED_IPS'] = []

            rv = self.app.get(url_for('api_04.view_class', view_class='place'))
            assert 'Access denied' in rv.get_json()['title']
