class Search:
    @staticmethod
    def get_test_search_1(params):
        return {"results": [
            {
                '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
                'type': 'FeatureCollection', 'features': [{
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
                    'identifier': f'http://local.host/api/entity/{params["boundary_mark_id"]}',
                    'label': 'Boundary Mark', 'description': None,
                    'hierarchy': 'Place', 'value': None, 'unit': None}],
                'relations': [{
                    'label': 'Boundary Mark',
                    'relationTo': f'http://local.host/api/entity/{params["boundary_mark_id"]}',
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
                    'relationTo': f'http://local.host/api/entity/{params["location_mordor_id"]}',
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
                'depictions': None}]},
            {
                '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
                'type': 'FeatureCollection',
                'features': [{
                    '@id': f'http://local.host/entity/{params["shire_id"]}',
                    'type': 'Feature',
                    'crmClass': 'crm:E18 Physical Thing',
                    'systemClass': 'place',
                    'properties': {'title': 'Shire'},
                    'description': [
                        {
                            'value': 'The Shire was the homeland of the hobbits.'}],
                    'when': {
                        'timespans': [{
                            'start': {'earliest': '2018-01-31',
                                      'latest': '2018-03-01'},
                            'end': {'earliest': '2019-01-31',
                                    'latest': '2019-03-01'}}]},
                    'types': [{
                        'identifier': f'http://local.host/api/entity/{params["place_id"]}',
                        'label': 'Place', 'description': None, 'hierarchy': '',
                        'value': None, 'unit': None}, {
                        'identifier': f'http://local.host/api/entity/{params["height_id"]}',
                        'label': 'Height', 'description': None,
                        'hierarchy': 'Dimensions',
                        'value': 23.0,
                        'unit': 'centimeter'}],
                    'relations': [{
                        'label': 'Height',
                        'relationTo': f'http://local.host/api/entity/{params["height_id"]}',
                        'relationType': 'crm:P2 has type',
                        'relationSystemClass': 'type',
                        'relationDescription': '23.0',
                        'type': None,
                        'when': {
                            'timespans': [{
                                'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}}, {
                        'label': 'Home of Baggins',
                        'relationTo': f'http://local.host/api/entity/{params["home_id"]}',
                        'relationType': 'crm:P46 is composed of',
                        'relationSystemClass': 'feature',
                        'relationDescription': None,
                        'type': None,
                        'when': {
                            'timespans': [{
                                'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}}, {
                        'label': 'Location of Shire',
                        'relationTo': f'http://local.host/api/entity/{params["location_shire_id"]}',
                        'relationType': 'crm:P53 has former or current location',
                        'relationSystemClass': 'object_location',
                        'relationDescription': None,
                        'type': None,
                        'when': {
                            'timespans': [{
                                'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}}, {
                        'label': 'Place',
                        'relationTo': f'http://local.host/api/entity/{params["place_id"]}',
                        'relationType': 'crm:P2 has type',
                        'relationSystemClass': 'type',
                        'relationDescription': None,
                        'type': None,
                        'when': {
                            'timespans': [{
                                'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}}, {
                        'label': 'Sûza',
                        'relationTo': f'http://local.host/api/entity/{params["suza_id"]}',
                        'relationType': 'crm:P1 is identified by',
                        'relationSystemClass': 'appellation',
                        'relationDescription': None,
                        'type': None,
                        'when': {
                            'timespans': [{
                                'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}}, {
                        'label': 'GeoNames',
                        'relationTo': f'http://local.host/api/entity/{params["geonames_id"]}',
                        'relationType': 'crm:P67i is referred to by',
                        'relationSystemClass': 'reference_system',
                        'relationDescription': '2761369',
                        'type': 'closeMatch',
                        'when': {
                            'timespans': [{
                                'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}}, {
                        'label': 'https://lotr.fandom.com/',
                        'relationTo': f'http://local.host/api/entity/{params["lotr_id"]}',
                        'relationType': 'crm:P67i is referred to by',
                        'relationSystemClass': 'external_reference',
                        'relationDescription': 'Fandom Wiki of lord of the rings',
                        'type': None,
                        'when': {
                            'timespans': [{
                                'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}}, {
                        'label': 'Picture with a License',
                        'relationTo': f'http://local.host/api/entity/{params["picture_id"]}',
                        'relationType': 'crm:P67i is referred to by',
                        'relationSystemClass': 'file',
                        'relationDescription': None,
                        'type': None,
                        'when': {
                            'timespans': [{
                                'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}}],
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
                        '@id': f'http://local.host/api/entity/{params["picture_id"]}',
                        'title': 'Picture with a License',
                        'license': 'Open license',
                        'url': 'N/A'}]}]}
        ],
            "pagination": {
                "entities": 2,
                "entitiesPerPage": 20,
                "index": [
                    {
                        "page": 1,
                        "startId": params["mordor_id"]
                    }
                ],
                "totalPages": 1
            }
        }

    @staticmethod
    def get_test_search_2(params):
        return {
            "results": [
                {
                    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
                    'type': 'FeatureCollection',
                    'features': [{
                        '@id': f'http://local.host/entity/{params["shire_id"]}',
                        'type': 'Feature',
                        'crmClass': 'crm:E18 Physical Thing',
                        'systemClass': 'place',
                        'properties': {'title': 'Shire'},
                        'description': [
                            {
                                'value': 'The Shire was the homeland of the hobbits.'}],
                        'when': {
                            'timespans': [{
                                'start': {'earliest': '2018-01-31',
                                          'latest': '2018-03-01'},
                                'end': {'earliest': '2019-01-31',
                                        'latest': '2019-03-01'}}]},
                        'types': [{
                            'identifier': f'http://local.host/api/entity/{params["place_id"]}',
                            'label': 'Place', 'description': None,
                            'hierarchy': '',
                            'value': None, 'unit': None}, {
                            'identifier': f'http://local.host/api/entity/{params["height_id"]}',
                            'label': 'Height', 'description': None,
                            'hierarchy': 'Dimensions',
                            'value': 23.0,
                            'unit': 'centimeter'}],
                        'relations': [{
                            'label': 'Height',
                            'relationTo': f'http://local.host/api/entity/{params["height_id"]}',
                            'relationType': 'crm:P2 has type',
                            'relationSystemClass': 'type',
                            'relationDescription': '23.0',
                            'type': None,
                            'when': {
                                'timespans': [{
                                    'start': {'earliest': 'None',
                                              'latest': 'None'},
                                    'end': {'earliest': 'None',
                                            'latest': 'None'}}]}}, {
                            'label': 'Home of Baggins',
                            'relationTo': f'http://local.host/api/entity/{params["home_id"]}',
                            'relationType': 'crm:P46 is composed of',
                            'relationSystemClass': 'feature',
                            'relationDescription': None,
                            'type': None,
                            'when': {
                                'timespans': [{
                                    'start': {'earliest': 'None',
                                              'latest': 'None'},
                                    'end': {'earliest': 'None',
                                            'latest': 'None'}}]}}, {
                            'label': 'Location of Shire',
                            'relationTo': f'http://local.host/api/entity/{params["location_shire_id"]}',
                            'relationType': 'crm:P53 has former or current location',
                            'relationSystemClass': 'object_location',
                            'relationDescription': None,
                            'type': None,
                            'when': {
                                'timespans': [{
                                    'start': {'earliest': 'None',
                                              'latest': 'None'},
                                    'end': {'earliest': 'None',
                                            'latest': 'None'}}]}}, {
                            'label': 'Place',
                            'relationTo': f'http://local.host/api/entity/{params["place_id"]}',
                            'relationType': 'crm:P2 has type',
                            'relationSystemClass': 'type',
                            'relationDescription': None,
                            'type': None,
                            'when': {
                                'timespans': [{
                                    'start': {'earliest': 'None',
                                              'latest': 'None'},
                                    'end': {'earliest': 'None',
                                            'latest': 'None'}}]}}, {
                            'label': 'Sûza',
                            'relationTo': f'http://local.host/api/entity/{params["suza_id"]}',
                            'relationType': 'crm:P1 is identified by',
                            'relationSystemClass': 'appellation',
                            'relationDescription': None,
                            'type': None,
                            'when': {
                                'timespans': [{
                                    'start': {'earliest': 'None',
                                              'latest': 'None'},
                                    'end': {'earliest': 'None',
                                            'latest': 'None'}}]}}, {
                            'label': 'GeoNames',
                            'relationTo': f'http://local.host/api/entity/{params["geonames_id"]}',
                            'relationType': 'crm:P67i is referred to by',
                            'relationSystemClass': 'reference_system',
                            'relationDescription': '2761369',
                            'type': 'closeMatch',
                            'when': {
                                'timespans': [{
                                    'start': {'earliest': 'None',
                                              'latest': 'None'},
                                    'end': {'earliest': 'None',
                                            'latest': 'None'}}]}}, {
                            'label': 'https://lotr.fandom.com/',
                            'relationTo': f'http://local.host/api/entity/{params["lotr_id"]}',
                            'relationType': 'crm:P67i is referred to by',
                            'relationSystemClass': 'external_reference',
                            'relationDescription': 'Fandom Wiki of lord of the rings',
                            'type': None,
                            'when': {
                                'timespans': [{
                                    'start': {'earliest': 'None',
                                              'latest': 'None'},
                                    'end': {'earliest': 'None',
                                            'latest': 'None'}}]}}, {
                            'label': 'Picture with a License',
                            'relationTo': f'http://local.host/api/entity/{params["picture_id"]}',
                            'relationType': 'crm:P67i is referred to by',
                            'relationSystemClass': 'file',
                            'relationDescription': None,
                            'type': None,
                            'when': {
                                'timespans': [{
                                    'start': {'earliest': 'None',
                                              'latest': 'None'},
                                    'end': {'earliest': 'None',
                                            'latest': 'None'}}]}}],
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
                            '@id': f'http://local.host/api/entity/{params["picture_id"]}',
                            'title': 'Picture with a License',
                            'license': 'Open license',
                            'url': 'N/A'}]}]}
            ],
            "pagination": {
                "entities": 1,
                "entitiesPerPage": 20,
                "index": [
                    {
                        "page": 1,
                        "startId": params["shire_id"]
                    }
                ],
                "totalPages": 1
            }
        }

    @staticmethod
    def get_test_search_3(params):
        return {
            'results': [
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
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]},
                        'types': None,
                        'relations': [{
                            'label': 'Sam',
                            'relationTo':
                                f'http://local.host/api/entity/{params["sam_id"]}',
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
                            "label": "The ring bearer",
                            "relationTo": f'http://local.host/api/entity/{params["alias2_id"]}',
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
                            'relationTo': 'http://local.host/api/entity/115',
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
                                f'http://local.host/api/entity/{params["ring_id"]}',
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
                                f'http://local.host/api/entity/{params["travel_id"]}',
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
                            '@id': 'http://local.host/api/entity/115',
                            'title': 'File without license',
                            'license': None,
                            'url': 'N/A'}]}]},
                {
                '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
                'type': 'FeatureCollection',
                'features': [{
                    '@id': f'http://local.host/entity/{params["home_id"]}',
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
                        'relationTo': f'http://local.host/api/entity/{params["kitchen_id"]}',
                        'relationType': 'crm:P46 is composed of',
                        'relationSystemClass': 'stratigraphic_unit',
                        'relationDescription': None,
                        'type': None,
                        'when': {
                            'timespans': [{
                                'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}}, {
                        'label': 'Location of Home of Baggins',
                        'relationTo': f'http://local.host/api/entity/{params["location_home_id"]}',
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
                        'relationTo': f'http://local.host/api/entity/{params["shire_id"]}',
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
                    'depictions': None}]},
                {
                '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
                'type': 'FeatureCollection',
                'features': [{
                    '@id': f'http://local.host/entity/{params["kitchen_id"]}',
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
                        'relationTo': f'http://local.host/api/entity/{params["location_kitchen_id"]}',
                        'relationType': 'crm:P53 has former or current location',
                        'relationSystemClass': 'object_location',
                        'relationDescription': None,
                        'type': None,
                        'when': {
                            'timespans': [{
                                'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}}, {
                        'label': 'Home of Baggins',
                        'relationTo': f'http://local.host/api/entity/{params["home_id"]}',
                        'relationType': 'crm:P46i forms part of',
                        'relationSystemClass': 'feature',
                        'relationDescription': None,
                        'type': None,
                        'when': {
                            'timespans': [{
                                'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}}],
                    'names': None,
                    'links': None,
                    'geometry': {
                        'type': 'GeometryCollection',
                        'geometries': []},
                    'depictions': None}]},
                {
                    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
                    'type': 'FeatureCollection', 'features': [{
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
                        'identifier': f'http://local.host/api/entity/{params["boundary_mark_id"]}',
                        'label': 'Boundary Mark', 'description': None,
                        'hierarchy': 'Place', 'value': None, 'unit': None}],
                    'relations': [{
                        'label': 'Boundary Mark',
                        'relationTo': f'http://local.host/api/entity/{params["boundary_mark_id"]}',
                        'relationType': 'crm:P2 has type',
                        'relationSystemClass': 'type',
                        'relationDescription': None,
                        'type': None,
                        'when': {
                            'timespans': [{
                                'start': {
                                    'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}}, {
                        'label': 'Location of Mordor',
                        'relationTo': f'http://local.host/api/entity/{params["location_mordor_id"]}',
                        'relationType': 'crm:P53 has former or current location',
                        'relationSystemClass': 'object_location',
                        'relationDescription': None,
                        'type': None,
                        'when': {
                            'timespans': [{
                                'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}}],
                    'names': None,
                    'links': None,
                    'geometry': {'type': 'GeometryCollection',
                                 'geometries': []},
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
                                'relationTo': f'http://local.host/api/entity/{params["location_shire_id"]}',
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
                                    f'http://local.host/api/entity/{params["frodo_id"]}',
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
                                    f'http://local.host/api/entity/{params["travel_id"]}',
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
                        'depictions': None}]},
                {
                    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
                    'type': 'FeatureCollection',
                    'features': [{
                        '@id': f'http://local.host/entity/{params["ring_id"]}',
                        'type': 'Feature',
                        'crmClass': 'crm:E22 Man-Made Object',
                        'systemClass': 'artifact',
                        'properties': {'title': 'The One Ring'},
                        'description': None,
                        'when': {
                            'timespans': [{
                                'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]},
                        'types': None,
                        'relations': [{
                            'label': 'Frodo',
                            'relationTo': f'http://local.host/api/entity/{params["frodo_id"]}',
                            'relationType': 'crm:P52 has current owner',
                            'relationSystemClass': 'person',
                            'relationDescription': None,
                            'type': None,
                            'when': {
                                'timespans': [{
                                    'start': {'earliest': 'None',
                                              'latest': 'None'},
                                    'end': {'earliest': 'None',
                                            'latest': 'None'}}]}}, {
                            'label': 'Location of The One Ring',
                            'relationTo': f'http://local.host/api/entity/{params["location_ring_id"]}',
                            'relationType': 'crm:P53 has former or current location',
                            'relationSystemClass': 'object_location',
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
                            'type': 'GeometryCollection',
                            'geometries': []},
                        'depictions': None}]}
            ],
            'pagination': {
                'entities': 6,
                'entitiesPerPage': 20,
                'index': [{
                    'page': 1,
                    'startId': params["frodo_id"]}],
                'totalPages': 1}}

    @staticmethod
    def get_test_search_4(params):
        return {
            'results': [
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
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]},
                        'types': None,
                        'relations': [{
                            'label': 'Sam',
                            'relationTo':
                                f'http://local.host/api/entity/{params["sam_id"]}',
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
                            "label": "The ring bearer",
                            "relationTo": f'http://local.host/api/entity/{params["alias2_id"]}',
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
                            'relationTo': 'http://local.host/api/entity/115',
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
                                f'http://local.host/api/entity/{params["ring_id"]}',
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
                                f'http://local.host/api/entity/{params["travel_id"]}',
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
                            '@id': 'http://local.host/api/entity/115',
                            'title': 'File without license',
                            'license': None,
                            'url': 'N/A'}]}]},
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
                                'relationTo': f'http://local.host/api/entity/{params["location_shire_id"]}',
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
                                    f'http://local.host/api/entity/{params["frodo_id"]}',
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
                                    f'http://local.host/api/entity/{params["travel_id"]}',
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
                        'depictions': None}]},
            ],
            'pagination': {
                'entities': 2,
                'entitiesPerPage': 20,
                'index': [{
                    'page': 1,
                    'startId': params["frodo_id"]}],
                'totalPages': 1}}
