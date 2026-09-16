# Used to join data from OpenAtlas projects
# Before running the script make sure you have configured:
# * The database to write to in instance/production.py
# * The database to read from in this script

# Work in progress, to do:
# * Prevent double system references type match links
# * Link admin units
# * Files
# * Add case studies
# * Check additional classes for reference systems
# * Check additional classes for types
#
# 2nd part when dealing with multiple data sests
# * Track manual mapping for e.g. duplicates
# * New reference systems

import time
from typing import Any

import psycopg2
from flask import g
from psycopg2 import extras

from openatlas import app
from openatlas.database import entity as db
from openatlas.database.entity import set_required
from openatlas.database.imports import import_data
from openatlas.models.entity import Entity, insert

DATABASE_NAME = 'openatlas_demo'  # The database to fetch data from
PROJECT_NAME = 'MEDCON'  # Will also be added as case study
PROJECT_DESCRIPTION = \
    'Mapping Medieval Conflicts (MEDCON). A digital approach towards ' \
    'political dynamics in the pre-modern period.'
IMPORT_USER_ID = 1


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
id_map: dict[int, int] = {}  # Map imported entity ids to existing ones
id_added: list[int] = []  # Track already inserted entities


def cleanup(id_: int) -> None:
    g.cursor.execute(
        """
        DELETE FROM model.entity
        WHERE id IN (
            SELECT entity_id
            FROM import.entity WHERE project_id = %(project_id)s);
        """, {'project_id': id_})
    g.cursor.execute(
        'DELETE FROM import.entity WHERE project_id = %(project_id)s;',
        {'project_id': id_})
    g.types = Entity.get_all_types(False)  # Reload type hierarchies


