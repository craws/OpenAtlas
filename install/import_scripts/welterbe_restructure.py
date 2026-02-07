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

from openatlas import app
from openatlas.models.entity import Entity


start = time.time()
with app.test_request_context():
    app.preprocess_request()
    places = Entity.get_by_class('place')
    print(len(places))
    for place in places:
        name_parts = place.name.split('_')
        if len(name_parts) < 2 or len(name_parts[0]) != 5:
            print('on no! ' + place.name)
        else:
            print(name_parts[0] + ' ' + name_parts[1])

print(f'Execution time: {int(time.time() - start)} seconds')
