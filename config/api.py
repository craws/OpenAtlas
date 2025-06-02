from pathlib import Path

API_VERSIONS = ['0.4']

OPENAPI_FILE = (Path(
    __file__).parent.parent / 'openatlas' / 'api' / 'openapi.json')
OPENAPI_INSTANCE_FILE = Path(__file__).parent.parent / 'files' / 'openapi.json'

API_CONTEXT = {
    'LPF':
        'https://raw.githubusercontent.com/LinkedPasts/linked-places/'
        'master/linkedplaces-context-v1.1.jsonld',
    'LOUD': 'https://linked.art/ns/v1/linked-art.json'}

CORS_ALLOWANCE = '*'  # Cross-Origin source (CORS)
ALLOWED_IPS = ['127.0.0.1']

RDF_FORMATS = {
    'pretty-xml': 'application/rdf+xml',
    'n3': 'text/rdf+n3',
    'turtle': 'application/x-turtle',
    'nt': 'text/plain',
    'xml': 'application/xml'}
JSON_FORMATS = {
    'lp': 'application/ld+json',
    'lpx': 'application/ld+json',
    'loud': 'application/ld+json',
    'geojson': 'application/json',
    'geojson-v2': 'application/json',
    'presentation': 'application/json'}
API_FORMATS = RDF_FORMATS | JSON_FORMATS

LOGICAL_OPERATOR: list[str] = ['and', 'or']
STR_VALUES: list[str] = [
    'entityName', 'entityDescription', 'entityAliases', 'entityCidocClass',
    'entitySystemClass', 'typeName', 'typeNameWithSubs',
    'beginFrom', 'beginTo', 'endFrom', 'endTo']
INT_VALUES: list[str] = [
    'entityID',
    'typeID',
    'typeIDWithSubs',
    'relationToID']
FLOAT_VALUES: list[str] = ['valueTypeID']
VALID_VALUES: list[str] = [
    *STR_VALUES,
    *INT_VALUES,
    *FLOAT_VALUES]
COMPARE_OPERATORS: list[str] = [
    'equal', 'notEqual', 'greaterThan', 'lesserThan', 'greaterThanEqual',
    'lesserThanEqual', 'like']

# Used to connect to ACDH-CH ARCHE systems
ARCHE = {'id': None, 'url': None}

# Used to connect to password protected Vocabs systems
VOCABS_PASS = ''

API_PRESENTATION_EXCLUDE_RELATION = [
    'bone',
    'file',
    'type',
    'type_tools'
    'appellation',
    'object_location',
    'reference_system',
    'administrative_unit',
    'bibliography',
    'edition',
    'external_reference']


LOCATION_PROPERTIES = {'P53', 'P74', 'OA8', 'OA9', 'P7', 'P26', 'P27'}
