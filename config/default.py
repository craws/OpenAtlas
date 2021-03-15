# Don't edit this file. To override settings please use instance/production.py
from pathlib import Path

from openatlas import app

VERSION = '6.1.0'
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

# Modules
MODULES = ['map_overlay', 'notes', 'sub_units']

# API
API_SCHEMA = 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld'
CORS_ALLOWANCE = '*'  # Cross-Origin source (CORS)
ALLOWED_IPS = ['127.0.0.1']

# Table options
TABLE_ROWS = {10: '10', 25: '25', 50: '50', 100: '100'}

# Minimum required characters for table filters
MIN_CHARS_JSTREE_SEARCH = 1

# Log levels
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

PROPERTY_TYPES = ['Actor actor relation', 'Actor function', 'Involvement']  # Needed for type moves
EXTERNAL_REFERENCES_FORMS = [
    'acquisition', 'activity', 'artifact',  'feature',  'find',  'group', 'human_remains',  'move',
    'person',  'place',  'type']

