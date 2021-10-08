import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_params import test_ids

test_node_overview = {'types': [{
    'standard': {
        'Actor actor relation': [
            {'id': 63, 'url': 'http://local.host/api/0.2/entity/63',
             'label': 'Economical', 'children': [
                {'id': 64, 'url': 'http://local.host/api/0.2/entity/64',
                 'label': 'Provider of (Customer of)', 'children': []}]},
            {'id': 54, 'url': 'http://local.host/api/0.2/entity/54',
             'label': 'Kindredship', 'children': [
                {'id': 55, 'url': 'http://local.host/api/0.2/entity/55',
                 'label': 'Parent of (Child of)', 'children': []}]},
            {'id': 60, 'url': 'http://local.host/api/0.2/entity/60',
             'label': 'Political', 'children': [
                {'id': 61, 'url': 'http://local.host/api/0.2/entity/61',
                 'label': 'Ally of', 'children': []},
                {'id': 62, 'url': 'http://local.host/api/0.2/entity/62',
                 'label': 'Leader of (Retinue of)', 'children': []}]},
            {'id': 56, 'url': 'http://local.host/api/0.2/entity/56',
             'label': 'Social', 'children': [
                {'id': 58, 'url': 'http://local.host/api/0.2/entity/58',
                 'label': 'Enemy of', 'children': []},
                {'id': 57, 'url': 'http://local.host/api/0.2/entity/57',
                 'label': 'Friend of', 'children': []},
                {'id': 59, 'url': 'http://local.host/api/0.2/entity/59',
                 'label': 'Mentor of (Student of)', 'children': []}]}],
        'Actor function': [
            {'id': 18, 'url': 'http://local.host/api/0.2/entity/18',
             'label': 'Abbot', 'children': []},
            {'id': 17, 'url': 'http://local.host/api/0.2/entity/17',
             'label': 'Bishop', 'children': []},
            {'id': 21, 'url': 'http://local.host/api/0.2/entity/21',
             'label': 'Count', 'children': []},
            {'id': 20, 'url': 'http://local.host/api/0.2/entity/20',
             'label': 'Emperor', 'children': []},
            {'id': 22, 'url': 'http://local.host/api/0.2/entity/22',
             'label': 'King', 'children': []},
            {'id': 19, 'url': 'http://local.host/api/0.2/entity/19',
             'label': 'Pope', 'children': []}], 'Artifact': [
            {'id': 24, 'url': 'http://local.host/api/0.2/entity/24',
             'label': 'Coin', 'children': []},
            {'id': 25, 'url': 'http://local.host/api/0.2/entity/25',
             'label': 'Statue', 'children': []}], 'Bibliography': [
            {'id': 5, 'url': 'http://local.host/api/0.2/entity/5',
             'label': 'Article', 'children': []},
            {'id': 6, 'url': 'http://local.host/api/0.2/entity/6',
             'label': 'Book', 'children': []},
            {'id': 4, 'url': 'http://local.host/api/0.2/entity/4',
             'label': 'Inbook', 'children': []}], 'Edition': [
            {'id': 8, 'url': 'http://local.host/api/0.2/entity/8',
             'label': 'Charter Edition', 'children': []},
            {'id': 10, 'url': 'http://local.host/api/0.2/entity/10',
             'label': 'Chronicle Edition', 'children': []},
            {'id': 9, 'url': 'http://local.host/api/0.2/entity/9',
             'label': 'Letter Edition', 'children': []}], 'Event': [
            {'id': 35, 'url': 'http://local.host/api/0.2/entity/35',
             'label': 'Change of Property', 'children': [
                {'id': 36, 'url': 'http://local.host/api/0.2/entity/36',
                 'label': 'Donation', 'children': []},
                {'id': 38, 'url': 'http://local.host/api/0.2/entity/38',
                 'label': 'Exchange', 'children': []},
                {'id': 37, 'url': 'http://local.host/api/0.2/entity/37',
                 'label': 'Sale', 'children': []}]},
            {'id': 39, 'url': 'http://local.host/api/0.2/entity/39',
             'label': 'Conflict', 'children': [
                {'id': 40, 'url': 'http://local.host/api/0.2/entity/40',
                 'label': 'Battle', 'children': []},
                {'id': 41, 'url': 'http://local.host/api/0.2/entity/41',
                 'label': 'Raid', 'children': []}]}], 'External reference': [
            {'id': 12, 'url': 'http://local.host/api/0.2/entity/12',
             'label': 'Link', 'children': []}], 'External reference match': [
            {'id': 15, 'url': 'http://local.host/api/0.2/entity/15',
             'label': 'close match', 'children': []},
            {'id': 14, 'url': 'http://local.host/api/0.2/entity/14',
             'label': 'exact match', 'children': []}], 'Feature': [
            {'id': 75, 'url': 'http://local.host/api/0.2/entity/75',
             'label': 'Grave', 'children': []},
            {'id': 76, 'url': 'http://local.host/api/0.2/entity/76',
             'label': 'Pit', 'children': []}], 'Human remains': [
            {'id': 82, 'url': 'http://local.host/api/0.2/entity/82',
             'label': 'Lower Body', 'children': []},
            {'id': 81, 'url': 'http://local.host/api/0.2/entity/81',
             'label': 'Upper Body', 'children': []}], 'Involvement': [
            {'id': 27, 'url': 'http://local.host/api/0.2/entity/27',
             'label': 'Creator', 'children': []},
            {'id': 30, 'url': 'http://local.host/api/0.2/entity/30',
             'label': 'Offender', 'children': []},
            {'id': 28, 'url': 'http://local.host/api/0.2/entity/28',
             'label': 'Sponsor', 'children': []},
            {'id': 29, 'url': 'http://local.host/api/0.2/entity/29',
             'label': 'Victim', 'children': []}], 'License': [
            {'id': 49, 'url': 'http://local.host/api/0.2/entity/49',
             'label': 'Open license', 'children': [
                {'id': 52, 'url': 'http://local.host/api/0.2/entity/52',
                 'label': 'CC BY-SA 4.0', 'children': []},
                {'id': 51, 'url': 'http://local.host/api/0.2/entity/51',
                 'label': 'CC BY 4.0', 'children': []},
                {'id': 50, 'url': 'http://local.host/api/0.2/entity/50',
                 'label': 'Public domain', 'children': []}]},
            {'id': 48, 'url': 'http://local.host/api/0.2/entity/48',
             'label': 'Proprietary license', 'children': []}], 'Place': [
            {'id': 72, 'url': 'http://local.host/api/0.2/entity/72',
             'label': 'Boundary Mark', 'children': []},
            {'id': 69, 'url': 'http://local.host/api/0.2/entity/69',
             'label': 'Burial Site', 'children': []},
            {'id': 71, 'url': 'http://local.host/api/0.2/entity/71',
             'label': 'Economic Site', 'children': []},
            {'id': 70, 'url': 'http://local.host/api/0.2/entity/70',
             'label': 'Infrastructure', 'children': []},
            {'id': 67, 'url': 'http://local.host/api/0.2/entity/67',
             'label': 'Military Facility', 'children': []},
            {'id': 68, 'url': 'http://local.host/api/0.2/entity/68',
             'label': 'Ritual Site', 'children': []},
            {'id': 66, 'url': 'http://local.host/api/0.2/entity/66',
             'label': 'Settlement', 'children': []},
            {'id': 73, 'url': 'http://local.host/api/0.2/entity/73',
             'label': 'Topographical Entity', 'children': []}], 'Source': [
            {'id': 43, 'url': 'http://local.host/api/0.2/entity/43',
             'label': 'Charter', 'children': []},
            {'id': 46, 'url': 'http://local.host/api/0.2/entity/46',
             'label': 'Contract', 'children': []},
            {'id': 45, 'url': 'http://local.host/api/0.2/entity/45',
             'label': 'Letter', 'children': []},
            {'id': 44, 'url': 'http://local.host/api/0.2/entity/44',
             'label': 'Testament', 'children': []}], 'Stratigraphic unit': [
            {'id': 78, 'url': 'http://local.host/api/0.2/entity/78',
             'label': 'Burial', 'children': []},
            {'id': 79, 'url': 'http://local.host/api/0.2/entity/79',
             'label': 'Deposit', 'children': []}]}, 'places': {
        'Administrative unit': [
            {'id': 84, 'url': 'http://local.host/api/0.2/entity/84',
             'label': 'Austria', 'children': [
                {'id': 86, 'url': 'http://local.host/api/0.2/entity/86',
                 'label': 'Niederösterreich', 'children': []},
                {'id': 85, 'url': 'http://local.host/api/0.2/entity/85',
                 'label': 'Wien', 'children': []}]},
            {'id': 89, 'url': 'http://local.host/api/0.2/entity/89',
             'label': 'Czech Republic', 'children': []},
            {'id': 87, 'url': 'http://local.host/api/0.2/entity/87',
             'label': 'Germany', 'children': []},
            {'id': 88, 'url': 'http://local.host/api/0.2/entity/88',
             'label': 'Italy', 'children': []},
            {'id': 90, 'url': 'http://local.host/api/0.2/entity/90',
             'label': 'Slovakia', 'children': []},
            {'id': 91, 'url': 'http://local.host/api/0.2/entity/91',
             'label': 'Slovenia', 'children': []}], 'Historical place': [
            {'id': 93, 'url': 'http://local.host/api/0.2/entity/93',
             'label': 'Carantania', 'children': []},
            {'id': 95, 'url': 'http://local.host/api/0.2/entity/95',
             'label': 'Comitatus Iauntal', 'children': []},
            {'id': 96, 'url': 'http://local.host/api/0.2/entity/96',
             'label': 'Kingdom of Serbia', 'children': []},
            {'id': 94, 'url': 'http://local.host/api/0.2/entity/94',
             'label': 'Marcha Orientalis', 'children': []}]}, 'custom': {
        'Sex': [{'id': 32, 'url': 'http://local.host/api/0.2/entity/32',
                 'label': 'Female', 'children': []},
                {'id': 33, 'url': 'http://local.host/api/0.2/entity/33',
                 'label': 'Male', 'children': []}], 'Source translation': [
            {'id': 98, 'url': 'http://local.host/api/0.2/entity/98',
             'label': 'Original Text', 'children': []},
            {'id': 99, 'url': 'http://local.host/api/0.2/entity/99',
             'label': 'Translation', 'children': []},
            {'id': 100, 'url': 'http://local.host/api/0.2/entity/100',
             'label': 'Transliteration', 'children': []}]}, 'value': {
        'Dimensions': [
            {'id': 102, 'url': 'http://local.host/api/0.2/entity/102',
             'label': 'Height', 'children': []},
            {'id': 103, 'url': 'http://local.host/api/0.2/entity/103',
             'label': 'Weight', 'children': []}]}}]}
