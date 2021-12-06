from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from flask import g, url_for

from openatlas import app
from openatlas.api.v03.resources.error import (EntityDoesNotExistError,
                                               FilterColumnError,
                                               FilterLogicalOperatorError,
                                               FilterOperatorError,
                                               InvalidCidocClassCode,
                                               InvalidCodeError,
                                               InvalidLimitError,
                                               InvalidSubunitError,
                                               InvalidSystemClassError,
                                               LastEntityError,
                                               NoEntityAvailable,
                                               NoSearchStringError,
                                               QueryEmptyError, TypeIDError)
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type
from tests.base import TestBaseCase, insert_entity


class ApiTests(TestBaseCase):

    def test_api(self) -> None:

        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                params = {
                    f'{(node.name.lower()).replace(" ", "_")}_id': id_ for
                    (id_, node) in Type.get_all().items()}
                # Creation of Shire (place)
                place = insert_entity(
                    'Shire', 'place',
                    description='The Shire was the homeland of the hobbits.')
                if not place:  # Needed for Mypy
                    return  # pragma: no cover

                # Adding Created and Modified
                place.created = str(datetime.now())
                place.modified = str(datetime.now())

                # Adding Dates to place
                place.begin_from = '2018-01-31'
                place.begin_to = '2018-03-01'
                place.begin_comment = 'Begin of the shire'
                place.end_from = '2019-01-31'
                place.end_to = '2019-03-01'
                place.end_comment = 'Descent of Shire'
                place.update()

                location = place.get_linked_entity_safe('P53')
                Gis.add_example_geom(location)

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
                feature = insert_entity('Home of Baggins', 'feature', place)
                feature.created = str(datetime.now())
                feature.modified = str(datetime.now())

                # Adding stratigraphic to place
                strati = insert_entity('Kitchen', 'stratigraphic_unit', feature)
                strati.created = str(datetime.now())
                strati.modified = str(datetime.now())

                # Adding Administrative Unit Type
                unit_node = Type.get_hierarchy('Administrative unit')

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
                    'Frodo', 'person',
                    description='That is Frodo')
                if not place:  # Needed for Mypy
                    return  # pragma: no cover

                alias2 = insert_entity('The ring bearer', 'actor_appellation')
                actor.link('P131', alias2)

                # Adding file to actor
                file2 = insert_entity('File without license', 'file')
                file2.link('P67', actor)

                # Adding artefact to actor
                artifact = insert_entity('The One Ring', 'artifact')
                artifact.link('P52', actor)

                # Creation of second actor (Sam)
                actor2 = insert_entity(
                    'Sam', 'person',
                    description='That is Sam')
                if not place:  # Needed for Mypy
                    return  # pragma: no cover

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

                # Creation of Mordor (place)
                place2 = insert_entity(
                    'Mordor', 'place',
                    description='The heart of evil.')
                if not place:  # Needed for Mypy
                    return  # pragma: no cover

                # Adding Type Settlement
                place2.link('P2', Entity.get_by_id(Type.get_types('Place')[1]))

                # Creation of Silmarillion (source)
                source = insert_entity('Silmarillion', 'source')

            # ---Content Endpoints---
            # ClassMapping
            for rv in [self.app.get(url_for('api_02.class_mapping')).get_json(),
                       self.app.get(
                           url_for('api_03.class_mapping')).get_json()]:
                assert ApiTests.get_class_mapping(rv)

            # Content
            for rv in [self.app.get(
                    url_for('api_02.content', lang='de',
                            download=True)).get_json(),
                       self.app.get(url_for('api_03.content', lang='de',
                                            download=True)).get_json()]:
                assert bool(rv['intro'] == 'Das ist Deutsch')
            for rv in [self.app.get(url_for('api_02.content')).get_json(),
                       self.app.get(url_for('api_03.content')).get_json()]:
                assert bool(rv['intro'] == 'This is English')

            # geometric_entities/
            for rv in [
                self.app.get(url_for('api_02.geometric_entities')).get_json(),
                self.app.get(url_for(
                    'api_02.geometric_entities',
                    download=True)).get_json(),
                self.app.get(url_for('api_03.geometric_entities')).get_json(),
                self.app.get(url_for(
                    'api_03.geometric_entities',
                    download=True)).get_json()]:
                assert bool(rv['features'][0]['geometry'][
                                'coordinates'])
                assert ApiTests.get_geom_properties(rv, 'id')
                assert ApiTests.get_geom_properties(rv, 'objectDescription')
                assert ApiTests.get_geom_properties(rv, 'objectId')
                assert ApiTests.get_geom_properties(rv, 'objectName')
                assert ApiTests.get_geom_properties(rv, 'shapeType')

            # system_class_count/
            for rv in [
                self.app.get(url_for('api_02.system_class_count')).get_json(),
                self.app.get(url_for('api_03.system_class_count')).get_json()]:
                assert bool(rv['person'])

            # overview_count/
            rv = self.app.get(url_for('api_02.overview_count')).get_json()
            assert bool(rv[0]['systemClass'])

            # ---Entity Endpoints---
            # /entity
            # Test Entity
            for rv in [
                self.app.get(url_for('api_02.entity', id_=place.id)),
                self.app.get(
                    url_for('api_02.entity', id_=place.id, download=True)),
                self.app.get(url_for('api_03.entity', id_=place.id)),
                self.app.get(
                    url_for('api_03.entity', id_=place.id, download=True))]:
                rv = rv.get_json()
                rv = rv['features'][0]
                assert ApiTests.get_bool(
                    rv,
                    '@id')
                assert ApiTests.get_bool(
                    rv,
                    'type',
                    'Feature')
                assert ApiTests.get_bool(
                    rv,
                    'crmClass',
                    'crm:E18 Physical Thing')
                assert ApiTests.get_bool(
                    rv,
                    'systemClass',
                    'place')
                assert ApiTests.get_bool(
                    rv['properties'],
                    'title')
                assert ApiTests.get_bool(
                    rv['description'][0],
                    'value',
                    'The Shire was the homeland of the hobbits.')
                assert ApiTests.get_bool(
                    rv['when']['timespans'][0]['start'],
                    'earliest',
                    '2018-01-31')
                assert ApiTests.get_bool(
                    rv['when']['timespans'][0]['start'],
                    'latest',
                    '2018-03-01')
                assert ApiTests.get_bool(
                    rv['when']['timespans'][0]['end'],
                    'earliest',
                    '2019-01-31')
                assert ApiTests.get_bool(
                    rv['when']['timespans'][0]['end'],
                    'latest',
                    '2019-03-01')
                assert ApiTests.get_bool(
                    rv['types'][0],
                    'identifier')
                assert ApiTests.get_bool(
                    rv['types'][0],
                    'label',
                    'Boundary Mark')
                assert ApiTests.get_bool(
                    rv['relations'][1],
                    'label',
                    'Height')
                assert ApiTests.get_bool(
                    rv['relations'][0],
                    'relationTo')
                assert ApiTests.get_bool(
                    rv['relations'][0],
                    'relationType',
                    'crm:P2 has type')
                assert ApiTests.get_bool(
                    rv['relations'][0],
                    'relationSystemClass',
                    'type')
                assert ApiTests.get_bool(
                    rv['relations'][1],
                    'relationDescription',
                    '23.0')
                assert ApiTests.get_bool(
                    rv['names'][0],
                    'alias',
                    'Sûza')
                assert ApiTests.get_bool(
                    rv['links'][0],
                    'type',
                    'closeMatch')
                assert ApiTests.get_bool(
                    rv['links'][0],
                    'identifier',
                    'https://www.geonames.org/2761369')
                assert ApiTests.get_bool(
                    rv['links'][0],
                    'referenceSystem',
                    'GeoNames')
                assert ApiTests.get_bool(
                    rv['geometry'],
                    'type',
                    'Point')
                assert ApiTests.get_bool(
                    rv['geometry'],
                    'coordinates',
                    [9, 17])
                assert ApiTests.get_bool(
                    rv['depictions'][0],
                    '@id')
                assert ApiTests.get_bool(
                    rv['depictions'][0],
                    'title',
                    'Picture with a License')
                assert ApiTests.get_bool(
                    rv['depictions'][0],
                    'license',
                    'Open license')
                assert ApiTests.get_bool(
                    rv['depictions'][0],
                    'url')

            # Test entity in GeoJSON format
            for rv in [
                self.app.get(url_for('api_02.entity', id_=place.id,
                                     format='geojson')),
                self.app.get(url_for('api_03.entity', id_=place.id,
                                     format='geojson'))]:
                rv = rv.get_json()
                rv = rv['features'][0]
                assert ApiTests.get_bool(
                    rv['geometry'],
                    'type')
                assert ApiTests.get_bool(
                    rv['geometry'],
                    'coordinates')
                assert ApiTests.get_bool(
                    rv['properties'],
                    '@id')
                assert ApiTests.get_bool(
                    rv['properties'],
                    'systemClass')
                assert ApiTests.get_bool(
                    rv['properties'],
                    'name')
                assert ApiTests.get_bool(
                    rv['properties'],
                    'description')
                assert ApiTests.get_bool(
                    rv['properties'],
                    'begin_earliest')
                assert ApiTests.get_bool(
                    rv['properties'],
                    'begin_latest')
                assert ApiTests.get_bool(
                    rv['properties'],
                    'begin_comment')
                assert ApiTests.get_bool(
                    rv['properties'],
                    'end_earliest')
                assert ApiTests.get_bool(
                    rv['properties'],
                    'end_latest')
                assert ApiTests.get_bool(
                    rv['properties'],
                    'end_comment')
                assert ApiTests.get_bool(
                    rv['properties'],
                    'types')

            # Test Entity export and RDFS
            for rv in [
                self.app.get(url_for(
                    'api_02.entity',
                    id_=place.id,
                    format='pretty-xml')),
                self.app.get(url_for(
                    'api_03.entity',
                    id_=place.id,
                    format='pretty-xml')),
                self.app.get(
                    url_for('api_02.entity', id_=place.id, export='csv')),
                self.app.get(
                    url_for('api_03.entity', id_=place.id, export='csv')),
                self.app.get(url_for(
                    'api_02.code',
                    code='place',
                    format='pretty-xml')),
                self.app.get(url_for(
                    'api_03.code',
                    code='place',
                    format='pretty-xml')),
                self.app.get(
                    url_for('api_02.code', code='place', export='csv')),
                self.app.get(
                    url_for('api_03.code', code='place', export='csv')),
                self.app.get(url_for(
                    'api_02.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    export='csv')),
                self.app.get(url_for(
                    'api_03.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    export='csv'))
            ]:
                assert b'Shire' in rv.data

            # Test Entities endpoints
            for rv in [
                self.app.get(url_for('api_02.class', class_code='E21')),
                self.app.get(url_for(
                    'api_02.code',
                    code='place',
                    type_id=boundary_mark.id)),
                self.app.get(url_for('api_02.latest', latest=2)),
                self.app.get(
                    url_for('api_02.system_class', system_class='artifact')),
                self.app.get(
                    url_for('api_02.entities_linked_to_entity', id_=event.id)),
                self.app.get(url_for(
                    'api_02.type_entities',
                    id_=boundary_mark.id)),
                self.app.get(url_for(
                    'api_02.type_entities',
                    id_=relation_sub_id)),
                self.app.get(url_for(
                    'api_02.type_entities_all',
                    id_=unit_node.id)),
                self.app.get(url_for(
                    'api_02.type_entities_all',
                    id_=relation_sub_id)),
                self.app.get(
                    url_for(
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
                    filter=f"and|begin_from|eq|{place.begin_from}")),
                self.app.get(url_for(
                    'api_03.class',
                    class_code='E21')),
                self.app.get(url_for(
                    'api_03.code',
                    code='place',
                    type_id=boundary_mark.id)),
                self.app.get(url_for('api_03.latest', latest=2)),
                self.app.get(
                    url_for('api_03.system_class', system_class='artifact')),
                self.app.get(
                    url_for('api_03.entities_linked_to_entity', id_=event.id)),
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
                self.app.get(
                    url_for(
                        'api_03.query',
                        entities=location.id,
                        classes='E18',
                        codes='artifact',
                        system_classes='person',
                        last=actor.id)),
                self.app.get(url_for(
                    'api_03.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    sort='desc',
                    column='id',
                    download=True,
                    actor=place.id))
            ]:
                rv = rv.get_json()
                rv_results = rv['results'][0]['features'][0]
                rv_page = rv['pagination']
                assert ApiTests.get_bool(rv_results, '@id')
                assert ApiTests.get_bool(rv_page, 'entities')
                assert ApiTests.get_bool(rv_page, 'entitiesPerPage')
                assert ApiTests.get_bool(rv_page, 'index')
                assert ApiTests.get_bool(rv_page, 'totalPages')

            # Test Entities with show=none
            for rv in [
                self.app.get(url_for('api_02.class', class_code='E21',
                                     show='none')),
                self.app.get(url_for('api_03.class', class_code='E21',
                                     show='none'))]:
                rv = rv.get_json()
                rv = rv['results'][0]['features'][0]
                assert ApiTests.get_bool_inverse(rv, 'geometry')
                assert ApiTests.get_no_key(rv, 'depictions')
                assert ApiTests.get_no_key(rv, 'links')
                assert ApiTests.get_no_key(rv, 'types')

            # Test Entities limit
            for rv in [
                self.app.get(url_for(
                    'api_02.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    limit=1,
                    first=actor2.id)),
                self.app.get(url_for(
                    'api_03.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    limit=1,
                    first=actor2.id))]:
                rv = rv.get_json()
                assert bool(len(rv['results']) == 1)

            # Test if Query returns enough entities
            for rv in [
                self.app.get(url_for(
                    'api_02.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    limit=1,
                    first=actor2.id)),
                self.app.get(url_for(
                    'api_03.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    limit=1,
                    first=actor2.id))]:
                rv = rv.get_json()
                assert bool(rv['pagination']['entities'] == 8)

            # Test Entities count
            for rv in [self.app.get(url_for(
                    'api_02.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    count=True)),
                self.app.get(url_for(
                    'api_03.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    count=True))]:
                assert bool(rv.get_json() == 8)

            # Test Entities count
            for rv in [
                self.app.get(url_for(
                    'api_02.geometric_entities',
                    count=True)),
                self.app.get(url_for(
                    'api_03.geometric_entities',
                    count=True))]:
                assert bool(rv.get_json() == 1)

            # Test entities with GeoJSON Format
            for rv in [
                self.app.get(url_for(
                    'api_02.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    format='geojson')),
                self.app.get(url_for(
                    'api_03.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    format='geojson'))]:
                rv = rv.get_json()
                rv = rv['results'][0]['features'][0]
                assert ApiTests.get_bool(
                    rv['properties'],
                    '@id')
                assert ApiTests.get_bool(
                    rv['properties'],
                    'systemClass')

            # ---Type Endpoints---

            # Test Type Entities
            for rv in [
                self.app.get(url_for(
                    'api_02.node_entities',
                    id_=unit_node.id,
                    download=True)),
                self.app.get(url_for(
                    'api_03.node_entities',
                    id_=unit_node.id,
                    download=True))]:
                rv = rv.get_json()
                rv = rv['nodes'][0]
                assert ApiTests.get_bool(rv, 'label')

            # Test Type Entities All
            for rv in [
                self.app.get(url_for(
                    'api_02.node_entities_all',
                    id_=unit_node.id)),
                self.app.get(url_for(
                    'api_03.node_entities_all',
                    id_=unit_node.id))]:
                rv = rv.get_json()
                rv = rv['nodes']
                assert bool([True for i in rv if
                             i['label'] == 'Wien'])

            # Test Type Entities count
            for rv in [
                self.app.get(url_for(
                    'api_02.node_entities',
                    id_=unit_node.id,
                    count=True)),
                self.app.get(url_for(
                    'api_03.node_entities',
                    id_=unit_node.id,
                    count=True))]:
                assert bool(rv.get_json() == 6)

                # Test Type Overview
            for rv in [
                self.app.get(url_for('api_02.node_overview')),
                self.app.get(url_for('api_02.node_overview', download=True))]:
                rv = rv.get_json()
                rv = rv['types'][0]['place']['Administrative unit']
                assert bool([True for i in rv if
                             i['label'] == 'Austria'])

            for rv in [
                self.app.get(url_for('api_03.node_overview')),
                self.app.get(url_for('api_03.node_overview', download=True))]:
                rv = rv.get_json()
                rv = rv['types']['place']['Administrative unit']
                assert bool([True for i in rv if
                             i['label'] == 'Austria'])

            # Test Type Tree
            for rv in [
                self.app.get(url_for('api_02.type_tree')),
                self.app.get(url_for('api_02.type_tree', download=True))
            ]:
                rv = rv.get_json()
                assert bool(rv['typeTree'][0])

            for rv in [
                self.app.get(url_for('api_03.type_tree')),
                self.app.get(url_for('api_03.type_tree', download=True)),
            ]:
                rv = rv.get_json()
                assert bool(rv['typeTree'])

            # Test search parameter
            for rv in [
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    format='lp',
                    search=f'{{"entityCidocClass":[{{"operator":"equal",'
                           f'"values":["E21"],'
                           f'"logicalOperator":"and"}}]}}')),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    format='lp',
                    search=f'{{"entitySystemClass":[{{"operator":"equal",'
                           f'"values":["person"],'
                           f'"logicalOperator":"and"}}]}}'))]:
                rv = rv.get_json()
                assert bool(rv['pagination']['entities'] == 2)

            # Test search parameter
            for rv in [
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    format='lp',
                    search=f'{{"typeID":[{{"operator":"equal",'
                           f'"values":[{params["boundary_mark_id"]},'
                           f'{params["height_id"]}],'
                           f'"logicalOperator":"or"}}]}}')),
                self.app.get(url_for(
                    'api_03.query',
                    system_classes='place',
                    search=f'{{"entityName":[{{"operator":"notEqual",'
                           f'"values":["Mordor"],'
                           f'"logicalOperator":"or"}}]}}')),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    format='lp',
                    search=f'{{"typeName":[{{"operator":"equal",'
                           f'"values":["Boundary Mark", "Height"],'
                           f'"logicalOperator":"and"}}]}}'))]:
                rv = rv.get_json()
                assert bool(rv['pagination']['entities'] == 1)

            # Test search parameter
            for rv in [
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    format='lp',
                    search=f'{{"typeName":[{{"operator":"notEqual",'
                           f'"values":["Boundary Mark", "Height"],'
                           f'"logicalOperator":"and"}}]}}')),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    format='lp',
                    search=f'{{"entityID":[{{"operator":"notEqual",'
                           f'"values":[{place.id}],'
                           f'"logicalOperator":"and"}}]}}')),
                self.app.get(url_for(
                    'api_03.query',
                    entities=place.id,
                    classes='E18',
                    codes='artifact',
                    system_classes='person',
                    format='lp',
                    search=f'{{"entityAliases":[{{"operator":"notEqual",'
                           f'"values":["Sûza"],'
                           f'"logicalOperator":"and"}}]}}'))]:
                rv = rv.get_json()
                assert bool(rv['pagination']['entities'] == 6)

            # Test search parameter
            rv = self.app.get(url_for(
                'api_03.query',
                system_classes='place',
                search=f'{{"entityName":[{{"operator":"notEqual",'
                       f'"values":["Mordor"],'
                       f'"logicalOperator":"or"}}]}}')).get_json()
            assert bool(rv['pagination']['entities'] == 1)

            # subunit/
            rv = self.app.get(
                url_for('api_02.subunit', id_=place.id)).get_json()
            assert bool(rv['nodes'][0][
                            'label'] == 'Home of Baggins')

            # subunit_hierarchy/
            rv = self.app.get(
                url_for('api_02.subunit_hierarchy', id_=place.id)).get_json()
            assert bool(rv['nodes'][1]['label'] == 'Kitchen')

            # subunits/
            for rv in [
                self.app.get(
                    url_for('api_03.subunits', id_=place.id)),
                self.app.get(
                    url_for('api_03.subunits', id_=place.id, download=True))]:
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

            rv = self.app.get(
                url_for('api_03.subunits', id_=place.id, count=True))
            assert b'3' in rv.data

            for rv in [
                self.app.get(
                    url_for('api_03.subunits', id_=place.id, format='xml')),
                self.app.get(
                    url_for('api_03.subunits',
                            id_=place.id,
                            format='xml',
                            download=True))]:
                assert b'Shire' in rv.data

            with self.assertRaises(EntityDoesNotExistError):
                self.app.get(url_for('api_03.entity', id_=233423424))
            with self.assertRaises(EntityDoesNotExistError):
                self.app.get(url_for(
                    'api_03.class',
                    class_code='E18',
                    last=1231))
            with self.assertRaises(LastEntityError):
                self.app.get(url_for(
                    'api_03.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
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
                    'api_03.class',
                    class_code='E68',
                    last=1231))
            with self.assertRaises(InvalidSystemClassError):
                self.app.get(url_for(
                    'api_03.system_class',
                    system_class='Wrong'))
            with self.assertRaises(QueryEmptyError):
                self.app.get(url_for('api_03.query'))
            with self.assertRaises(InvalidSubunitError):
                self.app.get(url_for(
                    'api_03.node_entities',
                    id_=1234))
            with self.assertRaises(InvalidSubunitError):
                self.app.get(url_for(
                    'api_03.node_entities_all',
                    id_=1234))
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
                    'api_03.class',
                    class_code='e99999999'))
            with self.assertRaises(InvalidCodeError):
                self.app.get(url_for(
                    'api_03.code',
                    code='Invalid'))
            with self.assertRaises(InvalidLimitError):
                self.app.get(url_for(
                    'api_03.latest',
                    latest='99999999'))
            with self.assertRaises(NoEntityAvailable):
                self.app.get(url_for(
                    'api_03.code',
                    entities=place.id,
                    code='place',
                    search=f'{{"typeName":[{{"operator":"equal",'
                           f'"values":["Boundary Mark", "Height", "Dimension"],'
                           f'"logicalOperator":"and"}}]}}'))
            with self.assertRaises(FilterOperatorError):
                self.app.get(url_for(
                    'api_03.code',
                    entities=place.id,
                    code='place',
                    search=f'{{"typeName":[{{"operator":"notEqualT",'
                           f'"values":["Boundary Mark", "Height"],'
                           f'"logicalOperator":"and"}}]}}'))
            with self.assertRaises(FilterLogicalOperatorError):
                self.app.get(url_for(
                    'api_03.code',
                    entities=place.id,
                    code='place',
                    search=f'{{"typeName":[{{"operator":"notEqual",'
                           f'"values":["Boundary Mark", "Height"],'
                           f'"logicalOperator":"xor"}}]}}'))
            with self.assertRaises(FilterColumnError):
                self.app.get(url_for(
                    'api_03.code',
                    entities=place.id,
                    code='place',
                    search=f'{{"All":[{{"operator":"notEqual",'
                           f'"values":["Boundary Mark", "Height"],'
                           f'"logicalOperator":"or"}}]}}'))
            with self.assertRaises(NoSearchStringError):
                self.app.get(url_for(
                    'api_03.code',
                    entities=place.id,
                    code='place',
                    search=f'{{"typeName":[{{"operator":"notEqual",'
                           f'"values":[],'
                           f'"logicalOperator":"or"}}]}}'))

    @staticmethod
    def get_bool(
            data: Dict[str, Any], key: str,
            value: Optional[Union[str, List[Any]]] = None) -> bool:
        if value:
            return bool(data[key] == value)
        return bool(data[key])

    @staticmethod
    def get_bool_inverse(data: Dict[str, Any], key: str) -> bool:
        return bool(not data[key])

    @staticmethod
    def get_no_key(data: Dict[str, Any], key: str) -> bool:
        return bool(key not in data.keys())

    @staticmethod
    def get_geom_properties(geom: Dict[str, Any], key: str) -> bool:
        return bool(geom['features'][0]['properties'][key])

    @staticmethod
    def get_class_mapping(data: List[Dict[str, Any]]) -> bool:
        return bool(data[0]['systemClass']
                    and data[0]['crmClass']
                    and data[0]['view']
                    and data[0]['icon']
                    and data[0]['en'])
