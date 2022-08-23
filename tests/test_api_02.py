from datetime import datetime

from flask import g, url_for

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type
from tests.base import (
    TestBaseCase, get_bool, get_bool_inverse, get_class_mapping,
    get_geom_properties, get_no_key, insert_entity)


class Api02(TestBaseCase):

    def test_api_02(self) -> None:

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
            for rv in [
                self.app.get(url_for('api_02.entity', id_=place.id)),
                self.app.get(
                    url_for('api_02.entity', id_=place.id, download=True))]:
                rv = rv.get_json()
                rv = rv['features'][0]
                assert get_bool(
                    rv,
                    '@id')
                assert get_bool(
                    rv,
                    'type',
                    'Feature')
                assert get_bool(
                    rv,
                    'crmClass',
                    'crm:E18 Physical Thing')
                assert get_bool(
                    rv,
                    'systemClass',
                    'place')
                assert get_bool(
                    rv['properties'],
                    'title')
                assert get_bool(
                    rv['description'][0],
                    'value',
                    'The Shire was the homeland of the hobbits.')
                assert get_bool(
                    rv['when']['timespans'][0]['start'],
                    'earliest',
                    '2018-01-31T00:00:00')
                assert get_bool(
                    rv['when']['timespans'][0]['start'],
                    'latest',
                    '2018-03-01T00:00:00')
                assert get_bool(
                    rv['when']['timespans'][0]['end'],
                    'earliest',
                    '2019-01-31T00:00:00')
                assert get_bool(
                    rv['when']['timespans'][0]['end'],
                    'latest',
                    '2019-03-01T00:00:00')
                assert get_bool(
                    rv['types'][0],
                    'identifier')
                assert get_bool(
                    rv['types'][0],
                    'label',
                    'Boundary Mark')
                assert get_bool(
                    rv['relations'][1],
                    'label',
                    'Height')
                assert get_bool(
                    rv['relations'][0],
                    'relationTo')
                assert get_bool(
                    rv['relations'][0],
                    'relationType',
                    'crm:P2 has type')
                assert get_bool(
                    rv['relations'][0],
                    'relationSystemClass',
                    'type')
                assert get_bool(
                    rv['relations'][1],
                    'relationDescription',
                    '23.0')
                assert get_bool(
                    rv['names'][0],
                    'alias',
                    'Sûza')
                assert get_bool(
                    rv['links'][0],
                    'type',
                    'closeMatch')
                assert get_bool(
                    rv['links'][0],
                    'identifier',
                    'https://www.geonames.org/2761369')
                assert get_bool(
                    rv['links'][0],
                    'referenceSystem',
                    'GeoNames')
                assert get_bool(
                    rv['geometry'],
                    'type',
                    'Point')
                assert get_bool(
                    rv['geometry'],
                    'coordinates',
                    [9, 17])
                assert get_bool(
                    rv['depictions'][0],
                    '@id')
                assert get_bool(
                    rv['depictions'][0],
                    'title',
                    'Picture with a License')
                assert get_bool(
                    rv['depictions'][0],
                    'license',
                    'Open license')
                assert get_bool(
                    rv['depictions'][0],
                    'url')

            # Test entity in GeoJSON format
            rv = self.app.get(
                url_for('api_02.entity', id_=place.id, format='geojson'))
            rv = rv.get_json()['features'][0]
            assert get_bool(
                rv['geometry'],
                'type')
            assert get_bool(
                rv['geometry'],
                'coordinates')
            assert get_bool(
                rv['properties'],
                '@id')
            assert get_bool(
                rv['properties'],
                'systemClass')
            assert get_bool(
                rv['properties'],
                'name')
            assert get_bool(
                rv['properties'],
                'description')
            assert get_bool(
                rv['properties'],
                'begin_earliest')
            assert get_bool(
                rv['properties'],
                'begin_latest')
            assert get_bool(
                rv['properties'],
                'begin_comment')
            assert get_bool(
                rv['properties'],
                'end_earliest')
            assert get_bool(
                rv['properties'],
                'end_latest')
            assert get_bool(
                rv['properties'],
                'end_comment')
            assert get_bool(
                rv['properties'],
                'types')

            # Test Entity export and RDFS
            for rv in [
                self.app.get(url_for(
                    'api_02.entity',
                    id_=place.id,
                    format='xml')),
                self.app.get(url_for(
                    'api_02.entity',
                    id_=place.id,
                    export='csv')),
                self.app.get(url_for(
                    'api_02.code',
                    code='place',
                    format='xml')),
                self.app.get(url_for(
                    'api_02.code',
                    code='place',
                    export='csv')),
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
                self.app.get(url_for(
                    'api_02.class',
                    class_code='E21')),
                self.app.get(url_for(
                    'api_02.code',
                    code='place',
                    type_id=boundary_mark.id)),
                self.app.get(url_for(
                    'api_02.latest',
                    latest=2)),
                self.app.get(url_for(
                    'api_02.system_class',
                    system_class='artifact')),
                self.app.get(url_for(
                    'api_02.entities_linked_to_entity',
                    id_=event.id)),
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
                    filter=f"and|begin_from|eq|{place.begin_from}"))]:
                rv = rv.get_json()
                rv_results = rv['results'][0]['features'][0]
                rv_page = rv['pagination']
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
            assert bool(rv['results'][0]['features'][0]['properties'][
                            'title'] == place.name)

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
            rv = self.app.get(url_for(
                'api_02.geometric_entities',
                count=True))
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
                'api_02.node_entities',
                id_=unit_node.id,
                download=True)).get_json()
            assert get_bool(rv['nodes'][0], 'label')

            # Test type entities all
            rv = self.app.get(url_for(
                'api_02.node_entities_all',
                id_=unit_node.id)).get_json()
            assert bool([True for i in rv['nodes'] if i['label'] == 'Wien'])

            # Test type entities count
            rv = self.app.get(url_for(
                'api_02.node_entities',
                id_=unit_node.id,
                count=True))
            assert bool(rv.get_json() == 3)

            # Test type overview
            for rv in [
                self.app.get(url_for(
                    'api_02.node_overview')),
                self.app.get(url_for(
                    'api_02.node_overview', download=True))]:
                rv = rv.get_json()
                rv = rv['types'][0]['place']['Administrative unit']
                assert bool(
                    [True for i in rv if i['label'] == 'Austria'])

            # Test type tree
            for rv in [
                self.app.get(url_for(
                    'api_02.type_tree')),
                self.app.get(url_for(
                    'api_02.type_tree',
                    download=True))]:
                rv = rv.get_json()
                assert bool(rv['typeTree'][0])

            # subunit/
            rv = self.app.get(
                url_for('api_02.subunit', id_=place.id)).get_json()
            assert bool(rv['nodes'][0]['label'] == 'Home of Baggins')

            # subunit_hierarchy/
            rv = self.app.get(url_for(
                'api_02.subunit_hierarchy', id_=place.id)).get_json()
            assert bool(rv['nodes'][1]['label'] == 'Bar')
