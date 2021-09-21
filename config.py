# Don't edit this file. To override settings please use instance/production.py
from pathlib import Path

from openatlas import app

VERSION = '6.6.0'
DEMO_MODE = False  # If activated some options are disabled, login is pre filled
IS_UNIT_TEST = False

LANGUAGES = {'en': 'English', 'de': 'Deutsch'}
DEBUG = False

DATABASE_NAME = 'openatlas'
DATABASE_USER = 'openatlas'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 5432
DATABASE_PASS = 'CHANGE ME'
MAIL_PASSWORD = 'CHANGE ME'
SECRET_KEY = 'CHANGE ME'

# Files with these extensions are can be displayed in the browser
DISPLAY_FILE_EXTENSIONS = \
    ['.bmp', '.gif', '.ico', '.jpeg', '.jpg', '.png', '.svg']

# Paths are implemented operating system independent using pathlib.
# To override them (in instance/production.py) either use them like here
# or use absolute paths like e.g. pathlib.Path('/some/location/somewhere')
TMP_DIR = Path('/tmp')  # used e.g. for processing import and export files
EXPORT_DIR = Path(app.root_path) / 'export'
UPLOAD_DIR = Path(app.root_path) / 'uploads'

# Image processing
PROCESSED_IMAGE_DIR = Path(app.root_path) / 'processed_images'
RESIZED_IMAGES = Path(PROCESSED_IMAGE_DIR) / 'resized'
IMAGE_SIZE = {
    'thumbnail': '200',
    'table': '100'}
NONE_DISPLAY_EXT = ['.tiff', '.tif']
ALLOWED_IMAGE_EXT = DISPLAY_FILE_EXTENSIONS + NONE_DISPLAY_EXT
PROCESSED_EXT = '.jpeg'

# Security
SESSION_COOKIE_SECURE = False  # Should be True in production.py if using HTTPS
REMEMBER_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'

# API
API_SCHEMA = 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld'
CORS_ALLOWANCE = '*'  # Cross-Origin source (CORS)
ALLOWED_IPS = ['127.0.0.1']
RDF_FORMATS = {
    'xml': 'application/rdf+xml',
    'pretty-xml': 'application/rdf+xml',
    'n3': 'text/rdf+n3',
    'turtle': 'application/x-turtle',
    'nt': 'text/plain'}
JSON_FORMATS = {
    'lp': 'application/json',
    'geojson': 'application/json'}
API_FORMATS = {**RDF_FORMATS, **JSON_FORMATS}

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
    'button': {
        'primary': 'btn btn-outline-primary btn-sm',
        'secondary': 'btn btn-secondary btn-xsm'}}

# Property types work differently than regular types, e.g. no move functionality
PROPERTY_TYPES = ['Actor actor relation', 'Actor function', 'Involvement']
