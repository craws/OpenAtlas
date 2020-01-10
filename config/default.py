# Don't edit this file. To override settings please use instance/production.py
import pathlib

from flask_babel import lazy_gettext as _

from openatlas import app

VERSION = '4.1.0'
DEMO_MODE = False  # If in demo mode some options are disabled and the login form is pre filled

LANGUAGES = {'en': 'English', 'de': 'Deutsch'}
DEBUG = True


DATABASE_NAME = 'openatlas'
DATABASE_USER = 'openatlas'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 5432
DATABASE_PASS = 'CHANGE ME'
MAIL_PASSWORD = 'CHANGE ME'
SECRET_KEY = 'CHANGE ME'

# Files with these extensions are available as profile image and will be displayed in the browser
DISPLAY_FILE_EXTENSIONS = ['bmp', 'gif', 'ico', 'jpeg', 'jpg', 'png', 'svg']

# Files with these extension are selectable for import, it would make no sense to overwrite them
IMPORT_FILE_EXTENSIONS = ['csv']

# Paths are implemented operating system independent using pathlib.
# If you want to override them (in instance/production.py) either use them like here
# or use absolute paths like e.g. pathlib.Path('/some/location/somewhere')
TMP_FOLDER_PATH = pathlib.Path('/tmp')  # e.g. for processing import/export files
ROOT_PATH = pathlib.Path(app.root_path)
EXPORT_FOLDER_PATH = ROOT_PATH.joinpath('export')
UPLOAD_FOLDER_PATH = ROOT_PATH.joinpath('uploads')

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
