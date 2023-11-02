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
    'entityName', 'entityDescription', 'entityAliases', 'entityCidocClass',
    'entitySystemClass', 'typeName', 'typeNameWithSubs',
    'beginFrom', 'beginTo', 'endFrom', 'endTo']
INT_CATEGORIES: list[str] = [
    'entityID', 'typeID', 'typeIDWithSubs', 'relationToID']
SET_CATEGORIES: list[str] = ['valueTypeID']
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

IMAGE_FORMATS = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'jpe': 'image/jpeg',
    'jfif': 'image/jpeg',
    'pjpeg': 'image/pjpeg',
    'pjp': 'image/pjpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'bmp': 'image/bmp',
    'ico': 'image/x-icon',
    'tiff': 'image/tiff',
    'tif': 'image/tiff',
    'webp': 'image/webp',
    'svg': 'image/svg+xml',
    'svgz': 'image/svg+xml',
    'apng': 'image/apng',
    'wbmp': 'image/vnd.wap.wbmp',
    'xbm': 'image/x-xbitmap',
    'avif': 'image/avif',
    'heic': 'image/heic',
    'heif': 'image/heif',
    'jp2': 'image/jp2',
    'jpx': 'image/jpx',
    'jpm': 'image/jpm',
    'jxr': 'image/jxr',
    'wdp': 'image/vnd.ms-photo',
    'hdp': 'image/vnd.ms-photo',
    'bpg': 'image/bpg',
    'dib': 'image/bmp',
    'jpeg2000': 'image/jpeg2000',
    'exr': 'image/aces',
    'hdr': 'image/vnd.radiance',
}
