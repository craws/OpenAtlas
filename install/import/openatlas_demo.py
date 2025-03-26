# Used to join data from OpenAtlas projects to the demo version
# Before running the script make sure you have configured the db to write to in
# instance/production.py

import time
from typing import Any

import psycopg2.extras
from flask import g
from psycopg2 import extras

from openatlas import app
from openatlas.database.imports import import_data
from openatlas.models.entity import Entity

DATABASE_NAME = 'openatlas_demo'  # The database to fetch data from
PROJECT_ID = 1
IMPORT_USER_ID = 2


def connect() -> Any:
    return psycopg2.connect(
        database=DATABASE_NAME,
        user=app.config['DATABASE_USER'],
        password=app.config['DATABASE_PASS'],
        port=app.config['DATABASE_PORT'],
        host=app.config['DATABASE_HOST'])


start = time.time()
connection = connect()
cursor = connection.cursor(cursor_factory=extras.DictCursor)


def cleanup():
    with app.test_request_context():
        app.preprocess_request()
        g.cursor.execute(
            """
            DELETE FROM model.entity
            WHERE id IN (
                SELECT entity_id
                FROM import.entity
                WHERE project_id = %(project_id)s);
            """, {'project_id': PROJECT_ID})
        g.cursor.execute(
            'DELETE FROM import.entity WHERE project_id = %(project_id)s;',
            {'project_id': PROJECT_ID})


cleanup()
cursor.execute(
    """
    SELECT
        id,
        cidoc_class_code,
        name,
        description,
        created,
        modified,
        begin_from,
        begin_to,
        begin_comment,
        end_from,
        end_to,
        end_comment,
        openatlas_class_name
    FROM model.entity;
    """)
with app.test_request_context():
    app.preprocess_request()
    for row in list(cursor):
        if row['openatlas_class_name'] not in [
                'administrative_unit',
                'object_location',
                'type',
                'type_tools']:
            entity = Entity.insert(
                row['openatlas_class_name'],
                row['name'],
                row['description'])
            import_data(
                PROJECT_ID,
                entity.id,
                IMPORT_USER_ID,
                origin_id=row['id'])
print(f'Execution time: {int(time.time() - start)} seconds')
