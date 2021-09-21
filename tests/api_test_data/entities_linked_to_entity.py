test_entities_linked_to = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/113',
         'type': 'Feature',
         'crmClass': 'crm:E21 Person',
         'systemClass': 'person',
         'properties': {'title': 'Frodo'},
         'description': [{'value': 'That is Frodo'}],
         'when': {'timespans': [
             {'start': {'earliest': 'None', 'latest': 'None'},
              'end': {'earliest': 'None', 'latest': 'None'}}]},
         'types': None,
         'relations': [{
             'label': 'Sam',
             'relationTo': 'http://local.host/api/0.2/entity/118',
             'relationType': 'crm:OA7 has relationship to',
             'relationSystemClass': 'person',
             'relationDescription': None, 'type': 'Economical',
             'when': {'timespans': [
                 {'start': {'earliest': 'None', 'latest': 'None'},
                  'end': {'earliest': 'None', 'latest': 'None'}}]}},
             {'label': 'File without license',
              'relationTo': 'http://local.host/api/0.2/entity/115',
              'relationType': 'crm:P67i is referred to by',
              'relationSystemClass': 'file',
              'relationDescription': None, 'type': None, 'when': {
                 'timespans': [
                     {'start': {'earliest': 'None', 'latest': 'None'},
                      'end': {'earliest': 'None',
                              'latest': 'None'}}]}},
             {'label': 'The One Ring',
              'relationTo': 'http://local.host/api/0.2/entity/116',
              'relationType': 'crm:P52i is current owner of',
              'relationSystemClass': 'artifact',
              'relationDescription': None, 'type': None, 'when': {
                 'timespans': [
                     {'start': {'earliest': 'None', 'latest': 'None'},
                      'end': {'earliest': 'None',
                              'latest': 'None'}}]}},
             {'label': 'Travel to Mordor',
              'relationTo': 'http://local.host/api/0.2/entity/119',
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
         'depictions': [
             {'@id': 'http://local.host/api/0.2/entity/115',
              'title': 'File without license',
              'license': None,
              'url': 'N/A'}]}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/105',
         'type': 'Feature',
         'crmClass': 'crm:E53 Place',
         'systemClass': 'object_location',
         'properties': {'title': 'Location of Shire'},
         'description': None,
         'when': {'timespans': [
             {'start': {'earliest': 'None', 'latest': 'None'},
              'end': {'earliest': 'None', 'latest': 'None'}}]},
         'types': None,
         'relations': [{
             'label': 'Shire',
             'relationTo': 'http://local.host/api/0.2/entity/104',
             'relationType': 'crm:P53i is former or current location of',
             'relationSystemClass': 'place',
             'relationDescription': None, 'type': None, 'when': {
                 'timespans': [{'start': {'earliest': '2018-01-31',
                                          'latest': '2018-03-01'},
                                'end': {'earliest': '2019-01-31',
                                        'latest': '2019-03-01'}}]}},
             {'label': 'Travel to Mordor',
              'relationTo': 'http://local.host/api/0.2/entity/119',
              'relationType': 'crm:P7i witnessed',
              'relationSystemClass': 'activity',
              'relationDescription': None, 'type': None, 'when': {
                 'timespans': [
                     {'start': {'earliest': 'None', 'latest': 'None'},
                      'end': {'earliest': 'None',
                              'latest': 'None'}}]}}],
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
    'features': [
        {'@id': 'http://local.host/entity/118',
         'type': 'Feature',
         'crmClass': 'crm:E21 Person',
         'systemClass': 'person',
         'properties': {'title': 'Sam'},
         'description': [{'value': 'That is Sam'}],
         'when': {'timespans': [
             {'start': {'earliest': 'None', 'latest': 'None'},
              'end': {'earliest': 'None', 'latest': 'None'}}]},
         'types': None,
         'relations': [{
             'label': 'Frodo',
             'relationTo': 'http://local.host/api/0.2/entity/113',
             'relationType': 'crm:OA7 has relationship to',
             'relationSystemClass': 'person',
             'relationDescription': None, 'type': 'Economical',
             'when': {'timespans': [
                 {'start': {'earliest': 'None', 'latest': 'None'},
                  'end': {'earliest': 'None', 'latest': 'None'}}]}},
             {'label': 'Travel to Mordor',
              'relationTo': 'http://local.host/api/0.2/entity/119',
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
         'depictions': None}]}],
    'pagination': {
        'entities': 3,
        'entitiesPerPage': 20,
        'index': [{'page': 1, 'startId': 113}],
        'totalPages': 1}}
