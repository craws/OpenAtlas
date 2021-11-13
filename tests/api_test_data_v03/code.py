class Code:
    @staticmethod
    def get_test_code(params):
        return {'results': [{
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
                    'relationTo':
                        f'http://local.host/api/0.3/entity/{params["kitchen_id"]}',
                    'relationType': 'crm:P46 is composed of',
                    'relationSystemClass': 'stratigraphic_unit',
                    'relationDescription': None,
                    'type': None,
                    'when': {
                        'timespans': [{
                            'start': {'earliest': 'None', 'latest': 'None'},
                            'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
                    'label': 'Location of Home of Baggins',
                    'relationTo':
                        f'http://local.host/api/0.3/entity/{params["location_home_id"]}',
                    'relationType': 'crm:P53 has former or current location',
                    'relationSystemClass': 'object_location',
                    'relationDescription': None, 'type': None, 'when': {
                        'timespans': [{
                            'start': {'earliest': 'None', 'latest': 'None'},
                            'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
                    'label': 'Shire',
                    'relationTo':
                        f'http://local.host/api/0.3/entity/{params["shire_id"]}',
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
                'depictions': None}]}, {
            '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
            'type': 'FeatureCollection',
            'features': [
                {'@id': f'http://local.host/entity/{params["kitchen_id"]}',
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
                     'relationTo':
                         f'http://local.host/api/0.3/entity/{params["location_kitchen_id"]}',
                     'relationType': 'crm:P53 has former or current location',
                     'relationSystemClass': 'object_location',
                     'relationDescription': None,
                     'type': None,
                     'when': {
                         'timespans': [{
                             'start': {'earliest': 'None', 'latest': 'None'},
                             'end': {'earliest': 'None', 'latest': 'None'}}]}},
                     {
                         'label': 'Home of Baggins',
                         'relationTo': f'http://local.host/api/0.3/entity/{params["home_id"]}',
                         'relationType': 'crm:P46i forms part of',
                         'relationSystemClass': 'feature',
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
                 'geometry': {'type': 'GeometryCollection', 'geometries': []},
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
                        f'http://local.host/api/0.3/entity/{params["boundary_mark_id"]}',
                    'label': 'Boundary Mark', 'description': None,
                    'hierarchy': 'Place', 'value': None, 'unit': None}],
                'relations': [{
                    'label': 'Boundary Mark',
                    'relationTo':
                        f'http://local.host/api/0.3/entity/{params["boundary_mark_id"]}',
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
                        f'http://local.host/api/0.3/entity/{params["location_mordor_id"]}',
                    'relationType': 'crm:P53 has former or current location',
                    'relationSystemClass': 'object_location',
                    'relationDescription': None, 'type': None, 'when': {
                        'timespans': [{
                            'start': {'earliest': 'None', 'latest': 'None'},
                            'end': {'earliest': 'None', 'latest': 'None'}}]}}],
                'names': None,
                'links': None,
                'geometry': {'type': 'GeometryCollection', 'geometries': []},
                'depictions': None}]}, {
            '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
            'type': 'FeatureCollection', 'features': [
                {'@id': f'http://local.host/entity/{params["shire_id"]}',
                 'type': 'Feature',
                 'crmClass': 'crm:E18 Physical Thing',
                 'systemClass': 'place',
                 'properties': {'title': 'Shire'},
                 'description': [{
                     'value': 'The Shire was the homeland of the hobbits.'}],
                 'when': {
                     'timespans': [{
                         'start': {'earliest': '2018-01-31',
                                   'latest': '2018-03-01'},
                         'end': {'earliest': '2019-01-31',
                                 'latest': '2019-03-01'}}]},
                 'types': [{
                     'identifier':
                         f'http://local.host/api/0.3/entity/{params["place_id"]}',
                     'label': 'Place',
                     'description': None,
                     'hierarchy': '',
                     'value': None,
                     'unit': None}, {
                     'identifier':
                         f'http://local.host/api/0.3/entity/{params["height_id"]}',
                     'label': 'Height', 'description': None,
                     'hierarchy': 'Dimensions', 'value': 23.0,
                     'unit': 'centimeter'}],
                 'relations': [{
                     'label': 'Height',
                     'relationTo':
                         f'http://local.host/api/0.3/entity/{params["height_id"]}',
                     'relationType': 'crm:P2 has type',
                     'relationSystemClass': 'type',
                     'relationDescription': '23.0',
                     'type': None,
                     'when': {
                         'timespans': [{
                             'start': {'earliest': 'None', 'latest': 'None'},
                             'end': {'earliest': 'None', 'latest': 'None'}}]}},
                     {
                         'label': 'Home of Baggins',
                         'relationTo': f'http://local.host/api/0.3/entity/{params["home_id"]}',
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
                         'relationTo': f'http://local.host/api/0.3/entity/{params["location_shire_id"]}',
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
                         'relationTo': f'http://local.host/api/0.3/entity/{params["place_id"]}',
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
                         'relationTo':
                             f'http://local.host/api/0.3/entity/{params["suza_id"]}',
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
                         'relationTo':
                             f'http://local.host/api/0.3/entity/{params["geonames_id"]}',
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
                         'relationTo':
                             f'http://local.host/api/0.3/entity/{params["lotr_id"]}',
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
                         'relationTo':
                             f'http://local.host/api/0.3/entity/{params["picture_id"]}',
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
                     '@id': f'http://local.host/api/0.3/entity/{params["picture_id"]}',
                     'title': 'Picture with a License',
                     'license': 'Open license',
                     'url': 'N/A'}]}]}],
            'pagination': {
                'entities': 4,
                'entitiesPerPage': 20,
                'index': [{'page': 1, 'startId': params["home_id"]}],
                'totalPages': 1}}
