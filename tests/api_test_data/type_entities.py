import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_params import test_ids

test_type_entities = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["shire_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'place',
        'properties': {'title': 'Shire'},
        'description': [{
            'value': 'The Shire was the homeland of the hobbits.'}],
        'when': {
            'timespans': [{
                'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]},
        'types': [{
            'identifier':
                f'http://local.host/api/0.2/entity/{test_ids["place_id"]}',
            'label': 'Place', 'description': None, 'hierarchy': '',
            'value': None, 'unit': None}, {
            'identifier':
                f'http://local.host/api/0.2/entity/{test_ids["height_id"]}',
            'label': 'Height', 'description': None,
            'hierarchy': 'Dimensions', 'value': 23.0,
            'unit': 'centimeter'}],
        'relations': [{
            'label': 'Height',
            'relationTo':
                f'http://local.host/api/0.2/entity/{test_ids["height_id"]}',
            'relationType': 'crm:P2 has type',
            'relationSystemClass': 'type',
            'relationDescription': '23.0',
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Home of Baggins',
            'relationTo':
                f'http://local.host/api/0.2/entity/{test_ids["home_id"]}',
            'relationType': 'crm:P46 is composed of',
            'relationSystemClass': 'feature',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Location of Shire',
            'relationTo':
                f'http://local.host/api/0.2/entity/{test_ids["location_shire_id"]}',
            'relationType': 'crm:P53 has former or current location',
            'relationSystemClass': 'object_location',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Place',
            'relationTo':
                f'http://local.host/api/0.2/entity/{test_ids["place_id"]}',
            'relationType': 'crm:P2 has type',
            'relationSystemClass': 'type',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Sûza',
            'relationTo':
                f'http://local.host/api/0.2/entity/{test_ids["suza_id"]}',
            'relationType': 'crm:P1 is identified by',
            'relationSystemClass': 'appellation',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'GeoNames',
            'relationTo':
                f'http://local.host/api/0.2/entity/{test_ids["geonames_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'reference_system',
            'relationDescription': '2761369',
            'type': 'closeMatch',
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'https://lotr.fandom.com/',
            'relationTo':
                f'http://local.host/api/0.2/entity/{test_ids["lotr_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'external_reference',
            'relationDescription': 'Fandom Wiki of lord of the rings',
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Picture with a License',
            'relationTo':
                f'http://local.host/api/0.2/entity/{test_ids["picture_id"]}',
            'relationType': 'crm:P67i is referred to by',
            'relationSystemClass': 'file',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
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
            '@id': f'http://local.host/api/0.2/entity/{test_ids["picture_id"]}',
            'title': 'Picture with a License', 'license': 'Open license',
            'url': 'N/A'}]}]}],
    'pagination': {
        'entities': 1,
        'entitiesPerPage': 20,
        'index': [{'page': 1, 'startId': test_ids["shire_id"]}],
        'totalPages': 1}}
test_type_entities_all_special = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["austria_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E53 Place',
        'systemClass': 'administrative_unit',
        'properties': {'title': 'Austria'},
        'description': None,
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Administrative unit',
            'relationTo':
                f'http://local.host/api/0.2/entity/{test_ids["administrative_id"]}',
            'relationType': 'crm:P89 falls within',
            'relationSystemClass': 'administrative_unit',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Niederösterreich',
            'relationTo':
                f'http://local.host/api/0.2/entity/{test_ids["nieder_id"]}',
            'relationType': 'crm:P89i contains',
            'relationSystemClass': 'administrative_unit',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}, {
            'label': 'Wien',
            'relationTo':
                f'http://local.host/api/0.2/entity/{test_ids["wien_id"]}',
            'relationType': 'crm:P89i contains',
            'relationSystemClass': 'administrative_unit',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': None,
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["czech_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E53 Place',
        'systemClass': 'administrative_unit',
        'properties': {'title': 'Czech Republic'},
        'description': None,
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Administrative unit',
            'relationTo':
                f'http://local.host/api/0.2/entity/{test_ids["administrative_id"]}',
            'relationType': 'crm:P89 falls within',
            'relationSystemClass': 'administrative_unit',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': None,
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["germany_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E53 Place',
        'systemClass': 'administrative_unit',
        'properties': {'title': 'Germany'},
        'description': None,
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Administrative unit',
            'relationTo':
                f'http://local.host/api/0.2/entity/{test_ids["administrative_id"]}',
            'relationType': 'crm:P89 falls within',
            'relationSystemClass': 'administrative_unit',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': None,
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["italy_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E53 Place',
        'systemClass': 'administrative_unit',
        'properties': {
            'title': 'Italy'},
        'description': None,
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Administrative unit',
            'relationTo':
                f'http://local.host/api/0.2/entity/{test_ids["administrative_id"]}',
            'relationType': 'crm:P89 falls within',
            'relationSystemClass': 'administrative_unit',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': None,
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["slovakia_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E53 Place',
        'systemClass': 'administrative_unit',
        'properties': {'title': 'Slovakia'},
        'description': None,
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Administrative unit',
            'relationTo':
                f'http://local.host/api/0.2/entity/{test_ids["administrative_id"]}',
            'relationType': 'crm:P89 falls within',
            'relationSystemClass': 'administrative_unit',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': None,
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["slovenia_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E53 Place',
        'systemClass': 'administrative_unit',
        'properties': {'title': 'Slovenia'},
        'description': None,
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Administrative unit',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["administrative_id"]}',
            'relationType': 'crm:P89 falls within',
            'relationSystemClass': 'administrative_unit',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': None,
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["nieder_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E53 Place',
        'systemClass': 'administrative_unit',
        'properties': {'title': 'Niederösterreich'},
        'description': None,
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Austria',
            'relationTo':
                f'http://local.host/api/0.2/entity/{test_ids["austria_id"]}',
            'relationType': 'crm:P89 falls within',
            'relationSystemClass': 'administrative_unit',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': None,
        'depictions': None}]}, {
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': f'http://local.host/entity/{test_ids["wien_id"]}',
        'type': 'Feature',
        'crmClass': 'crm:E53 Place',
        'systemClass': 'administrative_unit',
        'properties': {'title': 'Wien'},
        'description': None,
        'when': {
            'timespans': [{
                'start': {'earliest': 'None', 'latest': 'None'},
                'end': {'earliest': 'None', 'latest': 'None'}}]},
        'types': None,
        'relations': [{
            'label': 'Austria',
            'relationTo': f'http://local.host/api/0.2/entity/{test_ids["austria_id"]}',
            'relationType': 'crm:P89 falls within',
            'relationSystemClass': 'administrative_unit',
            'relationDescription': None,
            'type': None,
            'when': {
                'timespans': [{
                    'start': {'earliest': 'None', 'latest': 'None'},
                    'end': {'earliest': 'None', 'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': None,
        'depictions': None}]}],
    'pagination': {
        'entities': 8,
        'entitiesPerPage': 20,
        'index': [{
            'page': 1,
            'startId': test_ids["austria_id"]}],
        'totalPages': 1}}
