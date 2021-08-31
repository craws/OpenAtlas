api_linked_place_template = {
    "@context": "https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld",
    "type": "FeatureCollection",
    "features": [
        {
            "@id": "http://local.host/entity/104",
            "type": "Feature",
            "crmClass": "crm:E18 Physical Thing",
            "systemClass": "place",
            "properties": {
                "title": "Nostromos"
            },
            "description": [
                {
                    "value": "That is the Nostromos"
                }
            ],
            "when": {
                "timespans": [
                    {
                        "start": {
                            "earliest": "2018-01-31",
                            "latest": "2018-03-01"
                        },
                        "end": {
                            "earliest": "2019-01-31",
                            "latest": "2019-03-01"
                        }
                    }
                ]
            },
            "types": [
                {
                    "identifier": "http://local.host/api/0.2/entity/65",
                    "label": "Place",
                    "description": None,
                    "hierarchy": "",
                    "value": None,
                    "unit": None
                },
                {
                    "identifier": "http://local.host/api/0.2/entity/102",
                    "label": "Height",
                    "description": None,
                    "hierarchy": "Dimensions",
                    "value": 23,
                    "unit": "centimeter"
                }
            ],
            "relations": [
                {
                    "label": "Cargo hauler",
                    "relationTo": "http://local.host/api/0.2/entity/106",
                    "relationType": "crm:P1 is identified by",
                    "relationSystemClass": "appellation",
                    "type": None,
                    "when": {
                        "timespans": [
                            {
                                "start": {
                                    "earliest": None,
                                    "latest": None
                                },
                                "end": {
                                    "earliest": None,
                                    "latest": None
                                }
                            }
                        ]
                    }
                },
                {
                    "label": "Feature",
                    "relationTo": "http://local.host/api/0.2/entity/108",
                    "relationType": "crm:P46 is composed of",
                    "relationSystemClass": "feature",
                    "type": None,
                    "when": {
                        "timespans": [
                            {
                                "start": {
                                    "earliest": None,
                                    "latest": None
                                },
                                "end": {
                                    "earliest": None,
                                    "latest": None
                                }
                            }
                        ]
                    }
                },
                {
                    "label": "Height",
                    "relationTo": "http://local.host/api/0.2/entity/102",
                    "relationType": "crm:P2 has type",
                    "relationSystemClass": "type",
                    "type": None,
                    "when": {
                        "timespans": [
                            {
                                "start": {
                                    "earliest": None,
                                    "latest": None
                                },
                                "end": {
                                    "earliest": None,
                                    "latest": None
                                }
                            }
                        ]
                    }
                },
                {
                    "label": "Location of Nostromos",
                    "relationTo": "http://local.host/api/0.2/entity/105",
                    "relationType": "crm:P53 has former or current location",
                    "relationSystemClass": "object_location",
                    "type": None,
                    "when": {
                        "timespans": [
                            {
                                "start": {
                                    "earliest": None,
                                    "latest": None
                                },
                                "end": {
                                    "earliest": None,
                                    "latest": None
                                }
                            }
                        ]
                    }
                },
                {
                    "label": "Place",
                    "relationTo": "http://local.host/api/0.2/entity/65",
                    "relationType": "crm:P2 has type",
                    "relationSystemClass": "type",
                    "type": None,
                    "when": {
                        "timespans": [
                            {
                                "start": {
                                    "earliest": None,
                                    "latest": None
                                },
                                "end": {
                                    "earliest": None,
                                    "latest": None
                                }
                            }
                        ]
                    }
                },
                {
                    "label": "Datei",
                    "relationTo": "http://local.host/api/0.2/entity/112",
                    "relationType": "crm:P67i is referred to by",
                    "relationSystemClass": "file",
                    "type": None,
                    "when": {
                        "timespans": [
                            {
                                "start": {
                                    "earliest": None,
                                    "latest": None
                                },
                                "end": {
                                    "earliest": None,
                                    "latest": None
                                }
                            }
                        ]
                    }
                },
                {
                    "label": "GeoNames",
                    "relationTo": "http://local.host/api/0.2/entity/1",
                    "relationType": "crm:P67i is referred to by",
                    "relationSystemClass": "reference_system",
                    "type": "close match",
                    "when": {
                        "timespans": [
                            {
                                "start": {
                                    "earliest": None,
                                    "latest": None
                                },
                                "end": {
                                    "earliest": None,
                                    "latest": None
                                }
                            }
                        ]
                    }
                },
                {
                    "label": "https://openatlas.eu",
                    "relationTo": "http://local.host/api/0.2/entity/107",
                    "relationType": "crm:P67i is referred to by",
                    "relationSystemClass": "external_reference",
                    "type": None,
                    "when": {
                        "timespans": [
                            {
                                "start": {
                                    "earliest": None,
                                    "latest": None
                                },
                                "end": {
                                    "earliest": None,
                                    "latest": None
                                }
                            }
                        ]
                    }
                }
            ],
            "names": [
                {
                    "alias": "Cargo hauler"
                }
            ],
            "links": [
                {
                    "type": "close match",
                    "identifier": "https://www.geonames.org/2761369",
                    "referenceSystem": "GeoNames"
                }
            ],
            "geometry": {
                "type": "Point",
                "coordinates": [
                    9,
                    17
                ],
                "title": "",
                "description": ""
            },
            "depictions": [
                {
                    "@id": "http://local.host/api/0.2/entity/112",
                    "title": "Datei",
                    "license": "Open license",
                    "url": "N/A"
                }
            ]
        }
    ]
}

