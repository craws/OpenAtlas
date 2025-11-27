# Don't edit this file. To override settings please use instance/production.py
from pathlib import Path

from rdflib import Namespace

from config.database_versions import DATABASE_VERSIONS

VERSION = '8.15.1'
DATABASE_VERSION = DATABASE_VERSIONS[0]
DEMO_MODE = False  # If activated some options are disabled, login is prefilled
DEBUG = False

DATABASE_NAME = 'openatlas'
DATABASE_USER = 'openatlas'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 5432
DATABASE_PASS = 'CHANGE ME'
MAIL_PASSWORD = 'CHANGE ME'
SECRET_KEY = 'CHANGE ME'  # Used for cookies and jwt tokens

LANGUAGES = {
    'ca': 'Català',
    'de': 'Deutsch',
    'en': 'English',
    'es': 'Español',
    'fr': 'Français',
    'pl': 'Polski'}

# Paths are implemented operating system independent using pathlib.
# To override them (in instance/production.py) either use them like here
# or use absolute paths like e.g. pathlib.Path('/some/location/somewhere')
FILES_PATH = Path(__file__).parent.parent / 'files'
EXPORT_PATH = Path(FILES_PATH) / 'export'
SQL_PATH = Path(EXPORT_PATH) / 'sql'
ARCHE_PATH = Path(EXPORT_PATH) / 'arche'
RDF_PATH = Path(EXPORT_PATH) / 'rdf'
UPLOAD_PATH = Path(FILES_PATH) / 'uploads'
TMP_PATH = Path('/tmp')  # For processing files e.g. at import and export

# Image processing
DISPLAY_FILE_EXT = ['.bmp', '.gif', '.ico', '.jpeg', '.jpg', '.png', '.svg']
PROCESSABLE_EXT = ['.tiff', '.tif']
PROCESSED_EXT = '.jpeg'
PROCESSED_IMAGE_PATH = Path(FILES_PATH) / 'processed_images'
RESIZED_IMAGES = Path(PROCESSED_IMAGE_PATH) / 'resized'
IMAGE_SIZE = {
    'thumbnail': '200',
    'table': '100'}

# Security
SESSION_COOKIE_SECURE = False  # Should be True in production.py if using HTTPS
REMEMBER_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Proxies (e.g. for calls to remote APIs when behind an institution firewall)
# e.g. PROXIES = {
#    'http': 'http://someurl.org:8080',
#    'https': 'http://someurl.org:8080'}
PROXIES: dict[str, str] = {}

# Table options
TABLE_ROWS = {10: '10', 25: '25', 50: '50', 100: '100'}

# Minimum required characters for table filters
MIN_CHARS_JSTREE_SEARCH = 1

CSS = {
    'string_field': 'form-control form-control-sm',
    'button': {
        'primary': 'btn btn-outline-primary btn-sm',
        'secondary': 'btn btn-outline-secondary btn-sm'}}

# Tests
LOAD_WINDOWS_TEST_SQL = False

# External APIs
API_WIKIDATA = 'https://www.wikidata.org/w/api.php'
API_GEONAMES = 'http://api.geonames.org/get'
USER_AGENT = {
    "User-Agent":
        f"OpenAtlas/{VERSION} (https://github.com/craws/OpenAtlas; "
        "openatlas@oeaw.ac.at)"}

CSP_HEADER = "frame-ancestors 'self'"

# ARCHE export
ACDH = Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")  # type: ignore
ARCHE_URI_RULES = \
    'https://raw.githubusercontent.com/acdh-oeaw/arche-assets' \
    '/refs/heads/master/AcdhArcheAssets/uriNormRules.json'
ARCHE_METADATA = {
    'topCollection': '',
    'language': 'en',
    'depositor': [],
    'acceptedDate': '',
    'hasMetadataCreator': [],
    'curator': [],
    'principalInvestigator': [],
    'relatedDiscipline': [],
    'typeIds': [],
    'excludeReferenceSystems': []}

# Configure map point colors
# Defined colors for type_ids override the default, top ones are prioritised
MAP_TYPE_COLOR = {
    'default': '#007bd9',
    '123': '#007bd9'}
