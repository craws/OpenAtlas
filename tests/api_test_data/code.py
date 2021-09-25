test_code = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [
        {'@id': 'http://local.host/entity/108',
         'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing',
         'systemClass': 'feature',
         'properties': {'title': 'Home of Baggins'},
         'description': None,
         'when': {'timespans': [
             {'start': {'earliest': 'None', 'latest': 'None'},
              'end': {'earliest': 'None', 'latest': 'None'}}]},
         'types': None,
         'relations': [
             {'label': 'Kitchen',
              'relationTo': 'http://local.host/api/0.2/entity/110',
              'relationType': 'crm:P46 is composed of',
              'relationSystemClass': 'stratigraphic_unit',
              'relationDescription': None, 'type': None, 'when': {
                 'timespans': [{'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}},
             {'label': 'Location of Home of Baggins',
              'relationTo': 'http://local.host/api/0.2/entity/109',
              'relationType': 'crm:P53 has former or current location',
              'relationSystemClass': 'object_location',
              'relationDescription': None, 'type': None, 'when': {
                 'timespans': [
                     {'start': {'earliest': 'None', 'latest': 'None'},
                      'end': {'earliest': 'None',
                              'latest': 'None'}}]}},
             {'label': 'Shire',
              'relationTo': 'http://local.host/api/0.2/entity/104',
              'relationType': 'crm:P46i forms part of',
              'relationSystemClass': 'place',
              'relationDescription': None, 'type': None, 'when': {
                 'timespans': [{'start': {'earliest': '2018-01-31',
                                          'latest': '2018-03-01'},
                                'end': {'earliest': '2019-01-31',
                                        'latest': '2019-03-01'}}]}}],
         'names': None,
         'links': None,
         'geometry': {'type': 'GeometryCollection',
                      'geometries': []},
         'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [
        {'@id': 'http://local.host/entity/110',
         'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing',
         'systemClass': 'stratigraphic_unit',
         'properties': {'title': 'Kitchen'},
         'description': None,
         'when': {
             'timespans': [{'start': {'earliest': 'None', 'latest': 'None'},
                            'end': {'earliest': 'None', 'latest': 'None'}}]},
         'types': None,
         'relations': [
             {'label': 'Location of Kitchen',
              'relationTo': 'http://local.host/api/0.2/entity/111',
              'relationType': 'crm:P53 has former or current location',
              'relationSystemClass': 'object_location',
              'relationDescription': None,
              'type': None, 'when': {'timespans': [
                 {'start': {'earliest': 'None', 'latest': 'None'},
                  'end': {'earliest': 'None', 'latest': 'None'}}]}},
             {'label': 'Home of Baggins',
              'relationTo': 'http://local.host/api/0.2/entity/108',
              'relationType': 'crm:P46i forms part of',
              'relationSystemClass': 'feature',
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
         'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [
        {'@id': 'http://local.host/entity/120',
         'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing',
         'systemClass': 'place',
         'properties': {'title': 'Mordor'},
         'description': [{'value': 'The heart of evil.'}],
         'when': {
             'timespans': [{'start': {'earliest': 'None', 'latest': 'None'},
                            'end': {'earliest': 'None', 'latest': 'None'}}]},
         'types': [
             {'identifier': 'http://local.host/api/0.2/entity/72',
              'label': 'Boundary Mark', 'description': None,
              'hierarchy': 'Place', 'value': None, 'unit': None}],
         'relations': [
             {'label': 'Boundary Mark',
              'relationTo': 'http://local.host/api/0.2/entity/72',
              'relationType': 'crm:P2 has type',
              'relationSystemClass': 'type',
              'relationDescription': None, 'type': None, 'when': {
                 'timespans': [{'start': {'earliest': 'None', 'latest': 'None'},
                                'end': {'earliest': 'None',
                                        'latest': 'None'}}]}},
             {'label': 'Location of Mordor',
              'relationTo': 'http://local.host/api/0.2/entity/121',
              'relationType': 'crm:P53 has former or current location',
              'relationSystemClass': 'object_location',
              'relationDescription': None, 'type': None, 'when': {
                 'timespans': [
                     {'start': {'earliest': 'None', 'latest': 'None'},
                      'end': {'earliest': 'None',
                              'latest': 'None'}}]}}],
         'names': None,
         'links': None,
         'geometry': {'type': 'GeometryCollection', 'geometries': []},
         'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/104',
         'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing',
         'systemClass': 'place',
         'properties': {'title': 'Shire'},
         'description': [
             {'value': 'The Shire was the homeland of the hobbits.'}],
         'when': {
             'timespans': [
                 {'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                  'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]},
         'types': [
             {'identifier': 'http://local.host/api/0.2/entity/65',
              'label': 'Place', 'description': None, 'hierarchy': '',
              'value': None, 'unit': None},
             {'identifier': 'http://local.host/api/0.2/entity/102',
              'label': 'Height', 'description': None,
              'hierarchy': 'Dimensions', 'value': 23.0,
              'unit': 'centimeter'}],
         'relations': [
             {'label': 'Height',
              'relationTo': 'http://local.host/api/0.2/entity/102',
              'relationType': 'crm:P2 has type',
              'relationSystemClass': 'type',
              'relationDescription': '23.0',
              'type': None,
              'when': {
                  'timespans': [{
                      'start': {
                          'earliest': 'None',
                          'latest': 'None'},
                      'end': {
                          'earliest': 'None',
                          'latest': 'None'}}]}},
             {
                 'label': 'Home of Baggins',
                 'relationTo': 'http://local.host/api/0.2/entity/108',
                 'relationType': 'crm:P46 is composed of',
                 'relationSystemClass': 'feature',
                 'relationDescription': None,
                 'type': None,
                 'when': {
                     'timespans': [
                         {
                             'start': {
                                 'earliest': 'None',
                                 'latest': 'None'},
                             'end': {
                                 'earliest': 'None',
                                 'latest': 'None'}}]}},
             {
                 'label': 'Location of Shire',
                 'relationTo': 'http://local.host/api/0.2/entity/105',
                 'relationType': 'crm:P53 has former or current location',
                 'relationSystemClass': 'object_location',
                 'relationDescription': None,
                 'type': None,
                 'when': {
                     'timespans': [
                         {
                             'start': {
                                 'earliest': 'None',
                                 'latest': 'None'},
                             'end': {
                                 'earliest': 'None',
                                 'latest': 'None'}}]}},
             {'label': 'Place',
              'relationTo': 'http://local.host/api/0.2/entity/65',
              'relationType': 'crm:P2 has type',
              'relationSystemClass': 'type',
              'relationDescription': None,
              'type': None,
              'when': {
                  'timespans': [{
                      'start': {
                          'earliest': 'None',
                          'latest': 'None'},
                      'end': {
                          'earliest': 'None',
                          'latest': 'None'}}]}},
             {'label': 'Sûza',
              'relationTo': 'http://local.host/api/0.2/entity/106',
              'relationType': 'crm:P1 is identified by',
              'relationSystemClass': 'appellation',
              'relationDescription': None,
              'type': None,
              'when': {
                  'timespans': [{
                      'start': {
                          'earliest': 'None',
                          'latest': 'None'},
                      'end': {
                          'earliest': 'None',
                          'latest': 'None'}}]}},
             {'label': 'GeoNames',
              'relationTo': 'http://local.host/api/0.2/entity/1',
              'relationType': 'crm:P67i is referred to by',
              'relationSystemClass': 'reference_system',
              'relationDescription': '2761369',
              'type': 'closeMatch',
              'when': {
                  'timespans': [{
                      'start': {
                          'earliest': 'None',
                          'latest': 'None'},
                      'end': {
                          'earliest': 'None',
                          'latest': 'None'}}]}},
             {
                 'label': 'https://lotr.fandom.com/',
                 'relationTo': 'http://local.host/api/0.2/entity/107',
                 'relationType': 'crm:P67i is referred to by',
                 'relationSystemClass': 'external_reference',
                 'relationDescription': 'Fandom Wiki of lord of the rings',
                 'type': None,
                 'when': {
                     'timespans': [
                         {
                             'start': {
                                 'earliest': 'None',
                                 'latest': 'None'},
                             'end': {
                                 'earliest': 'None',
                                 'latest': 'None'}}]}},
             {
                 'label': 'Picture with a License',
                 'relationTo': 'http://local.host/api/0.2/entity/112',
                 'relationType': 'crm:P67i is referred to by',
                 'relationSystemClass': 'file',
                 'relationDescription': None,
                 'type': None,
                 'when': {
                     'timespans': [
                         {
                             'start': {
                                 'earliest': 'None',
                                 'latest': 'None'},
                             'end': {
                                 'earliest': 'None',
                                 'latest': 'None'}}]}}],
         'names': [{'alias': 'Sûza'}],
         'links': [{'type': 'closeMatch',
                    'identifier': 'https://www.geonames.org/2761369',
                    'referenceSystem': 'GeoNames'}],
         'geometry': {'type': 'Point',
                      'coordinates': [9, 17],
                      'title': '',
                      'description': ''},
         'depictions': [
             {'@id': 'http://local.host/api/0.2/entity/112',
              'title': 'Picture with a License', 'license': 'Open license',
              'url': 'N/A'}]}]}],
    'pagination': {'entities': 4,
                   'entitiesPerPage': 20,
                   'index': [{'page': 1, 'startId': 108}],
                   'totalPages': 1}}