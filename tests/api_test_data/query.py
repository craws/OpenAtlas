import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_params import test_ids


# todo: further


test_query = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [
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
             'relationDescription': None,
             'type': None,
             'when': {
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
         'geometry': {'type': 'Point', 'coordinates': [9, 17], 'title': '',
                      'description': ''},
         'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [
        {'@id': 'http://local.host/entity/116',
         'type': 'Feature',
         'crmClass': 'crm:E22 Man-Made Object',
         'systemClass': 'artifact',
         'properties': {'title': 'The One Ring'},
         'description': None,
         'when': {
             'timespans': [{'start': {'earliest': 'None', 'latest': 'None'},
                            'end': {'earliest': 'None', 'latest': 'None'}}]},
         'types': None, 'relations': [{
            'label': 'Frodo',
            'relationTo': 'http://local.host/api/0.2/entity/113',
            'relationType': 'crm:P52 has current owner',
            'relationSystemClass': 'person',
            'relationDescription': None,
            'type': None, 'when': {'timespans': [
                {'start': {'earliest': 'None', 'latest': 'None'},
                 'end': {'earliest': 'None', 'latest': 'None'}}]}},
            {'label': 'Location of The One Ring',
             'relationTo': 'http://local.host/api/0.2/entity/117',
             'relationType': 'crm:P53 has former or current location',
             'relationSystemClass': 'object_location',
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
         'depictions': [{
             '@id': 'http://local.host/api/0.2/entity/115',
             'title': 'File without license', 'license': None,
             'url': 'N/A'}]}]}, {
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
         'depictions': None}]}, {
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
         'relations': [{
             'label': 'Kitchen',
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
         'geometry': {'type': 'GeometryCollection', 'geometries': []},
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
         'relations': [{
             'label': 'Location of Kitchen',
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
    'type': 'FeatureCollection', 'features': [
        {'@id': 'http://local.host/entity/120',
         'type': 'Feature',
         'crmClass': 'crm:E18 Physical Thing',
         'systemClass': 'place',
         'properties': {'title': 'Mordor'},
         'description': [{'value': 'The heart of evil.'}],
         'when': {
             'timespans': [{'start': {'earliest': 'None', 'latest': 'None'},
                            'end': {'earliest': 'None', 'latest': 'None'}}]},
         'types': [{
             'identifier': 'http://local.host/api/0.2/entity/72',
             'label': 'Boundary Mark', 'description': None,
             'hierarchy': 'Place', 'value': None, 'unit': None}],
         'relations': [{
             'label': 'Boundary Mark',
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
    'type': 'FeatureCollection',
    'features': [
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
         'types': [{
             'identifier': 'http://local.host/api/0.2/entity/65',
             'label': 'Place', 'description': None, 'hierarchy': '',
             'value': None, 'unit': None},
             {'identifier': 'http://local.host/api/0.2/entity/102',
              'label': 'Height', 'description': None,
              'hierarchy': 'Dimensions', 'value': 23.0,
              'unit': 'centimeter'}],
         'relations': [{
             'label': 'Height',
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
    'pagination': {
        'entities': 8,
        'entitiesPerPage': 20,
        'index': [{'page': 1, 'startId': 105}],
        'totalPages': 1}}
test_query_geojson = {'results': [{
    'type': 'FeatureCollection',
    'features': [{
        'type': 'Feature',
        'geometry': {'type': 'Point',
                     'coordinates': [9,
                                     17],
                     'title': '',
                     'description': ''},
        'properties': {'@id': 105,
                       'systemClass': 'object_location',
                       'name': 'Location of Shire',
                       'description': None,
                       'begin_earliest': None,
                       'begin_latest': None,
                       'begin_comment': None,
                       'end_earliest': None,
                       'end_latest': None,
                       'end_comment': None,
                       'types': None}},
        {'type': 'Feature',
         'geometry': None,
         'properties': {'@id': 116,
                        'systemClass': 'artifact',
                        'name': 'The One Ring',
                        'description': None,
                        'begin_earliest': None,
                        'begin_latest': None,
                        'begin_comment': None,
                        'end_earliest': None,
                        'end_latest': None,
                        'end_comment': None,
                        'types': None}},
        {'type': 'Feature',
         'geometry': None,
         'properties': {'@id': 113,
                        'systemClass': 'person',
                        'name': 'Frodo',
                        'description': 'That is Frodo',
                        'begin_earliest': None,
                        'begin_latest': None,
                        'begin_comment': None,
                        'end_earliest': None,
                        'end_latest': None,
                        'end_comment': None,
                        'types': None}},
        {'type': 'Feature',
         'geometry': None,
         'properties': {'@id': test_ids["sam_id"],
                        'systemClass': 'person',
                        'name': 'Sam',
                        'description': 'That is Sam',
                        'begin_earliest': None,
                        'begin_latest': None,
                        'begin_comment': None,
                        'end_earliest': None,
                        'end_latest': None,
                        'end_comment': None,
                        'types': None}},
        {'type': 'Feature',
         'geometry': None,
         'properties': {'@id': 108,
                        'systemClass': 'feature',
                        'name': 'Home of Baggins',
                        'description': None,
                        'begin_earliest': None,
                        'begin_latest': None,
                        'begin_comment': None,
                        'end_earliest': None,
                        'end_latest': None,
                        'end_comment': None,
                        'types': None}},
        {'type': 'Feature',
         'geometry': None,
         'properties': {'@id': 110,
                        'systemClass': 'stratigraphic_unit',
                        'name': 'Kitchen',
                        'description': None,
                        'begin_earliest': None,
                        'begin_latest': None,
                        'begin_comment': None,
                        'end_earliest': None,
                        'end_latest': None,
                        'end_comment': None,
                        'types': None}},
        {'type': 'Feature',
         'geometry': None,
         'properties': {'@id': 120,
                        'systemClass': 'place',
                        'name': 'Mordor',
                        'description': 'The heart of evil.',
                        'begin_earliest': None,
                        'begin_latest': None,
                        'begin_comment': None,
                        'end_earliest': None,
                        'end_latest': None,
                        'end_comment': None,
                        'types': [
                            'Boundary Mark']}},
        {'type': 'Feature',
         'geometry': {'type': 'Point',
                      'coordinates': [9,
                                      17],
                      'title': '',
                      'description': ''},
         'properties': {'@id': 104,
                        'systemClass': 'place',
                        'name': 'Shire',
                        'description': 'The Shire was the homeland of the hobbits.',
                        'begin_earliest': '2018-01-31',
                        'begin_latest': '2018-03-01',
                        'begin_comment': 'Begin of the shire',
                        'end_earliest': '2019-01-31',
                        'end_latest': '2019-03-01',
                        'end_comment': 'Descent of Shire',
                        'types': ['Place',
                                  'Height']}}]}],
    'pagination': {'entities': 8,
                   'entitiesPerPage': 20,
                   'index': [{'page': 1, 'startId': 105}],
                   'totalPages': 1}}
test_query_filter = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [
        {'@id': 'http://local.host/entity/105',
         'type': 'Feature',
         'crmClass': 'crm:E53 Place',
         'systemClass': 'object_location',
         'properties': {'title': 'Location of Shire'},
         'description': None,
         'when': {'timespans': [
             {'start': {'earliest': 'None', 'latest': 'None'},
              'end': {'earliest': 'None', 'latest': 'None'}}]}, 'types': None,
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
         'links': [{
             'type': 'closeMatch',
             'identifier': 'https://www.geonames.org/2761369',
             'referenceSystem': 'GeoNames'}],
         'geometry': {
             'type': 'Point',
             'coordinates': [9, 17],
             'title': '',
             'description': ''},
         'depictions': [
             {'@id': 'http://local.host/api/0.2/entity/112',
              'title': 'Picture with a License', 'license': 'Open license',
              'url': 'N/A'}]}]}],
    'pagination': {'entities': 2, 'entitiesPerPage': 20,
                   'index': [{'page': 1, 'startId': 105}], 'totalPages': 1}}
test_query_filter_date = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [
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
         'relations': [
             {'label': 'Shire',
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
        {'@id': 'http://local.host/entity/116',
         'type': 'Feature',
         'crmClass': 'crm:E22 Man-Made Object',
         'systemClass': 'artifact',
         'properties': {'title': 'The One Ring'},
         'description': None, 'when': {
            'timespans': [{'start': {'earliest': 'None', 'latest': 'None'},
                           'end': {'earliest': 'None', 'latest': 'None'}}]},
         'types': None,
         'relations': [
             {'label': 'Frodo',
              'relationTo': 'http://local.host/api/0.2/entity/113',
              'relationType': 'crm:P52 has current owner',
              'relationSystemClass': 'person',
              'relationDescription': None,
              'type': None, 'when': {'timespans': [
                 {'start': {'earliest': 'None', 'latest': 'None'},
                  'end': {'earliest': 'None', 'latest': 'None'}}]}},
             {'label': 'Location of The One Ring',
              'relationTo': 'http://local.host/api/0.2/entity/117',
              'relationType': 'crm:P53 has former or current location',
              'relationSystemClass': 'object_location',
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
         'links': [{
             'type': 'closeMatch',
             'identifier': 'https://www.geonames.org/2761369',
             'referenceSystem': 'GeoNames'}],
         'geometry': {
             'type': 'Point',
             'coordinates': [9, 17],
             'title': '',
             'description': ''},
         'depictions': [
             {'@id': 'http://local.host/api/0.2/entity/112',
              'title': 'Picture with a License', 'license': 'Open license',
              'url': 'N/A'}]}]}, {
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
         'relations': [{'label': 'Frodo',
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
         'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [
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
         'relations': [
             {'label': 'Sam',
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
    'type': 'FeatureCollection',
    'features': [
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
         'links': [
             {'type': 'closeMatch',
              'identifier': 'https://www.geonames.org/2761369',
              'referenceSystem': 'GeoNames'}],
         'geometry': {
             'type': 'Point',
             'coordinates': [9, 17],
             'title': '',
             'description': ''},
         'depictions': [
             {'@id': 'http://local.host/api/0.2/entity/112',
              'title': 'Picture with a License', 'license': 'Open license',
              'url': 'N/A'}]}]}, {
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
         'relations': [{
             'label': 'Location of Kitchen',
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
         'geometry': {'type': 'GeometryCollection', 'geometries': []},
         'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [
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
         'types': [{
             'identifier': 'http://local.host/api/0.2/entity/65',
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
         'links': [
             {'type': 'closeMatch',
              'identifier': 'https://www.geonames.org/2761369',
              'referenceSystem': 'GeoNames'}],
         'geometry':
             {'type': 'Point',
              'coordinates': [9, 17],
              'title': '',
              'description': ''},
         'depictions': [
             {'@id': 'http://local.host/api/0.2/entity/112',
              'title': 'Picture with a License', 'license': 'Open license',
              'url': 'N/A'}]}]}],
    'pagination': {
        'entities': 10,
        'entitiesPerPage': 20,
        'index': [{'page': 1, 'startId': 105}],
        'totalPages': 1}}
test_query_first = {'results': [{
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
         'relations': [
             {'label': 'Frodo',
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
        'entities': 8,
        'entitiesPerPage': 1,
        'index': [
            {'page': 1, 'startId': 105},
            {'page': 2, 'startId': 116},
            {'page': 3, 'startId': 113},
            {'page': 4, 'startId': test_ids["sam_id"]},
            {'page': 5, 'startId': 108},
            {'page': 6, 'startId': 110},
            {'page': 7, 'startId': 120},
            {'page': 8, 'startId': 104}],
        'totalPages': 8}}
test_query_last = {'results': [{
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
         'geometry': {'type': 'GeometryCollection', 'geometries': []},
         'depictions': None}]}],
    'pagination': {
        'entities': 8,
        'entitiesPerPage': 1,
        'index': [
            {'page': 1, 'startId': 105},
            {'page': 2, 'startId': 116},
            {'page': 3, 'startId': 113},
            {'page': 4, 'startId': test_ids["sam_id"]},
            {'page': 5, 'startId': 108},
            {'page': 6, 'startId': 110},
            {'page': 7, 'startId': 120},
            {'page': 8, 'startId': 104}],
        'totalPages': 8}}
test_query_type = {'results': [{
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
         'depictions': None}]}],
    'pagination': {
        'entities': 1,
        'entitiesPerPage': 20,
        'index': [{'page': 1, 'startId': 120}],
        'totalPages': 1}}
