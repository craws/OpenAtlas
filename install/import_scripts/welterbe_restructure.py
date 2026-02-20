"""
This script is for restructuring place hierarchies from the Welterbe project.
Basically:
* Places -> Custom hierarchy cadaster
* Feature and artifacts -> Places

To do:
* Link system cadaster ext ref system to administrative units (valid URLs?)
* Add infos from former places to new cadaster (to be discussed in meeting)
* Connect new places to cadaster
* Delete place types
* Change feature and artifact types to place types
* Test everything and once looking ok upload online to be tested by others too

"""
import time
from typing import Any

import psycopg2
from flask import g
from psycopg2 import extras

from openatlas import app
from openatlas.models.entity import Entity, insert
from tests.base import get_hierarchy


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


def prepare_cadasters() -> None:
    hierarchy = insert({
        'name': 'Cadaster',
        'openatlas_class_name': 'administrative_unit'})
    Entity.insert_hierarchy(hierarchy, 'place', ['place'], True)
    for place in places:
        if ' ' in place.name:
            print(f'Whitespace! in {place.name}')
        name_parts = place.name.split('_')
        if len(name_parts) < 2 or len(name_parts[0]) != 5:
            print('on no! ' + place.name)
            return
        place.name = name_parts[1]
        place.cadaster_name = name_parts[0]
        cadaster_supers.add(name_parts[0])
    for item in cadaster_supers:
        entity = insert({
            'name': item,
            'openatlas_class_name': 'administrative_unit'})
        entity.link('P89', hierarchy)
        entity.unset_selectable()
        cadaster_mapping[item] = entity


def insert_cadasters() -> None:
    for place in places:
        name = place.name.replace('F', '.').replace('G', '/').replace('N', '')
        entity = insert({
            'name': name,
            'openatlas_class_name': 'administrative_unit',
            'description': place.description})
        entity.link(
            'P89',
            cadaster_mapping[place.cadaster_name])  # type: ignore


def link_cadasters() -> None:
    g.types = Entity.get_all_types(False)
    for node in cadaster_mapping.values():
        parent = g.types[node.id]
        for id_ in parent.subs:
            entity = g.types[id_]
            system.link('P67', entity, f'{parent.name}-{entity.name}')


def clean_up():
    count = 0
    try:
        hierarchy = get_hierarchy('Cadaster')
        for sub_id in hierarchy.get_sub_ids_recursive():
            g.types[sub_id].delete()
            count += 1
        hierarchy.delete()
        count += 1
    except:
        pass
    print(f'{count} former cadaster place types deleted')


def feature_and_artifact_to_place():
    g.cursor.execute(
        """
        UPDATE model.entity SET openatlas_class_name = 'place'
        WHERE openatlas_class_name IN ('artifact', 'feature');
        """)


with app.test_request_context():
    app.preprocess_request()
    system = Entity.get_by_id(11611)
    clean_up()
    places = Entity.get_by_class('place')
    cadaster_supers = set()
    cadaster_mapping = {}
    prepare_cadasters()
    insert_cadasters()
    link_cadasters()
    # feature_and_artifact_to_place()

print(f'Execution time: {int(time.time() - start)} seconds')
