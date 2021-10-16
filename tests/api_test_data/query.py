import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_params import test_ids

test_query = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["location_shire_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E53 Place',
        'systemClass': 'object_location',
        'properties': {'title': 'Location of Shire'},
        'description': None,
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Shire',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["shire_id"]}',
            'relationType': 'crm:P53i is former or current location of',
            'relationSystemClass': 'place',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {
                        'earliest': '2018-01-31', 'latest': '2018-03-01'},
                    'end': {
                        'earliest': '2019-01-31', 'latest': '2019-03-01'}}]}}, {
            'label': 'Travel to Mordor',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["travel_id"]}',
            'relationType': 'crm:P7i witnessed',
            'relationSystemClass': 'activity',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': {
            'type': 'Point',
            'coordinates': [9, 17],
            'title': '',
            'description': ''},
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["ring_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E22 Man-Made Object',
        'systemClass': 'artifact',
        'properties': {'title': 'The One Ring'},
        'description': None,
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Frodo',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["frodo_id"]}',
            'relationType': 'crm:P52 has current owner',
            'relationSystemClass': 'person',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Location of The One Ring',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["location_ring_id"]}',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': {
            'type': 'GeometryCollection',
            'geometries': []},
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["frodo_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E21 Person',
        'systemClass': 'person',
        'properties': {'title': 'Frodo'},
        'description': [{'value': 'That is Frodo'}],
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Sam',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["sam_id"]}',
            'relationType': 'crm:OA7 has relationship to',
            'relationSystemClass': 'person',
            'relationDescription': None, 'type': 'Economical',
            'when': {'timespans': [
                {'start': {'earliest': 'None', 'latest': 'None'},
                 'end': {'earliest': 'None', 'latest': 'None'}}]}},
            {'label': 'File without license',
             'relationTo': f'http://local.host/api/0.2/entity/{test_ids["file_without_id"]}',
             'relationType': 'crm:P67i is referred to by',
             'relationSystemClass': 'file',
             'relationDescription': None, 'type': None, 'when': {
                'timespans': [
                    {'start': {'earliest': 'None', 'latest': 'None'},
                     'end': {'earliest': 'None',
                             'latest': 'None'}}]}},
            {'label': 'The One Ring',
             'relationTo': f'http://local.host/api/0.2/entity/{test_ids["ring_id"]}',
             'relationType': 'crm:P52i is current owner of',
             'relationSystemClass': 'artifact',
             'relationDescription': None, 'type': None, 'when': {
                'timespans': [
                    {'start': {'earliest': 'None', 'latest': 'None'},
                     'end': {'earliest': 'None',
                             'latest': 'None'}}]}},
            {'label': 'Travel to Mordor',
             'relationTo': f'http://local.host/api/0.2/entity/{test_ids["travel_id"]}',
             'relationType': 'crm:P11i participated in',
             'relationSystemClass': 'activity',
             'relationDescription': None, 'type': None, 'when': {
                'timespans': [
                    {'start': {'earliest': 'None', 'latest': 'None'},
                     'end': {'earliest': 'None',
                             'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': None,
        'depictions': [{
            '@id': f'http://local.host/api/0.2/entity/{test_ids["file_without_id"]}',
            'title': 'File without license', 'license': None,
            'url': 'N/A'}]}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["sam_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E21 Person',
        'systemClass': 'person',
        'properties': {'title': 'Sam'},
        'description': [{'value': 'That is Sam'}],
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Frodo',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["frodo_id"]}',
            'relationType': 'crm:OA7 has relationship to',
            'relationSystemClass': 'person',
            'relationDescription': None, 'type': 'Economical',
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}},
            {'label': 'Travel to Mordor',
             'relationTo': f'http://local.host/api/0.2/entity/{test_ids["travel_id"]}',
             'relationType': 'crm:P14i performed',
             'relationSystemClass': 'activity',
             'relationDescription': None, 'type': None, 'when': {
                'timespans': [
                    {'start': {'earliest': 'None', 'latest': 'None'},
                     'end': {'earliest': 'None',
                             'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': None,
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["home_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'feature',
        'properties': {'title': 'Home of Baggins'},
        'description': None,
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Kitchen',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["kitchen_id"]}',
            'relationType': 'crm:P46 is composed of',
            'relationSystemClass': 'stratigraphic_unit',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Location of Home of Baggins',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["location_home_id"]}',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None',
                            'latest': 'None'}}]}}, {
            'label': 'Shire',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["shire_id"]}',
            'relationType': 'crm:P46i forms part of',
            'relationSystemClass': 'place',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {
                        'earliest': '2018-01-31',
                        'latest': '2018-03-01'},
                    'end': {
                        'earliest': '2019-01-31',
                        'latest': '2019-03-01'}}]}}],
        'names': None,
        'links': None,
        'geometry': {
            'type': 'GeometryCollection',
            'geometries': []},
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["kitchen_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'stratigraphic_unit',
        'properties': {'title': 'Kitchen'},
        'description': None,
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Location of Kitchen',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["location_kitchen_id"]}',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Home of Baggins',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["home_id"]}',
            'relationType': 'crm:P46i forms part of',
            'relationSystemClass': 'feature',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': {
            'type': 'GeometryCollection',
            'geometries': []},
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [{
        '@id': f'http://local.host/entity/{test_ids["mordor_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'place',
        'properties': {'title': 'Mordor'},
        'description': [{'value': 'The heart of evil.'}],
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': [{
            'identifier': f'http://local.host/api/0.2/entity/{test_ids["boundary_id"]}',
            'label': 'Boundary Mark', 'description': None,
            'hierarchy': 'Place', 'value': None, 'unit': None}],
        'relations': [{
            'label': 'Boundary Mark',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["boundary_id"]}',
            'relationType': 'crm:P2 has type',
            'relationSystemClass': 'type',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {
                        'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Location of Mordor',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["location_mordor_id"]}',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': {'type': 'GeometryCollection', 'geometries': []},
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["shire_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'place',
        'properties': {'title': 'Shire'},
        'description': [
            {'value': 'The Shire was the homeland of the hobbits.'}],
        'when': {
            'timespans': [{
                'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]},
        'types': [{
            'identifier': f'http://local.host/api/0.2/entity/{test_ids["place_id"]}',
            'label': 'Place', 'description': None, 'hierarchy': '',
            'value': None, 'unit': None}, {
            'identifier': f'http://local.host/api/0.2/entity/{test_ids["height_id"]}',
            'label': 'Height', 'description': None,
            'hierarchy': 'Dimensions',
            'value': 23.0,
            'unit': 'centimeter'}],
        'relations': [{
            'label': 'Height',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["height_id"]}',
            'relationType': 'crm:P2 has type',
            'relationSystemClass': 'type',
            'relationDescription': '23.0',
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Home of Baggins',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["home_id"]}',
            'relationType': 'crm:P46 is composed of',
            'relationSystemClass': 'feature',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Location of Shire',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["location_shire_id"]}',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Place',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["place_id"]}',
            'relationType': 'crm:P2 has type',
            'relationSystemClass': 'type',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Sûza',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["suza_id"]}',
            'relationType': 'crm:P1 is identified by',
            'relationSystemClass': 'appellation',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'GeoNames',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["geonames_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'reference_system',
            'relationDescription': '2761369',
            'type': 'closeMatch',
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'https://lotr.fandom.com/',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["lotr_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'external_reference',
            'relationDescription': 'Fandom Wiki of lord of the rings',
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Picture with a License',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["picture_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'file',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': [{'alias': 'Sûza'}],
        'links': [{
            'type': 'closeMatch',
            'identifier': 'https://www.geonames.org/2761369',
            'referenceSystem': 'GeoNames'}],
        'geometry': {
            'type': 'Point',
            'coordinates': [9, 17],
            'title': '',
            'description': ''},
        'depictions': [{
            '@id': f'http://local.host/api/0.2/entity/{test_ids["picture_id"]}',
            'title': 'Picture with a License',
            'license': 'Open license',
            'url': 'N/A'}]}]}],
    'pagination': {
        'entities': 8,
        'entitiesPerPage': 20,
        'index': [{
            'page': test_ids["geonames_id"],
            'startId': test_ids["location_shire_id"]}],
        'totalPages': 1}}
test_query_geojson = {
    'results': [{
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [9, 17],
                'title': '',
                'description': ''},
            'properties': {
                '@id': test_ids["location_shire_id"],
                'systemClass': 'object_location',
                'name': 'Location of Shire',
                'description': None,
                'begin_earliest': None,
                'begin_latest': None,
                'begin_comment': None,
                'end_earliest': None,
                'end_latest': None,
                'end_comment': None,
                'types': None}}, {
            'type': 'Feature',
            'geometry': None,
            'properties': {
                '@id': test_ids["ring_id"],
                'systemClass': 'artifact',
                'name': 'The One Ring',
                'description': None,
                'begin_earliest': None,
                'begin_latest': None,
                'begin_comment': None,
                'end_earliest': None,
                'end_latest': None,
                'end_comment': None,
                'types': None}}, {
            'type': 'Feature',
            'geometry': None,
            'properties': {
                '@id': test_ids["frodo_id"],
                'systemClass': 'person',
                'name': 'Frodo',
                'description': 'That is Frodo',
                'begin_earliest': None,
                'begin_latest': None,
                'begin_comment': None,
                'end_earliest': None,
                'end_latest': None,
                'end_comment': None,
                'types': None}}, {
            'type': 'Feature',
            'geometry': None,
            'properties': {
                '@id': test_ids["sam_id"],
                'systemClass': 'person',
                'name': 'Sam',
                'description': 'That is Sam',
                'begin_earliest': None,
                'begin_latest': None,
                'begin_comment': None,
                'end_earliest': None,
                'end_latest': None,
                'end_comment': None,
                'types': None}}, {
            'type': 'Feature',
            'geometry': None,
            'properties': {
                '@id': test_ids["home_id"],
                'systemClass': 'feature',
                'name': 'Home of Baggins',
                'description': None,
                'begin_earliest': None,
                'begin_latest': None,
                'begin_comment': None,
                'end_earliest': None,
                'end_latest': None,
                'end_comment': None,
                'types': None}}, {
            'type': 'Feature',
            'geometry': None,
            'properties': {
                '@id': test_ids["kitchen_id"],
                'systemClass': 'stratigraphic_unit',
                'name': 'Kitchen',
                'description': None,
                'begin_earliest': None,
                'begin_latest': None,
                'begin_comment': None,
                'end_earliest': None,
                'end_latest': None,
                'end_comment': None,
                'types': None}}, {
            'type': 'Feature',
            'geometry': None,
            'properties': {
                '@id': test_ids["mordor_id"],
                'systemClass': 'place',
                'name': 'Mordor',
                'description': 'The heart of evil.',
                'begin_earliest': None,
                'begin_latest': None,
                'begin_comment': None,
                'end_earliest': None,
                'end_latest': None,
                'end_comment': None,
                'types': ['Boundary Mark']}}, {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [9, 17],
                'title': '',
                'description': ''},
            'properties': {
                '@id': test_ids["shire_id"],
                'systemClass': 'place',
                'name': 'Shire',
                'description': 'The Shire was the homeland of the hobbits.',
                'begin_earliest': '2018-01-31',
                'begin_latest': '2018-03-01',
                'begin_comment': 'Begin of the shire',
                'end_earliest': '2019-01-31',
                'end_latest': '2019-03-01',
                'end_comment': 'Descent of Shire',
                'types': ['Place',
                          'Height']}}]}],
    'pagination': {
        'entities': 8,
        'entitiesPerPage': 20,
        'index': [{
            'page': test_ids["geonames_id"],
            'startId': test_ids["location_shire_id"]}],
        'totalPages': test_ids["geonames_id"]}}
