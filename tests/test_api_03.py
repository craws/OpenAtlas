from datetime import datetime
from typing import Any, Optional, Union

from flask import g, url_for

from openatlas import app
from openatlas.api.v03.resources.error import (
    EntityDoesNotExistError, FilterColumnError, FilterLogicalOperatorError,
    FilterOperatorError, InvalidCidocClassCode, InvalidCodeError,
    InvalidLimitError, InvalidSearchSyntax, InvalidSubunitError,
    InvalidSystemClassError, LastEntityError, NoEntityAvailable,
    NoSearchStringError, NotAPlaceError, QueryEmptyError, TypeIDError,
    ValueNotIntegerError)
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type
from tests.base import TestBaseCase, insert_entity


class Api03(TestBaseCase):

    def test_api_03(self) -> None:

        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                params = {
                    f'{(node.name.lower()).replace(" ", "_")}_id': id_ for
                    (id_, node) in Type.get_all().items()}
                # Creation of Shire (place)
                place = insert_entity(
                    'Shire',
                    'place',
                    'The Shire was the homeland of the hobbits.')

                # Adding Created and Modified
                place.created = str(datetime.now())
                place.modified = str(datetime.now())

                # Adding Dates to place
                place.update({'attributes': {
                    'begin_from': '2018-01-31',
                    'begin_to': '2018-03-01',
                    'begin_comment': 'Begin of the shire',
                    'end_from': '2019-01-31',
                    'end_to': '2019-03-01',
                    'end_comment': 'Descent of Shire'}})
                location = place.get_linked_entity_safe('P53')
                Gis.insert(location, {
                    'point':
                        '[{"type":"Feature","geometry":'
                        '{"type":"Point","coordinates":[9, 17]},'
                        '"properties":{"name":"","description":"",'
                        '"shapeType":"centerpoint"}}]'})

                # Adding Type Place
                boundary_mark = Entity.get_by_id(
                    Type.get_hierarchy('Place').subs[0])
                place.link('P2', boundary_mark)

                # Adding Alias
                alias = insert_entity('Sûza', 'appellation')
                place.link('P1', alias)

                # Adding External Reference
                external_reference = insert_entity(
                    'https://lotr.fandom.com/',
                    'external_reference')
                external_reference.link(
                    'P67',
                    place,
                    description='Fandom Wiki of lord of the rings')

                # Adding feature to place
                feature = insert_entity(
                    'Home of Baggins',
                    'feature',
                    origin=place)
                feature.created = str(datetime.now())
                feature.modified = str(datetime.now())

                # Adding stratigraphic to place
                strati = insert_entity(
                    'Bar',
                    'stratigraphic_unit',
                    origin=feature)
                strati.created = str(datetime.now())
                strati.modified = str(datetime.now())

                # Adding Administrative Unit Type
                admin_unit = Type.get_hierarchy('Administrative unit')
                unit_node = g.types[admin_unit.subs[0]]
                location.link('P89', unit_node)

                # Adding File to place
                file = insert_entity('Picture with a License', 'file')
                file.link('P67', place)
                file.link('P2', g.types[Type.get_hierarchy('License').subs[0]])

                # Adding Value Type
                value_type = Type.get_hierarchy('Dimensions')
                place.link('P2', Entity.get_by_id(value_type.subs[0]), '23.0')

                # Adding Geonames
                geonames = Entity.get_by_id(
                    ReferenceSystem.get_by_name('GeoNames').id)
                precision_id = Type.get_hierarchy(
                    'External reference match').subs[0]
                geonames.link(
                    'P67',
                    place,
                    description='2761369',
                    type_id=precision_id)

                # Creation of actor (Frodo)
                actor = insert_entity(
                    'Frodo',
                    'person',
                    description='That is Frodo')

                alias2 = insert_entity('The ring bearer', 'appellation')
                actor.link('P1', alias2)

                # Adding file to actor
                file2 = insert_entity('File without license', 'file')
                file2.link('P67', actor)

                # Adding artefact to actor
                artifact = insert_entity('The One Ring', 'artifact')
                artifact.link('P52', actor)

                # Creation of second actor (Sam)
                actor2 = insert_entity(
                    'Sam',
                    'person',
                    description='That is Sam')

                # Adding residence
                actor2.link('P74', location)

                # Adding actor relation
                relation_id = Type.get_hierarchy('Actor actor relation').id
                relation_sub_id = g.types[relation_id].subs[0]
                actor.link('OA7', actor2, type_id=relation_sub_id)

                # Creation of event
                event = insert_entity('Travel to Mordor', 'activity')
                event.link('P11', actor)
                event.link('P14', actor2)
                event.link('P7', location)
                event2 = insert_entity('Exchange of the one ring', 'activity')
                event2.link('P2', Entity.get_by_id(params["exchange_id"]))
                place2 = insert_entity('Mordor', 'place', 'The heart of evil.')
                place2.link('P2', Entity.get_by_id(Type.get_types('Place')[1]))
                insert_entity('Silmarillion', 'source')

            # ---Content Endpoints---
            # ClassMapping
            rv = self.app.get(url_for('api_03.class_mapping')).get_json()
            assert Api03.get_class_mapping(rv)

            # Content
            rv = self.app.get(
                url_for('api_03.content', lang='de', download=True)).get_json()
            assert bool(rv['intro'] == 'Das ist Deutsch')
            rv = self.app.get(url_for('api_03.content')).get_json()
            assert bool(rv['intro'] == 'This is English')

            # geometric_entities/
            for rv in [
                self.app.get(url_for(
                    'api_03.geometric_entities')).get_json(),
                self.app.get(url_for(
                    'api_03.geometric_entities',
                    download=True)).get_json()]:
                assert bool(rv['features'][0]['geometry']['coordinates'])
                assert Api03.get_geom_properties(rv, 'id')
                assert Api03.get_geom_properties(rv, 'objectDescription')
                assert Api03.get_geom_properties(rv, 'objectId')
                assert Api03.get_geom_properties(rv, 'objectName')
                assert Api03.get_geom_properties(rv, 'shapeType')

            # system_class_count/
            rv = self.app.get(url_for('api_03.system_class_count')).get_json()
            assert bool(rv['person'])

            # ---Entity Endpoints---
            # /entity
            # Test Entity
            for rv in [
                self.app.get(url_for(
                    'api_03.entity',
                    id_=place.id)),
                self.app.get(url_for(
                    'api_03.entity',
                    id_=place.id, download=True))]:
                rv = rv.get_json()
                rv = rv['features'][0]
                assert Api03.get_bool(
                    rv,
                    '@id')
                assert Api03.get_bool(
                    rv,
                    'type',
                    'Feature')
                assert Api03.get_bool(
                    rv,
                    'crmClass',
                    'crm:E18 Physical Thing')
                assert Api03.get_bool(
                    rv,
                    'systemClass',
                    'place')
                assert Api03.get_bool(
                    rv['properties'],
                    'title')
                assert Api03.get_bool(
                    rv['descriptions'][0],
                    'value',
                    'The Shire was the homeland of the hobbits.')
                assert Api03.get_bool(
                    rv['when']['timespans'][0]['start'],
                    'earliest',
                    '2018-01-31T00:00:00')
                assert Api03.get_bool(
                    rv['when']['timespans'][0]['start'],
                    'latest',
                    '2018-03-01T00:00:00')
                assert Api03.get_bool(
                    rv['when']['timespans'][0]['end'],
                    'earliest',
                    '2019-01-31T00:00:00')
                assert Api03.get_bool(
                    rv['when']['timespans'][0]['end'],
                    'latest',
                    '2019-03-01T00:00:00')
                assert Api03.get_bool(
                    rv['types'][0],
                    'identifier')
                assert Api03.get_bool(
                    rv['types'][0],
                    'label',
                    'Boundary Mark')
                assert Api03.get_bool(
                    rv['relations'][1],
                    'label',
                    'Height')
                assert Api03.get_bool(
                    rv['relations'][0],
                    'relationTo')
                assert Api03.get_bool(
                    rv['relations'][0],
                    'relationType',
                    'crm:P2 has type')
                assert Api03.get_bool(
                    rv['relations'][0],
                    'relationSystemClass',
                    'type')
                assert Api03.get_bool(
                    rv['relations'][1],
                    'relationDescription',
                    '23.0')
                assert Api03.get_bool(
                    rv['names'][0],
                    'alias',
                    'Sûza')
                assert Api03.get_bool(
                    rv['links'][0],
                    'type',
                    'closeMatch')
                assert Api03.get_bool(
                    rv['links'][0],
                    'identifier',
                    'https://www.geonames.org/2761369')
                assert Api03.get_bool(
                    rv['links'][0],
                    'referenceSystem',
                    'GeoNames')
                assert Api03.get_bool(
                    rv['geometry'],
                    'type',
                    'Point')
                assert Api03.get_bool(
                    rv['geometry'],
                    'coordinates',
                    [9, 17])
                assert Api03.get_bool(
                    rv['depictions'][0],
                    '@id')
                assert Api03.get_bool(
                    rv['depictions'][0],
                    'title',
                    'Picture with a License')
                assert Api03.get_bool(
                    rv['depictions'][0],
                    'license',
                    'Open license')
                assert Api03.get_bool(
                    rv['depictions'][0],
                    'url')

            # Test entity in GeoJSON format
            rv = self.app.get(url_for(
                'api_03.entity',
                id_=place.id,
                format='geojson')).get_json()
            rv = rv['features'][0]
            assert Api03.get_bool(
                rv['geometry'],
                'type')
            assert Api03.get_bool(
                rv['geometry'],
                'coordinates')
            assert Api03.get_bool(
                rv['properties'],
                '@id')
            assert Api03.get_bool(
                rv['properties'],
                'systemClass')
            assert Api03.get_bool(
                rv['properties'],
                'name')
            assert Api03.get_bool(
                rv['properties'],
                'description')
            assert Api03.get_bool(
                rv['properties'],
                'begin_earliest')
            assert Api03.get_bool(
                rv['properties'],
                'begin_latest')
            assert Api03.get_bool(
                rv['properties'],
                'begin_comment')
            assert Api03.get_bool(
                rv['properties'],
                'end_earliest')
            assert Api03.get_bool(
                rv['properties'],
                'end_latest')
            assert Api03.get_bool(
                rv['properties'],
                'end_comment')
            assert Api03.get_bool(
                rv['properties'],
                'types')

            # Test Entity export and RDFS
            for rv in [
                self.app.get(url_for(
                    'api_03.entity',
                    id_=place.id,
                    format='xml')),
                self.app.get(url_for(
                    'api_03.entity',
                    id_=place.id,
                    export='csv')),
                self.app.get(url_for(
                    'api_03.entity',
                    id_=place.id,
                    export='csvNetwork')),
                self.app.get(url_for(
                    'api_03.view_class',
                    view_class='place',
                    format='xml')),
                self.app.get(url_for(
                    'api_03.view_class',
                    view_class='place',
                    export='csv')),
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
                self.app.get(url_for(
                    'api_03.cidoc_class',
                    cidoc_class='E21')),
                self.app.get(url_for(
                    'api_03.view_class',
                    view_class='place',
                    sort='desc',
                    column='id',
                    relation_type='P2',
                    type_id=boundary_mark.id)),
                self.app.get(url_for(
                    'api_03.latest', latest=2)),
                self.app.get(url_for(
                    'api_03.system_class',
                    system_class='artifact')),
                self.app.get(url_for(
                    'api_03.entities_linked_to_entity',
                    id_=event.id)),
                self.app.get(url_for(
                    'api_03.type_entities',
                    id_=boundary_mark.id)),
                self.app.get(url_for(
                    'api_03.type_entities',
                    id_=relation_sub_id)),
                self.app.get(url_for(
                    'api_03.type_entities_all',
                    id_=unit_node.id)),
                self.app.get(url_for(
                    'api_03.type_entities_all',
                    id_=relation_sub_id)),
                self.app.get(url_for(
                    'api_03.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    sort='desc',
                    column='cidoc_class',
                    system_classes='person',
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
                assert Api03.get_bool(rv_results, '@id')
                assert Api03.get_bool(rv_page, 'entities')
                assert Api03.get_bool(rv_page, 'entitiesPerPage')
                assert Api03.get_bool(rv_page, 'index')
                assert Api03.get_bool(rv_page, 'totalPages')

            # Test Entities with show=none
            rv = self.app.get(url_for(
                'api_03.cidoc_class',
                cidoc_class='E21',
                show='none')).get_json()
            rv = rv['results'][0]['features'][0]
            assert Api03.get_bool_inverse(rv, 'geometry')
            assert Api03.get_no_key(rv, 'depictions')
            assert Api03.get_no_key(rv, 'links')
            assert Api03.get_no_key(rv, 'types')

            # Test Entities limit
            rv = self.app.get(url_for(
                'api_03.query',
                entities=location.id,
                cidoc_classes='E18',
                view_classes='artifact',
                system_classes='person',
                limit=1,
                first=actor2.id)).get_json()
            assert bool(len(rv['results']) == 1)

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
            assert bool(rv['results'][0]['features'][0]['properties'][
                            'title'] == place.name)

            # Test Entities count
            rv = self.app.get(url_for(
                'api_03.query',
                entities=location.id,
                cidoc_classes='E18',
                view_classes='artifact',
                system_classes='person',
                count=True))
            assert bool(rv.get_json() == 8)

            # Test Entities count
            rv = self.app.get(url_for(
                'api_03.geometric_entities',
                count=True))
            assert bool(rv.get_json() == 1)

            # Test entities with GeoJSON Format
            rv = self.app.get(url_for(
                'api_03.query',
                entities=location.id,
                cidoc_classes='E18',
                view_classes='artifact',
                system_classes='person',
                format='geojson')).get_json()
            rv = rv['results'][0]['features'][0]
            assert Api03.get_bool(rv['properties'], '@id')
            assert Api03.get_bool(rv['properties'], 'systemClass')

            # ---Type Endpoints---

            for rv in [
                self.app.get(url_for(
                    'api_03.type_overview')),
                self.app.get(url_for(
                    'api_03.type_overview',
                    download=True))]:
                rv = rv.get_json()
                rv = rv['place'][0]['children'][0]
                assert bool(rv['label'] == 'Austria')

            for rv in [
                self.app.get(url_for(
                    'api_03.type_by_view_class')),
                self.app.get(url_for(
                    'api_03.type_by_view_class',
                    download=True))]:
                rv = rv.get_json()
                rv = rv['place'][0]['children'][0]
                assert bool(rv['label'] == 'Boundary Mark')

            # Test type tree

            for rv in [
                self.app.get(url_for(
                    'api_03.type_tree')),
                self.app.get(url_for(
                    'api_03.type_tree',
                    download=True))]:
                rv = rv.get_json()
                assert bool(rv['typeTree'])

            # Test search parameter
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
                           f'"values":[{params["boundary_mark_id"]},'
                           f'{params["height_id"]},'
                           f'{params["change_of_property_id"]}],'
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
                rv = rv.get_json()
                assert bool(rv['pagination']['entities'] == 2)

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
                           f'"values":[({params["height_id"]},23.0)],'
                           f'"logicalOperator":"or"}}]}}')),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search=f'{{"typeID":[{{"operator":"equal",'
                           f'"values":[{params["boundary_mark_id"]},'
                           f'{params["height_id"]}],'
                           f'"logicalOperator":"or"}}]}}')),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='lp',
                    search=f'{{"typeIDWithSubs":[{{"operator":"equal",'
                           f'"values":[{params["boundary_mark_id"]},'
                           f'{params["height_id"]}],'
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
                    search=
                    '{"endTo":[{"operator":"greaterThanEqual", '
                    '"values":["2019-03-01"],"logicalOperator":"and"}]}')),
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
                           '"logicalOperator": "and"}]}'))]:
                rv = rv.get_json()
                assert bool(rv['pagination']['entities'] == 1)

            # Test search parameter
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
                rv = rv.get_json()
                assert bool(rv['pagination']['entities'] == 6)

            # Test search parameter
            rv = self.app.get(url_for(
                'api_03.query',
                system_classes='place',
                search="""{"entityName":[{"operator":"notEqual",
                    "values":["Mordor"],
                    "logicalOperator":"or"}]}""")).get_json()
            assert bool(rv['pagination']['entities'] == 1)

            # subunits/
            for rv in [
                self.app.get(url_for(
                    'api_03.subunits',
                    id_=place.id)),
                self.app.get(url_for(
                    'api_03.subunits',
                    id_=place.id,
                    download=True))]:
                rv = rv.get_json()
                rv = rv[str(place.id)][0]
                assert bool(rv['id'] == place.id)
                assert bool(rv['openatlasClassName'] == "place")
                assert bool(rv['children'] == [feature.id])
                rv = rv['properties']
                assert bool(rv['name'] == place.name)
                assert bool(rv['description'] == place.description)
                assert bool(rv['aliases'] == [alias.name])
                assert bool(rv['externalReferences'])
                assert bool(rv['timespan'])
                assert bool(rv['standardType'])
                assert bool(rv['files'])
                assert bool(rv['types'])

            rv = self.app.get(url_for(
                'api_03.subunits', id_=place.id, count=True))
            assert b'3' in rv.data

            for rv in [
                self.app.get(url_for(
                    'api_03.subunits',
                    id_=place.id,
                    format='xml')),
                self.app.get(url_for(
                    'api_03.subunits',
                    id_=place.id,
                    format='xml',
                    download=True))]:
                assert b'Shire' in rv.data

            with self.assertRaises(EntityDoesNotExistError):
                self.app.get(url_for(
                    'api_03.entity',
                    id_=233423424))
            with self.assertRaises(NotAPlaceError):
                self.app.get(url_for(
                    'api_03.subunits',
                    id_=actor.id))
            with self.assertRaises(EntityDoesNotExistError):
                self.app.get(url_for(
                    'api_03.cidoc_class',
                    cidoc_class='E18',
                    last=1231))
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
                self.app.get(url_for(
                    'api_03.query',
                    entities=12345))
            with self.assertRaises(NoEntityAvailable):
                self.app.get(url_for(
                    'api_03.cidoc_class',
                    cidoc_class='E68',
                    last=1231))
            with self.assertRaises(InvalidSystemClassError):
                self.app.get(url_for(
                    'api_03.system_class',
                    system_class='Wrong'))
            with self.assertRaises(QueryEmptyError):
                self.app.get(url_for('api_03.query'))
            with self.assertRaises(InvalidSubunitError):
                self.app.get(url_for(
                    'api_03.type_entities',
                    id_=1234))
            with self.assertRaises(InvalidSubunitError):
                self.app.get(url_for(
                    'api_03.type_entities_all',
                    id_=1234))
            with self.assertRaises(InvalidCidocClassCode):
                self.app.get(url_for(
                    'api_03.cidoc_class',
                    cidoc_class='e99999999'))
            with self.assertRaises(InvalidCodeError):
                self.app.get(url_for(
                    'api_03.view_class',
                    view_class='Invalid'))
            with self.assertRaises(InvalidLimitError):
                self.app.get(url_for(
                    'api_03.latest',
                    latest='99999999'))
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

    @staticmethod
    def get_bool(
            data: dict[str, Any], key: str,
            value: Optional[Union[str, list[Any]]] = None) -> bool:
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
    def get_class_mapping(data: list[dict[str, Any]]) -> bool:
        return bool(data[0]['systemClass']
                    and data[0]['crmClass']
                    and data[0]['view']
                    and data[0]['icon']
                    and data[0]['en'])
