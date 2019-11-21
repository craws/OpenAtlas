# Don't edit this file. To override settings please use instance/production.py
import os

from flask_babel import lazy_gettext as _

VERSION = '4.0.0'
DEMO_MODE = False  # If in demo mode some options are disabled and the login form is pre filled

LANGUAGES = {'en': 'English', 'de': 'Deutsch'}
DEBUG = False

DATABASE_NAME = 'openatlas'
DATABASE_USER = 'openatlas'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 5432
DATABASE_PASS = 'CHANGE ME'
MAIL_PASSWORD = 'CHANGE ME'
SECRET_KEY = 'CHANGE ME'

IMPORT_FOLDER_PATH = '/tmp'  # Needed for processing of import files, any temp folder will do
IMPORT_FILE_EXTENSIONS = ['csv', 'xls', 'xlsx']
EXPORT_FOLDER_PATH = os.path.dirname(__file__) + '/../openatlas/export'
UPLOAD_FOLDER_PATH = os.path.dirname(__file__) + '/../openatlas/uploads'
DISPLAY_FILE_EXTENSIONS = ['bmp', 'gif', 'ico', 'jpeg', 'jpg', 'png', 'svg']

# Security
SESSION_COOKIE_SECURE = False  # Should be set to True in production.py if using HTTPS only
REMEMBER_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Map
MAX_ZOOM = 18  # Can be overridden by users in their profile
GEONAMES_USERNAME = 'openatlas'
GEONAMES_VIEW_URL = 'http://www.geonames.org/'
THUNDERFOREST_KEY = '7878b4fb224f4902ab42fc846e92b96a'

# Table options
DEFAULT_TABLE_ROWS = {10: '10', 25: '25', 50: '50', 100: '100'}

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

# Feedback
FEEDBACK_SUBJECTS = {_('suggestion').title(): _('suggestion').title(),
                     _('question').title(): _('question').title(),
                     _('problem').title(): _('problem').title()}

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
    'place': ['E18', 'E22'],
    'reference': ['E31'],
    'source': ['E33']}

PROPERTY_TYPES = ['Actor Actor Relation', 'Actor Function', 'Involvement']

BASE_TYPES = ['Place', 'Information Carrier', 'Bibliography', 'Source', 'Edition', 'Event', 'Actor',
              'Stratigraphic Unit', 'Feature', 'Find']
