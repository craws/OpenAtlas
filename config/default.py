# Don't edit this file. To override settings please use instance/production.py
from pathlib import Path

from config.database_versions import DATABASE_VERSIONS

VERSION = '7.17.0'
DATABASE_VERSION = DATABASE_VERSIONS[0]
DEMO_MODE = False  # If activated some options are disabled, login is prefilled
DEBUG = False

DATABASE_NAME = 'openatlas'
DATABASE_USER = 'openatlas'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 5432
DATABASE_PASS = 'CHANGE ME'
MAIL_PASSWORD = 'CHANGE ME'
SECRET_KEY = 'CHANGE ME'  # Used for cookies

LANGUAGES = {
    'ca': 'Català',
    'de': 'Deutsch',
    'en': 'English',
    'es': 'Español',
    'fr': 'Français'}

# Files with these extensions are can be displayed in the browser
DISPLAY_FILE_EXTENSIONS = \
    ['.bmp', '.gif', '.ico', '.jpeg', '.jpg', '.png', '.svg']

# Paths are implemented operating system independent using pathlib.
# To override them (in instance/production.py) either use them like here
# or use absolute paths like e.g. pathlib.Path('/some/location/somewhere')
FILES_PATH = Path(__file__).parent.parent / 'files'
EXPORT_PATH = Path(FILES_PATH) / 'export'
UPLOAD_PATH = Path(FILES_PATH) / 'uploads'
TMP_PATH = Path('/tmp')  # used e.g. for processing imports and export files

# Image processing
PROCESSED_IMAGE_PATH = Path(FILES_PATH) / 'processed_images'
RESIZED_IMAGES = Path(PROCESSED_IMAGE_PATH) / 'resized'
IMAGE_SIZE = {
    'thumbnail': '200',
    'table': '100'}
NONE_DISPLAY_EXT = ['.tiff', '.tif']
ALLOWED_IMAGE_EXT = DISPLAY_FILE_EXTENSIONS + NONE_DISPLAY_EXT
PROCESSED_EXT = '.jpeg'

IIIF_ACTIVATE = False
IIIF_PATH = ''
IIIF_PREFIX = ''  # has to end with /
IIIF_URL = ''

# For system checks
WRITABLE_PATHS = [
    UPLOAD_PATH,
    EXPORT_PATH,
    RESIZED_IMAGES]

# Security
SESSION_COOKIE_SECURE = False  # Should be True in production.py if using HTTPS
REMEMBER_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Table options
TABLE_ROWS = {10: '10', 25: '25', 50: '50', 100: '100'}

# Minimum required characters for table filters
MIN_CHARS_JSTREE_SEARCH = 1

CSS = {
    'string_field': 'form-control form-control-sm',
    'button': {
        'primary': 'btn btn-outline-primary btn-sm',
        'secondary': 'btn btn-outline-secondary btn-sm'}}
