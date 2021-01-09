# Don't edit this file. To override settings please use instance/production.py
from pathlib import Path

from openatlas import app

VERSION = '5.7.0'
DEMO_MODE = False  # If in demo mode some options are disabled and the login form is pre filled
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

# Files with these extensions are available as profile image and will be displayed in the browser
DISPLAY_FILE_EXTENSIONS = ['.bmp', '.gif', '.ico', '.jpeg', '.jpg', '.png', '.svg']

# Paths are implemented operating system independent using pathlib.
# If you want to override them (in instance/production.py) either use them like here
# or use absolute paths like e.g. pathlib.Path('/some/location/somewhere')
TMP_DIR = Path('/tmp')  # e.g. for processing import/export files
EXPORT_DIR = Path(app.root_path) / 'export'
UPLOAD_DIR = Path(app.root_path) / 'uploads'

# Security
SESSION_COOKIE_SECURE = False  # Should be set to True in production.py if using HTTPS only
REMEMBER_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Key for Thunderforest map layer
THUNDERFOREST_KEY = '7878b4fb224f4902ab42fc846e92b96a'

# External References
EXTERNAL_REFERENCES_FORMS = ['Event', 'Feature', 'Find', 'Group', 'Human_Remains', 'Legal Body',
                             'Person', 'Place', 'Stratigraphic Unit']

# Will moved to db and be configurable in admin when more options (GeoNames URL already is in db)
EXTERNAL_REFERENCES = {'geonames': {'name': 'GeoNames', 'url': '', 'placeholder': '1234567'},
                       'wikidata': {'name': 'Wikidata',
                                    'url': 'https://www.wikidata.org/entity/',
                                    'placeholder': 'Q123'}}
REFERENCE_PRECISION = [('', ''), ('close match', 'close match'), ('exact match', 'exact match')]

# Modules
MODULES = ['geonames', 'wikidata', 'map_overlay', 'notes', 'sub_units']

# API
API_SCHEMA = 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.jsonld'
CORS_ALLOWANCE = '*'  # Cross-Origin source (CORS),  # Todo: move to backend config
ALLOWED_IPS = ['127.0.0.1']  # Todo: move to backend config

# Table options
TABLE_ROWS = {10: '10', 25: '25', 50: '50', 100: '100'}

# Minimum required characters for table filters
MIN_CHARS_JSTREE_SEARCH = 1

# Log levels
LOG_LEVELS = {0: 'emergency',
              1: 'alert',
              2: 'critical',
              3: 'error',
              4: 'warn',
              5: 'notice',
              6: 'info',
              7: 'debug'}

# Types
PROPERTY_TYPES = ['Actor Actor Relation', 'Actor Function', 'Involvement']
BASE_TYPES = ['Actor', 'Bibliography', 'Edition', 'Event', 'Feature', 'Find', 'Human Remains',
              'Information Carrier', 'Place', 'Source', 'Stratigraphic Unit']

# Mappings between model and user interface
CODE_CLASS = {
    'E21': 'actor',
    'E40': 'actor',
    'E74': 'actor',
    'E7': 'event',
    'E8': 'event',
    'E9': 'event',
    'E84': 'object',
    'E18': 'place',
    'E20': 'place',
    'E22': 'place',
    'E31': 'reference',
    'E33': 'source'}

CLASS_CODES = {
    'actor': ['E21', 'E74', 'E40'],
    'event': ['E7', 'E8', 'E9'],
    'group': ['E40', 'E74'],
    'information_carrier': ['E84'],
    'object': ['E84'],
    'person': ['E21'],
    'place': ['E18', 'E20', 'E22'],
    'reference': ['E31'],
    'source': ['E33']}

CSS = {'button': {'primary': 'btn btn-outline-primary btn-sm',
                  'secondary': 'btn btn-secondary btn-xsm'}}
