DEBUG = True
VERSION = '3.0.0'
LANGUAGES = {
    'en': 'English',
    'de': 'Deutsch'}

# whitelisted domains are ignored by the link checker
WHITELISTED_DOMAINS = ['E61']

# this prevents editing/deleting the event root, only change it if you need to rename the entity
EVENT_ROOT_NAME = 'History of the World'

DATABASE_NAME = 'openatlas'
DATABASE_USER = 'openatlas'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 5432

DEBUG = False

# Set these options in /instance/INSTANCE_NAME.py
DATABASE_PASS = 'CHANGE ME'
SECRET_KEY = 'CHANGE ME'
