import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_params import test_ids

test_geometric_entity = {
    'type': 'FeatureCollection',
    'features': [{
        'type': 'Feature',
        'geometry': {'coordinates': [9, 17], 'type': 'Point'},
        'properties': {
            'id': 1,
            'name': '',
            'description': '',
            'objectId': {test_ids["shire_id"]},
            'objectDescription': 'The Shire was the homeland of the hobbits.',
            'objectName': 'Shire',
            'objectType': None,
            'shapeType': 'centerpoint'}}]}
