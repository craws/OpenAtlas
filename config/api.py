API_VERSIONS = ['0.3', '0.4']

API_CONTEXT = {
    'LPF': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/'
           'master/linkedplaces-context-v1.1.jsonld',
    'LOUD': 'https://linked.art/ns/v1/linked-art.json'}

CORS_ALLOWANCE = '*'  # Cross-Origin source (CORS)
ALLOWED_IPS = ['127.0.0.1']
API_PROXY = ''

RDF_FORMATS = {
    'pretty-xml': 'application/rdf+xml',
    'n3': 'text/rdf+n3',
    'turtle': 'application/x-turtle',
    'nt': 'text/plain',
    'xml': 'application/xml'}
JSON_FORMATS = {
    'lp': 'application/ld+json',
    'loud': 'application/ld+json',
    'geojson': 'application/json',
    'geojson-v2': 'application/json'}
API_FORMATS = RDF_FORMATS | JSON_FORMATS

LOGICAL_OPERATOR: list[str] = ['and', 'or']
STR_CATEGORIES: list[str] = [
    "entityName", "entityDescription", "entityAliases", "entityCidocClass",
    "entitySystemClass", "typeName", "typeNameWithSubs",
    "beginFrom", "beginTo", "endFrom", "endTo"]
INT_CATEGORIES: list[str] = [
    "entityID", "typeID", "typeIDWithSubs", "relationToID"]
SET_CATEGORIES: list[str] = ["valueTypeID"]
VALID_CATEGORIES: list[str] = [
    *STR_CATEGORIES,
    *INT_CATEGORIES,
    *SET_CATEGORIES]
COMPARE_OPERATORS: list[str] = [
    'equal', 'notEqual', 'greaterThan', 'lesserThan', 'greaterThanEqual',
    'lesserThanEqual', 'like']

# Used to connect to ACDH-CH ARCHE systems
ARCHE = {'id': None, 'url': None}

# Used to connect to password protected Vocabs systems
VOCABS_PASS = ''