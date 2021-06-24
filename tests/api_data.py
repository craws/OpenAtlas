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

api_geojson_template = [
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                9,
                17
            ],
            "title": "",
            "description": ""
        },
        "properties":
            {
                "@id": 104,
                "systemClass": "place",
                "name": "Nostromos",
                "description": "That is the Nostromos",
                "begin_earliest": "2018-01-31",
                "begin_latest": "2018-03-01",
                "begin_comment": "Begin of the Nostromos",
                "end_earliest": "2019-01-31",
                "end_latest": "2019-03-01",
                "end_comment": "Destruction of the Nostromos",
                "types": [
                    "Place",
                    "Height"
                ]
            }
    },
    {
        "type": "Feature",
        "geometry": None,
        "properties":
            {
                "@id": 104,
                "systemClass": "place",
                "name": "Nostromos",
                "description": "That is the Nostromos",
                "begin_earliest": "2018-01-31",
                "begin_latest": "2018-03-01",
                "begin_comment": "Begin of the Nostromos",
                "end_earliest": "2019-01-31",
                "end_latest": "2019-03-01",
                "end_comment": "Destruction of the Nostromos",
                "types": [
                    "Place",
                    "Height"
                ]
            }
    }
]

api_geometries_template = {'features': [{'geometry': {'coordinates': [9, 17], 'type': 'Point'},
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

api_content_en = {'intro': 'This is English', 'contact': '', 'legalNotice': '', 'siteName': ''}
api_content_de = {'intro': 'Das ist Deutsch', 'contact': '', 'legalNotice': '', 'siteName': ''}

api_overview_count = [{'systemClass': 'external_reference', 'count': 1},
                      {'systemClass': 'reference_system', 'count': 2},
                      {'systemClass': 'file', 'count': 1}, {'systemClass': 'feature', 'count': 1},
                      {'systemClass': 'type', 'count': 87},
                      {'systemClass': 'administrative_unit', 'count': 14},
                      {'systemClass': 'place', 'count': 1},
                      {'systemClass': 'stratigraphic_unit', 'count': 1}]

api_node_entities = {
    'nodes': [{'id': 84, 'label': 'Austria', 'url': 'http://local.host/api/0.2/entity/84'},
              {'id': 89, 'label': 'Czech Republic', 'url': 'http://local.host/api/0.2/entity/89'},
              {'id': 87, 'label': 'Germany', 'url': 'http://local.host/api/0.2/entity/87'},
              {'id': 88, 'label': 'Italy', 'url': 'http://local.host/api/0.2/entity/88'},
              {'id': 90, 'label': 'Slovakia', 'url': 'http://local.host/api/0.2/entity/90'},
              {'id': 91, 'label': 'Slovenia', 'url': 'http://local.host/api/0.2/entity/91'}]}

api_node_entities_all = {
    'nodes': [{'id': 84, 'label': 'Austria', 'url': 'http://local.host/api/0.2/entity/84'},
              {'id': 89, 'label': 'Czech Republic', 'url': 'http://local.host/api/0.2/entity/89'},
              {'id': 87, 'label': 'Germany', 'url': 'http://local.host/api/0.2/entity/87'},
              {'id': 88, 'label': 'Italy', 'url': 'http://local.host/api/0.2/entity/88'},
              {'id': 90, 'label': 'Slovakia', 'url': 'http://local.host/api/0.2/entity/90'},
              {'id': 91, 'label': 'Slovenia', 'url': 'http://local.host/api/0.2/entity/91'},
              {'id': 86, 'label': 'Niederösterreich', 'url': 'http://local.host/api/0.2/entity/86'},
              {'id': 85, 'label': 'Wien', 'url': 'http://local.host/api/0.2/entity/85'}]}

api_node_overview = {'types': [{'standard': {'Actor actor relation': [
    {'id': 63, 'url': 'http://local.host/api/0.2/entity/63', 'label': 'Economical', 'children': [
        {'id': 64, 'url': 'http://local.host/api/0.2/entity/64',
         'label': 'Provider of (Customer of)', 'children': []}]},
    {'id': 54, 'url': 'http://local.host/api/0.2/entity/54', 'label': 'Kindredship', 'children': [
        {'id': 55, 'url': 'http://local.host/api/0.2/entity/55', 'label': 'Parent of (Child of)',
         'children': []}]},
    {'id': 60, 'url': 'http://local.host/api/0.2/entity/60', 'label': 'Political', 'children': [
        {'id': 61, 'url': 'http://local.host/api/0.2/entity/61', 'label': 'Ally of',
         'children': []},
        {'id': 62, 'url': 'http://local.host/api/0.2/entity/62', 'label': 'Leader of (Retinue of)',
         'children': []}]},
    {'id': 56, 'url': 'http://local.host/api/0.2/entity/56', 'label': 'Social', 'children': [
        {'id': 58, 'url': 'http://local.host/api/0.2/entity/58', 'label': 'Enemy of',
         'children': []},
        {'id': 57, 'url': 'http://local.host/api/0.2/entity/57', 'label': 'Friend of',
         'children': []},
        {'id': 59, 'url': 'http://local.host/api/0.2/entity/59', 'label': 'Mentor of (Student of)',
         'children': []}]}], 'Actor function': [
    {'id': 18, 'url': 'http://local.host/api/0.2/entity/18', 'label': 'Abbot', 'children': []},
    {'id': 17, 'url': 'http://local.host/api/0.2/entity/17', 'label': 'Bishop', 'children': []},
    {'id': 21, 'url': 'http://local.host/api/0.2/entity/21', 'label': 'Count', 'children': []},
    {'id': 20, 'url': 'http://local.host/api/0.2/entity/20', 'label': 'Emperor', 'children': []},
    {'id': 22, 'url': 'http://local.host/api/0.2/entity/22', 'label': 'King', 'children': []},
    {'id': 19, 'url': 'http://local.host/api/0.2/entity/19', 'label': 'Pope', 'children': []}],
    'Artifact': [{'id': 24,
                  'url': 'http://local.host/api/0.2/entity/24',
                  'label': 'Coin', 'children': []},
                 {'id': 25,
                  'url': 'http://local.host/api/0.2/entity/25',
                  'label': 'Statue', 'children': []}],
    'Bibliography': [{'id': 5,
                      'url': 'http://local.host/api/0.2/entity/5',
                      'label': 'Article', 'children': []},
                     {'id': 6,
                      'url': 'http://local.host/api/0.2/entity/6',
                      'label': 'Book', 'children': []},
                     {'id': 4,
                      'url': 'http://local.host/api/0.2/entity/4',
                      'label': 'Inbook', 'children': []}],
    'Edition': [{'id': 8,
                 'url': 'http://local.host/api/0.2/entity/8',
                 'label': 'Charter Edition',
                 'children': []}, {'id': 10,
                                   'url': 'http://local.host/api/0.2/entity/10',
                                   'label': 'Chronicle Edition',
                                   'children': []},
                {'id': 9,
                 'url': 'http://local.host/api/0.2/entity/9',
                 'label': 'Letter Edition',
                 'children': []}], 'Event': [
        {'id': 35, 'url': 'http://local.host/api/0.2/entity/35', 'label': 'Change of Property',
         'children': [{'id': 36, 'url': 'http://local.host/api/0.2/entity/36', 'label': 'Donation',
                       'children': []},
                      {'id': 38, 'url': 'http://local.host/api/0.2/entity/38', 'label': 'Exchange',
                       'children': []},
                      {'id': 37, 'url': 'http://local.host/api/0.2/entity/37', 'label': 'Sale',
                       'children': []}]},
        {'id': 39, 'url': 'http://local.host/api/0.2/entity/39', 'label': 'Conflict', 'children': [
            {'id': 40, 'url': 'http://local.host/api/0.2/entity/40', 'label': 'Battle',
             'children': []},
            {'id': 41, 'url': 'http://local.host/api/0.2/entity/41', 'label': 'Raid',
             'children': []}]}], 'External reference': [
        {'id': 12, 'url': 'http://local.host/api/0.2/entity/12', 'label': 'Link', 'children': []}],
    'External reference match': [{'id': 15,
                                  'url': 'http://local.host/api/0.2/entity/15',
                                  'label': 'close match',
                                  'children': []},
                                 {'id': 14,
                                  'url': 'http://local.host/api/0.2/entity/14',
                                  'label': 'exact match',
                                  'children': []}],
    'Feature': [{'id': 75,
                 'url': 'http://local.host/api/0.2/entity/75',
                 'label': 'Grave', 'children': []},
                {'id': 76,
                 'url': 'http://local.host/api/0.2/entity/76',
                 'label': 'Pit', 'children': []}],
    'Human remains': [{'id': 82,
                       'url': 'http://local.host/api/0.2/entity/82',
                       'label': 'Lower Body',
                       'children': []}, {'id': 81,
                                         'url': 'http://local.host/api/0.2/entity/81',
                                         'label': 'Upper Body',
                                         'children': []}],
    'Involvement': [{'id': 27,
                     'url': 'http://local.host/api/0.2/entity/27',
                     'label': 'Creator', 'children': []},
                    {'id': 30,
                     'url': 'http://local.host/api/0.2/entity/30',
                     'label': 'Offender', 'children': []},
                    {'id': 28,
                     'url': 'http://local.host/api/0.2/entity/28',
                     'label': 'Sponsor', 'children': []},
                    {'id': 29,
                     'url': 'http://local.host/api/0.2/entity/29',
                     'label': 'Victim', 'children': []}],
    'License': [{'id': 49,
                 'url': 'http://local.host/api/0.2/entity/49',
                 'label': 'Open license', 'children': [
            {'id': 51,
             'url': 'http://local.host/api/0.2/entity/51',
             'label': 'CC BY 4.0', 'children': []},
            {'id': 52,
             'url': 'http://local.host/api/0.2/entity/52',
             'label': 'CC BY-SA 4.0', 'children': []},
            {'id': 50,
             'url': 'http://local.host/api/0.2/entity/50',
             'label': 'Public domain', 'children': []}]},
                {'id': 48,
                 'url': 'http://local.host/api/0.2/entity/48',
                 'label': 'Proprietary license',
                 'children': []}], 'Place': [
        {'id': 72, 'url': 'http://local.host/api/0.2/entity/72', 'label': 'Boundary Mark',
         'children': []},
        {'id': 69, 'url': 'http://local.host/api/0.2/entity/69', 'label': 'Burial Site',
         'children': []},
        {'id': 71, 'url': 'http://local.host/api/0.2/entity/71', 'label': 'Economic Site',
         'children': []},
        {'id': 70, 'url': 'http://local.host/api/0.2/entity/70', 'label': 'Infrastructure',
         'children': []},
        {'id': 67, 'url': 'http://local.host/api/0.2/entity/67', 'label': 'Military Facility',
         'children': []},
        {'id': 68, 'url': 'http://local.host/api/0.2/entity/68', 'label': 'Ritual Site',
         'children': []},
        {'id': 66, 'url': 'http://local.host/api/0.2/entity/66', 'label': 'Settlement',
         'children': []},
        {'id': 73, 'url': 'http://local.host/api/0.2/entity/73', 'label': 'Topographical Entity',
         'children': []}], 'Source': [
        {'id': 43, 'url': 'http://local.host/api/0.2/entity/43', 'label': 'Charter',
         'children': []},
        {'id': 46, 'url': 'http://local.host/api/0.2/entity/46', 'label': 'Contract',
         'children': []},
        {'id': 45, 'url': 'http://local.host/api/0.2/entity/45', 'label': 'Letter', 'children': []},
        {'id': 44, 'url': 'http://local.host/api/0.2/entity/44', 'label': 'Testament',
         'children': []}], 'Stratigraphic unit': [
        {'id': 78, 'url': 'http://local.host/api/0.2/entity/78', 'label': 'Burial', 'children': []},
        {'id': 79, 'url': 'http://local.host/api/0.2/entity/79', 'label': 'Deposit',
         'children': []}]}, 'places': {'Administrative unit': [
    {'id': 84, 'url': 'http://local.host/api/0.2/entity/84', 'label': 'Austria', 'children': [
        {'id': 86, 'url': 'http://local.host/api/0.2/entity/86', 'label': 'Niederösterreich',
         'children': []},
        {'id': 85, 'url': 'http://local.host/api/0.2/entity/85', 'label': 'Wien', 'children': []}]},
    {'id': 89, 'url': 'http://local.host/api/0.2/entity/89', 'label': 'Czech Republic',
     'children': []},
    {'id': 87, 'url': 'http://local.host/api/0.2/entity/87', 'label': 'Germany', 'children': []},
    {'id': 88, 'url': 'http://local.host/api/0.2/entity/88', 'label': 'Italy', 'children': []},
    {'id': 90, 'url': 'http://local.host/api/0.2/entity/90', 'label': 'Slovakia', 'children': []},
    {'id': 91, 'url': 'http://local.host/api/0.2/entity/91', 'label': 'Slovenia', 'children': []}],
    'Historical place': [
        {'id': 93, 'url': 'http://local.host/api/0.2/entity/93',
         'label': 'Carantania', 'children': []},
        {'id': 95, 'url': 'http://local.host/api/0.2/entity/95',
         'label': 'Comitatus Iauntal', 'children': []},
        {'id': 96, 'url': 'http://local.host/api/0.2/entity/96',
         'label': 'Kingdom of Serbia', 'children': []},
        {'id': 94, 'url': 'http://local.host/api/0.2/entity/94',
         'label': 'Marcha Orientalis', 'children': []}]},
    'custom': {'Sex': [
        {'id': 32, 'url': 'http://local.host/api/0.2/entity/32',
         'label': 'Female', 'children': []},
        {'id': 33, 'url': 'http://local.host/api/0.2/entity/33',
         'label': 'Male', 'children': []}], 'Source translation': [
        {'id': 98, 'url': 'http://local.host/api/0.2/entity/98',
         'label': 'Original Text', 'children': []},
        {'id': 99, 'url': 'http://local.host/api/0.2/entity/99',
         'label': 'Translation', 'children': []},
        {'id': 100, 'url': 'http://local.host/api/0.2/entity/100',
         'label': 'Transliteration', 'children': []}]}, 'value': {
        'Dimensions': [{'id': 102, 'url': 'http://local.host/api/0.2/entity/102', 'label': 'Height',
                        'children': []},
                       {'id': 103, 'url': 'http://local.host/api/0.2/entity/103', 'label': 'Weight',
                        'children': []}]}}]}

api_subunit = {
    'nodes': [{'id': 108, 'label': 'Feature', 'url': 'http://local.host/api/0.2/entity/108'}]}

api_subunit_hierarchy = {
    'nodes': [{'id': 108, 'label': 'Feature', 'url': 'http://local.host/api/0.2/entity/108'},
              {'id': 110, 'label': 'Strato', 'url': 'http://local.host/api/0.2/entity/110'}]}

api_type_tree = {'typeTree': [{'18': {'id': 18, 'name': 'Abbot', 'description': None,
                                      'origin_id': None, 'first': None, 'last': None, 'root': [16],
                                      'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
                                      'standard': False}}, {
                                  '53': {'id': 53, 'name': 'Actor actor relation',
                                         'description': 'Categories for the relationship between two actors. This may be a mutual relationship (e.g. actor A is friend of actor B and vice versa), or a directional relationship (e.g. actor A is the child of actor B, while actor B is the parent of actor A).',
                                         'origin_id': None, 'first': None, 'last': None, 'root': [],
                                         'subs': [63, 54, 60, 56], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': True}}, {
                                  '16': {'id': 16, 'name': 'Actor function',
                                         'description': 'Definitions of an actor\'s function within a group. An actor can for example be member of a group and this membership is defined by a certain function during a certain period of time. E.g. actor "Charlemagne" is member of the group "Frankish Reign" from 768 to 814 in the function of "King" and he is member of the group "Roman Empire" from 800 to 814 in the function "Emperor".',
                                         'origin_id': None, 'first': None, 'last': None, 'root': [],
                                         'subs': [18, 17, 21, 20, 22, 19], 'count': 0,
                                         'count_subs': 0, 'locked': False, 'standard': True}}, {
                                  '61': {'id': 61, 'name': 'Ally of', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [60, 53], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '5': {'id': 5, 'name': 'Article', 'description': None,
                                        'origin_id': None, 'first': None, 'last': None, 'root': [3],
                                        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
                                        'standard': False}}, {
                                  '23': {'id': 23, 'name': 'Artifact', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None, 'root': [],
                                         'subs': [24, 25], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': True}}, {
                                  '40': {'id': 40, 'name': 'Battle', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [39, 34], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '3': {'id': 3, 'name': 'Bibliography',
                                        'description': 'Categories for bibliographical entries as used for example in BibTeX, e.g. Book, Inbook, Article etc.',
                                        'origin_id': None, 'first': None, 'last': None, 'root': [],
                                        'subs': [5, 6, 4], 'count': 0, 'count_subs': 0,
                                        'locked': False, 'standard': True}}, {
                                  '17': {'id': 17, 'name': 'Bishop', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [16], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '6': {'id': 6, 'name': 'Book', 'description': None,
                                        'origin_id': None, 'first': None, 'last': None, 'root': [3],
                                        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
                                        'standard': False}}, {
                                  '72': {'id': 72, 'name': 'Boundary Mark', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [65], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '78': {'id': 78, 'name': 'Burial', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [77], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '69': {'id': 69, 'name': 'Burial Site', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [65], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '52': {'id': 52, 'name': 'CC BY-SA 4.0', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [49, 47], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '51': {'id': 51, 'name': 'CC BY 4.0', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [49, 47], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '35': {'id': 35, 'name': 'Change of Property',
                                         'description': None, 'origin_id': None, 'first': None,
                                         'last': None, 'root': [34], 'subs': [36, 38, 37],
                                         'count': 0, 'count_subs': 0, 'locked': False,
                                         'standard': False}}, {
                                  '43': {'id': 43, 'name': 'Charter', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [42], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '8': {'id': 8, 'name': 'Charter Edition', 'description': None,
                                        'origin_id': None, 'first': None, 'last': None, 'root': [7],
                                        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
                                        'standard': False}}, {
                                  '10': {'id': 10, 'name': 'Chronicle Edition', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [7], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '15': {'id': 15, 'name': 'close match',
                                         'description': 'Concepts are sufficiently similar that they can be used interchangeably in some information retrieval applications.',
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [13], 'subs': [], 'count': 1, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '24': {'id': 24, 'name': 'Coin', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [23], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '39': {'id': 39, 'name': 'Conflict', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [34], 'subs': [40, 41], 'count': 0,
                                         'count_subs': 0, 'locked': False, 'standard': False}}, {
                                  '46': {'id': 46, 'name': 'Contract', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [42], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '21': {'id': 21, 'name': 'Count', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [16], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '27': {'id': 27, 'name': 'Creator', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [26], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '79': {'id': 79, 'name': 'Deposit', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [77], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '101': {'id': 101, 'name': 'Dimensions',
                                          'description': 'Physical dimensions like weight and height.',
                                          'origin_id': None, 'first': None, 'last': None,
                                          'root': [], 'subs': [102, 103], 'count': 0,
                                          'count_subs': 1, 'locked': False, 'standard': False}}, {
                                  '36': {'id': 36, 'name': 'Donation', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [35, 34], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '71': {'id': 71, 'name': 'Economic Site', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [65], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '63': {'id': 63, 'name': 'Economical', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [53], 'subs': [64], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '7': {'id': 7, 'name': 'Edition',
                                        'description': "Categories for the classification of written sources' editions like charter editions, chronicle edition etc.",
                                        'origin_id': None, 'first': None, 'last': None, 'root': [],
                                        'subs': [8, 10, 9], 'count': 0, 'count_subs': 0,
                                        'locked': False, 'standard': True}}, {
                                  '20': {'id': 20, 'name': 'Emperor', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [16], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '58': {'id': 58, 'name': 'Enemy of', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [56, 53], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '34': {'id': 34, 'name': 'Event',
                                         'description': 'Categories for the type of events like Change of property, Conflict, Movement, Attendance etc.',
                                         'origin_id': None, 'first': None, 'last': None, 'root': [],
                                         'subs': [35, 39], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': True}}, {
                                  '14': {'id': 14, 'name': 'exact match',
                                         'description': 'High degree of confidence that the concepts can be used interchangeably.',
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [13], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '38': {'id': 38, 'name': 'Exchange', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [35, 34], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '11': {'id': 11, 'name': 'External reference',
                                         'description': 'Categories for the classification of external references like a link to Wikipedia',
                                         'origin_id': None, 'first': None, 'last': None, 'root': [],
                                         'subs': [12], 'count': 0, 'count_subs': 0, 'locked': False,
                                         'standard': True}}, {
                                  '13': {'id': 13, 'name': 'External reference match',
                                         'description': 'SKOS based definition of the confidence degree that concepts can be used interchangeable.',
                                         'origin_id': None, 'first': None, 'last': None, 'root': [],
                                         'subs': [15, 14], 'count': 0, 'count_subs': 1,
                                         'locked': True, 'standard': True}}, {
                                  '74': {'id': 74, 'name': 'Feature',
                                         'description': 'Classification of the archaeological feature e.g. grave, pit, ...',
                                         'origin_id': None, 'first': None, 'last': None, 'root': [],
                                         'subs': [75, 76], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': True}}, {
                                  '32': {'id': 32, 'name': 'Female', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [31], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '57': {'id': 57, 'name': 'Friend of', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [56, 53], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '75': {'id': 75, 'name': 'Grave', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [74], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '102': {'id': 102, 'name': 'Height', 'description': 'centimeter',
                                          'origin_id': None, 'first': None, 'last': None,
                                          'root': [101], 'subs': [], 'count': 1, 'count_subs': 0,
                                          'locked': False, 'standard': False}}, {
                                  '80': {'id': 80, 'name': 'Human remains',
                                         'description': 'Human remains, that for example were discovered during archaeological excavations. They are associated with a stratigraphic unit (in most cases a skeleton) that is composed of (P46) one or multiple parts (in most cases bones) that are classified as biological objects (E20). From a hierarchical point of view the human remains are one level below the stratigraphic unit respectively the entity whose sum of parts resembles the individual/skeleton. This way individual bones or body parts can be treated individually and be connected with separate classifications (e.g. Injuries of the right upper arm or caries on a certain tooth).',
                                         'origin_id': None, 'first': None, 'last': None, 'root': [],
                                         'subs': [82, 81], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': True}}, {
                                  '4': {'id': 4, 'name': 'Inbook', 'description': None,
                                        'origin_id': None, 'first': None, 'last': None, 'root': [3],
                                        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
                                        'standard': False}}, {
                                  '70': {'id': 70, 'name': 'Infrastructure', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [65], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '26': {'id': 26, 'name': 'Involvement',
                                         'description': 'Categories to define the involvement of an actor within an event. E.g. "Napoleon" participated in the event "Invasion of Russia" as "Commander" or "Michelangelo" performed the event "painting of the Sistine chapel" as "Artist".',
                                         'origin_id': None, 'first': None, 'last': None, 'root': [],
                                         'subs': [27, 30, 28, 29], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': True}}, {
                                  '54': {'id': 54, 'name': 'Kindredship', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [53], 'subs': [55], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '22': {'id': 22, 'name': 'King', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [16], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '62': {'id': 62, 'name': 'Leader of (Retinue of)',
                                         'description': None, 'origin_id': None, 'first': None,
                                         'last': None, 'root': [60, 53], 'subs': [], 'count': 0,
                                         'count_subs': 0, 'locked': False, 'standard': False}}, {
                                  '45': {'id': 45, 'name': 'Letter', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [42], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '9': {'id': 9, 'name': 'Letter Edition', 'description': None,
                                        'origin_id': None, 'first': None, 'last': None, 'root': [7],
                                        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
                                        'standard': False}}, {'47': {'id': 47, 'name': 'License',
                                                                     'description': 'Types for the licensing of a file',
                                                                     'origin_id': None,
                                                                     'first': None, 'last': None,
                                                                     'root': [], 'subs': [49, 48],
                                                                     'count': 0, 'count_subs': 1,
                                                                     'locked': False,
                                                                     'standard': True}}, {
                                  '12': {'id': 12, 'name': 'Link', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [11], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '82': {'id': 82, 'name': 'Lower Body', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [80], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '33': {'id': 33, 'name': 'Male', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [31], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '59': {'id': 59, 'name': 'Mentor of (Student of)',
                                         'description': None, 'origin_id': None, 'first': None,
                                         'last': None, 'root': [56, 53], 'subs': [], 'count': 0,
                                         'count_subs': 0, 'locked': False, 'standard': False}}, {
                                  '67': {'id': 67, 'name': 'Military Facility', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [65], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '30': {'id': 30, 'name': 'Offender', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [26], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '49': {'id': 49, 'name': 'Open license', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [47], 'subs': [52, 51, 50], 'count': 1,
                                         'count_subs': 0, 'locked': False, 'standard': False}}, {
                                  '98': {'id': 98, 'name': 'Original Text', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [97], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '55': {'id': 55, 'name': 'Parent of (Child of)',
                                         'description': None, 'origin_id': None, 'first': None,
                                         'last': None, 'root': [54, 53], 'subs': [], 'count': 0,
                                         'count_subs': 0, 'locked': False, 'standard': False}}, {
                                  '76': {'id': 76, 'name': 'Pit', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [74], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '65': {'id': 65, 'name': 'Place',
                                         'description': 'Types for non-moveable entities (i.e. places) with a certain extent and/or location like Settlement, Burial site, Ritual site, Fortification etc.',
                                         'origin_id': None, 'first': None, 'last': None, 'root': [],
                                         'subs': [72, 69, 71, 70, 67, 68, 66, 73], 'count': 1,
                                         'count_subs': 0, 'locked': False, 'standard': True}}, {
                                  '60': {'id': 60, 'name': 'Political', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [53], 'subs': [61, 62], 'count': 0,
                                         'count_subs': 0, 'locked': False, 'standard': False}}, {
                                  '19': {'id': 19, 'name': 'Pope', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [16], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '48': {'id': 48, 'name': 'Proprietary license',
                                         'description': None, 'origin_id': None, 'first': None,
                                         'last': None, 'root': [47], 'subs': [], 'count': 0,
                                         'count_subs': 0, 'locked': False, 'standard': False}}, {
                                  '64': {'id': 64, 'name': 'Provider of (Customer of)',
                                         'description': None, 'origin_id': None, 'first': None,
                                         'last': None, 'root': [63, 53], 'subs': [], 'count': 0,
                                         'count_subs': 0, 'locked': False, 'standard': False}}, {
                                  '50': {'id': 50, 'name': 'Public domain', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [49, 47], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '41': {'id': 41, 'name': 'Raid', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [39, 34], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '68': {'id': 68, 'name': 'Ritual Site', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [65], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '37': {'id': 37, 'name': 'Sale', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [35, 34], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '66': {'id': 66, 'name': 'Settlement', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [65], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '31': {'id': 31, 'name': 'Sex',
                                         'description': 'Categories for sex like female, male.',
                                         'origin_id': None, 'first': None, 'last': None, 'root': [],
                                         'subs': [32, 33], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '56': {'id': 56, 'name': 'Social', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [53], 'subs': [58, 57, 59], 'count': 0,
                                         'count_subs': 0, 'locked': False, 'standard': False}}, {
                                  '42': {'id': 42, 'name': 'Source',
                                         'description': 'Types for historical sources like charter, chronicle, letter etc.',
                                         'origin_id': None, 'first': None, 'last': None, 'root': [],
                                         'subs': [43, 46, 45, 44], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': True}}, {
                                  '97': {'id': 97, 'name': 'Source translation',
                                         'description': None, 'origin_id': None, 'first': None,
                                         'last': None, 'root': [], 'subs': [98, 99, 100],
                                         'count': 0, 'count_subs': 0, 'locked': False,
                                         'standard': False}}, {
                                  '28': {'id': 28, 'name': 'Sponsor', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [26], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '25': {'id': 25, 'name': 'Statue', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [23], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '77': {'id': 77, 'name': 'Stratigraphic unit',
                                         'description': 'Classification of the archaeological SU e.g. burial, deposit, ...',
                                         'origin_id': None, 'first': None, 'last': None, 'root': [],
                                         'subs': [78, 79], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': True}}, {
                                  '44': {'id': 44, 'name': 'Testament', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [42], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '73': {'id': 73, 'name': 'Topographical Entity',
                                         'description': None, 'origin_id': None, 'first': None,
                                         'last': None, 'root': [65], 'subs': [], 'count': 0,
                                         'count_subs': 0, 'locked': False, 'standard': False}}, {
                                  '99': {'id': 99, 'name': 'Translation', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [97], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '100': {'id': 100, 'name': 'Transliteration', 'description': None,
                                          'origin_id': None, 'first': None, 'last': None,
                                          'root': [97], 'subs': [], 'count': 0, 'count_subs': 0,
                                          'locked': False, 'standard': False}}, {
                                  '81': {'id': 81, 'name': 'Upper Body', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [80], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '29': {'id': 29, 'name': 'Victim', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [26], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '103': {'id': 103, 'name': 'Weight', 'description': 'gram',
                                          'origin_id': None, 'first': None, 'last': None,
                                          'root': [101], 'subs': [], 'count': 0, 'count_subs': 0,
                                          'locked': False, 'standard': False}}, {
                                  '83': {'id': 83, 'name': 'Administrative unit',
                                         'description': 'Hierarchy of administrative units like "Austria", "Germany", "Italy" and their respective subunits like "Lower Austria", "Styria" and their subunits etc.',
                                         'origin_id': None, 'first': None, 'last': None, 'root': [],
                                         'subs': [84, 89, 87, 88, 90, 91], 'count': 6,
                                         'count_subs': 2, 'locked': False, 'standard': True}}, {
                                  '84': {'id': 84, 'name': 'Austria', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [83], 'subs': [86, 85], 'count': 2,
                                         'count_subs': 0, 'locked': False, 'standard': False}}, {
                                  '93': {'id': 93, 'name': 'Carantania', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [92], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '95': {'id': 95, 'name': 'Comitatus Iauntal', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [92], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '89': {'id': 89, 'name': 'Czech Republic', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [83], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '87': {'id': 87, 'name': 'Germany', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [83], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '92': {'id': 92, 'name': 'Historical place',
                                         'description': 'Hierarchy of historical places respectively historical administrative units like: Duchy of Bavaria, Lombard Kingdom etc.',
                                         'origin_id': None, 'first': None, 'last': None, 'root': [],
                                         'subs': [93, 95, 96, 94], 'count': 4, 'count_subs': 0,
                                         'locked': False, 'standard': True}}, {
                                  '88': {'id': 88, 'name': 'Italy', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [83], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '96': {'id': 96, 'name': 'Kingdom of Serbia', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [92], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '94': {'id': 94, 'name': 'Marcha Orientalis', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [92], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '86': {'id': 86, 'name': 'Niederösterreich', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [84, 83], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '90': {'id': 90, 'name': 'Slovakia', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [83], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '91': {'id': 91, 'name': 'Slovenia', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [83], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}, {
                                  '85': {'id': 85, 'name': 'Wien', 'description': None,
                                         'origin_id': None, 'first': None, 'last': None,
                                         'root': [84, 83], 'subs': [], 'count': 0, 'count_subs': 0,
                                         'locked': False, 'standard': False}}]}

api_code_reference = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/107', 'type': 'Feature', 'crmClass': 'crm:E31 Document',
         'systemClass': 'external_reference', 'properties': {'title': 'https://openatlas.eu'},
         'description': None, 'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                                      'end': {'earliest': None, 'latest': None}}]},
         'types': None, 'relations': [
            {'label': 'Nostromos', 'relationTo': 'http://local.host/api/0.2/entity/104',
             'relationType': 'crm:P67 refers to', 'relationSystemClass': 'place', 'type': None,
             'when': {'timespans': [{'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                                     'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]}}],
         'names': None, 'links': None, 'geometry': None, 'depictions': None}]}],
    'pagination': {'entities': 1, 'entitiesPerPage': 20,
                   'index': [{'page': 1, 'startId': 107}], 'totalPages': 1}}

api_code_reference_geojson = {'pagination': {'entities': 1,
                                             'entitiesPerPage': 20,
                                             'index': [{'page': 1, 'startId': 107}],
                                             'totalPages': 1},
                              'results': [{'features': [{'geometry': None,
                                                         'properties': {'@id': 107,
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
         'properties': {'title': 'Feature'}, 'description': None, 'when': {'timespans': [
            {'start': {'earliest': None, 'latest': None},
             'end': {'earliest': None, 'latest': None}}]}, 'types': None, 'relations': [
            {'label': 'Location of Feature', 'relationTo': 'http://local.host/api/0.2/entity/109',
             'relationType': 'crm:P53 has former or current location',
             'relationSystemClass': 'object_location', 'type': None, 'when': {'timespans': [
                {'start': {'earliest': None, 'latest': None},
                 'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Strato', 'relationTo': 'http://local.host/api/0.2/entity/110',
             'relationType': 'crm:P46 is composed of', 'relationSystemClass': 'stratigraphic_unit',
             'type': None, 'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                                   'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Nostromos', 'relationTo': 'http://local.host/api/0.2/entity/104',
             'relationType': 'crm:P46i forms part of', 'relationSystemClass': 'place', 'type': None,
             'when': {'timespans': [{'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                                     'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]}}],
         'names': None, 'links': None, 'geometry': {'type': 'GeometryCollection', 'geometries': []},
         'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/104', 'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing', 'systemClass': 'place',
         'properties': {'title': 'Nostromos'}, 'description': [{'value': 'That is the Nostromos'}],
         'when': {'timespans': [{'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                                 'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]},
         'types': [{'identifier': 'http://local.host/api/0.2/entity/65', 'label': 'Place',
                    'description': None, 'hierarchy': '', 'value': None, 'unit': None},
                   {'identifier': 'http://local.host/api/0.2/entity/102', 'label': 'Height',
                    'description': None, 'hierarchy': 'Dimensions', 'value': 23.0,
                    'unit': 'centimeter'}], 'relations': [
            {'label': 'Cargo hauler', 'relationTo': 'http://local.host/api/0.2/entity/106',
             'relationType': 'crm:P1 is identified by', 'relationSystemClass': 'appellation',
             'type': None, 'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                                   'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Feature', 'relationTo': 'http://local.host/api/0.2/entity/108',
             'relationType': 'crm:P46 is composed of', 'relationSystemClass': 'feature',
             'type': None, 'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                                   'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Height', 'relationTo': 'http://local.host/api/0.2/entity/102',
             'relationType': 'crm:P2 has type', 'relationSystemClass': 'type', 'type': None,
             'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                     'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Location of Nostromos', 'relationTo': 'http://local.host/api/0.2/entity/105',
             'relationType': 'crm:P53 has former or current location',
             'relationSystemClass': 'object_location', 'type': None, 'when': {'timespans': [
                {'start': {'earliest': None, 'latest': None},
                 'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Place', 'relationTo': 'http://local.host/api/0.2/entity/65',
             'relationType': 'crm:P2 has type', 'relationSystemClass': 'type', 'type': None,
             'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                     'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Datei', 'relationTo': 'http://local.host/api/0.2/entity/112',
             'relationType': 'crm:P67i is referred to by', 'relationSystemClass': 'file',
             'type': None, 'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                                   'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'GeoNames', 'relationTo': 'http://local.host/api/0.2/entity/1',
             'relationType': 'crm:P67i is referred to by',
             'relationSystemClass': 'reference_system', 'type': 'close match', 'when': {
                'timespans': [{'start': {'earliest': None, 'latest': None},
                               'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'https://openatlas.eu', 'relationTo': 'http://local.host/api/0.2/entity/107',
             'relationType': 'crm:P67i is referred to by',
             'relationSystemClass': 'external_reference', 'type': None, 'when': {'timespans': [
                {'start': {'earliest': None, 'latest': None},
                 'end': {'earliest': None, 'latest': None}}]}}],
         'names': [{'alias': 'Cargo hauler'}], 'links': [
            {'type': 'close match', 'identifier': 'https://www.geonames.org/2761369',
             'referenceSystem': 'GeoNames'}],
         'geometry': {'type': 'Point', 'coordinates': [9, 17], 'title': '', 'description': ''},
         'depictions': [{'@id': 'http://local.host/api/0.2/entity/112', 'title': 'Datei',
                         'license': 'Open license', 'url': 'N/A'}]}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/110', 'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing', 'systemClass': 'stratigraphic_unit',
         'properties': {'title': 'Strato'}, 'description': None, 'when': {'timespans': [
            {'start': {'earliest': None, 'latest': None},
             'end': {'earliest': None, 'latest': None}}]}, 'types': None, 'relations': [
            {'label': 'Location of Strato', 'relationTo': 'http://local.host/api/0.2/entity/111',
             'relationType': 'crm:P53 has former or current location',
             'relationSystemClass': 'object_location', 'type': None, 'when': {'timespans': [
                {'start': {'earliest': None, 'latest': None},
                 'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Feature', 'relationTo': 'http://local.host/api/0.2/entity/108',
             'relationType': 'crm:P46i forms part of', 'relationSystemClass': 'feature',
             'type': None, 'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                                   'end': {'earliest': None, 'latest': None}}]}}],
         'names': None, 'links': None, 'geometry': {'type': 'GeometryCollection', 'geometries': []},
         'depictions': None}]}], 'pagination': {'entities': 3, 'entitiesPerPage': 20,
                                                'index': [{'page': 1, 'startId': 108}],
                                                'totalPages': 1}}

api_code_place_filter_time = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/108', 'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing', 'systemClass': 'feature',
         'properties': {'title': 'Feature'}, 'description': None, 'when': {'timespans': [
            {'start': {'earliest': None, 'latest': None},
             'end': {'earliest': None, 'latest': None}}]}, 'types': None, 'relations': [
            {'label': 'Location of Feature', 'relationTo': 'http://local.host/api/0.2/entity/109',
             'relationType': 'crm:P53 has former or current location',
             'relationSystemClass': 'object_location', 'type': None, 'when': {'timespans': [
                {'start': {'earliest': None, 'latest': None},
                 'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Strato', 'relationTo': 'http://local.host/api/0.2/entity/110',
             'relationType': 'crm:P46 is composed of', 'relationSystemClass': 'stratigraphic_unit',
             'type': None, 'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                                   'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Nostromos', 'relationTo': 'http://local.host/api/0.2/entity/104',
             'relationType': 'crm:P46i forms part of', 'relationSystemClass': 'place', 'type': None,
             'when': {'timespans': [{'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                                     'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]}}],
         'names': None, 'links': None, 'geometry': {'type': 'GeometryCollection', 'geometries': []},
         'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/104', 'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing', 'systemClass': 'place',
         'properties': {'title': 'Nostromos'}, 'description': [{'value': 'That is the Nostromos'}],
         'when': {'timespans': [{'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                                 'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]},
         'types': [{'identifier': 'http://local.host/api/0.2/entity/65', 'label': 'Place',
                    'description': None, 'hierarchy': '', 'value': None, 'unit': None},
                   {'identifier': 'http://local.host/api/0.2/entity/102', 'label': 'Height',
                    'description': None, 'hierarchy': 'Dimensions', 'value': 23.0,
                    'unit': 'centimeter'}], 'relations': [
            {'label': 'Cargo hauler', 'relationTo': 'http://local.host/api/0.2/entity/106',
             'relationType': 'crm:P1 is identified by', 'relationSystemClass': 'appellation',
             'type': None, 'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                                   'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Feature', 'relationTo': 'http://local.host/api/0.2/entity/108',
             'relationType': 'crm:P46 is composed of', 'relationSystemClass': 'feature',
             'type': None, 'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                                   'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Height', 'relationTo': 'http://local.host/api/0.2/entity/102',
             'relationType': 'crm:P2 has type', 'relationSystemClass': 'type', 'type': None,
             'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                     'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Location of Nostromos', 'relationTo': 'http://local.host/api/0.2/entity/105',
             'relationType': 'crm:P53 has former or current location',
             'relationSystemClass': 'object_location', 'type': None, 'when': {'timespans': [
                {'start': {'earliest': None, 'latest': None},
                 'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Place', 'relationTo': 'http://local.host/api/0.2/entity/65',
             'relationType': 'crm:P2 has type', 'relationSystemClass': 'type', 'type': None,
             'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                     'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Datei', 'relationTo': 'http://local.host/api/0.2/entity/112',
             'relationType': 'crm:P67i is referred to by', 'relationSystemClass': 'file',
             'type': None, 'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                                   'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'GeoNames', 'relationTo': 'http://local.host/api/0.2/entity/1',
             'relationType': 'crm:P67i is referred to by',
             'relationSystemClass': 'reference_system', 'type': 'close match', 'when': {
                'timespans': [{'start': {'earliest': None, 'latest': None},
                               'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'https://openatlas.eu', 'relationTo': 'http://local.host/api/0.2/entity/107',
             'relationType': 'crm:P67i is referred to by',
             'relationSystemClass': 'external_reference', 'type': None, 'when': {'timespans': [
                {'start': {'earliest': None, 'latest': None},
                 'end': {'earliest': None, 'latest': None}}]}}],
         'names': [{'alias': 'Cargo hauler'}], 'links': [
            {'type': 'close match', 'identifier': 'https://www.geonames.org/2761369',
             'referenceSystem': 'GeoNames'}],
         'geometry': {'type': 'Point', 'coordinates': [9, 17], 'title': '', 'description': ''},
         'depictions': [{'@id': 'http://local.host/api/0.2/entity/112', 'title': 'Datei',
                         'license': 'Open license', 'url': 'N/A'}]}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/110', 'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing', 'systemClass': 'stratigraphic_unit',
         'properties': {'title': 'Strato'}, 'description': None, 'when': {'timespans': [
            {'start': {'earliest': None, 'latest': None},
             'end': {'earliest': None, 'latest': None}}]}, 'types': None, 'relations': [
            {'label': 'Location of Strato', 'relationTo': 'http://local.host/api/0.2/entity/111',
             'relationType': 'crm:P53 has former or current location',
             'relationSystemClass': 'object_location', 'type': None, 'when': {'timespans': [
                {'start': {'earliest': None, 'latest': None},
                 'end': {'earliest': None, 'latest': None}}]}},
            {'label': 'Feature', 'relationTo': 'http://local.host/api/0.2/entity/108',
             'relationType': 'crm:P46i forms part of', 'relationSystemClass': 'feature',
             'type': None, 'when': {'timespans': [{'start': {'earliest': None, 'latest': None},
                                                   'end': {'earliest': None, 'latest': None}}]}}],
         'names': None, 'links': None, 'geometry': {'type': 'GeometryCollection', 'geometries': []},
         'depictions': None}]}], 'pagination': {'entities': 3, 'entitiesPerPage': 20,
                                                'index': [{'page': 1, 'startId': 108}],
                                                'totalPages': 1}}
