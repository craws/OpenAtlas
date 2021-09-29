from flask import g, url_for

from openatlas import app
from openatlas.api.v02.endpoints.content.class_mapping import ClassMapping
from openatlas.api.v02.resources.error import (
    EntityDoesNotExistError, FilterOperatorError, InvalidCidocClassCode,
    InvalidCodeError, InvalidLimitError, InvalidSearchDateError,
    InvalidSearchNumberError, InvalidSubunitError, QueryEmptyError,
    FilterLogicalOperatorError, FilterColumnError,
    InvalidSystemClassError, NoEntityAvailable, TypeIDError,
    NoSearchStringError)
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.node import Node
from openatlas.models.reference_system import ReferenceSystem
from tests.api_test_data import entity, cidoc_class, code, \
    entities_linked_to_entity, latest, system_class, type_entities, query, \
    content, geometric_entities, system_class_count, node_entities, \
    subunit, overview_count
from tests.base import TestBaseCase, insert_entity


class ApiTests(TestBaseCase):

    def test_api(self) -> None:
        with app.app_context():  # type: ignore
            with app.test_request_context():
                app.preprocess_request()  # type: ignore

                # Creation of Shire (place)
                place = insert_entity(
                    'Shire', 'place',
                    description='The Shire was the homeland of the hobbits.')
                if not place:  # Needed for Mypy
                    return  # pragma: no cover

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
                place.link('P2', Node.get_hierarchy('Place'))

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

                # Adding stratigraphic to place
                insert_entity('Kitchen', 'stratigraphic_unit', feature)

                # Adding Administrative Unit Node
                unit_node = Node.get_hierarchy('Administrative unit')

                # Adding File to place
                file = insert_entity('Picture with a License', 'file')
                file.link('P67', place)
                file.link('P2', g.nodes[Node.get_hierarchy('License').subs[0]])

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

                alias2 = insert_entity('The ring bearer', 'appellation')
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
                actor2.link('P74', place)

                # Adding actor relation
                relation_id = Node.get_hierarchy('Actor actor relation').id
                relation_sub_id = g.nodes[relation_id].subs[0]
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
                place2.link('P2', Entity.get_by_id(Node.get_nodes('Place')[0]))

                # Creation of Silmarillion (source)
                insert_entity('Silmarillion', 'source')

            self.maxDiff = None

            # ---Entity Endpoints---
            # /entity
            rv = self.app.get(url_for(
                'api.entity',
                id_=place.id))
            self.assertDictEqual(rv.get_json(), entity.test_lpf)
            rv = self.app.get(url_for(
                'api.entity',
                id_=place.id,
                export='csv'))
            assert b'Shire' in rv.data
            rv = self.app.get(url_for(
                'api.entity',
                id_=place.id,
                download=True))
            self.assertDictEqual(rv.get_json(), entity.test_lpf)
            rv = self.app.get(url_for(
                'api.entity',
                id_=place.id,
                format='xml'))
            assert b'Shire' in rv.data
            rv = self.app.get(url_for(
                'api.entity',
                id_=place.id,
                format='geojson'))
            self.assertDictEqual(rv.get_json(), entity.test_geojson)

            # /class
            rv = self.app.get(url_for(
                'api.class',
                class_code='E21'))
            self.assertDictEqual(rv.get_json(), cidoc_class.test_cidoc_class)
            rv = self.app.get(url_for(
                'api.class',
                class_code='E21',
                show='none'))
            self.assertDictEqual(
                rv.get_json(),
                cidoc_class.test_cidoc_class_show_none)

            # /code
            rv = self.app.get(url_for(
                'api.code',
                code='place'))
            # self.assertDictEqual(rv.get_json(), code.test_code)

            # /entities_linked_to_entity
            rv = self.app.get(url_for(
                'api.entities_linked_to_entity',
                id_=event.id))
            self.assertDictEqual(
                rv.get_json(),
                entities_linked_to_entity.test_entities_linked_to)

            # /latest
            rv = self.app.get(url_for(
                'api.latest',
                latest=2))
            self.assertDictEqual(rv.get_json(), latest.test_latest)

            # /system_class
            rv = self.app.get(url_for(
                'api.system_class',
                system_class='artifact'))
            self.assertDictEqual(rv.get_json(), system_class.test_system_class)

            # /type_entities
            rv = self.app.get(url_for(
                'api.type_entities',
                id_=Node.get_hierarchy('Place').id))
            # self.assertDictEqual(
            #    rv.get_json(),
            #    type_entities.test_type_entities)
            rv = self.app.get(url_for(
                'api.type_entities',
                id_=relation_sub_id))
            self.assertDictEqual(
                rv.get_json(),
                cidoc_class.test_cidoc_class)

            # /type_entities_all
            rv = self.app.get(url_for(
                'api.type_entities_all',
                id_=relation_sub_id))
            self.assertDictEqual(rv.get_json(), cidoc_class.test_cidoc_class)
            rv = self.app.get(url_for(
                'api.type_entities_all',
                id_=unit_node.id))
            # self.assertDictEqual(
            #    rv.get_json(),
            #    type_entities.test_type_entities_all_special)

            # /query
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person'))
            # self.assertDictEqual(rv.get_json(), query.test_query)

            # /query with different parameter
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                type_id=Node.get_nodes('Place')[0]))
            # self.assertDictEqual(rv.get_json(), query.test_query_type)
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                limit=1,
                first=actor2.id))
            # self.assertDictEqual(rv.get_json(), query.test_query_first)
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                limit=1,
                last=actor2.id))
            # self.assertDictEqual(rv.get_json(), query.test_query_last)
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                download=True))
            # self.assertDictEqual(rv.get_json(), query.test_query)
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
            self.assertDictEqual(rv.get_json(), query.test_query_geojson)
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                filter='and|name|like|Shire',
                sort='desc',
                column='id'))
            # self.assertDictEqual(rv.get_json(), query.test_query_filter)
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                filter='or|begin_from|ge|2018-1-1',
                sort='desc',
                column='id'))
            # self.assertDictEqual(rv.get_json(), query.test_query_filter_date)
            rv = self.app.get(url_for(
                'api.query',
                entities=location.id,
                classes='E18',
                codes='artifact',
                system_classes='person',
                filter='and|id|gt|100'))
            # self.assertDictEqual(rv.get_json(), query.test_query)

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
                geometric_entities.test_geometric_entity)
            rv = self.app.get(url_for(
                'api.geometric_entities',
                count=True))
            assert b'1' in rv.data
            rv = self.app.get(url_for(
                'api.geometric_entities',
                download=True))
            self.assertDictEqual(
                rv.get_json(),
                geometric_entities.test_geometric_entity)

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
            # self.assertDictEqual(
            #    rv.get_json(),
            #    node_entities.test_node_entities)

            # node_entities_all/
            rv = self.app.get(url_for(
                'api.node_entities_all',
                id_=unit_node.id))
            # self.assertDictEqual(
            #    rv.get_json(),
            #    node_entities.test_node_entities_all)

            # node_overview/
            rv = self.app.get(url_for('api.node_overview'))
            assert b'Actor actor relation' in rv.data
            # self.assertDictEqual(
            #    rv.get_json(),
            #    node_overview.test_node_overview)
            rv = self.app.get(url_for(
                'api.node_overview',
                download=True))
            # self.assertDictEqual(
            #    rv.get_json(),
            #    node_overview.test_node_overview)
            assert b'Actor actor relation' in rv.data

            # type_tree/
            rv = self.app.get(url_for('api.type_tree'))
            # self.assertDictEqual(rv.get_json(), type_tree.test_type_tree)
            assert b'Source' in rv.data
            rv = self.app.get(url_for(
                'api.type_tree',
                download=True))
            assert b'Source' in rv.data
            # self.assertDictEqual(rv.get_json(), type_tree.test_type_tree)

            # subunit/
            rv = self.app.get(url_for(
                'api.subunit',
                id_=place.id))
            self.assertDictEqual(rv.get_json(), subunit.test_subunit)

            # subunit_hierarchy/
            rv = self.app.get(url_for(
                'api.subunit_hierarchy',
                id_=place.id))
            self.assertDictEqual(rv.get_json(), subunit.test_subunit_hierarchy)

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
            # self.assertDictEqual(
            #    rv.get_json(),
            #    node_entities.test_node_entities)

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
            with self.assertRaises(FilterLogicalOperatorError):
                self.app.get(url_for(
                    'api.code',
                    code='place',
                    filter='Wrong|name|like|Nostromos'))
            with self.assertRaises(FilterColumnError):
                self.app.get(url_for(
                    'api.code',
                    code='place',
                    filter='or|Wrong|like|Nostromos'))
            with self.assertRaises(FilterOperatorError):
                self.app.get(url_for(
                    'api.code',
                    code='place',
                    filter='or|name|Wrong|Nostromos'))
            with self.assertRaises(FilterOperatorError):
                self.app.get(url_for(
                    'api.code',
                    code='place',
                    filter='or|name|Wrong|'))
            with self.assertRaises(NoSearchStringError):
                self.app.get(url_for(
                    'api.code',
                    code='place',
                    filter='or|name|like|'))
            with self.assertRaises(InvalidSearchDateError):
                self.app.get(url_for(
                    'api.system_class',
                    system_class='place',
                    filter='or|begin_from|like|19970-18-09'))
            with self.assertRaises(InvalidSearchNumberError):
                self.app.get(url_for(
                    'api.code',
                    code='place',
                    filter='or|id|eq|25.5'))
