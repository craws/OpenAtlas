import json
from pathlib import Path
from typing import Any

from flask import url_for

from openatlas import app
from openatlas.api.resources.api_entity import ApiEntity
from tests.base import ApiTestCase


class Api(ApiTestCase):

    def test_api(self) -> None:
        c = self.client
        logo_path = Path(app.root_path) / 'static' / 'images' / 'layout'

        with open(logo_path / 'logo.png', 'rb') as img:
            c.post(
                url_for('insert', class_='file'),
                data={
                    'name': 'OpenAtlas logo',
                    'file': img,
                    'creator': 'Max',
                    'license_holder': 'Moritz',
                    'public': True},
                follow_redirects=True)

        with app.test_request_context():
            app.preprocess_request()
            for entity in ApiEntity.get_by_cidoc_classes(['all']):
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
                    case 'Weight':
                        weight_ = entity
                    case 'Change of Property':
                        change_of_property = entity
                    case 'File not public':
                        file_not_public = entity
                    case 'File without license':
                        file_without_licences = entity
                    case 'File without file':
                        file_without_file = entity
                    case 'OpenAtlas logo':
                        file = entity
                    case 'Public domain':
                        open_license = entity

            file.link('P2', open_license)

        # Test Swagger UI
        if app.config['OPENAPI_INSTANCE_FILE'].exists():
            app.config['OPENAPI_INSTANCE_FILE'].unlink()
        rv: Any = c.get(url_for('flasgger.apidocs'))
        assert b'Flasgger' in rv.data
        with app.config['OPENAPI_INSTANCE_FILE'].open(mode='r+') as f:
            data = json.load(f)
            data['servers'][0]['description'] = 'Wrong description'
            f.seek(0)
            json.dump(data, f)
            f.truncate()
        rv = c.get(url_for('flasgger.apidocs'))
        assert b'Flasgger' in rv.data
        with app.config['OPENAPI_INSTANCE_FILE'].open(mode='r+') as f:
            data = json.load(f)
            data['info']['version'] = '9.9.9'
            f.seek(0)
            json.dump(data, f)
            f.truncate()
        rv = c.get(url_for('flasgger.apidocs'))
        assert b'Flasgger' in rv.data

        # ---Content Endpoints---
        rv = c.get(url_for('api_04.classes')).get_json()
        assert self.get_classes(rv)
        rv = c.get(url_for('api_04.class_mapping', locale='de')).get_json()
        assert self.get_class_mapping(rv, 'de')
        rv = c.get(url_for('api_04.class_mapping', locale='ca', download=True))
        assert self.get_class_mapping(rv.get_json(), 'ca')

        rv = c.get(url_for('api_04.properties', locale='de')).get_json()
        assert rv['P2']['nameInverse'] == 'ist Typus von'
        assert rv['P2']['name']
        assert rv['P2']['nameInverse']
        assert rv['P2']['i18n']
        assert rv['P2']['i18nInverse']
        assert rv['P2']['code']

        rv = c.get(url_for('api_04.properties', locale='fr', download=True))
        assert rv.get_json()['P2']['name'] == 'est de type'
        rv = c.get(url_for('api_04.backend_details')).get_json()
        assert rv['version'] == app.config['VERSION']
        rv = c.get(url_for('api_04.backend_details', download=True)).get_json()
        assert rv['version'] == app.config['VERSION']
        rv = c.get(url_for('api_04.system_class_count')).get_json()
        assert rv['person']
        rv = c.get(
            url_for('api_04.system_class_count', type_id=boundary_mark.id))
        assert rv.get_json()['place']

        rv = c.get(url_for('api.licensed_file_overview', file_id=file.id))
        assert rv.get_json()[str(file.id)]['license'] == 'Public domain'

        rv = c.get(url_for('api.licensed_file_overview'))
        assert len(rv.get_json().keys()) == 5

        rv = c.get(
            url_for(
                'api_04.network_visualisation',
                exclude_system_classes='type'))
        rv = rv.get_json()
        assert len(rv['results']) == 65
        rv = c.get(
            url_for(
                'api_04.network_visualisation',
                linked_to_ids=boundary_mark.id))
        rv = rv.get_json()
        assert len(rv['results']) == 3
        rv = c.get(url_for('api_04.network_visualisation', download=True))
        rv = rv.get_json()
        assert len(rv['results']) == 154

        for rv in [
                c.get(url_for('api_04.geometric_entities')),
                c.get(url_for('api_04.geometric_entities', download=True))]:
            rv = rv.get_json()
            assert rv['features'][0]['geometry']['coordinates']
            assert rv['features'][0]['properties']['id']
            assert rv['features'][0]['properties']['objectDescription']
            assert rv['features'][0]['properties']['objectId']
            assert rv['features'][0]['properties']['objectName']
            assert rv['features'][0]['properties']['shapeType']

        rv = c.get(url_for('api_04.export_database', format_='xml'))
        assert b'Shire' in rv.data
        assert 'application/xml' in rv.headers.get('Content-Type')
        rv = c.get(url_for('api_04.export_database', format_='json'))
        assert b'Shire' in rv.data
        assert 'application/json' in rv.headers.get('Content-Type')
        rv = c.get(url_for('api_04.export_database', format_='csv'))
        assert b'Shire' in rv.data
        assert 'application/zip' in rv.headers.get('Content-Type')

        # ---Entity Endpoints---
        # Test Entity
        rv = c.get(url_for('api_04.entity', id_=place.id, download=True))
        assert 'application/json' in rv.headers.get('Content-Type')
        rv = rv.get_json()['features'][0]
        assert rv['@id']
        assert rv['type'] == 'Feature'
        assert rv['crmClass'] == 'crm:E18 Physical Thing'
        assert rv['systemClass'] == 'place'
        assert rv['properties']['title'] == 'Shire'
        desc = rv['descriptions'][0]
        assert desc['value'] == 'The Shire was the homeland of the hobbits.'
        timespan = rv['when']['timespans'][0]
        assert timespan['start']['earliest'] == '2018-01-31T00:00:00'
        assert timespan['start']['latest'] == '2018-03-01T00:00:00'
        assert timespan['end']['earliest'] == '2019-01-31T00:00:00'
        assert timespan['end']['latest'] == '2019-03-01T00:00:00'
        assert rv['types'][0]['identifier']
        assert rv['types'][0]['label'] == 'Boundary Mark'
        assert rv['relations'][1]['label'] == 'Height'
        assert rv['relations'][1]['relationDescription'] == '23.0'
        assert rv['relations'][0]['relationTo']
        assert rv['relations'][0]['relationType'] == 'crm:P2 has type'
        assert rv['relations'][0]['relationSystemClass'] == 'type'
        assert rv['names'][0]['alias'] == 'Sûza'
        links = rv['links'][0]
        assert links['type'] == 'closeMatch'
        assert links['identifier'] == 'https://www.geonames.org/2761369'
        assert links['referenceSystem'] == 'GeoNames'
        assert rv['geometry']['type'] == 'GeometryCollection'
        assert rv['geometry']['geometries'][1]['coordinates'] \
            == [16.37069611, 48.208571233]
        assert rv['depictions'][0]['@id']
        assert rv['depictions'][0]['title'] == 'Picture with a License'
        assert rv['depictions'][0]['license'] == 'Public domain'
        assert rv['depictions'][0]['url']

        rv = c.get(
            url_for('api_04.entity', id_=place.id, format='lpx', locale='de'))
        assert 'application/json' in rv.headers.get('Content-Type')
        rv = rv.get_json()['features'][0]

        assert rv['relations'][1]['label'] == 'Height'
        assert rv['relations'][1]['relationDescription'] == '23.0'
        assert rv['relations'][0]['relationTo']
        assert rv['relations'][0]['relationType'] == 'crm:P2_has_type'
        assert rv['relations'][0]['relationTypeLabel'] == 'hat den Typus'

        geojson_checklist = [
            '@id', 'systemClass', 'name', 'description', 'begin_earliest',
            'begin_latest', 'begin_comment', 'end_earliest', 'end_latest',
            'end_comment', 'types']
        # Test entity in GeoJSON format
        rv = c.get(url_for('api_04.entity', id_=place.id, format='geojson'))
        assert 'application/json' in rv.headers.get('Content-Type')
        rv = rv.get_json()['features'][0]
        assert rv['geometry']['type']
        assert rv['geometry']['coordinates']
        for key in geojson_checklist:
            assert rv['properties'][key]
        rv = c.get(url_for('api_04.entity', id_=place.id, format='geojson-v2'))
        assert 'application/json' in rv.headers.get('Content-Type')
        rv = rv.get_json()['features'][0]
        assert rv['geometry']['type']
        assert rv['geometry']['geometries'][0]['coordinates']
        for key in geojson_checklist:
            assert rv['properties'][key]

        # Test entity in Linked Open Usable Data
        rv = c.get(url_for('api_04.entity', id_=place.id, format='loud'))
        assert 'application/json' in rv.headers.get('Content-Type')
        rv = rv.get_json()
        assert rv['type'] == 'PhysicalThing'
        assert rv['_label'] == 'Shire'
        assert rv['content'] == 'The Shire was the homeland of the hobbits.'
        assert rv['timespan']['begin_of_the_begin'] == '2018-01-31T00:00:00'
        assert rv['identified_by'][0]['_label'] == 'Sûza'
        assert rv['classified_as'][0]['_label'] == 'Boundary Mark'
        assert (rv['former_or_current_location'][0]['_label']
                == 'Location of Shire')
        assert (rv['former_or_current_location'][0]['defined_by']
                == 'POLYGON((28.9389559878606 41.0290525580955,'
                   '28.9409293485759 41.0273124142771,28.941969652866 '
                   '41.0284940983463,28.9399641177912 41.0297647897435'
                   ',28.9389559878606 41.0290525580955))')

        # Test Entity export and RDFS
        for rv in [
            c.get(url_for('api_04.entity', id_=place.id, export='csv')),
            c.get(
                url_for(
                    'api_04.query',
                    entities=location.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    export='csv'))]:
            assert b'Shire' in rv.data
            assert 'text/csv' in rv.headers.get('Content-Type')
        #
        # for rv in [
        #     c.get(
        #         url_for('api_04.entity', id_=place.id, export='csvNetwork')),
        #     c.get(
        #         url_for(
        #             'api_04.query',
        #             entities=location.id,
        #             cidoc_classes='E18',
        #             view_classes='artifact',
        #             system_classes='person',
        #             export='csvNetwork'))]:
        #     assert b'Shire' in rv.data
        #     assert 'application/zip' in rv.headers.get('Content-Type')

        rv = c.get(
            url_for(
                'api_04.linked_entities_by_properties_recursive',
                id_=place.id,
                properties='P46'))
        rv = rv.get_json()
        names = [place.name, feature.name, 'Bar']
        for item in rv['results']:
            assert item['features'][0]['properties']['title'] in names
        rv = c.get(
            url_for(
                'api_04.linked_entities_by_properties_recursive',
                id_=place.id,
                properties='all'))
        rv = rv.get_json()
        assert rv['results'][0]['features'][0]['properties']

        # Test Entities endpoints
        for rv in [
            c.get(url_for('api_04.cidoc_class', class_='E21')),
            c.get(
                url_for(
                    'api_04.view_class',
                    class_='place',
                    sort='desc',
                    column='id',
                    relation_type='P2',
                    type_id=boundary_mark.id)),
            c.get(
                url_for(
                    'api_04.view_class',
                    class_='place',
                    sort='desc',
                    column='begin_from',
                    relation_type='P2',
                    type_id=boundary_mark.id)),
            c.get(url_for('api_04.latest', limit=2)),
            c.get(url_for('api_04.system_class', class_='artifact')),
            c.get(url_for('api_04.entities_linked_to_entity', id_=event.id)),
            c.get(url_for('api_04.type_entities', id_=boundary_mark.id)),
            c.get(url_for('api_04.type_entities', id_=relation_sub.id)),
            c.get(url_for('api_04.type_entities_all', id_=unit_node.id)),
            c.get(url_for('api_04.type_entities_all', id_=relation_sub.id)),
            c.get(
                url_for(
                    'api_04.query',
                    entities=location.id,
                    classes='E18',
                    codes='artifact',
                    sort='desc',
                    column='cidoc_class',
                    system_classes='person',
                    download=True,
                    last=actor.id)),
            c.get(
                url_for(
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
            assert rv['results'][0]['features'][0]['@id']
            assert rv['pagination']['entities']
            assert rv['pagination']['entitiesPerPage']
            assert rv['pagination']['index']
            assert rv['pagination']['totalPages']

        # Test Entities with show=none
        rv = c.get(url_for('api_04.cidoc_class', class_='E21', show='none'))
        rv = rv.get_json()['results'][0]['features'][0]
        assert not rv['geometry']
        assert not rv.get('depictions')
        assert not rv.get('links')
        assert not rv.get('types')

        # Test if Query returns enough entities
        rv = c.get(
            url_for(
                'api_04.query',
                entities=location.id,
                cidoc_classes='E18',
                view_classes='artifact',
                system_classes='person',
                limit=0,
                first=actor2.id)).get_json()
        assert rv['pagination']['entities'] == 8

        # Test page parameter
        rv = c.get(
            url_for(
                'api_04.query',
                entities=location.id,
                cidoc_classes='E18',
                view_classes='artifact',
                system_classes='person',
                limit=1,
                page=7)).get_json()
        properties = rv['results'][0]['features'][0]['properties']
        assert properties['title'] == place.name
        assert len(rv['results']) == 1

        # Test Entities count
        rv = c.get(
            url_for(
                'api_04.query',
                entities=location.id,
                cidoc_classes='E18',
                view_classes='artifact',
                system_classes='person',
                count=True))
        assert rv.get_json() == 8

        rv = c.get(url_for('api_04.geometric_entities', count=True))
        assert rv.get_json() == 6

        # Test entities with GeoJSON Format
        for rv in [
            c.get(
                url_for(
                    'api_04.query',
                    entities=location.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='geojson')),
            c.get(
                url_for(
                    'api_04.query',
                    entities=location.id,
                    cidoc_classes='E18',
                    view_classes='artifact',
                    system_classes='person',
                    format='geojson-v2'))]:
            rv = rv.get_json()['results'][0]['features'][0]
            assert rv['properties']['@id']
            assert rv['properties']['systemClass']

        # Test entities with Linked Open Usable Data Format
        rv = c.get(
            url_for(
                'api_04.query',
                entities=location.id,
                cidoc_classes=['E18', 'E53'],
                view_classes='artifact',
                system_classes=['person', 'type'],
                format='loud',
                limit=0))
        rv = rv.get_json()['results'][0]
        assert rv['type'] == 'Type'
        assert rv['_label'] == 'Abbot'

        # ---Type Endpoints---
        for rv in [
                c.get(url_for('api_04.type_overview')),
                c.get(url_for('api_04.type_overview', download=True))]:
            assert 'Austria' in str(rv.get_json())

        for rv in [
                c.get(url_for('api_04.type_by_view_class')),
                c.get(url_for('api_04.type_by_view_class', download=True))]:
            assert 'Boundary Mark' in str(rv.get_json())
        rv = c.get(url_for('api_04.type_tree'))
        assert rv.get_json()['typeTree']
        rv = c.get(url_for('api_04.type_tree', download=True))
        assert rv.get_json()['typeTree']
        rv = c.get(url_for('api_04.type_tree', count=True))
        assert rv.get_json() > 0

        # ---Test search---
        search_string_constructor = {
            0: [{
                "entityAliases": [{
                    "operator": "equal",
                    "values": ["Sûza"],
                    "logicalOperator": "and"}],
                "typeID": [{
                    "operator": "equal", "values": [1121212],
                    "logicalOperator": "and"}]}, {
                "valueTypeID": [{
                    "operator": "lesserThanEqual",
                    "values": [(height.id, 1.0), (weight_.id, 1.0)],
                    "logicalOperator": "and"}]}, {
                "entityAliases": [{
                    "operator": "greaterThan", "values": ["Sûza"]}],
                "typeID": [{"operator": "equal", "values": [1121212]}]}],
            1: [{
                "valueTypeID": [{
                    "operator": "equal",
                    "values": [(height.id, 23.0)]}]}, {
                "valueTypeID": [{
                    "operator": "greaterThanEqual",
                    "values": [(height.id, 23.0)]}]}, {
                "typeName": [{
                    "operator": "equal",
                    "values": ["Boundary Mark", "Height"],
                    "logicalOperator": "and"}]}, {
                "beginFrom": [{
                    "operator": "lesserThan",
                    "values": ["2020-01-01"],
                    "logicalOperator": "and"}]}, {
                "beginFrom": [{
                    "operator": "lesserThan",
                    "values": ["2020-01-01"]}]}, {
                "beginTo": [{
                    "operator": "lesserThanEqual",
                    "values": ["2018-03-01"],
                    "logicalOperator": "and"}]}, {
                "beginTo": [{
                    "operator": "lesserThanEqual",
                    "values": ["2018-03-01"]}]}, {
                "endFrom": [{
                    "operator": "greaterThan",
                    "values": ["2013-02-01"],
                    "logicalOperator": "and"}]}, {
                "endFrom": [{
                    "operator": "greaterThan",
                    "values": ["2013-02-01"]}]}, {
                "endTo": [{
                    "operator": "greaterThanEqual",
                    "values": ["2019-03-01"],
                    "logicalOperator": "and"}]}, {
                "endTo": [{
                    "operator": "greaterThanEqual",
                    "values": ["2019-03-01"]}]}, {
                "entityAliases": [
                    {"operator": "like", "values": ["S"]}]}, {
                "typeName": [{
                    "operator": "like",
                    "values": ["Oun", "mark"],
                    "logicalOperator": "and"}]}, {
                "entityDescription": [{
                    "operator": "equal",
                    "values": [
                        "the shirE Was the Homeland of the hobbits.",
                        "homeland"]}]}, {
                "valueTypeID": [{
                    "operator": "greaterThanEqual",
                    "values": [(height.id, 23.0), (weight_.id, 999.0)],
                    "logicalOperator": "and"}]}],
            2: [{
                "entityCidocClass": [{
                    "operator": "equal",
                    "values": ["E21"],
                    "logicalOperator": "and"}]}, {
                "entitySystemClass": [{
                    "operator": "equal",
                    "values": ["person"],
                    "logicalOperator": "and"}]}, {
                "typeIDWithSubs": [{
                    "operator": "equal",
                    "values": [boundary_mark.id, height.id]}]}, {
                "typeIDWithSubs": [{
                    "operator": "equal",
                    "values": [boundary_mark.id],
                    "logicalOperator": "and"}]}, {
                "typeID": [{
                    "operator": "equal",
                    "values": [boundary_mark.id, height.id]}]}],
            3: [{
                "typeIDWithSubs": [{
                    "operator": "equal",
                    "values": [
                        boundary_mark.id, height.id,
                        change_of_property.id]}]}, {
                "entityDescription": [{
                    "operator": "like",
                    "values": ["FrOdO", "sam"]}]}],
            5: [{"entityName": [{"operator": "like", "values": ["Fr"]}]}],
            9: [{
                "relationToID": [{
                    "operator": "equal", "values": [place.id]}]}],
            161: [{
                "typeIDWithSubs": [{
                    "operator": "notEqual",
                    "values": [boundary_mark.id],
                    "logicalOperator": "and"}]}],
            162: [{
                "typeName": [{
                    "operator": "notEqual",
                    "values": ["Boundary Mark", "Height"],
                    "logicalOperator": "and"}]}, {
                "entityID": [{
                    "operator": "notEqual",
                    "values": [place.id],
                    "logicalOperator": "and"}]}, {
                "entityAliases": [{
                    "operator": "notEqual",
                    "values": ["Sûza"],
                    "logicalOperator": "and"}]}, {
                "entityName": [
                    {"operator": "notEqual", "values": ["Mordor"]}]}]}

        for count, search_string in search_string_constructor.items():
            rv = c.get(
                url_for(
                    'api_04.query',
                    system_classes='all',
                    search=search_string))
            assert rv.get_json()['pagination']['entities'] == count

        for rv in [
                c.get(url_for('api_04.subunits', id_=place.id)),
                c.get(
                    url_for('api_04.subunits', id_=place.id, download=True))]:
            assert 'application/json' in rv.headers.get('Content-Type')
        rv = rv.get_json()[str(place.id)]
        for item in rv:
            if item['id'] == place.id:
                assert item['id'] == place.id
                assert item['openatlasClassName'] == "place"
                assert item['children'] == [feature.id]
                item = item['properties']
                assert item['name'] == place.name
                assert item['description'] == place.description
                assert item['aliases'] == [alias.name]
                assert item['externalReferences']
                assert item['timespan']
                assert item['standardType']
                assert item['files']
                assert item['types']

        rv = c.get(url_for('api_04.subunits', id_=place.id, count=True))
        assert b'3' in rv.data
        for rv in [
            c.get(url_for('api_04.subunits', id_=place.id, format='xml')),
            c.get(
                url_for(
                    'api_04.subunits',
                    id_=place.id,
                    format='xml',
                    download=True))]:
            assert b'Shire' in rv.data

        # Test centroid
        for id_ in [feature.id, feature_location.id]:
            for format_ in ['lp', 'geojson', 'geojson-v2']:
                rv = c.get(
                    url_for(
                        'api_04.entity',
                        id_=id_,
                        format=format_,
                        centroid=True))
                assert b'(autogenerated)' in rv.data
                assert 'application/json' in rv.headers.get('Content-Type')
                rv = c.get(
                    url_for('api_04.subunits', id_=place.id, centroid=True))
                assert b'(autogenerated)' in rv.data
                assert 'application/json' in rv.headers.get('Content-Type')
        rv = c.get(
            url_for('api_04.view_class', class_='all', centroid=True, limit=0))
        assert b'(autogenerated)' in rv.data
        assert 'application/json' in rv.headers.get('Content-Type')

        rv = c.get(
            url_for(
                'api_04.display',
                filename=f'{file.id}',
                image_size='table'))
        self.assertTrue(rv.headers['Content-Type'].startswith('image'))

        # Test Error Handling
        for rv in [
                c.get(url_for('api_04.entity', id_=233423424)),
                c.get(url_for('api_04.cidoc_class', class_='E18', last=1231))]:
            rv = rv.get_json()
        assert 'Entity does not exist' in rv['title']

        rv = c.get(url_for('api_04.subunits', id_=actor.id))
        assert 'ID is not a valid place' in rv.get_json()['title']

        rv = c.get(
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

        rv = c.get(url_for('api_04.system_class', class_='Wrong'))
        assert 'Invalid system_classes value' in rv.get_json()['title']

        rv = c.get(url_for('api_04.query'))
        assert 'No query parameters given' in rv.get_json()['title']

        rv = c.get(url_for('api_04.cidoc_class', class_='e99999999'))
        assert 'Invalid cidoc_classes value' in rv.get_json()['title']

        rv = c.get(url_for('api_04.view_class', class_='Invalid'))
        assert 'Invalid view_classes value' in rv.get_json()['title']

        rv = c.get(url_for('api_04.latest', limit='99999999'))
        assert 'Invalid limit value' in rv.get_json()['title']

        rv = c.get(
            url_for(
                'api_04.view_class',
                class_='place',
                search='{"typeID":[{"operator":"equal",'
                       '"values":["Boundary Mark", "Height", "Dimension"],'
                       '"logicalOperator":"and"}]}'))
        assert 'Invalid search value' in rv.get_json()['title']

        rv = c.get(
            url_for(
                'api_04.view_class',
                class_='place',
                search='{"typeID":[{"operator":"like",'
                       '"values":["Boundary Mark", "Height", "Dimension"],'
                       '"logicalOperator":"and"}]}'))
        assert 'Operator not supported' in rv.get_json()['title']

        rv = c.get(
            url_for(
                'api_04.view_class',
                class_='place',
                search={
                    "All": [{
                        "operator": "notEqual",
                        "values": ["Boundary Mark", "Height"]}]}))
        assert 'Invalid search category' in rv.get_json()['title']

        rv = c.get(
            url_for(
                'api_04.view_class',
                class_='place',
                search={"typeName": [{"operator": "notEqual", "values": []}]}))
        assert 'No search value' in rv.get_json()['title']

        rv = c.get(
            url_for(
                'api_04.view_class',
                class_='place',
                search={
                    "beginFrom": [{
                        "operator": "notEqual",
                        "values": ["Help"]}]}))
        assert 'Invalid search values' in rv.get_json()['title']

        rv = c.get(
            url_for(
                'api_04.view_class',
                class_='place',
                search={
                    "beginFrom": [{
                        "operator": "notEqual",
                        "values": ["800-1-1", "Help"]}]}))
        assert 'Invalid search values' in rv.get_json()['title']

        rv = c.get(
            url_for(
                'api_04.view_class',
                class_='place',
                search='"beginFrom":[{"operator":"lesserThan",'
                       '"values":["2000-01-01"],'
                       '"logicalOperator":"or"}]}'))
        assert 'Invalid search syntax' in rv.get_json()['title']

        rv = c.get(url_for('api_04.type_entities', id_=1234))
        assert 'Entity is not a type' in rv.get_json()['title']

        rv = c.get(url_for('api_04.type_entities_all', id_=1234))
        assert 'Entity is not a type' in rv.get_json()['title']

        rv = c.get(url_for('api_04.system_class_count', type_id=999))
        assert 'Entity is not a type' in rv.get_json()['title']

        rv = c.get(
            url_for(
                'api_04.view_class',
                class_='place',
                search={
                    "typeName": [{
                        "operator": "notEqualT",
                        "values": ["Boundary Mark", "Height"],
                        "logicalOperator": "and"}]}))
        assert 'Invalid compare operator' in rv.get_json()['title']

        rv = c.get(
            url_for(
                'api_04.view_class',
                class_='place',
                search={
                    "typeName": [{
                        "operator": "notEqual",
                        "values": ["Boundary Mark", "Height"],
                        "logicalOperator": "xor"}]}))
        assert 'Invalid logical operator' in rv.get_json()['title']

        rv = c.get(
            url_for('api_04.display', filename=f'{file_without_licences.id}'))
        assert 'No license' in rv.get_json()['title']

        rv = c.get(
            url_for('api_04.display', filename=f'{file_without_file.id}'))
        assert 'File not found' in rv.get_json()['title']

        rv = c.get(url_for('api_04.iiif_manifest', version=2, id_=place.id))
        assert 'File not found' in rv.get_json()['title']

        rv = c.get(url_for('api_04.iiif_sequence', version=2, id_=place.id))
        assert 'File not found' in rv.get_json()['title']

        rv = c.get(url_for('api_04.display', filename=f'{file_not_public.id}'))
        assert 'Not public' in rv.get_json()['title']
        assert b'Endpoint not found' in c.get('/api/entity2').data

        c.get(url_for('logout'))
        app.config['ALLOWED_IPS'] = []

        rv = c.get(url_for('api_04.view_class', class_='place'))
        assert 'Access denied' in rv.get_json()['title']
