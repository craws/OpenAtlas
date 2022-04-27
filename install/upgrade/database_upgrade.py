# Script for upgrading the database to the current (software) version
# Usage from project root:
# python3 install/upgrade/database_upgrade.py
import os
import sys
import time
from pathlib import Path

from psycopg2 import extras

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.database_versions import application_database_versions
from config.default import (
    DATABASE_PASS, VERSION, DATABASE_VERSION, DATABASE_NAME, DATABASE_USER,
    DATABASE_HOST, DATABASE_PORT)
from instance import production
from openatlas import open_connection
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
    except:
        pass

db = open_connection(config)
cursor = db.cursor(cursor_factory=extras.DictCursor)
settings = Settings.get_settings(cursor)


def database_upgrade():
    print(f"{VERSION} OpenAtlas version")
    print(f"{DATABASE_VERSION} Database version required")

    check_database_version_exist()
    print(f"{settings['database_version']} Installed database version")

    check_database_version_supported()
    check_upgrade_needed()
    # backup_database()
    execute_upgrade_sqls()


def execute_upgrade_sqls():
    reversed_ = dict(reversed(list(application_database_versions.items())))
    is_before = True
    current_version = settings['database_version']
    for application_version, database_version in reversed_.items():
        if not is_before and current_version != database_version:
            print(f'Need to upgrade {current_version} to {database_version}')
            filename = f'{database_version}.sql'
            install_path = Path(os.getcwd()) / 'install'
            sql_file_path = None
            for path in install_path.rglob(filename):
                sql_file_path = path
                break
            if not sql_file_path:
                print(f'{filename} not found in {install_path}')
                print('Script is aborting.')
                end_output()
            try:
                with open(sql_file_path, 'r') as sql_file:
                    cursor.execute(sql_file.read())
            except Exception as e:
                print(f'Import of {sql_file_path} failed. {e}')
                end_output()
            current_version = database_version
        if database_version == settings['database_version']:
            is_before = False


def check_database_version_exist():
    if 'database_version' not in settings:
        print(
            'The database is too old to be upgraded automatically '
            '(database version unknown).')
        end_output()


def check_upgrade_needed():
    if DATABASE_VERSION == settings['database_version']:
        print(
            'The current database version already matches the required one. '
            'Have a nice day.')
        end_output()


def check_database_version_supported():
    if VERSION not in application_database_versions:
        print(f"Version {VERSION} isn't supported for automatic upgrades.")
        end_output()


def backup_database():
    print('Start database backup')
    if sql_export('_from_database_upgrade_script'):
        print('Successful backup of database.')
    else:
        print(f'\nDatabase backup failed.')
        end_output()


def end_output():
    print(f'Execution time: {int(time.time() - start)} seconds')
    exit()


database_upgrade()
