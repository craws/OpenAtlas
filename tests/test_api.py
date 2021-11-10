from flask import g, url_for

from openatlas import app
from openatlas.api.v03.endpoints.content.class_mapping import ClassMapping
from openatlas.api.v03.resources.error import (EntityDoesNotExistError,
                                               FilterColumnError,
                                               FilterLogicalOperatorError,
                                               FilterOperatorError,
                                               InvalidCidocClassCode,
                                               InvalidCodeError,
                                               InvalidLimitError,
                                               InvalidSubunitError,
                                               InvalidSystemClassError,
                                               NoEntityAvailable,
                                               NoSearchStringError,
                                               QueryEmptyError, TypeIDError)
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.node import Node
from openatlas.models.reference_system import ReferenceSystem
from tests.api_test_data import content, overview_count, \
    system_class_count
from tests.api_test_data.cidoc_class import CidocClass
from tests.api_test_data.code import Code
from tests.api_test_data.entities_linked_to_entity import EntitiesLinked
from tests.api_test_data.entity import Entity as TestEntity
from tests.api_test_data.geometric_entities import GeometricEntity
from tests.api_test_data.latest import Latest
from tests.api_test_data.node_entities import NodeEntities
from tests.api_test_data.node_overview import NodeOverview
from tests.api_test_data.query import Query
from tests.api_test_data.search import Search
from tests.api_test_data.subunit import Subunits
from tests.api_test_data.system_class import SystemClass
from tests.api_test_data.type_entities import TypeEntities
from tests.api_test_data.type_tree import TypeTree
from tests.base import TestBaseCase, insert_entity


