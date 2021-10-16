import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_params import test_ids

test_node_entities = {'nodes': [
    {'id': test_ids['austria_id'],
     'label': 'Austria',
     'url': 'http://local.host/api/0.2/entity/84'},
    {'id':  test_ids['czech_id'],
     'label': 'Czech Republic',
     'url': 'http://local.host/api/0.2/entity/89'},
    {'id':  test_ids['germany_id'],
     'label': 'Germany',
     'url': 'http://local.host/api/0.2/entity/87'},
    {'id':  test_ids['italy_id'],
     'label': 'Italy',
     'url': 'http://local.host/api/0.2/entity/88'},
    {'id':  test_ids['slovakia_id'],
     'label': 'Slovakia',
     'url': 'http://local.host/api/0.2/entity/90'},
    {'id':  test_ids['slovenia_id'],
     'label': 'Slovenia',
     'url': 'http://local.host/api/0.2/entity/91'}]}
test_node_entities_all = {'nodes': [
    {'id':  test_ids['austria_id'],
     'label': 'Austria',
     'url': 'http://local.host/api/0.2/entity/84'},
    {'id':  test_ids['czech_id'],
     'label': 'Czech Republic',
     'url': 'http://local.host/api/0.2/entity/89'},
    {'id':  test_ids['germany_id'],
     'label': 'Germany',
     'url': 'http://local.host/api/0.2/entity/87'},
    {'id':  test_ids['italy_id'],
     'label': 'Italy',
     'url': 'http://local.host/api/0.2/entity/88'},
    {'id':  test_ids['slovakia_id'],
     'label': 'Slovakia',
     'url': 'http://local.host/api/0.2/entity/90'},
    {'id':  test_ids['slovenia_id'],
     'label': 'Slovenia',
     'url': 'http://local.host/api/0.2/entity/91'},
    {'id':  test_ids['nieder_id'],
     'label': 'Niederösterreich',
     'url': 'http://local.host/api/0.2/entity/86'},
    {'id':  test_ids['wien_id'],
     'label': 'Wien',
     'url': 'http://local.host/api/0.2/entity/85'}]}
