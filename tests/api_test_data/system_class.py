import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_params import test_ids

test_system_class = {'results': [{
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
            'timespans': [{'start': {'earliest': 'None', 'latest': 'None'},
                           'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Frodo',
            'relationTo': 'http://local.host/api/0.2/entity/113',
            'relationType': 'crm:P52 has current owner',
            'relationSystemClass': 'person',
            'relationDescription': None,
            'type': None,
            'when':
                {'timespans': [
                    {'start': {'earliest': 'None', 'latest': 'None'},
                     'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Location of The One Ring',
            'relationTo': 'http://local.host/api/0.2/entity/117',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None,
            'type': None, 'when': {'timespans': [{
                'start': {
                    'earliest': 'None',
                    'latest': 'None'},
                'end': {
                    'earliest': 'None',
                    'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': {'type': 'GeometryCollection', 'geometries': []},
        'depictions': None}]}],
    'pagination': {
        'entities': 1,
        'entitiesPerPage': 20,
        'index': [{'page': 1, 'startId': test_ids["ring_id"]}],
        'totalPages': 1}}