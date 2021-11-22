class EntitiesLinked:
    @staticmethod
    def get_test_entities_linked_to(params):
        return {'results': [
            {
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
                            f'http://local.host/api/0.3/entity/{params["sam_id"]}',
                        'relationType': 'crm:OA7 has relationship to',
                        'relationSystemClass': 'person',
                        'relationDescription': None,
                        'type': 'Economical',
                        'when': {
                            'timespans': [{
                                'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}}, {
                        "label": "The ring bearer",
                        "relationTo": f'http://local.host/api/0.3/entity/{params["alias2_id"]}',
                        "relationType": "crm:P131 is identified by",
                        "relationSystemClass": "actor_appellation",
                        "relationDescription": None,
                        "type": None,
                        "when": {
                            "timespans": [{
                                "start": {
                                    "earliest": 'None',
                                    "latest": 'None'},
                                "end": {
                                    "earliest": 'None',
                                    "latest": 'None'}}]}}, {
                        'label': 'File without license',
                        'relationTo': 'http://local.host/api/0.3/entity/115',
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
                            f'http://local.host/api/0.3/entity/{params["ring_id"]}',
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
                            f'http://local.host/api/0.3/entity/{params["travel_id"]}',
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
                    'names': [{'alias': 'The ring bearer'}],
                    'links': None,
                    'geometry': None,
                    'depictions': [{
                        '@id': 'http://local.host/api/0.3/entity/115',
                        'title': 'File without license',
                        'license': None,
                        'url': 'N/A'}]}]},
            {
                '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
                'type': 'FeatureCollection', 'features': [{
                    '@id': f'http://local.host/entity/{params["location_shire_id"]}',
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
                        'label': 'Sam',
                        'relationTo': f'http://local.host/api/0.3/entity/{params["sam_id"]}',
                        'relationType': 'crm:P74i is current or former residence of',
                        'relationSystemClass': 'person',
                        'relationDescription': None,
                        'type': None,
                        'when': {
                            'timespans': [{
                                'start': {
                                    'earliest': 'None',
                                    'latest': 'None'},
                                'end': {
                                    'earliest': 'None',
                                    'latest': 'None'}}]}}, {
                        'label': 'Shire',
                        'relationTo':
                            f'http://local.host/api/0.3/entity/{params["shire_id"]}',
                        'relationType': 'crm:P53i is former or current location of',
                        'relationSystemClass': 'place',
                        'relationDescription': None,
                        'type': None,
                        'when': {
                            'timespans': [{
                                'start': {'earliest': '2018-01-31',
                                          'latest': '2018-03-01'},
                                'end': {
                                    'earliest': '2019-01-31',
                                    'latest': '2019-03-01'}}]}},
                        {'label': 'Travel to Mordor',
                         'relationTo': f'http://local.host/api/0.3/entity/{params["travel_id"]}',
                         'relationType': 'crm:P7i witnessed',
                         'relationSystemClass': 'activity',
                         'relationDescription': None,
                         'type': None,
                         'when': {
                             'timespans': [{
                                 'start': {'earliest': 'None',
                                           'latest': 'None'},
                                 'end': {'earliest': 'None',
                                         'latest': 'None'}}]}}],
                    'names': None,
                    'links': None,
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [9, 17],
                        'title': '',
                        'description': ''},
                    'depictions': None}]},
            {
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
                    'relations': [
                        {
                            'label': 'Location of Shire',
                            'relationTo': f'http://local.host/api/0.3/entity/{params["location_shire_id"]}',
                            'relationType': 'crm:P74 has current or former residence',
                            'relationSystemClass': 'object_location',
                            'relationDescription': None,
                            'type': None,
                            'when': {
                                'timespans': [{
                                    'start': {
                                        'earliest': 'None',
                                        'latest': 'None'},
                                    'end': {
                                        'earliest': 'None',
                                        'latest': 'None'}}]}}, {
                            'label': 'Frodo',
                            'relationTo':
                                f'http://local.host/api/0.3/entity/{params["frodo_id"]}',
                            'relationType': 'crm:OA7 has relationship to',
                            'relationSystemClass': 'person',
                            'relationDescription': None,
                            'type': 'Economical',
                            'when': {
                                'timespans': [{
                                    'start': {'earliest': 'None',
                                              'latest': 'None'},
                                    'end': {'earliest': 'None',
                                            'latest': 'None'}}]}}, {
                            'label': 'Travel to Mordor',
                            'relationTo':
                                f'http://local.host/api/0.3/entity/{params["travel_id"]}',
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
                'entities': 3,
                'entitiesPerPage': 20,
                'index': [{'page': 1, 'startId': params["frodo_id"]}],
                'totalPages': 1}}
