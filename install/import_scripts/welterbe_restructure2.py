"""
This script is for restructuring type hierarchies for the Welterbe project.
Basically some building levels types will be merged, see issue #2764
"""

import time
from typing import Any

import psycopg2
from flask import g
from psycopg2 import extras

from openatlas import app
from openatlas.database.checks import delete_link_duplicates
from openatlas.models.entity import Entity, insert


def connect() -> Any:
    return psycopg2.connect(
        database='openatlas_welterbe',
        user=app.config['DATABASE_USER'],
        password=app.config['DATABASE_PASS'],
        port=app.config['DATABASE_PORT'],
        host=app.config['DATABASE_HOST'])


start = time.time()
connection = connect()
cursor = connection.cursor(cursor_factory=extras.DictCursor)

former_hierarchies = [
    '10 Gebäude - 05 Erdgeschoß',
    '10 Gebäude - 06 1.Obergeschoß',
    '10 Gebäude - 06 2.Obergeschoß',
    '10 Gebäude - 06 3.Obergeschoß',
    '10 Gebäude - 06 4.Obergeschoß',
    '10 Gebäude - 06 5.Obergeschoß']


def get_mapping() -> None:
    for name in former_hierarchies:
        old_hierarchy = Entity.get_hierarchy(name)
        for id_ in old_hierarchy.subs:
            type_ = g.types[id_]
            if type_.name == 'vorhanden':
                continue
            if type_.name not in mapping:
                mapping[type_.name] = {'org_ids': [], 'subs': {}}
            mapping[type_.name]['org_ids'].append(id_)
            for sub_id in type_.subs:
                sub = g.types[sub_id]
                if sub.name not in mapping[type_.name]['subs']:
                    mapping[type_.name]['subs'][sub.name] = {'org_ids': []}
                mapping[type_.name]['subs'][sub.name]['org_ids'].append(sub_id)
                if sub.subs:
                    print(f'Warning: there are subs in {sub.id}')


def insert_new_types() -> None:
    for name, value in mapping.items():
        new_type = insert({
            'name': name,
            'description': '',
            'openatlas_class_name': 'type'})
        new_type.link('P127', hierarchy)
        value['new_id'] = new_type.id
        for sub_name in value['subs']:
            new_sub = insert({
                'name': sub_name,
                'description': '',
                'openatlas_class_name': 'type'})
            new_sub.link('P127', new_type)
            value['subs'][sub_name]['new_id'] = new_sub.id


def insert_new_type_links() -> None:
    for value in mapping.values():
        g.cursor.execute(
            """
            UPDATE model.link
            SET range_id = %(new_id)s
            WHERE property_code = 'P2' AND range_id IN %(org_ids)s;
            """,
            {'new_id': value['new_id'], 'org_ids': tuple(value['org_ids'])})
        for sub_name in value['subs']:
            g.cursor.execute(
                """
                UPDATE model.link
                SET range_id = %(new_id)s
                WHERE property_code = 'P2' AND range_id IN %(org_ids)s;
                """, {
                    'new_id': value['subs'][sub_name]['new_id'],
                    'org_ids': tuple(value['subs'][sub_name]['org_ids'])})
    delete_link_duplicates()


def move_usage_types() -> None:
    usage_mapping = {}
    current_usage_hierarchy = g.types[11329]
    for sub_id in current_usage_hierarchy.subs:
        usage_type = g.types[sub_id]
        usage_mapping[usage_type.name] = sub_id
    for name, data in mapping['Nutzungsart']['subs'].items():
        if name not in usage_mapping:
            new_type = insert({
                'name': name,
                'description': '',
                'openatlas_class_name': 'type'})
            new_type.link('P127', current_usage_hierarchy)
            usage_mapping[name] = new_type.id
        g.cursor.execute(
            """
            UPDATE model.link
            SET range_id = %(new_id)s
            WHERE property_code = 'P2' AND range_id = %(org_id)s;
            """,
            {'new_id': usage_mapping[name], 'org_id': data['new_id']})


def clean_up() -> None:
    for name in former_hierarchies:
        hierarchy_ = Entity.get_hierarchy(name)
        for sub_id in hierarchy_.get_sub_ids_recursive():
            g.types[sub_id].delete()
        hierarchy_.delete()
    g.types = Entity.get_all_types(False)
    former_usage_hierarchy = g.types[mapping['Nutzungsart']['new_id']]
    for sub_id in former_usage_hierarchy.get_sub_ids_recursive():
        g.types[sub_id].delete()
    former_usage_hierarchy.delete()
    delete_link_duplicates()


with app.test_request_context():
    app.preprocess_request()
    hierarchy = g.types[27145]
    hierarchy_usage = g.types[11329]
    mapping: dict[Any, Any] = {}
    get_mapping()
    insert_new_types()
    insert_new_type_links()
    move_usage_types()
    clean_up()
print(f'Execution time: {int(time.time() - start)} seconds')
