# Don't edit this file. To override settings please use instance/production.py

from pathlib import Path

# ---------------------------------------------------------------------
# Network and Security Configuration
# ---------------------------------------------------------------------

# CORS policy: allow all domains to access the API
CORS_ALLOWANCE = '*'

# List of allowed IPs to access API services
ALLOWED_IPS = ['127.0.0.1']

# ---------------------------------------------------------------------
# External System Integration
# ---------------------------------------------------------------------

# Configuration for connecting to ACDH ARCHE systems (if needed)
ARCHE = {'id': None, 'url': None}

# Password used to access protected Vocabs services
VOCABS_PASS = ''

# #####################################################################
# Do NOT overwrite the settings below, unless you know what you do!   #
# #####################################################################

# ---------------------------------------------------------------------
# API Versioning and OpenAPI Documentation
# ---------------------------------------------------------------------

API_VERSIONS = ['0.4']

# Path to the main OpenAPI definition file
OPENAPI_FILE = \
    Path(__file__).parent.parent / 'openatlas' / 'api' / 'openapi.json'

# Path to the instance-specific OpenAPI definition file
OPENAPI_INSTANCE_FILE = Path(__file__).parent.parent / 'files' / 'openapi.json'

# JSON-LD contexts used for semantic enrichment in API responses
API_CONTEXT = {
    'LPF':
        'https://raw.githubusercontent.com/LinkedPasts/linked-places/'
        'master/linkedplaces-context-v1.1.jsonld',
    'LOUD': 'https://linked.art/ns/v1/linked-art.json'}

# ---------------------------------------------------------------------
# API Output Formats
# ---------------------------------------------------------------------

RDF_FORMATS = {
    'pretty-xml': 'application/rdf+xml',
    'n3': 'text/rdf+n3',
    'turtle': 'text/plain',
    'nt': 'text/plain',
    'xml': 'application/xml'}

JSON_FORMATS = {
    'lp': 'application/ld+json',
    'lpx': 'application/ld+json',
    'loud': 'application/ld+json',
    'geojson': 'application/json',
    'geojson-v2': 'application/json',
    'table_row': 'application/json',
    'presentation': 'application/json'}

OTHER = {
    'gpkg': 'application/geopackage+sqlite3'}

API_FORMATS = RDF_FORMATS | JSON_FORMATS | OTHER

# ---------------------------------------------------------------------
# Search and Filter Configuration
# ---------------------------------------------------------------------

LOGICAL_OPERATOR: list[str] = ['and', 'or']

STR_VALUES: list[str] = [
    'entityName', 'entityDescription', 'entityAliases', 'entityCidocClass',
    'entitySystemClass', 'typeName', 'typeNameWithSubs',
    'beginFrom', 'beginTo', 'endFrom', 'endTo']

INT_VALUES: list[str] = [
    'entityID', 'typeID', 'typeIDWithSubs', 'relationToID']

FLOAT_VALUES: list[str] = ['valueTypeID']

VALID_VALUES: list[str] = [
    *STR_VALUES,
    *INT_VALUES,
    *FLOAT_VALUES]

COMPARE_OPERATORS: list[str] = [
    'equal', 'notEqual', 'greaterThan', 'lesserThan', 'greaterThanEqual',
    'lesserThanEqual', 'like']

# ---------------------------------------------------------------------
# API Presentation View Settings
# ---------------------------------------------------------------------

API_PRESENTATION_EXCLUDE_RELATION = [
    'bone',
    'file',
    'type',
    'type_tools',
    'appellation',
    'object_location',
    'reference_system',
    'administrative_unit',
    'bibliography',
    'edition',
    'external_reference']

# ---------------------------------------------------------------------
# Network Visualization Configuration
# ---------------------------------------------------------------------

# Properties used to identify spatial or location-related relationships
LOCATION_PROPERTIES = {'P53', 'P74', 'OA8', 'OA9', 'P7', 'P26', 'P27'}
