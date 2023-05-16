# Script for upgrading the database to the current (software) version
#
# A backup will be made before any database changes happen and although it is
# fully implemented and tested we still consider this script experimental.
#
# Limitations:
# You should only do this with the official main branch of OpenAtlas.
# If the database owner is not called "openatlas" (default) you will have to
# update the SQL files accordingly before.
#
# To use it, execute from project root:
# python3 install/upgrade/database_upgrade.py
#

import os
import sys
import time
from pathlib import Path

from psycopg2 import extras

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.database_versions import DATABASE_VERSIONS
from config.default import (
    DATABASE_PASS, VERSION, DATABASE_VERSION, DATABASE_NAME, DATABASE_USER,
    DATABASE_HOST, DATABASE_PORT, EXPORT_DIR)
from instance import production
from openatlas.database.connect import open_connection
from openatlas.database.settings import Settings
from openatlas.models.export import sql_export

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
    except Exception:
        pass

db = open_connection(config)
cursor = db.cursor(cursor_factory=extras.DictCursor)
settings = Settings.get_settings(cursor)


def database_upgrade() -> None:
    print(f"{VERSION} OpenAtlas version")
    check_database_version_exist()
    print(f"{settings['database_version']} Database version")
    print(f"{DATABASE_VERSION} Database version required")
    check_database_version_supported()
    check_upgrade_needed()
    backup_database()
    execute_upgrade()


def execute_upgrade() -> None:
    is_before = True
    current_version = settings['database_version']
    for version in reversed(DATABASE_VERSIONS):
        if not is_before and current_version != version:
            print(f'Upgrade {current_version} to {version}: start')
            filename = f'{version}.sql'
            upgrade_sql_path = Path(__file__).parent
            sql_file_path = None
            for path in upgrade_sql_path.rglob(filename):
                sql_file_path = path
                break
            if not sql_file_path:
                finish(f'{filename} not found in {upgrade_sql_path}. Aborting')
            try:
                with open(str(sql_file_path), 'r') as sql_file:
                    cursor.execute(sql_file.read())
            except Exception as e:
                finish(f'Import of {sql_file_path} failed.\n{e}')
            print(f'Upgrade {current_version} to {version}: success')
            current_version = version
        if version == settings['database_version']:
            is_before = False
    finish('Script finished successful')


def check_database_version_exist() -> None:
    if 'database_version' not in settings:
        finish(
            'The database seems to be too old to be upgraded automatically '
            '(database version unknown).')


def check_upgrade_needed() -> None:
    if DATABASE_VERSION == settings['database_version']:
        finish('Current database version already matches the required one.')


def check_database_version_supported() -> None:
    if DATABASE_VERSION not in DATABASE_VERSIONS:
        finish(f"Version {VERSION} isn't supported for automatic upgrades.")


def backup_database() -> None:
    path = EXPORT_DIR
    if not os.access(path, os.W_OK):
        finish(
            f'Directory for database backup not writeable ({path}). Aborting!')
    print('Database backup: start')
    if sql_export('_before_database_upgrade_script'):
        print(f'Database backup: successful backup at {path}')
    else:
        finish('Database backup failed.')


def finish(message: str) -> None:
    print(f'\n{message}')
    print(f'Execution time: {int(time.time() - start)} seconds')
    sys.exit()


database_upgrade()
