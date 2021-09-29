test_lpf = {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/104', 'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing', 'systemClass': 'place',
         'properties': {'title': 'Shire'},
         'description': [
             {'value': 'The Shire was the homeland of the hobbits.'}],
         'when': {
             'timespans': [
                 {'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                  'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]},
         'types': [{'identifier': 'http://local.host/api/0.2/entity/63',
                    'label': 'Place', 'description': None, 'hierarchy': '',
                    'value': None, 'unit': None},
                   {'identifier': 'http://local.host/api/0.2/entity/100',
                    'label': 'Height', 'description': None,
                    'hierarchy': 'Dimensions', 'value': 23.0,
                    'unit': 'centimeter'}],
         'relations': [
             {'label': 'Height',
              'relationTo': 'http://local.host/api/0.2/entity/100',
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
             {'label': 'Home of Baggins',
              'relationTo': 'http://local.host/api/0.2/entity/108',
              'relationType': 'crm:P46 is composed of',
              'relationSystemClass': 'feature',
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
             {'label': 'Location of Shire',
              'relationTo': 'http://local.host/api/0.2/entity/105',
              'relationType': 'crm:P53 has former or current location',
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
                          'latest': 'None'}}]}},
             {'label': 'Place',
              'relationTo': 'http://local.host/api/0.2/entity/63',
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
              'relationTo': 'http://local.host/api/0.2/entity/102',
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
             {'label': 'https://lotr.fandom.com/',
              'relationTo': 'http://local.host/api/0.2/entity/107',
              'relationType': 'crm:P67i is referred to by',
              'relationSystemClass': 'external_reference',
              'relationDescription': 'Fandom Wiki of lord of the rings',
              'type': None,
              'when': {
                  'timespans': [{
                      'start': {
                          'earliest': 'None',
                          'latest': 'None'},
                      'end': {
                          'earliest': 'None',
                          'latest': 'None'}}]}},
             {'label': 'Picture with a License',
              'relationTo': 'http://local.host/api/0.2/entity/112',
              'relationType': 'crm:P67i is referred to by',
              'relationSystemClass': 'file',
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
         'names': [{'alias': 'Sûza'}],
         'links': [{'type': 'closeMatch',
                    'identifier': 'https://www.geonames.org/2761369',
                    'referenceSystem': 'GeoNames'}],
         'geometry': {'type': 'Point', 'coordinates': [9, 17], 'title': '',
                      'description': ''},
         'depictions': [
             {'@id': 'http://local.host/api/0.2/entity/112',
              'title': 'Picture with a License', 'license': 'Open license',
              'url': 'N/A'}]}]}
test_geojson = {
    'type': 'FeatureCollection',
    'features': [{
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [9, 17],
            'title': '',
            'description': ''},
        'properties': {
            '@id': 104,
            'systemClass': 'place',
            'name': 'Shire',
            'description': 'The Shire was the homeland of the hobbits.',
            'begin_earliest': '2018-01-31',
            'begin_latest': '2018-03-01',
            'begin_comment': 'Begin of the shire',
            'end_earliest': '2019-01-31',
            'end_latest': '2019-03-01',
            'end_comment': 'Descent of Shire',
            'types': ['Place', 'Height']}}]}