test_query_filter = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["location_shire_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E53 Place',
        'systemClass': 'object_location',
        'properties': {'title': 'Location of Shire'},
        'description': None,
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Shire',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["shire_id"]}',
            'relationType': 'crm:P53i is former or current location of',
            'relationSystemClass': 'place',
            'relationDescription': None, 'type': None, 'when': {
                'timespans': [{
                    'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                    'end': {'earliest': '2019-01-31',
                            'latest': '2019-03-01'}}]}}, {
            'label': 'Travel to Mordor',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["travel_id"]}',
            'relationType': 'crm:P7i witnessed',
            'relationSystemClass': 'activity',
            'relationDescription': None, 'type': None, 'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': {
            'type': 'Point',
            'coordinates': [9, 17],
            'title': '',
            'description': ''},
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["shire_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'place',
        'properties': {'title': 'Shire'},
        'description': [
            {'value': 'The Shire was the homeland of the hobbits.'}],
        'when': {
            'timespans': [{
                'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]},
        'types': [{
            'identifier': f'http://local.host/api/0.2/entity/{test_ids["place_id"]}',
            'label': 'Place', 'description': None, 'hierarchy': '',
            'value': None, 'unit': None}, {
            'identifier': f'http://local.host/api/0.2/entity/{test_ids["height_id"]}',
            'label': 'Height', 'description': None,
            'hierarchy': 'Dimensions', 'value': 23.0,
            'unit': 'centimeter'}],
        'relations': [{
            'label': 'Height',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["height_id"]}',
            'relationType': 'crm:P2 has type',
            'relationSystemClass': 'type',
            'relationDescription': '23.0',
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Home of Baggins',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["home_id"]}',
            'relationType': 'crm:P46 is composed of',
            'relationSystemClass': 'feature',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Location of Shire',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["location_shire_id"]}',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Place',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["place_id"]}',
            'relationType': 'crm:P2 has type',
            'relationSystemClass': 'type',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Sûza',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["suza_id"]}',
            'relationType': 'crm:P1 is identified by',
            'relationSystemClass': 'appellation',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'GeoNames',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["geonames_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'reference_system',
            'relationDescription': '2761369',
            'type': 'closeMatch',
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'https://lotr.fandom.com/',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["lotr_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'external_reference',
            'relationDescription': 'Fandom Wiki of lord of the rings',
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Picture with a License',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["picture_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'file',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': [{'alias': 'Sûza'}],
        'links': [{
            'type': 'closeMatch',
            'identifier': 'https://www.geonames.org/2761369',
            'referenceSystem': 'GeoNames'}],
        'geometry': {
            'type': 'Point',
            'coordinates': [9, 17],
            'title': '',
            'description': ''},
        'depictions': [{
            '@id': f'http://local.host/api/0.2/entity/{test_ids["picture_id"]}',
            'title': 'Picture with a License',
            'license': 'Open license',
            'url': 'N/A'}]}]}],
    'pagination': {
        'entities': 2, 'entitiesPerPage': 20,
        'index': [{
            'page': test_ids["geonames_id"],
            'startId': test_ids["location_shire_id"]}],
        'totalPages': test_ids["geonames_id"]}}
test_query_filter_date = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["location_shire_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E53 Place',
        'systemClass': 'object_location',
        'properties': {'title': 'Location of Shire'},
        'description': None,
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Shire',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["shire_id"]}',
            'relationType': 'crm:P53i is former or current location of',
            'relationSystemClass': 'place',
            'relationDescription': None, 'type': None, 'when': {
                'timespans': [{
                    'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                    'end': {'earliest': '2019-01-31',
                            'latest': '2019-03-01'}}]}}, {
            'label': 'Travel to Mordor',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["travel_id"]}',
            'relationType': 'crm:P7i witnessed',
            'relationSystemClass': 'activity',
            'relationDescription': None, 'type': None, 'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': {
            'type': 'Point',
            'coordinates': [9, 17],
            'title': '',
            'description': ''},
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["ring_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E22 Man-Made Object',
        'systemClass': 'artifact',
        'properties': {'title': 'The One Ring'},
        'description': None, 'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Frodo',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["frodo_id"]}',
            'relationType': 'crm:P52 has current owner',
            'relationSystemClass': 'person',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Location of The One Ring',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["location_ring_id"]}',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None,
            'type': None,
            'when': {'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': {'type': 'GeometryCollection', 'geometries': []},
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["shire_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'place',
        'properties': {'title': 'Shire'},
        'description': [
            {'value': 'The Shire was the homeland of the hobbits.'}],
        'when': {
            'timespans': [{
                'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]},
        'types': [{
            'identifier': f'http://local.host/api/0.2/entity/{test_ids["place_id"]}',
            'label': 'Place',
            'description': None, 'hierarchy': '',
            'value': None,
            'unit': None}, {
            'identifier': f'http://local.host/api/0.2/entity/{test_ids["height_id"]}',
            'label': 'Height',
            'description': None,
            'hierarchy': 'Dimensions',
            'value': 23.0,
            'unit': 'centimeter'}],
        'relations': [{
            'label': 'Height',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["height_id"]}',
            'relationType': 'crm:P2 has type',
            'relationSystemClass': 'type',
            'relationDescription': '23.0',
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Home of Baggins',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["home_id"]}',
            'relationType': 'crm:P46 is composed of',
            'relationSystemClass': 'feature',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Location of Shire',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["location_shire_id"]}',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Place',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["place_id"]}',
            'relationType': 'crm:P2 has type',
            'relationSystemClass': 'type',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Sûza',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["suza_id"]}',
            'relationType': 'crm:P1 is identified by',
            'relationSystemClass': 'appellation',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'GeoNames',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["geonames_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'reference_system',
            'relationDescription': '2761369',
            'type': 'closeMatch',
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'https://lotr.fandom.com/',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["lotr_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'external_reference',
            'relationDescription': 'Fandom Wiki of lord of the rings',
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Picture with a License',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["picture_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'file',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': [{'alias': 'Sûza'}],
        'links': [{
            'type': 'closeMatch',
            'identifier': 'https://www.geonames.org/2761369',
            'referenceSystem': 'GeoNames'}],
        'geometry': {
            'type': 'Point',
            'coordinates': [9, 17],
            'title': '',
            'description': ''},
        'depictions': [{
            '@id': f'http://local.host/api/0.2/entity/{test_ids["picture_id"]}',
            'title': 'Picture with a License', 'license': 'Open license',
            'url': 'N/A'}]}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["sam_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E21 Person',
        'systemClass': 'person',
        'properties': {'title': 'Sam'},
        'description': [{'value': 'That is Sam'}],
        'when': {'timespans': [{
            'start': {'earliest': 'None', 'latest': 'None'},
            'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Frodo',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["frodo_id"]}',
            'relationType': 'crm:OA7 has relationship to',
            'relationSystemClass': 'person',
            'relationDescription': None, 'type': 'Economical',
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Travel to Mordor',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["travel_id"]}',
            'relationType': 'crm:P14i performed',
            'relationSystemClass': 'activity',
            'relationDescription': None, 'type': None, 'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': None,
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["frodo_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E21 Person',
        'systemClass': 'person',
        'properties': {'title': 'Frodo'},
        'description': [{'value': 'That is Frodo'}],
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Sam',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["sam_id"]}',
            'relationType': 'crm:OA7 has relationship to',
            'relationSystemClass': 'person',
            'relationDescription': None, 'type': 'Economical',
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'File without license',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["file_without_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'file',
            'relationDescription': None, 'type': None, 'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'The One Ring',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["ring_id"]}',
            'relationType': 'crm:P52i is current owner of',
            'relationSystemClass': 'artifact',
            'relationDescription': None, 'type': None, 'when': {
                'timespans': [
                    {'start': {'earliest': 'None', 'latest': 'None'},
                     'end': {'earliest': 'None',
                             'latest': 'None'}}]}}, {
            'label': 'Travel to Mordor',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["travel_id"]}',
            'relationType': 'crm:P11i participated in',
            'relationSystemClass': 'activity',
            'relationDescription': None, 'type': None, 'when': {
                'timespans': [
                    {'start': {'earliest': 'None', 'latest': 'None'},
                     'end': {'earliest': 'None',
                             'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': None,
        'depictions': [{
            '@id': f'http://local.host/api/0.2/entity/{test_ids["file_without_id"]}',
            'title': 'File without license',
            'license': None,
            'url': 'N/A'}]}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["shire_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'place',
        'properties': {'title': 'Shire'},
        'description': [
            {'value': 'The Shire was the homeland of the hobbits.'}],
        'when': {
            'timespans': [{
                'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]},
        'types': [{
            'identifier': f'http://local.host/api/0.2/entity/{test_ids["place_id"]}',
            'label': 'Place',
            'description': None,
            'hierarchy': '',
            'value': None,
            'unit': None}, {
            'identifier': f'http://local.host/api/0.2/entity/{test_ids["height_id"]}',
            'label': 'Height',
            'description': None,
            'hierarchy': 'Dimensions',
            'value': 23.0,
            'unit': 'centimeter'}],
        'relations': [{
            'label': 'Height',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["height_id"]}',
            'relationType': 'crm:P2 has type',
            'relationSystemClass': 'type',
            'relationDescription': '23.0',
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Home of Baggins',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["home_id"]}',
            'relationType': 'crm:P46 is composed of',
            'relationSystemClass': 'feature',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Location of Shire',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["location_shire_id"]}',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Place',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["place_id"]}',
            'relationType': 'crm:P2 has type',
            'relationSystemClass': 'type',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Sûza',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["suza_id"]}',
            'relationType': 'crm:P1 is identified by',
            'relationSystemClass': 'appellation',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'GeoNames',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["geonames_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'reference_system',
            'relationDescription': '2761369',
            'type': 'closeMatch',
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'https://lotr.fandom.com/',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["lotr_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'external_reference',
            'relationDescription': 'Fandom Wiki of lord of the rings',
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Picture with a License',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["picture_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'file',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': [{'alias': 'Sûza'}],
        'links': [{
            'type': 'closeMatch',
            'identifier': 'https://www.geonames.org/2761369',
            'referenceSystem': 'GeoNames'}],
        'geometry': {
            'type': 'Point',
            'coordinates': [9, 17],
            'title': '',
            'description': ''},
        'depictions': [{
            '@id': f'http://local.host/api/0.2/entity/{test_ids["picture_id"]}',
            'title': 'Picture with a License', 'license': 'Open license',
            'url': 'N/A'}]}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["mordor_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'place',
        'properties': {'title': 'Mordor'},
        'description': [{'value': 'The heart of evil.'}],
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': [{
            'identifier': f'http://local.host/api/0.2/entity/{test_ids["boundary_id"]}',
            'label': 'Boundary Mark',
            'description': None,
            'hierarchy': 'Place',
            'value': None,
            'unit': None}],
        'relations': [{
            'label': 'Boundary Mark',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["boundary_id"]}',
            'relationType': 'crm:P2 has type',
            'relationSystemClass': 'type',
            'relationDescription': None, 'type': None, 'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Location of Mordor',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["location_mordor_id"]}',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None, 'type': None, 'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': {'type': 'GeometryCollection', 'geometries': []},
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["kitchen_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'stratigraphic_unit',
        'properties': {'title': 'Kitchen'},
        'description': None,
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Location of Kitchen',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["location_kitchen_id"]}',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Home of Baggins',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["home_id"]}',
            'relationType': 'crm:P46i forms part of',
            'relationSystemClass': 'feature',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': {'type': 'GeometryCollection', 'geometries': []},
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["home_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'feature',
        'properties': {'title': 'Home of Baggins'},
        'description': None,
        'when': {'timespans': [{
            'start': {'earliest': 'None', 'latest': 'None'},
            'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Kitchen',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["kitchen_id"]}',
            'relationType': 'crm:P46 is composed of',
            'relationSystemClass': 'stratigraphic_unit',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Location of Home of Baggins',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["location_home_id"]}',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Shire',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["shire_id"]}',
            'relationType': 'crm:P46i forms part of',
            'relationSystemClass': 'place',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                    'end': {'earliest': '2019-01-31',
                            'latest': '2019-03-01'}}]}}],
        'names': None,
        'links': None,
        'geometry': {'type': 'GeometryCollection', 'geometries': []},
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["shire_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'place',
        'properties': {'title': 'Shire'},
        'description': [{
            'value': 'The Shire was the homeland of the hobbits.'}],
        'when': {
            'timespans': [{
                'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]},
        'types': [{
            'identifier': f'http://local.host/api/0.2/entity/{test_ids["place_id"]}',
            'label': 'Place',
            'description': None,
            'hierarchy': '',
            'value': None,
            'unit': None}, {
            'identifier': f'http://local.host/api/0.2/entity/{test_ids["height_id"]}',
            'label': 'Height',
            'description': None,
            'hierarchy': 'Dimensions',
            'value': 23.0,
            'unit': 'centimeter'}],
        'relations': [{
            'label': 'Height',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["height_id"]}',
            'relationType': 'crm:P2 has type',
            'relationSystemClass': 'type',
            'relationDescription': '23.0',
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Home of Baggins',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["home_id"]}',
            'relationType': 'crm:P46 is composed of',
            'relationSystemClass': 'feature',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Location of Shire',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["location_shire_id"]}',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Place',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["place_id"]}',
            'relationType': 'crm:P2 has type',
            'relationSystemClass': 'type',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Sûza',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["suza_id"]}',
            'relationType': 'crm:P1 is identified by',
            'relationSystemClass': 'appellation',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'GeoNames',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["geonames_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'reference_system',
            'relationDescription': '2761369',
            'type': 'closeMatch',
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'https://lotr.fandom.com/',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["lotr_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'external_reference',
            'relationDescription': 'Fandom Wiki of lord of the rings',
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Picture with a License',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["picture_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'file',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': [{'alias': 'Sûza'}],
        'links': [{
            'type': 'closeMatch',
            'identifier': 'https://www.geonames.org/2761369',
            'referenceSystem': 'GeoNames'}],
        'geometry': {
            'type': 'Point',
            'coordinates': [9, 17],
            'title': '',
            'description': ''},
        'depictions': [{
            '@id': f'http://local.host/api/0.2/entity/{test_ids["picture_id"]}',
            'title': 'Picture with a License', 'license': 'Open license',
            'url': 'N/A'}]}]}],
    'pagination': {
        'entities': 10,
        'entitiesPerPage': 20,
        'index': [{
            'page': test_ids["geonames_id"],
            'startId': test_ids["location_shire_id"]}],
        'totalPages': 1}}
test_query_first = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["sam_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E21 Person',
        'systemClass': 'person',
        'properties': {'title': 'Sam'},
        'description': [{'value': 'That is Sam'}],
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Frodo',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["frodo_id"]}',
            'relationType': 'crm:OA7 has relationship to',
            'relationSystemClass': 'person',
            'relationDescription': None,
            'type': 'Economical',
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Travel to Mordor',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["travel_id"]}',
            'relationType': 'crm:P14i performed',
            'relationSystemClass': 'activity',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': None,
        'depictions': None}]}],
    'pagination': {
        'entities': 8,
        'entitiesPerPage': 1,
        'index': [{
            'page': 1, 'startId': test_ids["location_shire_id"]}, {
            'page': 2, 'startId': test_ids["ring_id"]}, {
            'page': 3, 'startId': test_ids["frodo_id"]}, {
            'page': 4, 'startId': test_ids["sam_id"]}, {
            'page': 5, 'startId': test_ids["home_id"]}, {
            'page': 6, 'startId': test_ids["kitchen_id"]}, {
            'page': 7, 'startId': test_ids["mordor_id"]}, {
            'page': 8, 'startId': test_ids["shire_id"]}],
        'totalPages': 8}}
test_query_last = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["home_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'feature',
        'properties': {'title': 'Home of Baggins'},
        'description': None,
        'when': {'timespans': [{
            'start': {'earliest': 'None', 'latest': 'None'},
            'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Kitchen',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["kitchen_id"]}',
            'relationType': 'crm:P46 is composed of',
            'relationSystemClass': 'stratigraphic_unit',
            'relationDescription': None,
            'type': None, ''
                          'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Location of Home of Baggins',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["location_home_id"]}',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None, 'type': None, 'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Shire',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["shire_id"]}',
            'relationType': 'crm:P46i forms part of',
            'relationSystemClass': 'place',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                    'end': {'earliest': '2019-01-31',
                            'latest': '2019-03-01'}}]}}],
        'names': None,
        'links': None,
        'geometry': {'type': 'GeometryCollection', 'geometries': []},
        'depictions': None}]}],
    'pagination': {
        'entities': 8,
        'entitiesPerPage': 1,
        'index': [{
            'page': 1, 'startId': test_ids["location_shire_id"]}, {
            'page': 2, 'startId': test_ids["ring_id"]}, {
            'page': 3, 'startId': test_ids["frodo_id"]}, {
            'page': 4, 'startId': test_ids["sam_id"]}, {
            'page': 5, 'startId': test_ids["home_id"]}, {
            'page': 6, 'startId': test_ids["kitchen_id"]}, {
            'page': 7, 'startId': test_ids["mordor_id"]}, {
            'page': 8, 'startId': test_ids["shire_id"]}],
        'totalPages': 8}}
test_query_type = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["mordor_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'place',
        'properties': {'title': 'Mordor'},
        'description': [{'value': 'The heart of evil.'}],
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': [{
            'identifier': f'http://local.host/api/0.2/entity/{test_ids["boundary_id"]}',
            'label': 'Boundary Mark',
            'description': None,
            'hierarchy': 'Place',
            'value': None,
            'unit': None}],
        'relations': [{
            'label': 'Boundary Mark',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["boundary_id"]}',
            'relationType': 'crm:P2 has type',
            'relationSystemClass': 'type',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None',
                            'latest': 'None'}}]}}, {
            'label': 'Location of Mordor',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["location_mordor_id"]}',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': {'type': 'GeometryCollection', 'geometries': []},
        'depictions': None}]}],
    'pagination': {
        'entities': 1,
        'entitiesPerPage': 20,
        'index': [{
            'page': 1,
            'startId': test_ids["mordor_id"]}],
        'totalPages': 1}}
