class Latest:
    @staticmethod
    def get_test_latest(params):
        return {'results': [{
            '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
            'type': 'FeatureCollection',
            'features': [{
            '@id': f'http://local.host/entity/{params["silmarillion_id"]}',
            'type': 'Feature',
            'crmClass': 'crm:E33 Linguistic Object',
            'systemClass': 'source',
            'properties': {'title': 'Silmarillion'},
            'description': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]},
            'types': None,
            'relations': None,
            'names': None,
            'links': None,
            'geometry': None,
            'depictions': None}]}, {
        '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
        'type': 'FeatureCollection',
        'features': [{
            '@id': f'http://local.host/entity/{params["mordor_id"]}',
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
                'identifier':
                    f'http://local.host/api/0.2/entity/{params["boundary_mark_id"]}',
                'label': 'Boundary Mark', 'description': None,
                'hierarchy': 'Place', 'value': None, 'unit': None}],
            'relations': [{
                'label': 'Boundary Mark',
                'relationTo': f'http://local.host/api/0.2/entity/{params["boundary_mark_id"]}',
                'relationType': 'crm:P2 has type',
                'relationSystemClass': 'type',
                'relationDescription': None,
                'type': None,
                'when': {
                    'timespans': [{
                        'start': {'earliest': 'None', 'latest': 'None'},
                        'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
                'label': 'Location of Mordor',
                'relationTo':
                    f'http://local.host/api/0.2/entity/{params["location_mordor_id"]}',
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
            'entities': 2,
            'entitiesPerPage': 20,
            'index': [{'page': 1, 'startId': params["silmarillion_id"]}],
            'totalPages': 1}}