api_geojson_template = {'type': 'FeatureCollection', 'features': [
    {'type': 'Feature',
     'geometry': {'type': 'Point', 'coordinates': [9, 17], 'title': '',
                  'description': ''},
     'properties': {'@id': 104, 'systemClass': 'place', 'name': 'Nostromos',
                    'description': 'That is the Nostromos',
                    'begin_earliest': '2018-01-31',
                    'begin_latest': '2018-03-01',
                    'begin_comment': 'Begin of the Nostromos',
                    'end_earliest': '2019-01-31', 'end_latest': '2019-03-01',
                    'end_comment': 'Destruction of the Nostromos',
                    'types': ['Place', 'Height']}}]}

api_geometries_template = {
    'features': [{'geometry': {'coordinates': [9, 17], 'type': 'Point'},
                  'properties': {'description': '',
                                 'id': 1,
                                 'name': '',
                                 'objectDescription': 'That is the Nostromos',
                                 'objectId': 104,
                                 'objectName': 'Nostromos',
                                 'objectType': None,
                                 'shapeType': 'centerpoint'},
                  'type': 'Feature'}],
    'type': 'FeatureCollection'}

api_content_en = {'contact': '',
                  'imageSizes': {'table': '100', 'thumbnail': '200'},
                  'intro': 'This is English',
                  'legalNotice': '',
                  'siteName': ''}
api_content_de = {'contact': '',
                  'imageSizes': {'table': '100', 'thumbnail': '200'},
                  'intro': 'Das ist Deutsch',
                  'legalNotice': '',
                  'siteName': ''}
api_system_class_count = {'move': 0, 'bibliography': 0, 'person': 0,
                          'acquisition': 0,
                          'reference_system': 2, 'feature': 1, 'file': 1,
                          'activity': 0, 'type': 87,
                          'administrative_unit': 14, 'artifact': 0,
                          'source_translation': 0,
                          'place': 1, 'stratigraphic_unit': 1, 'edition': 0,
                          'group': 0,
                          'source': 0}

api_overview_count = [{'systemClass': 'external_reference', 'count': 1},
                      {'systemClass': 'reference_system', 'count': 2},
                      {'systemClass': 'file', 'count': 1},
                      {'systemClass': 'feature', 'count': 1},
                      {'systemClass': 'type', 'count': 87},
                      {'systemClass': 'administrative_unit', 'count': 14},
                      {'systemClass': 'place', 'count': 1},
                      {'systemClass': 'stratigraphic_unit', 'count': 1}]

api_node_entities = {
    'nodes': [{'id': 84, 'label': 'Austria',
               'url': 'http://local.host/api/0.2/entity/84'},
              {'id': 89, 'label': 'Czech Republic',
               'url': 'http://local.host/api/0.2/entity/89'},
              {'id': 87, 'label': 'Germany',
               'url': 'http://local.host/api/0.2/entity/87'},
              {'id': 88, 'label': 'Italy',
               'url': 'http://local.host/api/0.2/entity/88'},
              {'id': 90, 'label': 'Slovakia',
               'url': 'http://local.host/api/0.2/entity/90'},
              {'id': 91, 'label': 'Slovenia',
               'url': 'http://local.host/api/0.2/entity/91'}]}

api_node_entities_all = {
    'nodes': [{'id': 84, 'label': 'Austria',
               'url': 'http://local.host/api/0.2/entity/84'},
              {'id': 89, 'label': 'Czech Republic',
               'url': 'http://local.host/api/0.2/entity/89'},
              {'id': 87, 'label': 'Germany',
               'url': 'http://local.host/api/0.2/entity/87'},
              {'id': 88, 'label': 'Italy',
               'url': 'http://local.host/api/0.2/entity/88'},
              {'id': 90, 'label': 'Slovakia',
               'url': 'http://local.host/api/0.2/entity/90'},
              {'id': 91, 'label': 'Slovenia',
               'url': 'http://local.host/api/0.2/entity/91'},
              {'id': 86, 'label': 'Niederösterreich',
               'url': 'http://local.host/api/0.2/entity/86'},
              {'id': 85, 'label': 'Wien',
               'url': 'http://local.host/api/0.2/entity/85'}]}

api_subunit = {
    'nodes': [{'id': 108, 'label': 'Feature',
               'url': 'http://local.host/api/0.2/entity/108'}]}

api_subunit_hierarchy = {
    'nodes': [{'id': 108, 'label': 'Feature',
               'url': 'http://local.host/api/0.2/entity/108'},
              {'id': 110, 'label': 'Strato',
               'url': 'http://local.host/api/0.2/entity/110'}]}


api_code_reference = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/107', 'type': 'Feature',
         'crmClass': 'crm:E31 Document',
         'systemClass': 'external_reference',
         'properties': {'title': 'https://openatlas.eu'},
         'description': None,
         'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                 'end': {'earliest': None, 'latest': None}}]},
         'types': None, 'relations': [
            {'label': 'Nostromos',
             'relationTo': 'http://local.host/api/0.2/entity/104',
             'relationType': 'crm:P67 refers to',
             'relationSystemClass': 'place', 'type': None,
             'when': {'timespans': [
                 {'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                  'end': {'earliest': '2019-01-31',
                          'latest': '2019-03-01'}}]}}],
         'names': None, 'links': None, 'geometry': None, 'depictions': None}]}],
    'pagination': {'entities': 1, 'entitiesPerPage': 20,
                   'index': [{'page': 1, 'startId': 107}], 'totalPages': 1}}

