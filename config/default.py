# Don't edit this file. To override settings please use instance/production.py
from pathlib import Path

from config.database_versions import DATABASE_VERSIONS

VERSION = '7.10.0'
DATABASE_VERSION = DATABASE_VERSIONS[0]
DEMO_MODE = False  # If activated some options are disabled, login is prefilled
IS_UNIT_TEST = False

LANGUAGES = {'ca': 'Català', 'de': 'Deutsch', 'en': 'English', 'es': 'Español'}
DEBUG = False

DATABASE_NAME = 'openatlas'
DATABASE_USER = 'openatlas'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 5432
DATABASE_PASS = 'CHANGE ME'
MAIL_PASSWORD = 'CHANGE ME'
SECRET_KEY = 'CHANGE ME'  # Used for cookies

# Files with these extensions are can be displayed in the browser
DISPLAY_FILE_EXTENSIONS = \
    ['.bmp', '.gif', '.ico', '.jpeg', '.jpg', '.png', '.svg']

# Paths are implemented operating system independent using pathlib.
# To override them (in instance/production.py) either use them like here
# or use absolute paths like e.g. pathlib.Path('/some/location/somewhere')
FILES_PATH = Path(__file__).parent.parent / 'files'
EXPORT_DIR = Path(FILES_PATH) / 'export'
UPLOAD_DIR = Path(FILES_PATH) / 'uploads'
TMP_DIR = Path('/tmp')  # used e.g. for processing imports and export files

# Image processing
PROCESSED_IMAGE_DIR = Path(FILES_PATH) / 'processed_images'
RESIZED_IMAGES = Path(PROCESSED_IMAGE_DIR) / 'resized'
IMAGE_SIZE = {
    'thumbnail': '200',
    'table': '100'}
NONE_DISPLAY_EXT = ['.tiff', '.tif']
ALLOWED_IMAGE_EXT = DISPLAY_FILE_EXTENSIONS + NONE_DISPLAY_EXT
PROCESSED_EXT = '.jpeg'

# For system checks
WRITABLE_DIRS = [
    UPLOAD_DIR,
    EXPORT_DIR,
    RESIZED_IMAGES]

# Security
SESSION_COOKIE_SECURE = False  # Should be True in production.py if using HTTPS
REMEMBER_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'

# API
API_SCHEMA = \
    'https://raw.githubusercontent.com/LinkedPasts/linked-places' \
    '/master/linkedplaces-context-v1.1.jsonld'
CORS_ALLOWANCE = '*'  # Cross-Origin source (CORS)
ALLOWED_IPS = ['127.0.0.1']
RDF_FORMATS = {
    'pretty-xml': 'application/rdf+xml',
    'n3': 'text/rdf+n3',
    'turtle': 'application/x-turtle',
    'nt': 'text/plain',
    'xml': 'application/xml'}
JSON_FORMATS = {
    'lp': 'application/json',
    'geojson': 'application/json',
    'geojson-v2': 'application/json'}
API_FORMATS = RDF_FORMATS | JSON_FORMATS
# Used to connect to ACDH-CH ARCHE systems
ARCHE = {
    'id': None,
    'collection_ids': None,
    'base_url': None,
    'thumbnail_url': 'https://arche-thumbnails.acdh.oeaw.ac.at/'}

# Table options
TABLE_ROWS = {10: '10', 25: '25', 50: '50', 100: '100'}

# Minimum required characters for table filters
MIN_CHARS_JSTREE_SEARCH = 1

LOG_LEVELS = {
    0: 'emergency',
    1: 'alert',
    2: 'critical',
    3: 'error',
    4: 'warn',
    5: 'notice',
    6: 'info',
    7: 'debug'}

CSS = {
    'string_field': 'form-control form-control-sm',
    'button': {
        'primary': 'btn btn-outline-primary btn-sm',
        'secondary': 'btn btn-outline-secondary btn-sm'}}

# Property types work differently, e.g. no move functionality
PROPERTY_TYPES = [
    'Actor relation',
    'Actor function',
    'External reference match',
    'Involvement']