class ApiTests(TestBaseCase):

    def test_api(self) -> None:

        with app.app_context():  # type: ignore
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                params = {
                    f'{(node.name.lower()).replace(" ", "_")}_id': id_ for
                    (id_, node) in Node.get_all_nodes().items()}
                params['geonames_id'] = 102

                # Creation of Shire (place)
                place = insert_entity(
                    'Shire',
                    'place',
                    description='The Shire was the homeland of the hobbits.')
                if not place:  # Needed for Mypy
                    return  # pragma: no cover
                params['shire_id'] = place.id

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
                params['location_shire_id'] = location.id

                # Adding Type Place
                place.link('P2', Node.get_hierarchy('Place'))

                # Adding Alias
                alias = insert_entity('Sûza', 'appellation')
                place.link('P1', alias)
                params['suza_id'] = alias.id

                # Adding External Reference
                external_reference = insert_entity(
                    'https://lotr.fandom.com/',
                    'external_reference')
                external_reference.link(
                    'P67',
                    place,
                    description='Fandom Wiki of lord of the rings')
                params['lotr_id'] = external_reference.id

                # Adding feature to place
                feature = insert_entity('Home of Baggins', 'feature', place)
                params['home_id'] = feature.id
                params['location_home_id'] = feature.id + 1

                # Adding stratigraphic to place
                strati = insert_entity('Kitchen', 'stratigraphic_unit', feature)
                params['kitchen_id'] = strati.id
                params['location_kitchen_id'] = strati.id + 1

                # Adding Administrative Unit Node
                unit_node = Node.get_hierarchy('Administrative unit')

                # Adding File to place
                file = insert_entity('Picture with a License', 'file')
                file.link('P67', place)
                file.link('P2', g.nodes[Node.get_hierarchy('License').subs[0]])
                params['picture_id'] = file.id

                # Adding Value Type
                value_type = Node.get_hierarchy('Dimensions')
                place.link('P2', Entity.get_by_id(value_type.subs[0]), '23.0')

                # Adding Geonames
                geonames = Entity.get_by_id(
                    ReferenceSystem.get_by_name('GeoNames').id)
                precision_id = Node.get_hierarchy(
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
                params['frodo_id'] = actor.id

                alias2 = insert_entity('The ring bearer', 'actor_appellation')
                actor.link('P131', alias2)
                params['alias2_id'] = alias2.id

                # Adding file to actor
                file2 = insert_entity('File without license', 'file')
                file2.link('P67', actor)
                params['file_without_id'] = file2.id

                # Adding artefact to actor
                artifact = insert_entity('The One Ring', 'artifact')
                artifact.link('P52', actor)
                params['ring_id'] = artifact.id
                params['location_ring_id'] = artifact.id + 1

                # Creation of second actor (Sam)
                actor2 = insert_entity(
                    'Sam', 'person',
                    description='That is Sam')
                if not place:  # Needed for Mypy
                    return  # pragma: no cover
                params['sam_id'] = actor2.id

                # Adding residence
                actor2.link('P74', location)

                # Adding actor relation
                relation_id = Node.get_hierarchy('Actor actor relation').id
                relation_sub_id = g.nodes[relation_id].subs[0]
                actor.link('OA7', actor2, type_id=relation_sub_id)

                # Creation of event
                event = insert_entity('Travel to Mordor', 'activity')
                event.link('P11', actor)
                event.link('P14', actor2)
                event.link('P7', location)
                params['travel_id'] = event.id

                # Creation of Mordor (place)
                place2 = insert_entity(
                    'Mordor', 'place',
                    description='The heart of evil.')
                if not place:  # Needed for Mypy
                    return  # pragma: no cover
                params['mordor_id'] = place2.id
                params['location_mordor_id'] = place2.id + 1

                # Adding Type Settlement
                place2.link('P2', Entity.get_by_id(Node.get_nodes('Place')[0]))

                # Creation of Silmarillion (source)
                source = insert_entity('Silmarillion', 'source')
                params['silmarillion_id'] = source.id

            self.maxDiff = None

            # ---Entity Endpoints---
            # /entity
            rv = self.app.get(url_for(
                'api.entity',
                id_=place.id))
            self.assertDictEqual(
                rv.get_json(),
                TestEntity.get_test_entity_lpf(params))
            rv = self.app.get(url_for(
                'api.entity',
                id_=place.id,
                export='csv'))
            assert b'Shire' in rv.data
            rv = self.app.get(url_for(
                'api.entity',
                id_=place.id,
                download=True))
            self.assertDictEqual(
                rv.get_json(),
                TestEntity.get_test_entity_lpf(params))
            rv = self.app.get(url_for(
                'api.entity',
                id_=place.id,
                format='xml'))
            assert b'Shire' in rv.data
            rv = self.app.get(url_for(
                'api.entity',
                id_=place.id,
                format='geojson'))
            self.assertDictEqual(
                rv.get_json(),
                TestEntity.get_test_entity_geojson(params))

            # /class
            rv = self.app.get(url_for(
                'api.class',
                class_code='E21'))
            self.assertDictEqual(
                rv.get_json(),
                CidocClass.get_test_cidoc_class(params))
            rv = self.app.get(url_for(
                'api.class',
                class_code='E21',
                show='none'))
            self.assertDictEqual(
                rv.get_json(),
                CidocClass.get_test_cidoc_class_show_none(params))

            # /code
            rv = self.app.get(url_for(
                'api.code',
                code='place'))
            self.assertDictEqual(rv.get_json(), Code.get_test_code(params))

            # /entities_linked_to_entity
            rv = self.app.get(url_for(
                'api.entities_linked_to_entity',
                id_=event.id))
            self.assertDictEqual(
                rv.get_json(),
                EntitiesLinked.get_test_entities_linked_to(params))

            # /latest
            rv = self.app.get(url_for(
                'api.latest',
                latest=2))
            self.assertDictEqual(rv.get_json(), Latest.get_test_latest(params))

            # /system_class
            rv = self.app.get(url_for(
                'api.system_class',
                system_class='artifact'))
            self.assertDictEqual(
                rv.get_json(),
                SystemClass.test_system_class(params))

            # /type_entities
            rv = self.app.get(url_for(
                'api.type_entities',
                id_=Node.get_hierarchy('Place').id))
            self.assertDictEqual(
                rv.get_json(),
                TypeEntities.get_test_type_entities(params))
            rv = self.app.get(url_for(
                'api.type_entities',
                id_=relation_sub_id))
            self.assertDictEqual(
                rv.get_json(),
                CidocClass.get_test_cidoc_class(params))

            # /type_entities_all
            rv = self.app.get(url_for(
                'api.type_entities_all',
                id_=relation_sub_id))
            self.assertDictEqual(
                rv.get_json(),
                CidocClass.get_test_cidoc_class(params))
            rv = self.app.get(url_for(
                'api.type_entities_all',
                id_=unit_node.id))
            self.assertDictEqual(
                rv.get_json(),
                TypeEntities.get_test_type_entities_all_special(params))

            # /query
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person'))
            self.assertDictEqual(
                rv.get_json(),
                Query.get_test_query(params))

            # /query with different parameter
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                type_id=Node.get_nodes('Place')[0]))
            self.assertDictEqual(
                rv.get_json(),
                Query.get_test_query_type(params))
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                limit=1,
                first=actor2.id))
            self.assertDictEqual(
                rv.get_json(),
                Query.get_test_query_first(params))
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                limit=1,
                last=actor2.id))
            self.assertDictEqual(
                rv.get_json(),
                Query.get_test_query_last(params))
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                download=True))
            self.assertDictEqual(
                rv.get_json(),
                Query.get_test_query(params))
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                count=True))
            assert b'8' in rv.data
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                format='xml'))
            assert b'Shire' in rv.data
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                export='csv'))
            assert b'Shire' in rv.data
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                format='geojson'))
            self.assertDictEqual(
                rv.get_json(),
                Query.get_test_query_geojson(params))

            # ---Content Endpoints---

            # /classes
            rv = self.app.get(url_for('api.class_mapping'))
            self.assertAlmostEqual(rv.get_json(), ClassMapping.mapping)

            # content/
            rv = self.app.get(url_for(
                'api.content',
                lang='de'))
            self.assertDictEqual(rv.get_json(), content.test_content)
            rv = self.app.get(url_for(
                'api.content',
                download=True,
                lang='en'))
            self.assertDictEqual(rv.get_json(), content.test_content_download)

            # geometric_entities/
            rv = self.app.get(url_for('api.geometric_entities'))
            self.assertDictEqual(
                rv.get_json(),
                GeometricEntity.get_test_geometric_entity(params))
            rv = self.app.get(url_for(
                'api.geometric_entities',
                count=True))
            assert b'1' in rv.data
            rv = self.app.get(url_for(
                'api.geometric_entities',
                download=True))
            self.assertDictEqual(
                rv.get_json(),
                GeometricEntity.get_test_geometric_entity(params))

            # system_class_count/
            rv = self.app.get(url_for('api.system_class_count'))
            self.assertDictEqual(
                rv.get_json(),
                system_class_count.test_system_class_count)

            # overview_count/
            rv = self.app.get(url_for('api.overview_count'))
            self.assertCountEqual(
                rv.get_json(),
                overview_count.test_overview_count)

            # ---Node Endpoints---

            # node_entities/
            rv = self.app.get(url_for(
                'api.node_entities',
                id_=unit_node.id))
            self.assertDictEqual(
                rv.get_json(),
                NodeEntities.get_test_node_entities(params))

            # node_entities_all/
            rv = self.app.get(url_for(
                'api.node_entities_all',
                id_=unit_node.id))
            self.assertDictEqual(
                rv.get_json(),
                NodeEntities.get_test_node_entities_all(params))

            # node_overview/
            # Todo: Alex remade the Nodes, I have no idea how they look now
            #  places is None and I don't know why!
            rv = self.app.get(url_for('api.node_overview'))
            self.assertDictEqual(
                rv.get_json(),
                NodeOverview.get_test_node_overview(params))
            rv = self.app.get(url_for(
                'api.node_overview',
                download=True))
            self.assertDictEqual(
                rv.get_json(),
                NodeOverview.get_test_node_overview(params))

            # type_tree/
            rv = self.app.get(url_for('api.type_tree'))
            self.assertDictEqual(
                rv.get_json(),
                TypeTree.get_test_type_tree(params))
            rv = self.app.get(url_for(
                'api.type_tree',
                download=True))
            self.assertDictEqual(
                rv.get_json(),
                TypeTree.get_test_type_tree(params))

            # subunit/
            rv = self.app.get(url_for(
                'api.subunit',
                id_=place.id))
            self.assertDictEqual(
                rv.get_json(),
                Subunits.get_test_subunit(params))

            # subunit_hierarchy/
            rv = self.app.get(url_for(
                'api.subunit_hierarchy',
                id_=place.id))
            self.assertDictEqual(
                rv.get_json(),
                Subunits.get_test_subunit_hierarchy(params))

            # node_entities/ with parameters
            rv = self.app.get(url_for(
                'api.node_entities',
                id_=unit_node.id,
                count=True))
            assert b'6' in rv.data
            rv = self.app.get(url_for(
                'api.node_entities',
                id_=unit_node.id,
                download=True))
            self.assertDictEqual(
                rv.get_json(),
                NodeEntities.get_test_node_entities(params))

            # search parameter
            rv = self.app.get(url_for(
                'api.query',
                entities=place.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                format='lp',
                search=f'{{"typeID":[{{"operator":"equal",'
                       f'"values":[{params["boundary_mark_id"]},{params["height_id"]}],'
                       f'"logicalOperator":"or"}}]}}'))
            self.assertDictEqual(
                rv.get_json(),
                Search.get_test_search_1(params))
            rv = self.app.get(url_for(
                'api.query',
                system_classes='place',
                search=f'{{"entityName":[{{"operator":"notEqual",'
                       f'"values":["Mordor"],'
                       f'"logicalOperator":"or"}}]}}'))
            self.assertDictEqual(
                rv.get_json(),
                Search.get_test_search_2(params))
            rv = self.app.get(url_for(
                'api.query',
                entities=place.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                format='lp',
                search=f'{{"typeName":[{{"operator":"equal",'
                       f'"values":["Place", "Height"],'
                       f'"logicalOperator":"and"}}]}}'))
            self.assertDictEqual(
                rv.get_json(),
                Search.get_test_search_2(params))
            rv = self.app.get(url_for(
                'api.query',
                entities=place.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                format='lp',
                search=f'{{"typeName":[{{"operator":"notEqual",'
                       f'"values":["Place", "Height"],'
                       f'"logicalOperator":"and"}}]}}'))
            self.assertDictEqual(
                rv.get_json(),
                Search.get_test_search_3(params))
            rv = self.app.get(url_for(
                'api.query',
                entities=place.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                format='lp',
                search=f'{{"entityID":[{{"operator":"notEqual",'
                       f'"values":[{place.id}],'
                       f'"logicalOperator":"and"}}]}}'))
            self.assertDictEqual(
                rv.get_json(),
                Search.get_test_search_3(params))
            rv = self.app.get(url_for(
                'api.query',
                entities=place.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                format='lp',
                search=f'{{"entityAliases":[{{"operator":"notEqual",'
                       f'"values":["Sûza"],'
                       f'"logicalOperator":"and"}}]}}'))
            self.assertDictEqual(
                rv.get_json(),
                Search.get_test_search_3(params))
            rv = self.app.get(url_for(
                'api.query',
                entities=place.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                format='lp',
                search=f'{{"entityCidocClass":[{{"operator":"equal",'
                       f'"values":["E21"],'
                       f'"logicalOperator":"and"}}]}}'))
            self.assertDictEqual(
                rv.get_json(),
                Search.get_test_search_4(params))
            rv = self.app.get(url_for(
                'api.query',
                entities=place.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                format='lp',
                search=f'{{"entitySystemClass":[{{"operator":"equal",'
                       f'"values":["person"],'
                       f'"logicalOperator":"and"}}]}}'))
            self.assertDictEqual(
                rv.get_json(),
                Search.get_test_search_4(params))

            with self.assertRaises(EntityDoesNotExistError):
                self.app.get(url_for(
                    'api.class',
                    class_code='E18',
                    last=1231))
            with self.assertRaises(TypeIDError):
                self.app.get(url_for(
                    'api.query',
                    system_classes='person',
                    type_id=Node.get_nodes('Place')[0]))
            with self.assertRaises(NoEntityAvailable):
                self.app.get(url_for(
                    'api.query',
                    entities=12345))
            with self.assertRaises(NoEntityAvailable):
                self.app.get(url_for(
                    'api.class',
                    class_code='E68',
                    last=1231))
            with self.assertRaises(InvalidSystemClassError):
                self.app.get(url_for(
                    'api.system_class',
                    system_class='Wrong'))
            with self.assertRaises(QueryEmptyError):
                self.app.get(url_for('api.query'))
            with self.assertRaises(InvalidSubunitError):
                self.app.get(url_for(
                    'api.node_entities',
                    id_=1234))
            with self.assertRaises(InvalidSubunitError):
                self.app.get(url_for(
                    'api.node_entities_all',
                    id_=1234))
            with self.assertRaises(InvalidSubunitError):
                self.app.get(url_for(
                    'api.type_entities',
                    id_=1234))
            with self.assertRaises(InvalidSubunitError):
                self.app.get(url_for(
                    'api.type_entities_all',
                    id_=1234))
            with self.assertRaises(InvalidCidocClassCode):
                self.app.get(url_for(
                    'api.class',
                    class_code='e99999999'))
            with self.assertRaises(InvalidCodeError):
                self.app.get(url_for(
                    'api.code',
                    code='Invalid'))
            with self.assertRaises(InvalidLimitError):
                self.app.get(url_for(
                    'api.latest',
                    latest='99999999'))
            with self.assertRaises(EntityDoesNotExistError):
                self.app.get(url_for(
                    'api.subunit',
                    id_='99999999'))
            with self.assertRaises(InvalidSubunitError):
                self.app.get(url_for(
                    'api.subunit',
                    id_=actor.id))
            with self.assertRaises(EntityDoesNotExistError):
                self.app.get(url_for(
                    'api.subunit_hierarchy',
                    id_='2342352525'))
            with self.assertRaises(InvalidSubunitError):
                self.app.get(url_for(
                    'api.subunit_hierarchy',
                    id_=actor.id))
            with self.assertRaises(NoEntityAvailable):
                self.app.get(url_for(
                    'api.code',
                    entities=place.id,
                    code='place',
                    search=f'{{"typeName":[{{"operator":"equal",'
                           f'"values":["Place", "Height", "Dimension"],'
                           f'"logicalOperator":"and"}}]}}'))
            with self.assertRaises(FilterOperatorError):
                self.app.get(url_for(
                    'api.code',
                    entities=place.id,
                    code='place',
                    search=f'{{"typeName":[{{"operator":"notEqualT",'
                           f'"values":["Place", "Height"],'
                           f'"logicalOperator":"and"}}]}}'))
            with self.assertRaises(FilterLogicalOperatorError):
                self.app.get(url_for(
                    'api.code',
                    entities=place.id,
                    code='place',
                    search=f'{{"typeName":[{{"operator":"notEqual",'
                           f'"values":["Place", "Height"],'
                           f'"logicalOperator":"xor"}}]}}'))
            with self.assertRaises(FilterColumnError):
                self.app.get(url_for(
                    'api.code',
                    entities=place.id,
                    code='place',
                    search=f'{{"All":[{{"operator":"notEqual",'
                           f'"values":["Place", "Height"],'
                           f'"logicalOperator":"or"}}]}}'))
            with self.assertRaises(NoSearchStringError):
                self.app.get(url_for(
                    'api.code',
                    entities=place.id,
                    code='place',
                    search=f'{{"typeName":[{{"operator":"notEqual",'
                           f'"values":[],'
                           f'"logicalOperator":"or"}}]}}'))
