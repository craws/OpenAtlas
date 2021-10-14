import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_params import test_ids

test_node_overview = {'types': [{
    'standard': {
        'Actor actor relation': [{
            'id': test_ids["economical_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["economical_id"]}',
            'label': 'Economical', 'children': [{
                'id': test_ids["provider_id"],
                'url': f'http://local.host/api/0.2/entity/{test_ids["provider_id"]}',
                'label': 'Provider of (Customer of)', 'children': []}]}, {
            'id': test_ids["kindredship_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["kindredship_id"]}',
            'label': 'Kindredship', 'children': [{
                'id': test_ids["parent_id"],
                'url': f'http://local.host/api/0.2/entity/{test_ids["parent_id"]}',
                'label': 'Parent of (Child of)', 'children': []}]}, {
            'id': test_ids["political_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["political_id"]}',
            'label': 'Political', 'children': [{
                'id': test_ids["ally_id"],
                'url': f'http://local.host/api/0.2/entity/{test_ids["ally_id"]}',
                'label': 'Ally of', 'children': []}, {
                'id': test_ids["leader_id"],
                'url': f'http://local.host/api/0.2/entity/{test_ids["leader_id"]}',
                'label': 'Leader of (Retinue of)', 'children': []}]}, {
            'id': test_ids["social_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
            'label': 'Social', 'children': [{
                'id': test_ids["enemy_id"],
                'url': f'http://local.host/api/0.2/entity/{test_ids["enemy_id"]}',
                'label': 'Enemy of', 'children': []}, {
                'id': test_ids["friend_id"],
                'url': f'http://local.host/api/0.2/entity/{test_ids["friend_id"]}',
                'label': 'Friend of', 'children': []}, {
                'id': test_ids["mentor_id"],
                'url': f'http://local.host/api/0.2/entity/ test_ids["mentor_id"]',
                'label': 'Mentor of (Student of)', 'children': []}]}],
        'Actor function': [{
            'id': test_ids["abbot_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["abbot_id"]}',
            'label': 'Abbot', 'children': []}, {
            'id': test_ids["bishop_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["bishop_id"]}',
            'label': 'Bishop', 'children': []}, {
            'id': test_ids["count_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["count_id"]}',
            'label': 'Count', 'children': []}, {
            'id': test_ids["emperor_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["emperor_id"]}',
            'label': 'Emperor', 'children': []}, {
            'id': test_ids["king_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["king_id"]}',
            'label': 'King', 'children': []}, {
            'id': test_ids["pope_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["pope_id"]}',
            'label': 'Pope', 'children': []}],
        'Artifact': [{
            'id': test_ids["coin_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["coin_id"]}',
            'label': 'Coin', 'children': []}, {
            'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Statue', 'children': []}],
        'Bibliography': [  {
            'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Article', 'children': []}, {
            'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Book', 'children': []},{
            'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Inbook', 'children': []}],
        'Edition': [  { # todo: return to work
            'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Charter Edition', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Chronicle Edition', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Letter Edition', 'children': []}], 'Event': [
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Change of Property', 'children': [
                {'id': test_ids["leader_id"],
                 'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
                 'label': 'Donation', 'children': []},
                {'id': test_ids["leader_id"],
                 'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
                 'label': 'Exchange', 'children': []},
                {'id': test_ids["leader_id"],
                 'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
                 'label': 'Sale', 'children': []}]},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Conflict', 'children': [
                {'id': test_ids["leader_id"],
                 'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
                 'label': 'Battle', 'children': []},
                {'id': test_ids["leader_id"],
                 'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
                 'label': 'Raid', 'children': []}]}], 'External reference': [
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Link', 'children': []}], 'External reference match': [
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'close match', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'exact match', 'children': []}], 'Feature': [
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Grave', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Pit', 'children': []}], 'Human remains': [
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Lower Body', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Upper Body', 'children': []}], 'Involvement': [
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Creator', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Offender', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Sponsor', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Victim', 'children': []}], 'License': [
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Open license', 'children': [
                {'id': test_ids["leader_id"],
                 'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
                 'label': 'CC BY-SA 4.0', 'children': []},
                {'id': test_ids["leader_id"],
                 'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
                 'label': 'CC BY 4.0', 'children': []},
                {'id': test_ids["leader_id"],
                 'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
                 'label': 'Public domain', 'children': []}]},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Proprietary license', 'children': []}], 'Place': [
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Boundary Mark', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Burial Site', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Economic Site', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Infrastructure', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Military Facility', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Ritual Site', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Settlement', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Topographical Entity', 'children': []}], 'Source': [
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Charter', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Contract', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Letter', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Testament', 'children': []}], 'Stratigraphic unit': [
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Burial', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Deposit', 'children': []}]}, 'places': {
        'Administrative unit': [
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Austria', 'children': [
                {'id': test_ids["leader_id"],
                 'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
                 'label': 'Niederösterreich', 'children': []},
                {'id': test_ids["leader_id"],
                 'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
                 'label': 'Wien', 'children': []}]},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Czech Republic', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Germany', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Italy', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Slovakia', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Slovenia', 'children': []}], 'Historical place': [
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Carantania', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Comitatus Iauntal', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Kingdom of Serbia', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Marcha Orientalis', 'children': []}]}, 'custom': {
        'Sex': [{'id': test_ids["leader_id"],
                 'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
                 'label': 'Female', 'children': []},
                {'id': test_ids["leader_id"],
                 'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
                 'label': 'Male', 'children': []}], 'Source translation': [
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Original Text', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
             'label': 'Translation', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}0',
             'label': 'Transliteration', 'children': []}]}, 'value': {
        'Dimensions': [
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}2',
             'label': 'Height', 'children': []},
            {'id': test_ids["leader_id"],
             'url': f'http://local.host/api/0.2/entity/{test_ids["leader_id"]}',
             'label': 'Weight', 'children': []}]}}]}