def insert_project() -> int:
    g.cursor.execute(
        """
        INSERT INTO import.project (name, description)
        VALUES (%(name)s, %(description)s)
        ON CONFLICT (name) DO UPDATE SET description = %(description)s
        RETURNING id;
        """,
        {'name': PROJECT_NAME, 'description': PROJECT_DESCRIPTION})
    return g.cursor.fetchone()['id']


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
        FROM
            web.hierarchy;
        """)
    for item in list(cursor):
        exists = False
        try:
            if existing := Entity.get_hierarchy(item['name']):
                exists = True
                id_map[item['id']] = existing.id
                print(f'Hierarchy exists: {existing.name}')
        except IndexError:
            pass
        if not exists:
            insert_hierarchy(item)


def insert_hierarchy(item: dict[str, Any]) -> None:
    print(f"New hierarchy: {item['name']}")
    cursor.execute(
        """
        SELECT
            name, openatlas_class_name, description,
            begin_from, begin_to, begin_comment, end_from, end_to, end_comment
        FROM model.entity
        WHERE id = %(id)s;
        """,
        {'id': item['id']})
    entity_ = insert(cursor.fetchone())
    import_data(project_id, entity_.id, IMPORT_USER_ID, item['id'])
    id_map[item['id']] = entity_.id
    id_added.append(entity_.id)
    cursor.execute(
       """
       SELECT openatlas_class_name
       FROM web.hierarchy_openatlas_class
       WHERE hierarchy_id = %(id)s;
       """, {'id': item['id']})
    Entity.insert_hierarchy(
       entity_,
       item['category'],
       [x[0] for x in list(cursor)],
       item['multiple'])
    if item['required']:
        set_required(entity_.id)


def types() -> None:
    cursor_current = g.cursor
    g.cursor = cursor
    import_types = Entity.get_all_types(False)
    g.cursor = cursor_current
    for import_hierarchy in [
            type_ for type_ in import_types.values() if not type_.root]:
        print(import_hierarchy.name)
        hierarchy = Entity.get_hierarchy(import_hierarchy.name)
        for id_ in import_hierarchy.subs:
            types_recursive(id_, hierarchy, import_types)
    g.types = Entity.get_all_types(False)


def types_recursive(
        id_: int,
        super_: Entity,
        import_types: dict[int, Entity]) -> None:
    exists = False
    for sub_id in super_.subs:
        if g.types[sub_id].name == import_types[id_].name:
            id_map[id_] = sub_id
            print(f'exists: {import_types[id_].name}')
            for import_sub_id in import_types[id_].subs:
                types_recursive(import_sub_id, g.types[sub_id], import_types)
            exists = True
            break
    if not exists:
        insert_type_recursive(import_types[id_], import_types)


def insert_type_recursive(
        import_type: Entity,
        import_types: dict[int, Entity]):
    print(f'New type: {import_type.name}')
    new_type = insert({
       'name': import_type.name,
       'description': import_type.description,
       'openatlas_class_name': import_type.class_.name,
       'begin_from': import_type.dates.begin_from,
       'begin_to': import_type.dates.begin_to,
       'begin_comment': import_type.dates.begin_comment,
       'end_from': import_type.dates.end_from,
       'end_to': import_type.dates.end_to,
       'end_comment': import_type.dates.end_comment})
    track(import_type.id, new_type.id)
    super_id = id_map[import_type.root[-1]]
    new_type.link(
        new_type.class_.relations['super'].property,
        g.types[super_id])
    g.types = Entity.get_all_types(False)
    for sub_id in import_type.subs:
        insert_type_recursive(import_types[sub_id], import_types)


def track(import_id: int, new_id: int) -> None:
    import_data(project_id, new_id, IMPORT_USER_ID, import_id)
    id_map[import_id] = new_id


def insert_entities() -> None:
    print('Insert entities')
    cursor.execute(
        """
        SELECT
            id,
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
        FROM
            model.entity
        WHERE openatlas_class_name NOT IN (
            'administrative_unit', 'reference_system', 'type', 'type_tools');
        """)
    for row in list(cursor):
        new_id = db.insert({
           'name': row['name'],
           'description': row['description'],
           'openatlas_class_name': row['openatlas_class_name'],
           'begin_from': row['begin_from'],
           'begin_to': row['begin_to'],
           'begin_comment': row['begin_comment'],
           'end_from': row['end_from'],
           'end_to': row['end_to'],
           'end_comment': row['end_comment']})
        track(row['id'], new_id)


def reference_systems() -> None:
    cursor_current = g.cursor
    g.cursor = cursor
    system_rows = db.get_reference_systems()
    g.cursor = cursor_current
    for row in system_rows:
        exists = False
        for existing_system in g.reference_systems.values():
            if row['name'] == existing_system.name:
                print(f'Reference system exists: {row['name']}')
                exists = True
                id_map[row['id']] = existing_system.id
        if not exists:
            # Todo: implement adding reference systems
            print(f'New reference system: {row['name']}')


def link_entities() -> None:
    print('Insert links')
    cursor.execute(
        """
        SELECT
            id,
            property_code,
            domain_id,
            range_id,
            description,
            created,
            modified,
            type_id,
            COALESCE(to_char(begin_from, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS begin_from, begin_comment,
            COALESCE(to_char(begin_to, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS begin_to,
            COALESCE(to_char(end_from, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS end_from, end_comment,
            COALESCE(to_char(end_to, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                AS end_to
        FROM model.link
        WHERE property_code NOT IN ('P127', 'P89');
        """)
    for row in list(cursor):
        if row['domain_id'] not in id_map:
            print(f'Missing domain_id in id_map: {row['domain_id']}')
            continue
        if row['range_id'] not in id_map:
            print(f'Missing range_id in id_map: {row['range_id']}')
            continue
        db.link({
            'property_code': row['property_code'],
            'domain_id': id_map[row['domain_id']],
            'range_id': id_map[row['range_id']],
            'description': row['description'],
            'type_id': id_map[row['type_id']] if row['type_id'] else None,
            'begin_from': row['begin_from'] or None,
            'begin_to': row['begin_to'] or None,
            'begin_comment': row['begin_comment'] or None,
            'end_from': row['end_from'] or None,
            'end_to': row['end_to'] or None,
            'end_comment': row['end_comment'] or None
        })


with app.test_request_context():
    app.preprocess_request()
    project_id = insert_project()
    cleanup(project_id)
    hierarchies()
    reference_systems()
    types()
    insert_entities()
    link_entities()

print(f'Execution time: {int(time.time() - start)} seconds')
