import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_params import test_ids


test_subunit = {'nodes': [{
    'id': 108, 'label': 'Home of Baggins',
    'url': 'http://local.host/api/0.2/entity/108'}]}
test_subunit_hierarchy = {'nodes': [
    {'id': 108, 'label': 'Home of Baggins',
     'url': 'http://local.host/api/0.2/entity/108'},
    {'id': 110, 'label': 'Kitchen',
     'url': 'http://local.host/api/0.2/entity/110'}]}
