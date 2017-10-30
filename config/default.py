from collections import OrderedDict

DEBUG = True
VERSION = '3.0.0'
LANGUAGES = {'en': 'English', 'de': 'Deutsch'}

DATABASE_NAME = 'openatlas'
DATABASE_USER = 'openatlas'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 5432

# Set these options in /instance/INSTANCE_NAME.py e.g. in /instance/production.py
DATABASE_PASS = 'CHANGE ME'
SECRET_KEY = 'CHANGE ME'

# Whitelisted domains are ignored by the link checker
WHITELISTED_DOMAINS = ['E61']

# This prevents editing/deleting the event root, only change it if you need to rename this entity
EVENT_ROOT_NAME = 'History of the World'

DEFAULT_TABLE_ROWS = OrderedDict()
DEFAULT_TABLE_ROWS[10] = '10'
DEFAULT_TABLE_ROWS[20] = '20'
DEFAULT_TABLE_ROWS[50] = '50'
DEFAULT_TABLE_ROWS[100] = '100'

LOG_LEVELS = OrderedDict()
LOG_LEVELS[0] = 'emergency'
LOG_LEVELS[1] = 'alert'
LOG_LEVELS[2] = 'critical'
LOG_LEVELS[3] = 'error'
LOG_LEVELS[4] = 'warn'
LOG_LEVELS[5] = 'notice'
LOG_LEVELS[6] = 'info'
LOG_LEVELS[7] = 'debug'
