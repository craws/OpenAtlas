SERVER_NAME = 'local.host'
DATABASE_NAME = 'openatlas_test'
DATABASE_PASS = 'CHANGE ME'
DEBUG = True

# Disable CSRF
WTF_CSRF_ENABLED = False
WTF_CSRF_METHODS: list[str] = []

ARCHE = {
    'id': 0,
    'collection_ids': [0],
    'base_url': 'https://arche-curation.acdh-dev.oeaw.ac.at/',
    'thumbnail_url': 'https://arche-thumbnails.acdh.oeaw.ac.at/'}

# For Windows user
# from pathlib import Path
# TMP_DIR = Path('C:\\Path\\to\\tmp')
