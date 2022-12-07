from flask import url_for

from openatlas import app
from openatlas.api.resources.error import (
    EntityDoesNotExistError, FilterColumnError, FilterLogicalOperatorError,
    FilterOperatorError, InvalidCidocClassCode, InvalidCodeError,
    InvalidLimitError, InvalidSearchSyntax, InvalidSubunitError,
    InvalidSystemClassError, LastEntityError, NoEntityAvailable,
    NoSearchStringError, NotAPlaceError, QueryEmptyError, TypeIDError,
    ValueNotIntegerError)
from openatlas.api.resources.model_mapper import get_by_cidoc_classes
from tests.base import (
    ApiTestCase, get_bool, get_bool_inverse, get_class_mapping,
    get_geom_properties, get_no_key)


class Api03(ApiTestCase):

    def test_api_03(self) -> None:

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
                    if entity.name == 'Change of Property':
                        change_of_property = entity

            # ---Content Endpoints---
            rv = self.app.get(url_for('api_03.class_mapping')).get_json()
            assert get_class_mapping(rv)

            rv = self.app.get(
                url_for('api_03.content', lang='de', download=True)).get_json()
            assert bool(rv['intro'] == 'Das ist Deutsch')
            rv = self.app.get(url_for('api_03.content')).get_json()
            assert bool(rv['intro'] == 'This is English')

            rv = self.app.get(url_for('api_03.system_class_count')).get_json()
            assert bool(rv['person'])

            for rv in [
                self.app.get(url_for('api_03.geometric_entities')),
                self.app.get(
                    url_for('api_03.geometric_entities', download=True))]:
                rv = rv.get_json()
                assert bool(rv['features'][0]['geometry']['coordinates'])
                assert get_geom_properties(rv, 'id')
                assert get_geom_properties(rv, 'objectDescription')
                assert get_geom_properties(rv, 'objectId')
                assert get_geom_properties(rv, 'objectName')
                assert get_geom_properties(rv, 'shapeType')

            for rv in [
                self.app.get(
                    url_for('api_03.export_database', format_='xml')),
                self.app.get(
                    url_for('api_03.export_database', format_='json')),
                self.app.get(
                    url_for('api_03.export_database', format_='csv'))]:
                assert b'Shire' in rv.data

            # ---Entity Endpoints---
            # Test Entity
            rv = self.app.get(
                url_for('api_03.entity', id_=place.id, download=True))
            rv = rv.get_json()['features'][0]
            assert get_bool(rv, '@id')
            assert get_bool(rv, 'type', 'Feature')
            assert get_bool(rv, 'crmClass', 'crm:E18 Physical Thing')
            assert get_bool(rv, 'systemClass', 'place')
            assert get_bool(rv['properties'], 'title')
            desc = rv['descriptions'][0]
            assert get_bool(
                desc, 'value', 'The Shire was the homeland of the hobbits.')
            timespan = rv['when']['timespans'][0]
            assert get_bool(
                timespan['start'], 'earliest', '2018-01-31T00:00:00')
            assert get_bool(
                timespan['start'], 'latest', '2018-03-01T00:00:00')
            assert get_bool(timespan['end'], 'earliest', '2019-01-31T00:00:00')
            assert get_bool(timespan['end'], 'latest', '2019-03-01T00:00:00')
            assert get_bool(rv['types'][0], 'identifier')
            assert get_bool(rv['types'][0], 'label', 'Boundary Mark')
            rel = rv['relations']
            assert get_bool(rel[1], 'label', 'Height')
            assert get_bool(rel[1], 'relationDescription', '23.0')
            assert get_bool(rel[0], 'relationTo')
            assert get_bool(rel[0], 'relationType', 'crm:P2 has type')
            assert get_bool(rel[0], 'relationSystemClass', 'type')
            assert get_bool(rv['names'][0], 'alias', 'Sûza')
            links = rv['links'][0]
            assert get_bool(links, 'type', 'closeMatch')
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
            for rv in [
                self.app.get(url_for(
                    'api_03.entity', id_=place.id, format='geojson')),
                self.app.get(url_for(
                    'api_03.entity', id_=place.id, format='geojson-v2'))]:
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
                    url_for('api_03.entity', id_=place.id, format='xml')),
                self.app.get(
                    url_for('api_03.entity', id_=place.id, export='csv')),
                self.app.get(url_for(
                    'api_03.entity', id_=place.id, export='csvNetwork')),
                self.app.get(url_for(
                    'api_03.view_class', view_class='place', format='xml')),
                self.app.get(url_for(
                    'api_03.query',
                    entities=location.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    export='csv')),
                self.app.get(url_for(
                    'api_03.query',
                    entities=location.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    export='csvNetwork'))]:
                assert b'Shire' in rv.data

            # Test Entities endpoints
            for rv in [
                self.app.get(url_for('api_03.cidoc_class', cidoc_class='E21')),
                self.app.get(url_for(
                    'api_03.view_class',
                    view_class='place',
                    sort='desc',
                    column='id',
                    relation_type='P2',
                    type_id=boundary_mark.id)),
                self.app.get(url_for(
                    'api_03.view_class',
                    view_class='place',
                    sort='desc',
                    column='begin_from',
                    relation_type='P2',
                    type_id=boundary_mark.id)),
                self.app.get(url_for('api_03.latest', limit=2)),
                self.app.get(
                    url_for('api_03.system_class', system_class='artifact')),
                self.app.get(
                    url_for('api_03.entities_linked_to_entity', id_=event.id)),
                self.app.get(
                    url_for('api_03.type_entities', id_=boundary_mark.id)),
                self.app.get(
                    url_for('api_03.type_entities', id_=relation_sub.id)),
                self.app.get(
                    url_for('api_03.type_entities_all', id_=unit_node.id)),
                self.app.get(
                    url_for('api_03.type_entities_all', id_=relation_sub.id)),
                self.app.get(url_for(
                    'api_03.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    sort='desc',
                    column='cidoc_class',
                    system_classes='person',
                    download=True,
                    last=actor.id)),
                self.app.get(url_for(
                    'api_03.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    sort='desc',
                    column='system_class',
                    download=True,
                    actor=place.id))]:
                rv = rv.get_json()
                rv_results = rv['results'][0]['features'][0]
                rv_page = rv['pagination']
                assert get_bool(rv_results, '@id')
                assert get_bool(rv_page, 'entities')
                assert get_bool(rv_page, 'entitiesPerPage')
                assert get_bool(rv_page, 'index')
                assert get_bool(rv_page, 'totalPages')

            # Test Entities with show=none
            rv = self.app.get(url_for(
                'api_03.cidoc_class', cidoc_class='E21', show='none'))
            rv = rv.get_json()['results'][0]['features'][0]
            assert get_bool_inverse(rv, 'geometry')
            assert get_no_key(rv, 'depictions')
            assert get_no_key(rv, 'links')
            assert get_no_key(rv, 'types')

            # Test if Query returns enough entities
            rv = self.app.get(url_for(
                'api_03.query',
                entities=location.id,
                cidoc_classes='E18',
                view_classes='artifact',
                system_classes='person',
                limit=0,
                first=actor2.id)).get_json()
            assert bool(rv['pagination']['entities'] == 8)

            # Test page parameter
            rv = self.app.get(url_for(
                'api_03.query',
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
                'api_03.query',
                entities=location.id,
                cidoc_classes='E18',
                view_classes='artifact',
                system_classes='person',
                count=True))
            assert bool(rv.get_json() == 8)

            rv = self.app.get(url_for('api_03.geometric_entities', count=True))
            assert bool(rv.get_json() == 3)

            # Test entities with GeoJSON Format
            for rv in [
                self.app.get(url_for(
                    'api_03.query',
                    entities=location.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='geojson')),
                self.app.get(url_for(
                    'api_03.query',
                    entities=location.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='geojson-v2'))]:
                rv = rv.get_json()['results'][0]['features'][0]
                assert get_bool(rv['properties'], '@id')
                assert get_bool(rv['properties'], 'systemClass')

            # ---Type Endpoints---
            for rv in [
                self.app.get(url_for('api_03.type_overview')),
                self.app.get(
                    url_for('api_03.type_overview', download=True))]:
                rv = rv.get_json()['place'][0]['children'][0]
            assert bool(rv['label'] == 'Austria')

            for rv in [
                self.app.get(url_for('api_03.type_by_view_class')),
                self.app.get(
                    url_for('api_03.type_by_view_class', download=True))]:
                rv = rv.get_json()['place'][0]['children'][0]
            assert bool(rv['label'] == 'Boundary Mark')

            for rv in [
                self.app.get(url_for('api_03.type_tree')),
                self.app.get(
                    url_for('api_03.type_tree', download=True))]:
                assert bool(rv.get_json()['typeTree'])

            for rv in [
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"entityCidocClass":[{"operator":"equal",
                        "values":["E21"],"logicalOperator":"and"}]}""")),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"entitySystemClass":[{"operator":"equal",
                        "values":["person"],"logicalOperator":"and"}]}""")),
                self.app.get(url_for(
                    'api_03.query',
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
                    'api_03.query',
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
                    'api_03.query',
                    entities=place.id,
                    classes='E18',
                    codes='place',
                    system_classes='person',
                    format='lp',
                    search=f'{{"valueTypeID":[{{"operator":"equal",'
                           f'"values":[({height.id},23.0)],'
                           f'"logicalOperator":"or"}}]}}')),
                self.app.get(url_for(
                    'api_03.query',
                    system_classes='place',
                    search="""{"entityName":[{"operator":"notEqual",
                        "values":["Mordor"],"logicalOperator":"or"}]}""")),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"typeName":[{"operator":"equal",
                        "values":["Boundary Mark", "Height"],
                        "logicalOperator":"and"}]}""")),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search=f'{{"relationToID":[{{"operator":"equal",'
                           f'"values":[{place.id}],'
                           f'"logicalOperator":"or"}}]}}')),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"beginFrom":[{"operator":"lesserThan",
                        "values":["2020-1-1"],"logicalOperator":"and"}]}""")),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"beginTo":[{"operator":"lesserThanEqual",
                        "values":["2018-3-01"],"logicalOperator":"and"}]}""")),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"beginTo":[{"operator":"lesserThanEqual",
                        "values":["2018-3-01"],"logicalOperator":"or"}]}""")),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"endFrom":[{"operator":"greaterThan",
                        "values":["2013-2-1"],"logicalOperator":"and"}]}""")),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"endFrom":[{"operator":"greaterThan",
                        "values":["2013-2-1"],"logicalOperator":"or"}]}""")),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search='{"endTo":[{"operator":"greaterThanEqual", '
                           '"values":["2019-03-01"],"logicalOperator":"and"}]}'
                )),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"endTo":[{"operator":"greaterThanEqual",
                    "values":["2019-03-01"],"logicalOperator":"or"}]}""")),
                self.app.get(url_for(
                    'api_03.query',
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
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search='{"entityName":[{"operator":"like",'
                           '"values":["Fr"],'
                           '"logicalOperator":"or"}]}')),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search='{"entityAliases":[{"operator":"like",'
                           '"values":["S"],'
                           '"logicalOperator":"or"}]}')),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search='{"typeName": [{"operator": "like",'
                           '"values": ["Oun", "HeI"],'
                           '"logicalOperator": "and"}]}')),
                self.app.get(url_for(
                    'api_03.query',
                    system_classes='place',
                    search="""{"entityName":[{"operator":"notEqual",
                                "values":["Mordor"],
                                "logicalOperator":"or"}]}"""))]:
                assert bool(rv.get_json()['pagination']['entities'] == 1)

            for rv in [
                self.app.get(url_for(
                    'api_03.query',
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
                    'api_03.query',
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
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"typeName":[{"operator":"notEqual",
                        "values":["Boundary Mark", "Height"],
                        "logicalOperator":"and"}]}""")),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search=f'{{"entityID":[{{"operator":"notEqual",'
                           f'"values":[{place.id}],'
                           f'"logicalOperator":"and"}}]}}')),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search="""{"entityAliases":[{"operator":"notEqual",
                        "values":["Sûza"],"logicalOperator":"and"}]}"""))]:
                assert bool(rv.get_json()['pagination']['entities'] == 6)

            for rv in [
                self.app.get(url_for('api_03.subunits', id_=place.id)),
                self.app.get(
                    url_for('api_03.subunits', id_=place.id, download=True))]:
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
                url_for('api_03.subunits', id_=place.id, count=True))
            assert b'3' in rv.data

            for rv in [
                self.app.get(
                    url_for('api_03.subunits', id_=place.id, format='xml')),
                self.app.get(url_for(
                    'api_03.subunits',
                    id_=place.id,
                    format='xml',
                    download=True))]:
                assert b'Shire' in rv.data

            # --Test Error Handling--
            with self.assertRaises(EntityDoesNotExistError):
                self.app.get(url_for('api_03.entity', id_=233423424))
            with self.assertRaises(NotAPlaceError):
                self.app.get(url_for('api_03.subunits', id_=actor.id))
            with self.assertRaises(EntityDoesNotExistError):
                self.app.get(url_for(
                    'api_03.cidoc_class', cidoc_class='E18', last=1231))
            with self.assertRaises(LastEntityError):
                self.app.get(url_for(
                    'api_03.query',
                    entities=location.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    sort='desc',
                    column='id',
                    download=True,
                    last=place.id))
            with self.assertRaises(TypeIDError):
                self.app.get(url_for(
                    'api_03.query',
                    system_classes='person',
                    type_id=boundary_mark.id))
            with self.assertRaises(NoEntityAvailable):
                self.app.get(url_for('api_03.query', entities=12345))
            with self.assertRaises(NoEntityAvailable):
                self.app.get(url_for(
                    'api_03.cidoc_class', cidoc_class='E68', last=1231))
            with self.assertRaises(InvalidSystemClassError):
                self.app.get(
                    url_for('api_03.system_class', system_class='Wrong'))
            with self.assertRaises(QueryEmptyError):
                self.app.get(url_for('api_03.query'))
            with self.assertRaises(InvalidSubunitError):
                self.app.get(url_for('api_03.type_entities', id_=1234))
            with self.assertRaises(InvalidSubunitError):
                self.app.get(url_for('api_03.type_entities_all', id_=1234))
            with self.assertRaises(InvalidCidocClassCode):
                self.app.get(
                    url_for('api_03.cidoc_class', cidoc_class='e99999999'))
            with self.assertRaises(InvalidCodeError):
                self.app.get(
                    url_for('api_03.view_class', view_class='Invalid'))
            with self.assertRaises(InvalidLimitError):
                self.app.get(url_for('api_03.latest', limit='99999999'))
            with self.assertRaises(ValueNotIntegerError):
                self.app.get(url_for(
                    'api_03.view_class',
                    view_class='place',
                    search='{"typeID":[{"operator":"equal",'
                           '"values":["Boundary Mark", "Height", "Dimension"],'
                           '"logicalOperator":"and"}]}'))
            with self.assertRaises(NoEntityAvailable):
                self.app.get(url_for(
                    'api_03.view_class',
                    view_class='place',
                    search='{"typeName":[{"operator":"equal",'
                           '"values":["Boundary Mark", "Height", "Dimension"],'
                           '"logicalOperator":"and"}]}'))
            with self.assertRaises(FilterOperatorError):
                self.app.get(url_for(
                    'api_03.view_class',
                    view_class='place',
                    search='{"typeName":[{"operator":"notEqualT",'
                           '"values":["Boundary Mark", "Height"],'
                           '"logicalOperator":"and"}]}'))
            with self.assertRaises(FilterLogicalOperatorError):
                self.app.get(url_for(
                    'api_03.view_class',
                    view_class='place',
                    search='{"typeName":[{"operator":"notEqual",'
                           '"values":["Boundary Mark", "Height"],'
                           '"logicalOperator":"xor"}]}'))
            with self.assertRaises(FilterColumnError):
                self.app.get(url_for(
                    'api_03.view_class',
                    view_class='place',
                    search='{"All":[{"operator":"notEqual",'
                           '"values":["Boundary Mark", "Height"],'
                           '"logicalOperator":"or"}]}'))
            with self.assertRaises(NoSearchStringError):
                self.app.get(url_for(
                    'api_03.view_class',
                    view_class='place',
                    search='{"typeName":[{"operator":"notEqual",'
                           '"values":[],'
                           '"logicalOperator":"or"}]}'))
            with self.assertRaises(NoEntityAvailable):
                self.app.get(url_for(
                    'api_03.view_class',
                    view_class='place',
                    search='{"beginFrom":[{"operator":"lesserThan",'
                           '"values":["2000-1-1"],'
                           '"logicalOperator":"or"}]}'))
            with self.assertRaises(NoEntityAvailable):
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search='{"entityDescription":[{"operator":"like",'
                           '"values":["IS", "sam", "FrOdo"],'
                           '"logicalOperator":"and"}]}'))
            with self.assertRaises(InvalidSearchSyntax):
                self.app.get(url_for(
                    'api_03.view_class',
                    view_class='place',
                    search='"beginFrom":[{"operator":"lesserThan",'
                           '"values":["2000-1-1"],'
                           '"logicalOperator":"or"}]}'))
