# Used to join data from OpenAtlas projects to the demo version
# Before running the script make sure you have configured the db to write to in
# instance/production.py

# This is work in progress: to do
# * Import new hierarchies and subs
# * What about place locations?
# * Link everything
# * What about files?

import time
from typing import Any

import psycopg2
from flask import g
from psycopg2 import extras

from openatlas import app
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
id_map = {}  # Map imported entity ids to existing ones


def cleanup() -> None:
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


def hierarchies() -> None:
    cursor.execute(
        """
        SELECT
            id,
            name,
            multiple,
            directional,
            created,
            modified,
            category,
            required
        FROM web.hierarchy;
        """)
    with app.test_request_context():
        app.preprocess_request()
        for item in list(cursor):
            exists = False
            try:
                if existing := Entity.get_hierarchy(item['name']):
                    exists = True
                    print(f'Hierarchy exists: {existing.name}')
            except IndexError:
                pass
            if not exists:
                insert_hierarchy(item)


def insert_hierarchy(item: dict[str, Any]) -> None:
    print(f"New hierarchy: {item['name']}")
    cursor.execute(
        'SELECT description FROM model.entity WHERE id = %(id)s;',
        {'id': item['id']})
    # description = cursor.fetchone()['description']
    # entity_ = insert('type', item['name'], description)
    # id_map[item['id']] = entity_.id
    # cursor.execute(
    #    """
    #    SELECT openatlas_class_name
    #    FROM web.hierarchy_openatlas_class
    #    WHERE hierarchy_id = %(id)s;
    #    """, {'id': item['id']})
    # Entity.insert_hierarchy(
    #    entity_,
    #    item['category'],
    #    [x[0] for x in list(cursor)],
    #   item['multiple'])


cleanup()
hierarchies()

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
    # for row in list(cursor):
    #     if row['openatlas_class_name'] not in [
    #             'administrative_unit',
    #             'type',
    #             'type_tools']:
    #         entity = insert(
    #             row['openatlas_class_name'],
    #             row['name'],
    #             row['description'])
    #         import_data(
    #             PROJECT_ID,
    #             entity.id,
    #             IMPORT_USER_ID,
    #             origin_id=row['id'])
print(f'Execution time: {int(time.time() - start)} seconds')
