"""
This script is for restructuring place hierarchies from the Welterbe project.
Basically:
* Places -> Custom hierarchy kataster
* Feature and artifacts -> Places

Steps:
* Add custom place hierarchy "Kataster"
* Link system cadaster ext ref system to admininstrative units
* Make non selectable top level Kataster entries e.g. 42005 for 42005_F407G8
* Change existing places to hierarchically place hierarchy entities
** Take care of different spellings, e.g. spaces, F and N characters, ...
** Add external reference link with correct spelling e.g. 42005/.407/8
* Change existing features and artifacts to places
* Delete place types
* Change feature and artifact types to place types
* Test everything and once looking ok upload online to be tested by others too

"""
import time

from flask import g

from openatlas import app
from openatlas.models.entity import Entity, insert
from tests.base import get_hierarchy

start = time.time()


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
        entity.link('P89', cadaster_mapping[place.cadaster_name])


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


with app.test_request_context():
    app.preprocess_request()
    # system = Entity.get_by_id(11611)
    clean_up()
    places = Entity.get_by_class('place')
    cadaster_supers = set()
    cadaster_mapping = {}
    prepare_cadasters()
    insert_cadasters()

print(f'Execution time: {int(time.time() - start)} seconds')