api_code_reference_geojson = {'pagination': {'entities': 1,
                                             'entitiesPerPage': 20,
                                             'index': [
                                                 {'page': 1, 'startId': 107}],
                                             'totalPages': 1},
                              'results': [{'features': [{'geometry': None,
                                                         'properties': {
                                                             '@id': 107,
                                                             'begin_comment': None,
                                                             'begin_earliest': None,
                                                             'begin_latest': None,
                                                             'description': None,
                                                             'end_comment': None,
                                                             'end_earliest': None,
                                                             'end_latest': None,
                                                             'name': 'https://openatlas.eu',
                                                             'systemClass': 'external_reference',
                                                             'types': None},
                                                         'type': 'Feature'}],
                                           'type': 'FeatureCollection'}]}

api_code_place_first_sort_show_limit = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/108', 'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing', 'systemClass': 'feature',
         'properties': {'title': 'Feature'}, 'description': None,
         'geometry': {'type': 'GeometryCollection', 'geometries': []}}]}],
    'pagination': {'entities': 3, 'entitiesPerPage': 2,
                   'index': [{'page': 1, 'startId': 110},
                             {'page': 2, 'startId': 108}],
                   'totalPages': 2}}

api_code_place_limit_sort_column_filter = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': 'http://local.host/entity/110',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'stratigraphic_unit',
        'properties': {
            'title': 'Strato'},
        'description': None,
        'when': {'timespans': [{
            'start': {
                'earliest': None,
                'latest': None},
            'end': {
                'earliest': None,
                'latest': None}}]},
        'types': None,
        'relations': [{
            'label': 'Location of Strato',
            'relationTo': 'http://local.host/api/0.2/entity/111',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'type': None,
            'when': {
                'timespans': [
                    {
                        'start': {
                            'earliest': None,
                            'latest': None},
                        'end': {
                            'earliest': None,
                            'latest': None}}]}},
            {
                'label': 'Feature',
                'relationTo': 'http://local.host/api/0.2/entity/108',
                'relationType': 'crm:P46i forms part of',
                'relationSystemClass': 'feature',
                'type': None,
                'when': {
                    'timespans': [
                        {
                            'start': {
                                'earliest': None,
                                'latest': None},
                            'end': {
                                'earliest': None,
                                'latest': None}}]}}],
        'names': None,
        'links': None,
        'geometry': {
            'type': 'GeometryCollection',
            'geometries': []},
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': 'http://local.host/entity/104',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'place',
        'properties': {
            'title': 'Nostromos'},
        'description': [{
            'value': 'That is the Nostromos'}],
        'when': {'timespans': [{
            'start': {
                'earliest': '2018-01-31',
                'latest': '2018-03-01'},
            'end': {
                'earliest': '2019-01-31',
                'latest': '2019-03-01'}}]},
        'types': [{
            'identifier': 'http://local.host/api/0.2/entity/65',
            'label': 'Place',
            'description': None,
            'hierarchy': '',
            'value': None,
            'unit': None},
            {
                'identifier': 'http://local.host/api/0.2/entity/102',
                'label': 'Height',
                'description': None,
                'hierarchy': 'Dimensions',
                'value': 23.0,
                'unit': 'centimeter'}],
        'relations': [{
            'label': 'Cargo hauler',
            'relationTo': 'http://local.host/api/0.2/entity/106',
            'relationType': 'crm:P1 is identified by',
            'relationSystemClass': 'appellation',
            'type': None,
            'when': {
                'timespans': [
                    {
                        'start': {
                            'earliest': None,
                            'latest': None},
                        'end': {
                            'earliest': None,
                            'latest': None}}]}},
            {
                'label': 'Feature',
                'relationTo': 'http://local.host/api/0.2/entity/108',
                'relationType': 'crm:P46 is composed of',
                'relationSystemClass': 'feature',
                'type': None,
                'when': {
                    'timespans': [
                        {
                            'start': {
                                'earliest': None,
                                'latest': None},
                            'end': {
                                'earliest': None,
                                'latest': None}}]}},
            {
                'label': 'Height',
                'relationTo': 'http://local.host/api/0.2/entity/102',
                'relationType': 'crm:P2 has type',
                'relationSystemClass': 'type',
                'type': None,
                'when': {
                    'timespans': [
                        {
                            'start': {
                                'earliest': None,
                                'latest': None},
                            'end': {
                                'earliest': None,
                                'latest': None}}]}},
            {
                'label': 'Location of Nostromos',
                'relationTo': 'http://local.host/api/0.2/entity/105',
                'relationType': 'crm:P53 has former or current location',
                'relationSystemClass': 'object_location',
                'type': None,
                'when': {
                    'timespans': [
                        {
                            'start': {
                                'earliest': None,
                                'latest': None},
                            'end': {
                                'earliest': None,
                                'latest': None}}]}},
            {
                'label': 'Place',
                'relationTo': 'http://local.host/api/0.2/entity/65',
                'relationType': 'crm:P2 has type',
                'relationSystemClass': 'type',
                'type': None,
                'when': {
                    'timespans': [
                        {
                            'start': {
                                'earliest': None,
                                'latest': None},
                            'end': {
                                'earliest': None,
                                'latest': None}}]}},
            {
                'label': 'Datei',
                'relationTo': 'http://local.host/api/0.2/entity/112',
                'relationType': 'crm:P67i is referred to by',
                'relationSystemClass': 'file',
                'type': None,
                'when': {
                    'timespans': [
                        {
                            'start': {
                                'earliest': None,
                                'latest': None},
                            'end': {
                                'earliest': None,
                                'latest': None}}]}},
            {
                'label': 'GeoNames',
                'relationTo': 'http://local.host/api/0.2/entity/1',
                'relationType': 'crm:P67i is referred to by',
                'relationSystemClass': 'reference_system',
                'type': 'close match',
                'when': {
                    'timespans': [
                        {
                            'start': {
                                'earliest': None,
                                'latest': None},
                            'end': {
                                'earliest': None,
                                'latest': None}}]}},
            {
                'label': 'https://openatlas.eu',
                'relationTo': 'http://local.host/api/0.2/entity/107',
                'relationType': 'crm:P67i is referred to by',
                'relationSystemClass': 'external_reference',
                'type': None,
                'when': {
                    'timespans': [
                        {
                            'start': {
                                'earliest': None,
                                'latest': None},
                            'end': {
                                'earliest': None,
                                'latest': None}}]}}],
        'names': [{
            'alias': 'Cargo hauler'}],
        'links': [{
            'type': 'close match',
            'identifier': 'https://www.geonames.org/2761369',
            'referenceSystem': 'GeoNames'}],
        'geometry': {
            'type': 'Point',
            'coordinates': [9,
                            17],
            'title': '',
            'description': ''},
        'depictions': [{
            '@id': 'http://local.host/api/0.2/entity/112',
            'title': 'Datei',
            'license': 'Open license',
            'url': 'N/A'}]}]},
    {
        '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
        'type': 'FeatureCollection',
        'features': [{
            '@id': 'http://local.host/entity/105',
            'type': 'Feature',
            'crmClass': 'crm:E53 Place',
            'systemClass': 'object_location',
            'properties': {
                'title': 'Location of Nostromos'},
            'description': None,
            'when': {'timespans': [{
                'start': {
                    'earliest': None,
                    'latest': None},
                'end': {
                    'earliest': None,
                    'latest': None}}]},
            'types': None,
            'relations': [{
                'label': 'Nostromos',
                'relationTo': 'http://local.host/api/0.2/entity/104',
                'relationType': 'crm:P53i is former or current location of',
                'relationSystemClass': 'place',
                'type': None,
                'when': {
                    'timespans': [
                        {
                            'start': {
                                'earliest': '2018-01-31',
                                'latest': '2018-03-01'},
                            'end': {
                                'earliest': '2019-01-31',
                                'latest': '2019-03-01'}}]}}],
            'names': None,
            'links': None,
            'geometry': {
                'type': 'Point',
                'coordinates': [9,
                                17],
                'title': '',
                'description': ''},
            'depictions': None}]}, {
        '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
        'type': 'FeatureCollection',
        'features': [{
            '@id': 'http://local.host/entity/108',
            'type': 'Feature',
            'crmClass': 'crm:E18 Physical Thing',
            'systemClass': 'feature',
            'properties': {
                'title': 'Feature'},
            'description': None,
            'when': {'timespans': [{
                'start': {
                    'earliest': None,
                    'latest': None},
                'end': {
                    'earliest': None,
                    'latest': None}}]},
            'types': None,
            'relations': [{
                'label': 'Location of Feature',
                'relationTo': 'http://local.host/api/0.2/entity/109',
                'relationType': 'crm:P53 has former or current location',
                'relationSystemClass': 'object_location',
                'type': None,
                'when': {
                    'timespans': [
                        {
                            'start': {
                                'earliest': None,
                                'latest': None},
                            'end': {
                                'earliest': None,
                                'latest': None}}]}},
                {
                    'label': 'Strato',
                    'relationTo': 'http://local.host/api/0.2/entity/110',
                    'relationType': 'crm:P46 is composed of',
                    'relationSystemClass': 'stratigraphic_unit',
                    'type': None,
                    'when': {
                        'timespans': [
                            {
                                'start': {
                                    'earliest': None,
                                    'latest': None},
                                'end': {
                                    'earliest': None,
                                    'latest': None}}]}},
                {
                    'label': 'Nostromos',
                    'relationTo': 'http://local.host/api/0.2/entity/104',
                    'relationType': 'crm:P46i forms part of',
                    'relationSystemClass': 'place',
                    'type': None,
                    'when': {
                        'timespans': [
                            {
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
            'depictions': None}]}],
    'pagination': {'entities': 4, 'entitiesPerPage': 10,
                   'index': [{'page': 1, 'startId': 110}],
                   'totalPages': 1}}
api_code_place_filter_id = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/108', 'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing', 'systemClass': 'feature',
         'properties': {'title': 'Feature'}, 'description': None,
         'when': {'timespans': [
             {'start': {'earliest': None, 'latest': None},
              'end': {'earliest': None, 'latest': None}}]}, 'types': None,
         'relations': [
             {'label': 'Location of Feature',
              'relationTo': 'http://local.host/api/0.2/entity/109',
              'relationType': 'crm:P53 has former or current location',
              'relationSystemClass': 'object_location', 'type': None,
              'when': {'timespans': [
                  {'start': {'earliest': None, 'latest': None},
                   'end': {'earliest': None, 'latest': None}}]}},
             {'label': 'Strato',
              'relationTo': 'http://local.host/api/0.2/entity/110',
              'relationType': 'crm:P46 is composed of',
              'relationSystemClass': 'stratigraphic_unit',
              'type': None, 'when': {
                 'timespans': [{'start': {'earliest': None, 'latest': None},
                                'end': {'earliest': None, 'latest': None}}]}},
             {'label': 'Nostromos',
              'relationTo': 'http://local.host/api/0.2/entity/104',
              'relationType': 'crm:P46i forms part of',
              'relationSystemClass': 'place', 'type': None,
              'when': {'timespans': [
                  {'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                   'end': {'earliest': '2019-01-31',
                           'latest': '2019-03-01'}}]}}],
         'names': None, 'links': None,
         'geometry': {'type': 'GeometryCollection', 'geometries': []},
         'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/104', 'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing', 'systemClass': 'place',
         'properties': {'title': 'Nostromos'},
         'description': [{'value': 'That is the Nostromos'}],
         'when': {'timespans': [
             {'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
              'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]},
         'types': [{'identifier': 'http://local.host/api/0.2/entity/65',
                    'label': 'Place',
                    'description': None, 'hierarchy': '', 'value': None,
                    'unit': None},
                   {'identifier': 'http://local.host/api/0.2/entity/102',
                    'label': 'Height',
                    'description': None, 'hierarchy': 'Dimensions',
                    'value': 23.0,
                    'unit': 'centimeter'}], 'relations': [
            {'label': 'Cargo hauler',
             'relationTo': 'http://local.host/api/0.2/entity/106',
             'relationType': 'crm:P1 is identified by',
             'relationSystemClass': 'appellation',
             'type': None, 'when': {
                'timespans': [{'start': {'earliest': None, 'latest': None},
                               'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Feature',
             'relationTo': 'http://local.host/api/0.2/entity/108',
             'relationType': 'crm:P46 is composed of',
             'relationSystemClass': 'feature',
             'type': None, 'when': {
                'timespans': [{'start': {'earliest': None, 'latest': None},
                               'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Height',
             'relationTo': 'http://local.host/api/0.2/entity/102',
             'relationType': 'crm:P2 has type', 'relationSystemClass': 'type',
             'type': None,
             'when': {
                 'timespans': [{'start': {'earliest': None, 'latest': None},
                                'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Location of Nostromos',
             'relationTo': 'http://local.host/api/0.2/entity/105',
             'relationType': 'crm:P53 has former or current location',
             'relationSystemClass': 'object_location', 'type': None,
             'when': {'timespans': [
                 {'start': {'earliest': None, 'latest': None},
                  'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Place',
             'relationTo': 'http://local.host/api/0.2/entity/65',
             'relationType': 'crm:P2 has type', 'relationSystemClass': 'type',
             'type': None,
             'when': {
                 'timespans': [{'start': {'earliest': None, 'latest': None},
                                'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Datei',
             'relationTo': 'http://local.host/api/0.2/entity/112',
             'relationType': 'crm:P67i is referred to by',
             'relationSystemClass': 'file',
             'type': None, 'when': {
                'timespans': [{'start': {'earliest': None, 'latest': None},
                               'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'GeoNames',
             'relationTo': 'http://local.host/api/0.2/entity/1',
             'relationType': 'crm:P67i is referred to by',
             'relationSystemClass': 'reference_system', 'type': 'close match',
             'when': {
                 'timespans': [{'start': {'earliest': None, 'latest': None},
                                'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'https://openatlas.eu',
             'relationTo': 'http://local.host/api/0.2/entity/107',
             'relationType': 'crm:P67i is referred to by',
             'relationSystemClass': 'external_reference', 'type': None,
             'when': {'timespans': [
                 {'start': {'earliest': None, 'latest': None},
                  'end': {'earliest': None, 'latest': None}}]}}],
         'names': [{'alias': 'Cargo hauler'}], 'links': [
            {'type': 'close match',
             'identifier': 'https://www.geonames.org/2761369',
             'referenceSystem': 'GeoNames'}],
         'geometry': {'type': 'Point', 'coordinates': [9, 17], 'title': '',
                      'description': ''},
         'depictions': [
             {'@id': 'http://local.host/api/0.2/entity/112', 'title': 'Datei',
              'license': 'Open license', 'url': 'N/A'}]}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/110', 'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing',
         'systemClass': 'stratigraphic_unit',
         'properties': {'title': 'Strato'}, 'description': None,
         'when': {'timespans': [
             {'start': {'earliest': None, 'latest': None},
              'end': {'earliest': None, 'latest': None}}]}, 'types': None,
         'relations': [
             {'label': 'Location of Strato',
              'relationTo': 'http://local.host/api/0.2/entity/111',
              'relationType': 'crm:P53 has former or current location',
              'relationSystemClass': 'object_location', 'type': None,
              'when': {'timespans': [
                  {'start': {'earliest': None, 'latest': None},
                   'end': {'earliest': None, 'latest': None}}]}},
             {'label': 'Feature',
              'relationTo': 'http://local.host/api/0.2/entity/108',
              'relationType': 'crm:P46i forms part of',
              'relationSystemClass': 'feature',
              'type': None, 'when': {
                 'timespans': [{'start': {'earliest': None, 'latest': None},
                                'end': {'earliest': None, 'latest': None}}]}}],
         'names': None, 'links': None,
         'geometry': {'type': 'GeometryCollection', 'geometries': []},
         'depictions': None}]}],
    'pagination': {'entities': 3, 'entitiesPerPage': 20,
                   'index': [{'page': 1, 'startId': 108}],
                   'totalPages': 1}}

api_code_place_filter_time = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/108', 'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing', 'systemClass': 'feature',
         'properties': {'title': 'Feature'}, 'description': None,
         'when': {'timespans': [
             {'start': {'earliest': None, 'latest': None},
              'end': {'earliest': None, 'latest': None}}]}, 'types': None,
         'relations': [
             {'label': 'Location of Feature',
              'relationTo': 'http://local.host/api/0.2/entity/109',
              'relationType': 'crm:P53 has former or current location',
              'relationSystemClass': 'object_location', 'type': None,
              'when': {'timespans': [
                  {'start': {'earliest': None, 'latest': None},
                   'end': {'earliest': None, 'latest': None}}]}},
             {'label': 'Strato',
              'relationTo': 'http://local.host/api/0.2/entity/110',
              'relationType': 'crm:P46 is composed of',
              'relationSystemClass': 'stratigraphic_unit',
              'type': None, 'when': {
                 'timespans': [{'start': {'earliest': None, 'latest': None},
                                'end': {'earliest': None, 'latest': None}}]}},
             {'label': 'Nostromos',
              'relationTo': 'http://local.host/api/0.2/entity/104',
              'relationType': 'crm:P46i forms part of',
              'relationSystemClass': 'place', 'type': None,
              'when': {'timespans': [
                  {'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                   'end': {'earliest': '2019-01-31',
                           'latest': '2019-03-01'}}]}}],
         'names': None, 'links': None,
         'geometry': {'type': 'GeometryCollection', 'geometries': []},
         'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/104', 'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing', 'systemClass': 'place',
         'properties': {'title': 'Nostromos'},
         'description': [{'value': 'That is the Nostromos'}],
         'when': {'timespans': [
             {'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
              'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]},
         'types': [{'identifier': 'http://local.host/api/0.2/entity/65',
                    'label': 'Place',
                    'description': None, 'hierarchy': '', 'value': None,
                    'unit': None},
                   {'identifier': 'http://local.host/api/0.2/entity/102',
                    'label': 'Height',
                    'description': None, 'hierarchy': 'Dimensions',
                    'value': 23.0,
                    'unit': 'centimeter'}], 'relations': [
            {'label': 'Cargo hauler',
             'relationTo': 'http://local.host/api/0.2/entity/106',
             'relationType': 'crm:P1 is identified by',
             'relationSystemClass': 'appellation',
             'type': None, 'when': {
                'timespans': [{'start': {'earliest': None, 'latest': None},
                               'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Feature',
             'relationTo': 'http://local.host/api/0.2/entity/108',
             'relationType': 'crm:P46 is composed of',
             'relationSystemClass': 'feature',
             'type': None, 'when': {
                'timespans': [{'start': {'earliest': None, 'latest': None},
                               'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Height',
             'relationTo': 'http://local.host/api/0.2/entity/102',
             'relationType': 'crm:P2 has type', 'relationSystemClass': 'type',
             'type': None,
             'when': {
                 'timespans': [{'start': {'earliest': None, 'latest': None},
                                'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Location of Nostromos',
             'relationTo': 'http://local.host/api/0.2/entity/105',
             'relationType': 'crm:P53 has former or current location',
             'relationSystemClass': 'object_location', 'type': None,
             'when': {'timespans': [
                 {'start': {'earliest': None, 'latest': None},
                  'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Place',
             'relationTo': 'http://local.host/api/0.2/entity/65',
             'relationType': 'crm:P2 has type', 'relationSystemClass': 'type',
             'type': None,
             'when': {
                 'timespans': [{'start': {'earliest': None, 'latest': None},
                                'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Datei',
             'relationTo': 'http://local.host/api/0.2/entity/112',
             'relationType': 'crm:P67i is referred to by',
             'relationSystemClass': 'file',
             'type': None, 'when': {
                'timespans': [{'start': {'earliest': None, 'latest': None},
                               'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'GeoNames',
             'relationTo': 'http://local.host/api/0.2/entity/1',
             'relationType': 'crm:P67i is referred to by',
             'relationSystemClass': 'reference_system', 'type': 'close match',
             'when': {
                 'timespans': [{'start': {'earliest': None, 'latest': None},
                                'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'https://openatlas.eu',
             'relationTo': 'http://local.host/api/0.2/entity/107',
             'relationType': 'crm:P67i is referred to by',
             'relationSystemClass': 'external_reference', 'type': None,
             'when': {'timespans': [
                 {'start': {'earliest': None, 'latest': None},
                  'end': {'earliest': None, 'latest': None}}]}}],
         'names': [{'alias': 'Cargo hauler'}], 'links': [
            {'type': 'close match',
             'identifier': 'https://www.geonames.org/2761369',
             'referenceSystem': 'GeoNames'}],
         'geometry': {'type': 'Point', 'coordinates': [9, 17], 'title': '',
                      'description': ''},
         'depictions': [
             {'@id': 'http://local.host/api/0.2/entity/112', 'title': 'Datei',
              'license': 'Open license', 'url': 'N/A'}]}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/110', 'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing',
         'systemClass': 'stratigraphic_unit',
         'properties': {'title': 'Strato'}, 'description': None,
         'when': {'timespans': [
             {'start': {'earliest': None, 'latest': None},
              'end': {'earliest': None, 'latest': None}}]}, 'types': None,
         'relations': [
             {'label': 'Location of Strato',
              'relationTo': 'http://local.host/api/0.2/entity/111',
              'relationType': 'crm:P53 has former or current location',
              'relationSystemClass': 'object_location', 'type': None,
              'when': {'timespans': [
                  {'start': {'earliest': None, 'latest': None},
                   'end': {'earliest': None, 'latest': None}}]}},
             {'label': 'Feature',
              'relationTo': 'http://local.host/api/0.2/entity/108',
              'relationType': 'crm:P46i forms part of',
              'relationSystemClass': 'feature',
              'type': None, 'when': {
                 'timespans': [{'start': {'earliest': None, 'latest': None},
                                'end': {'earliest': None, 'latest': None}}]}}],
         'names': None, 'links': None,
         'geometry': {'type': 'GeometryCollection', 'geometries': []},
         'depictions': None}]}],
    'pagination': {'entities': 3, 'entitiesPerPage': 20,
                   'index': [{'page': 1, 'startId': 108}],
                   'totalPages': 1}}

api_entities_linked_entity = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/112', 'type': 'Feature',
         'crmClass': 'crm:E31 Document',
         'systemClass': 'file', 'properties': {'title': 'Datei'},
         'description': None, 'when': {
            'timespans': [{'start': {'earliest': None, 'latest': None},
                           'end': {'earliest': None, 'latest': None}}]},
         'types': [
             {'identifier': 'http://local.host/api/0.2/entity/49',
              'label': 'Open license',
              'description': None, 'hierarchy': 'License', 'value': None,
              'unit': None}],
         'relations': [{'label': 'Nostromos',
                        'relationTo': 'http://local.host/api/0.2/entity/104',
                        'relationType': 'crm:P67 refers to',
                        'relationSystemClass': 'place',
                        'type': None, 'when': {'timespans': [
                 {'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                  'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]}},
                       {'label': 'Open license',
                        'relationTo': 'http://local.host/api/0.2/entity/49',
                        'relationType': 'crm:P2 has type',
                        'relationSystemClass': 'type',
                        'type': None, 'when': {'timespans': [
                           {'start': {'earliest': None, 'latest': None},
                            'end': {'earliest': None, 'latest': None}}]}}],
         'names': None,
         'links': None, 'geometry': None, 'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/1', 'type': 'Feature',
         'crmClass': 'crm:E32 Authority Document',
         'systemClass': 'reference_system',
         'properties': {'title': 'GeoNames'}, 'description': [
            {
                'value': 'Geographical database covering all countries and many places.'}],
         'when': {
             'timespans': [{'start': {'earliest': None, 'latest': None},
                            'end': {'earliest': None, 'latest': None}}]},
         'types': None,
         'relations': [{'label': 'Nostromos',
                        'relationTo': 'http://local.host/api/0.2/entity/104',
                        'relationType': 'crm:P67 refers to',
                        'relationSystemClass': 'place',
                        'type': 'close match', 'when': {'timespans': [
                 {'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                  'end': {'earliest': '2019-01-31',
                          'latest': '2019-03-01'}}]}}], 'names': None,
         'links': None, 'geometry': None, 'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/107', 'type': 'Feature',
         'crmClass': 'crm:E31 Document',
         'systemClass': 'external_reference',
         'properties': {'title': 'https://openatlas.eu'},
         'description': None,
         'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                 'end': {'earliest': None, 'latest': None}}]},
         'types': None, 'relations': [
            {'label': 'Nostromos',
             'relationTo': 'http://local.host/api/0.2/entity/104',
             'relationType': 'crm:P67 refers to',
             'relationSystemClass': 'place', 'type': None,
             'when': {'timespans': [
                 {'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                  'end': {'earliest': '2019-01-31',
                          'latest': '2019-03-01'}}]}}],
         'names': None, 'links': None, 'geometry': None, 'depictions': None}]},
    {
        '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
        'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/106', 'type': 'Feature',
         'crmClass': 'crm:E41 Appellation', 'systemClass': 'appellation',
         'properties': {'title': 'Cargo hauler'}, 'description': None,
         'when': {'timespans': [
             {'start': {'earliest': None, 'latest': None},
              'end': {'earliest': None, 'latest': None}}]}, 'types': None,
         'relations': [
             {'label': 'Nostromos',
              'relationTo': 'http://local.host/api/0.2/entity/104',
              'relationType': 'crm:P1i identifies',
              'relationSystemClass': 'place', 'type': None,
              'when': {'timespans': [
                  {'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                   'end': {'earliest': '2019-01-31',
                           'latest': '2019-03-01'}}]}}],
         'names': None, 'links': None, 'geometry': None, 'depictions': None}]},
    {
        '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
        'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/108', 'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing', 'systemClass': 'feature',
         'properties': {'title': 'Feature'}, 'description': None,
         'when': {'timespans': [
             {'start': {'earliest': None, 'latest': None},
              'end': {'earliest': None, 'latest': None}}]}, 'types': None,
         'relations': [
             {'label': 'Location of Feature',
              'relationTo': 'http://local.host/api/0.2/entity/109',
              'relationType': 'crm:P53 has former or current location',
              'relationSystemClass': 'object_location', 'type': None,
              'when': {'timespans': [
                  {'start': {'earliest': None, 'latest': None},
                   'end': {'earliest': None, 'latest': None}}]}},
             {'label': 'Strato',
              'relationTo': 'http://local.host/api/0.2/entity/110',
              'relationType': 'crm:P46 is composed of',
              'relationSystemClass': 'stratigraphic_unit',
              'type': None, 'when': {
                 'timespans': [{'start': {'earliest': None, 'latest': None},
                                'end': {'earliest': None, 'latest': None}}]}},
             {'label': 'Nostromos',
              'relationTo': 'http://local.host/api/0.2/entity/104',
              'relationType': 'crm:P46i forms part of',
              'relationSystemClass': 'place', 'type': None,
              'when': {'timespans': [
                  {'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                   'end': {'earliest': '2019-01-31',
                           'latest': '2019-03-01'}}]}}],
         'names': None, 'links': None,
         'geometry': {'type': 'GeometryCollection', 'geometries': []},
         'depictions': None}]}, {
        '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
        'type': 'FeatureCollection', 'features': [
            {'@id': 'http://local.host/entity/102', 'type': 'Feature',
             'crmClass': 'crm:E55 Type',
             'systemClass': 'type', 'properties': {'title': 'Height'},
             'description': [{'value': 'centimeter'}], 'when': {'timespans': [
                {'start': {'earliest': None, 'latest': None},
                 'end': {'earliest': None, 'latest': None}}]}, 'types': None,
             'relations': [
                 {'label': 'Dimensions',
                  'relationTo': 'http://local.host/api/0.2/entity/101',
                  'relationType': 'crm:P127 has broader term',
                  'relationSystemClass': 'type',
                  'type': None, 'when': {
                     'timespans': [{'start': {'earliest': None, 'latest': None},
                                    'end': {'earliest': None,
                                            'latest': None}}]}},
                 {'label': 'Nostromos',
                  'relationTo': 'http://local.host/api/0.2/entity/104',
                  'relationType': 'crm:P2i is type of',
                  'relationSystemClass': 'place', 'type': None,
                  'when': {'timespans': [{'start': {'earliest': '2018-01-31',
                                                    'latest': '2018-03-01'},
                                          'end': {'earliest': '2019-01-31',
                                                  'latest': '2019-03-01'}}]}}],
             'names': None, 'links': None, 'geometry': None,
             'depictions': None}]}, {
        '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
        'type': 'FeatureCollection', 'features': [
            {'@id': 'http://local.host/entity/105', 'type': 'Feature',
             'crmClass': 'crm:E53 Place',
             'systemClass': 'object_location',
             'properties': {'title': 'Location of Nostromos'},
             'description': None, 'when': {
                'timespans': [{'start': {'earliest': None, 'latest': None},
                               'end': {'earliest': None, 'latest': None}}]},
             'types': None, 'relations': [
                {'label': 'Nostromos',
                 'relationTo': 'http://local.host/api/0.2/entity/104',
                 'relationType': 'crm:P53i is former or current location of',
                 'relationSystemClass': 'place', 'type': None,
                 'when': {'timespans': [
                     {'start': {'earliest': '2018-01-31',
                                'latest': '2018-03-01'},
                      'end': {'earliest': '2019-01-31',
                              'latest': '2019-03-01'}}]}}], 'names': None,
             'links': None,
             'geometry': {'type': 'Point', 'coordinates': [9, 17], 'title': '',
                          'description': ''},
             'depictions': None}]}, {
        '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
        'type': 'FeatureCollection', 'features': [
            {'@id': 'http://local.host/entity/65', 'type': 'Feature',
             'crmClass': 'crm:E55 Type',
             'systemClass': 'type', 'properties': {'title': 'Place'},
             'description': [{
                 'value': 'Types for non-moveable entities (i.e. places) with a certain extent and/or location like Settlement, Burial site, Ritual site, Fortification etc.'}],
             'when': {
                 'timespans': [{'start': {'earliest': None, 'latest': None},
                                'end': {'earliest': None, 'latest': None}}]},
             'types': None,
             'relations': [
                 {'label': 'Boundary Mark',
                  'relationTo': 'http://local.host/api/0.2/entity/72',
                  'relationType': 'crm:P127i has narrower term',
                  'relationSystemClass': 'type',
                  'type': None, 'when': {
                     'timespans': [{'start': {'earliest': None, 'latest': None},
                                    'end': {'earliest': None,
                                            'latest': None}}]}},
                 {'label': 'Burial Site',
                  'relationTo': 'http://local.host/api/0.2/entity/69',
                  'relationType': 'crm:P127i has narrower term',
                  'relationSystemClass': 'type',
                  'type': None, 'when': {
                     'timespans': [{'start': {'earliest': None, 'latest': None},
                                    'end': {'earliest': None,
                                            'latest': None}}]}},
                 {'label': 'Economic Site',
                  'relationTo': 'http://local.host/api/0.2/entity/71',
                  'relationType': 'crm:P127i has narrower term',
                  'relationSystemClass': 'type',
                  'type': None, 'when': {
                     'timespans': [{'start': {'earliest': None, 'latest': None},
                                    'end': {'earliest': None,
                                            'latest': None}}]}},
                 {'label': 'Infrastructure',
                  'relationTo': 'http://local.host/api/0.2/entity/70',
                  'relationType': 'crm:P127i has narrower term',
                  'relationSystemClass': 'type',
                  'type': None, 'when': {
                     'timespans': [{'start': {'earliest': None, 'latest': None},
                                    'end': {'earliest': None,
                                            'latest': None}}]}},
                 {'label': 'Military Facility',
                  'relationTo': 'http://local.host/api/0.2/entity/67',
                  'relationType': 'crm:P127i has narrower term',
                  'relationSystemClass': 'type',
                  'type': None, 'when': {
                     'timespans': [{'start': {'earliest': None, 'latest': None},
                                    'end': {'earliest': None,
                                            'latest': None}}]}},
                 {'label': 'Nostromos',
                  'relationTo': 'http://local.host/api/0.2/entity/104',
                  'relationType': 'crm:P2i is type of',
                  'relationSystemClass': 'place', 'type': None,
                  'when': {'timespans': [{'start': {'earliest': '2018-01-31',
                                                    'latest': '2018-03-01'},
                                          'end': {'earliest': '2019-01-31',
                                                  'latest': '2019-03-01'}}]}},
                 {'label': 'Ritual Site',
                  'relationTo': 'http://local.host/api/0.2/entity/68',
                  'relationType': 'crm:P127i has narrower term',
                  'relationSystemClass': 'type',
                  'type': None, 'when': {
                     'timespans': [{'start': {'earliest': None, 'latest': None},
                                    'end': {'earliest': None,
                                            'latest': None}}]}},
                 {'label': 'Settlement',
                  'relationTo': 'http://local.host/api/0.2/entity/66',
                  'relationType': 'crm:P127i has narrower term',
                  'relationSystemClass': 'type',
                  'type': None, 'when': {
                     'timespans': [{'start': {'earliest': None, 'latest': None},
                                    'end': {'earliest': None,
                                            'latest': None}}]}},
                 {'label': 'Topographical Entity',
                  'relationTo': 'http://local.host/api/0.2/entity/73',
                  'relationType': 'crm:P127i has narrower term',
                  'relationSystemClass': 'type',
                  'type': None, 'when': {
                     'timespans': [{'start': {'earliest': None, 'latest': None},
                                    'end': {'earliest': None,
                                            'latest': None}}]}}],
             'names': None, 'links': None, 'geometry': None,
             'depictions': None}]}],
    'pagination': {'entities': 8, 'entitiesPerPage': 20,
                   'index': [{'page': 1, 'startId': 112}],
                   'totalPages': 1}}
