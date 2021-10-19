class CidocClass:
    @staticmethod
    def get_test_cidoc_class(params):
        return {
            'results': [{
                '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
                'type': 'FeatureCollection',
                'features': [{
                    '@id': f'http://local.host/entity/{params["frodo_id"]}',
                    'type': 'Feature',
                    'crmClass': 'crm:E21 Person', 'systemClass': 'person',
                    'properties': {'title': 'Frodo'},
                    'description': [{'value': 'That is Frodo'}],
                    'when': {
                        'timespans': [{
                            'start': {'earliest': 'None', 'latest': 'None'},
                            'end': {'earliest': 'None', 'latest': 'None'}}]},
                    'types': None,
                    'relations': [{
                        'label': 'Sam',
                        'relationTo':
                            f'http://local.host/api/0.2/entity/{params["sam_id"]}',
                        'relationType': 'crm:OA7 has relationship to',
                        'relationSystemClass': 'person',
                        'relationDescription': None, 'type': 'Economical',
                        'when': {
                            'timespans': [{
                                'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}}, {
                        'label': 'File without license',
                        'relationTo': 'http://local.host/api/0.2/entity/115',
                        'relationType': 'crm:P67i is referred to by',
                        'relationSystemClass': 'file',
                        'relationDescription': None, 'type': None,
                        'when': {
                            'timespans': [{
                                'start': {
                                    'earliest': 'None',
                                    'latest': 'None'},
                                'end': {
                                    'earliest': 'None',
                                    'latest': 'None'}}]}}, {
                        'label': 'The One Ring',
                        'relationTo':
                            f'http://local.host/api/0.2/entity/{params["ring_id"]}',
                        'relationType': 'crm:P52i is current owner of',
                        'relationSystemClass': 'artifact',
                        'relationDescription': None, 'type': None,
                        'when': {
                            'timespans': [{
                                'start': {
                                    'earliest': 'None',
                                    'latest': 'None'},
                                'end': {
                                    'earliest': 'None',
                                    'latest': 'None'}}]}}, {
                        'label': 'Travel to Mordor',
                        'relationTo':
                            f'http://local.host/api/0.2/entity/{params["travel_id"]}',
                        'relationType': 'crm:P11i participated in',
                        'relationSystemClass': 'activity',
                        'relationDescription': None, 'type': None,
                        'when': {
                            'timespans': [{
                                'start': {
                                    'earliest': 'None',
                                    'latest': 'None'},
                                'end': {
                                    'earliest': 'None',
                                    'latest': 'None'}}]}}],
                    'names': None,
                    'links': None,
                    'geometry': None,
                    'depictions': [{
                        '@id': 'http://local.host/api/0.2/entity/115',
                        'title': 'File without license',
                        'license': None,
                        'url': 'N/A'}]}]}, {
                '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
                'type': 'FeatureCollection',
                'features': [{
                    '@id': f'http://local.host/entity/{params["sam_id"]}',
                    'type': 'Feature',
                    'crmClass': 'crm:E21 Person',
                    'systemClass': 'person',
                    'properties': {'title': 'Sam'},
                    'description': [{'value': 'That is Sam'}],
                    'when': {
                        'timespans': [{
                            'start': {
                                'earliest': 'None',
                                'latest': 'None'},
                            'end': {
                                'earliest': 'None',
                                'latest': 'None'}}]},
                    'types': None,
                    'relations': [{
                        'label': 'Frodo',
                        'relationTo':
                            f'http://local.host/api/0.2/entity/{params["frodo_id"]}',
                        'relationType': 'crm:OA7 has relationship to',
                        'relationSystemClass': 'person',
                        'relationDescription': None,
                        'type': 'Economical',
                        'when': {
                            'timespans': [{
                                'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}}, {
                        'label': 'Travel to Mordor',
                        'relationTo':
                            f'http://local.host/api/0.2/entity/{params["travel_id"]}',
                        'relationType': 'crm:P14i performed',
                        'relationSystemClass': 'activity',
                        'relationDescription': None,
                        'type': None,
                        'when': {
                            'timespans': [{
                                'start': {
                                    'earliest': 'None',
                                    'latest': 'None'},
                                'end': {
                                    'earliest': 'None',
                                    'latest': 'None'}}]}}],
                    'names': None,
                    'links': None,
                    'geometry': None,
                    'depictions': None}]}],
            'pagination': {
                'entities': 2,
                'entitiesPerPage': 20,
                'index': [{'page': 1, 'startId': params["frodo_id"]}],
                'totalPages': 1}}

    @staticmethod
    def get_test_cidoc_class_show_none(params):
        return {'results': [{
            '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
            'type': 'FeatureCollection',
            'features': [{
                '@id': f'http://local.host/entity/{params["frodo_id"]}',
                'type': 'Feature',
                'crmClass': 'crm:E21 Person',
                'systemClass': 'person',
                'properties': {'title': 'Frodo'},
                'description': [{'value': 'That is Frodo'}],
                'geometry': None}]}, {
            '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
            'type': 'FeatureCollection',
            'features': [{
                '@id': f'http://local.host/entity/{params["sam_id"]}',
                'type': 'Feature',
                'crmClass': 'crm:E21 Person',
                'systemClass': 'person',
                'properties': {'title': 'Sam'},
                'description': [{'value': 'That is Sam'}],
                'geometry': None}]}],
            'pagination': {
                'entities': 2,
                'entitiesPerPage': 20,
                'index': [{'page': 1, 'startId': params["frodo_id"]}],
                'totalPages': 1}}
