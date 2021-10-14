import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_params import test_ids

test_subunit = {'nodes': [{
    'id': test_ids["home_id"], 'label': 'Home of Baggins',
    'url': f'http://local.host/api/0.2/entity/{test_ids["home_id"]}'}]}
test_subunit_hierarchy = {'nodes': [
    {'id': test_ids["home_id"], 'label': 'Home of Baggins',
     'url': f'http://local.host/api/0.2/entity/{test_ids["home_id"]}'},
    {'id': test_ids["kitchen_id"], 'label': 'Kitchen',
     'url': f'http://local.host/api/0.2/entity/{test_ids["kitchen_id"]}'}]}
