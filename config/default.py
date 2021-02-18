# Don't edit this file. To override settings please use instance/production.py
from pathlib import Path

from openatlas import app

VERSION = '5.8.0'
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

# External References
REFERENCE_PRECISION = [('', ''), ('close match', 'close match'), ('exact match', 'exact match')]
EXTERNAL_REFERENCES_FORMS = ['Artifact', 'Event', 'Feature', 'Find', 'Group', 'Human Remains',
                             'Legal Body', 'Person', 'Place', 'Stratigraphic Unit', 'Type']

# Modules
MODULES = ['map_overlay', 'notes', 'sub_units']

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

CSS = {'button': {'primary': 'btn btn-outline-primary btn-sm',
                  'secondary': 'btn btn-secondary btn-xsm'}}
