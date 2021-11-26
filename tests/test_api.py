from typing import Any, Dict, List

from flask import g, url_for

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.node import Node
from openatlas.models.reference_system import ReferenceSystem
from tests.base import TestBaseCase, insert_entity


class ApiTests(TestBaseCase):

    def test_api(self) -> None:

        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                params = {f'{(node.name.lower()).replace(" ", "_")}_id': id_ for
                          (id_, node) in Node.get_all_nodes().items()}
                params['geonames_id'] = ReferenceSystem.get_by_name(
                    'GeoNames').id

                # Creation of Shire (place)
                place = insert_entity(
                    'Shire', 'place',
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

            # ---Content Endpoints---
            # ClassMapping
            for rv in [
                self.app.get(url_for('api_02.class_mapping')).get_json(),
                self.app.get(url_for('api_03.class_mapping')).get_json()]:
                assert ApiTests.get_class_mapping(rv)

            # Content
            for rv in [
                self.app.get(
                    url_for('api_02.content', lang='de',
                            download=True)).get_json(),
                self.app.get(url_for('api_03.content', lang='de',
                                     download=True)).get_json()]:
                assert True if rv['intro'] == 'Das ist Deutsch' else False
            for rv in [
                self.app.get(
                    url_for('api_02.content')).get_json(),
                self.app.get(url_for('api_03.content')).get_json()]:
                assert True if rv['intro'] == 'This is English' else False

            # geometric_entities/
            for rv in [
                self.app.get(url_for('api_02.geometric_entities')).get_json(),
                self.app.get(url_for('api_03.geometric_entities')).get_json()]:
                assert True if rv['features'][0]['geometry'][
                    'coordinates'] else None
                assert ApiTests.get_geom_properties(rv, 'id')
                assert ApiTests.get_geom_properties(rv, 'objectDescription')
                assert ApiTests.get_geom_properties(rv, 'objectId')
                assert ApiTests.get_geom_properties(rv, 'objectName')
                assert ApiTests.get_geom_properties(rv, 'shapeType')

            # system_class_count/
            for rv in [
                self.app.get(url_for('api_02.system_class_count')).get_json(),
                self.app.get(url_for('api_03.system_class_count')).get_json()]:
                assert True if rv['person'] else False

            # overview_count/
            rv = self.app.get(url_for('api_02.overview_count')).get_json()
            assert True if rv[0]['systemClass'] else False

            # ---Entity Endpoints---
            # /entity
            for rv in [
                self.app.get(url_for('api_02.entity', id_=place.id)).get_json(),
                self.app.get(url_for('api_02.entity', id_=place.id,
                                     download=True)).get_json(),
                self.app.get(
                    url_for('api_03.entity', id_=place.id)).get_json(),
                self.app.get(
                    url_for('api_03.entity', id_=place.id,
                            download=True)).get_json()]:
                rv = rv['features'][0]
                assert ApiTests.get_bool(
                    rv,
                    '@id')
                assert ApiTests.get_bool(
                    rv,
                    'type')
                assert ApiTests.get_bool(
                    rv,
                    'crmClass')
                assert ApiTests.get_bool(
                    rv,
                    'systemClass')
                assert ApiTests.get_bool(
                    rv['properties'],
                    'title')
                assert ApiTests.get_bool(
                    rv['description'][0],
                    'value')
                assert ApiTests.get_bool(
                    rv['when']['timespans'][0]['start'],
                    'earliest')
                assert ApiTests.get_bool(
                    rv['when']['timespans'][0]['start'],
                    'latest')
                assert ApiTests.get_bool(
                    rv['when']['timespans'][0]['end'],
                    'earliest')
                assert ApiTests.get_bool(
                    rv['when']['timespans'][0]['end'],
                    'latest')
                assert ApiTests.get_bool(
                    rv['types'][0],
                    'identifier')
                assert ApiTests.get_bool(
                    rv['types'][0],
                    'label')
                assert ApiTests.get_bool(
                    rv['relations'][0],
                    'label')
                assert ApiTests.get_bool(
                    rv['relations'][0],
                    'relationTo')
                assert ApiTests.get_bool(
                    rv['relations'][0],
                    'relationType')
                assert ApiTests.get_bool(
                    rv['relations'][0],
                    'relationSystemClass')
                assert ApiTests.get_bool(
                    rv['names'][0],
                    'alias')
                assert ApiTests.get_bool(
                    rv['links'][0],
                    'type')
                assert ApiTests.get_bool(
                    rv['links'][0],
                    'identifier')
                assert ApiTests.get_bool(
                    rv['links'][0],
                    'referenceSystem')
                assert ApiTests.get_bool(
                    rv['geometry'],
                    'type')
                assert ApiTests.get_bool(
                    rv['geometry'],
                    'coordinates')
                assert ApiTests.get_bool(
                    rv['depictions'][0],
                    '@id')
                assert ApiTests.get_bool(
                    rv['depictions'][0],
                    'title')
                assert ApiTests.get_bool(
                    rv['depictions'][0],
                    'license')
                assert ApiTests.get_bool(
                    rv['depictions'][0],
                    'url')

            for rv in [
                self.app.get(url_for('api_02.entity', id_=place.id,
                                     format='geojson')).get_json(),
                self.app.get(url_for('api_03.entity', id_=place.id,
                                     format='geojson')).get_json()]:
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

            for rv in [
                self.app.get(
                    url_for('api_02.entity', id_=place.id, export='csv')),
                self.app.get(
                    url_for('api_03.entity', id_=place.id, export='csv')),
                self.app.get(
                    url_for('api_02.code', code='place', export='csv')),
                self.app.get(
                    url_for('api_03.code', code='place', export='csv'))]:
                assert b'Shire' in rv.data

            #
            for rv in [
                self.app.get(url_for('api_02.class', class_code='E21')),
                self.app.get(url_for('api_02.code', code='place')),
                self.app.get(url_for('api_02.latest', latest=2)),
                self.app.get(
                    url_for('api_02.system_class', system_class='artifact')),
                self.app.get(
                    url_for('api_02.entities_linked_to_entity', id_=event.id)),
                self.app.get(
                    url_for(
                        'api_02.query',
                        entities=location.id,
                        classes='E18',
                        codes='artifact',
                        system_classes='person'))]:
                rv = rv.get_json()
                rv_results = rv['results'][0]['features'][0]
                rv_page = rv['pagination']
                assert ApiTests.get_bool(rv_results, '@id')
                assert ApiTests.get_bool(rv_page, 'entities')
                assert ApiTests.get_bool(rv_page, 'entitiesPerPage')
                assert ApiTests.get_bool(rv_page, 'index')
                assert ApiTests.get_bool(rv_page, 'totalPages')

            # Test show=none
            for rv in [
                self.app.get(url_for('api_02.class', class_code='E21',
                                     show='none')).get_json()]:
                rv = rv['results'][0]['features'][0]
                assert ApiTests.get_bool_inverse(rv, 'geometry')
                assert ApiTests.get_no_key(rv, 'depictions')
                assert ApiTests.get_no_key(rv, 'links')
                assert ApiTests.get_no_key(rv, 'types')

    @staticmethod
    def get_bool(data: Dict[str, Any], key: str) -> bool:
        return True if data[key] else False

    @staticmethod
    def get_bool_inverse(data: Dict[str, Any], key: str) -> bool:
        return True if not data[key] else False

    @staticmethod
    def get_no_key(data: Dict[str, Any], key: str) -> bool:
        return True if key not in data.keys() else False

    @staticmethod
    def get_geom_properties(geom: Dict[str, Any], key: str) -> bool:
        return True if geom['features'][0]['properties'][key] else False

    @staticmethod
    def get_class_mapping(data: List[Dict[str, Any]]) -> bool:
        return True if data[0]["systemClass"] and \
                       data[0]["crmClass"] and \
                       data[0]['view'] and \
                       data[0]['icon'] and \
                       data[0]['en'] else False


        #
        # # /type_entities
        # rv = self.app.get(url_for(
        #     'api_02.type_entities',
        #     id_=Node.get_hierarchy('Place').id))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     TypeEntities.get_test_type_entities(params))
        # rv = self.app.get(url_for(
        #     'api_02.type_entities',
        #     id_=relation_sub_id))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     CidocClass.get_test_cidoc_class(params))
        #
        # # /type_entities_all
        # rv = self.app.get(url_for(
        #     'api_02.type_entities_all',
        #     id_=relation_sub_id))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     CidocClass.get_test_cidoc_class(params))
        # rv = self.app.get(url_for(
        #     'api_02.type_entities_all',
        #     id_=unit_node.id))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     TypeEntities.get_test_type_entities_all_special(params))
        #
        # # /query
        # rv = self.app.get(url_for(
        #     'api_02.query',
        #     entities=location.id,
        #     classes='E18',
        #     codes='artifact',
        #     system_classes='person'))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     Query.get_test_query(params))
        #
        # # /query with different parameter
        # rv = self.app.get(url_for(
        #     'api_02.query',
        #     entities=location.id,
        #     classes='E18',
        #     codes='artifact',
        #     system_classes='person',
        #     type_id=Node.get_nodes('Place')[0]))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     Query.get_test_query_type(params))
        # rv = self.app.get(url_for(
        #     'api_02.query',
        #     entities=location.id,
        #     classes='E18',
        #     codes='artifact',
        #     system_classes='person',
        #     limit=1,
        #     first=actor2.id))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     Query.get_test_query_first(params))
        # rv = self.app.get(url_for(
        #     'api_02.query',
        #     entities=location.id,
        #     classes='E18',
        #     codes='artifact',
        #     system_classes='person',
        #     limit=1,
        #     last=actor2.id))
        # self.assertDictEqual \
        #     (rv.get_json(),
        #      Query.get_test_query_last(params))
        # rv = self.app.get(url_for(
        #     'api_02.query',
        #     entities=location.id,
        #     classes='E18',
        #     codes='artifact',
        #     system_classes='person',
        #     download=True))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     Query.get_test_query(params))
        # rv = self.app.get(url_for(
        #     'api_02.query',
        #     entities=location.id,
        #     classes='E18',
        #     codes='artifact',
        #     system_classes='person',
        #     count=True))
        # assert b'8' in rv.data
        # rv = self.app.get(url_for(
        #     'api_02.query',
        #     entities=location.id,
        #     classes='E18',
        #     codes='artifact',
        #     system_classes='person',
        #     format='xml'))
        # assert b'Shire' in rv.data
        # rv = self.app.get(url_for(
        #     'api_02.query',
        #     entities=location.id,
        #     classes='E18',
        #     codes='artifact',
        #     system_classes='person',
        #     export='csv'))
        # assert b'Shire' in rv.data
        # rv = self.app.get(url_for(
        #     'api_02.query',
        #     entities=location.id,
        #     classes='E18',
        #     codes='artifact',
        #     system_classes='person',
        #     format='geojson'))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     Query.get_test_query_geojson(params))
        # rv = self.app.get(url_for(
        #     'api_02.query',
        #     entities=location.id,
        #     classes='E18',
        #     codes='artifact',
        #     system_classes='person',
        #     filter='and|name|like|Shire',
        #     sort='desc',
        #     column='id'))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     Query.get_test_query_filter(params))
        # rv = self.app.get(url_for(
        #     'api_02.query',
        #     entities=location.id,
        #     classes='E18',
        #     codes='artifact',
        #     system_classes='person',
        #     filter='or|begin_from|ge|2018-1-1',
        #     sort='desc',
        #     column='id'))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     Query.get_test_query_filter_date(params))
        # rv = self.app.get(url_for(
        #     'api_02.query',
        #     entities=location.id,
        #     classes='E18',
        #     codes='artifact',
        #     system_classes='person',
        #     filter='and|id|gt|100'))
        # self.assertDictEqual(rv.get_json(), Query.get_test_query(params))
        #
        # # ---Content Endpoints---
        #
        # # /classes
        # rv = self.app.get(url_for('api_02.class_mapping'))
        # assert b'systemClass' in rv.data
        #
        # # content/
        # rv = self.app.get(url_for(
        #     'api_02.content',
        #     lang='de'))
        # self.assertDictEqual(rv.get_json(), content.test_content)
        # rv = self.app.get(url_for(
        #     'api_02.content',
        #     download=True,
        #     lang='en'))
        # self.assertDictEqual(rv.get_json(), content.test_content_download)
        #
        # # geometric_entities/
        # rv = self.app.get(url_for('api_02.geometric_entities'))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     GeometricEntity.get_test_geometric_entity(params))
        # rv = self.app.get(url_for(
        #     'api_02.geometric_entities',
        #     count=True))
        # assert b'1' in rv.data
        # rv = self.app.get(url_for(
        #     'api_02.geometric_entities',
        #     download=True))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     GeometricEntity.get_test_geometric_entity(params))
        #
        # # system_class_count/
        # rv = self.app.get(url_for('api_02.system_class_count'))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     system_class_count.test_system_class_count)
        #
        # # overview_count/
        # rv = self.app.get(url_for('api_02.overview_count'))
        # self.assertCountEqual(
        #     rv.get_json(),
        #     overview_count.test_overview_count)
        #
        # # ---Node Endpoints---
        #
        # # node_entities/
        # rv = self.app.get(url_for(
        #     'api_02.node_entities',
        #     id_=unit_node.id))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     NodeEntities.get_test_node_entities(params))
        #
        # # node_entities_all/
        # rv = self.app.get(url_for(
        #     'api_02.node_entities_all',
        #     id_=unit_node.id))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     NodeEntities.get_test_node_entities_all(params))
        #
        # # node_overview/
        # rv = self.app.get(url_for('api_02.node_overview'))
        # # self.assertAlmostEqual(
        # #    rv.get_json(),
        # #    NodeOverview.get_test_node_overview(params))
        # rv = self.app.get(url_for(
        #     'api_02.node_overview',
        #     download=True))
        # # self.assertAlmostEqual(
        # #    rv.get_json(),
        # #    NodeOverview.get_test_node_overview(params))
        # NodeOverview.get_test_node_overview(params)  # for coverage
        #
        # # type_tree/
        # rv = self.app.get(url_for('api_02.type_tree'))
        # # self.assertDictEqual(
        # #    rv.get_json(),
        # #    TypeTree.get_test_type_tree(params))
        # rv = self.app.get(url_for(
        #     'api_02.type_tree',
        #     download=True))
        # # self.assertDictEqual(
        # #    rv.get_json(),
        # #    TypeTree.get_test_type_tree(params))
        # TypeTree.get_test_type_tree(params)  # for coverage
        #
        # # subunit/
        # rv = self.app.get(url_for(
        #     'api_02.subunit',
        #     id_=place.id))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     Subunits.get_test_subunit(params))
        #
        # # subunit_hierarchy/
        # rv = self.app.get(url_for(
        #     'api_02.subunit_hierarchy',
        #     id_=place.id))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     Subunits.get_test_subunit_hierarchy(params))
        #
        # # node_entities/ with parameters
        # rv = self.app.get(url_for(
        #     'api_02.node_entities',
        #     id_=unit_node.id,
        #     count=True))
        # assert b'6' in rv.data
        # rv = self.app.get(url_for(
        #     'api_02.node_entities',
        #     id_=unit_node.id,
        #     download=True))
        # self.assertDictEqual(
        #     rv.get_json(),
        #     NodeEntities.get_test_node_entities(params))

        # with self.assertRaises(EntityDoesNotExistError):
        #     self.app.get(url_for(
        #         'api_02.class',
        #         class_code='E18',
        #         last=12312884))
        # with self.assertRaises(TypeIDError):
        #     self.app.get(url_for(
        #         'api_02.query',
        #         system_classes='person',
        #         type_id=Node.get_nodes('Place')[0]))
        # with self.assertRaises(NoEntityAvailable):
        #     self.app.get(url_for(
        #         'api_02.query',
        #         entities=12345))
        # with self.assertRaises(NoEntityAvailable):
        #     self.app.get(url_for(
        #         'api_02.class',
        #         class_code='E68',
        #         last=1231))
        # with self.assertRaises(InvalidSystemClassError):
        #     self.app.get(url_for(
        #         'api_02.system_class',
        #         system_class='Wrong'))
        # with self.assertRaises(QueryEmptyError):
        #     self.app.get(url_for('api_02.query'))
        # with self.assertRaises(InvalidSubunitError):
        #     self.app.get(url_for(
        #         'api_02.node_entities',
        #         id_=1234))
        # with self.assertRaises(InvalidSubunitError):
        #     self.app.get(url_for(
        #         'api_02.node_entities_all',
        #         id_=1234))
        # with self.assertRaises(InvalidSubunitError):
        #     self.app.get(url_for(
        #         'api_02.type_entities',
        #         id_=1234))
        # with self.assertRaises(InvalidSubunitError):
        #     self.app.get(url_for(
        #         'api_02.type_entities_all',
        #         id_=1234))
        # with self.assertRaises(InvalidCidocClassCode):
        #     self.app.get(url_for(
        #         'api_02.class',
        #         class_code='e99999999'))
        # with self.assertRaises(InvalidCodeError):
        #     self.app.get(url_for(
        #         'api_02.code',
        #         code='Invalid'))
        # with self.assertRaises(InvalidLimitError):
        #     self.app.get(url_for(
        #         'api_02.latest',
        #         latest='99999999'))
        # with self.assertRaises(EntityDoesNotExistError):
        #     self.app.get(url_for(
        #         'api_02.subunit',
        #         id_='99999999'))
        # with self.assertRaises(InvalidSubunitError):
        #     self.app.get(url_for(
        #         'api_02.subunit',
        #         id_=actor.id))
        # with self.assertRaises(EntityDoesNotExistError):
        #     self.app.get(url_for(
        #         'api_02.subunit_hierarchy',
        #         id_='2342352525'))
        # with self.assertRaises(InvalidSubunitError):
        #     self.app.get(url_for(
        #         'api_02.subunit_hierarchy',
        #         id_=actor.id))
        # with self.assertRaises(FilterLogicalOperatorError):
        #     self.app.get(url_for(
        #         'api_02.code',
        #         code='place',
        #         filter='Wrong|name|like|Nostromos'))
        # with self.assertRaises(FilterColumnError):
        #     self.app.get(url_for(
        #         'api_02.code',
        #         code='place',
        #         filter='or|Wrong|like|Nostromos'))
        # with self.assertRaises(FilterOperatorError):
        #     self.app.get(url_for(
        #         'api_02.code',
        #         code='place',
        #         filter='or|name|Wrong|Nostromos'))
        # with self.assertRaises(FilterOperatorError):
        #     self.app.get(url_for(
        #         'api_02.code',
        #         code='place',
        #         filter='or|name|Wrong|'))
        # with self.assertRaises(NoSearchStringError):
        #     self.app.get(url_for(
        #         'api_02.code',
        #         code='place',
        #         filter='or|name|like|'))
        # with self.assertRaises(InvalidSearchDateError):
        #     self.app.get(url_for(
        #         'api_02.system_class',
        #         system_class='place',
        #         filter='or|begin_from|like|19970-18-09'))
        # with self.assertRaises(InvalidSearchNumberError):
        #     self.app.get(url_for(
        #         'api_02.code',
        #         code='place',
        #         filter='or|id|eq|25.5'))
