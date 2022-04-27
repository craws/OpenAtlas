# Script for upgrading the database to the current (software) version
# Usage from project root:
# python3 install/upgrade/database_upgrade.py

import sys
import time
from pathlib import Path

from psycopg2 import extras

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from openatlas import open_connection
from openatlas.database.settings import Settings
from config.database_versions import database_versions
from config.default import (
    DATABASE_PASS, VERSION, DATABASE_VERSION, DATABASE_NAME, DATABASE_USER,
    DATABASE_HOST, DATABASE_PORT)
from instance import production

config = {
    'DATABASE_NAME': DATABASE_NAME,
    'DATABASE_USER': DATABASE_USER,
    'DATABASE_PASS': DATABASE_PASS,
    'DATABASE_PORT': DATABASE_PORT,
    'DATABASE_HOST': DATABASE_HOST}

start = time.time()

for item in config:
    try:
        config[item] = vars(production)[item]
    except:
        pass

db = open_connection(config)
cursor = db.cursor(cursor_factory=extras.DictCursor)
settings = Settings.get_settings(cursor)


def end_output():
    print(f'Execution time: {int(time.time() - start)} seconds')
    exit()


print(f"{VERSION} OpenAtlas version")
print(f"{DATABASE_VERSION} Database version required")
print(f"{settings['database_version']} Installed database version")
print('')
if DATABASE_VERSION == settings['database_version']:
    print(
        'The current database version already matches the required one. '
        'Have a nice day.')
    end_output()

if VERSION not in database_versions:
    print(f"Sadly, version {VERSION} isn't supported for automatic upgrades.")
    end_output()
