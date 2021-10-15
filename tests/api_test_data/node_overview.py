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
            'id': test_ids["statue_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["statue_id"]}',
            'label': 'Statue', 'children': []}],
        'Bibliography': [{
            'id': test_ids["article_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["article_id"]}',
            'label': 'Article', 'children': []}, {
            'id': test_ids["book_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["book_id"]}',
            'label': 'Book', 'children': []}, {
            'id': test_ids["inbook_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["inbook_id"]}',
            'label': 'Inbook', 'children': []}],
        'Edition': [{
            'id': test_ids["charter_edition_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["charter_edition_id"]}',
            'label': 'Charter Edition', 'children': []}, {
            'id': test_ids["chronicle_edition_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["chronicle_edition_id"]}',
            'label': 'Chronicle Edition', 'children': []}, {
            'id': test_ids["letter_edition_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["letter_edition_id"]}',
            'label': 'Letter Edition', 'children': []}],
        'Event': [{
            'id': test_ids["change_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["change_id"]}',
            'label': 'Change of Property', 'children': [{
                'id': test_ids["donation_id"],
                'url': f'http://local.host/api/0.2/entity/{test_ids["donation_id"]}',
                'label': 'Donation', 'children': []}, {
                'id': test_ids["exchange_id"],
                'url': f'http://local.host/api/0.2/entity/{test_ids["exchange_id"]}',
                'label': 'Exchange', 'children': []}, {
                'id': test_ids["sale_id"],
                'url': f'http://local.host/api/0.2/entity/{test_ids["sale_id"]}',
                'label': 'Sale', 'children': []}]}, {
            'id': test_ids["conflict_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["conflict_id"]}',
            'label': 'Conflict', 'children': [{
                'id': test_ids["battle_id"],
                'url': f'http://local.host/api/0.2/entity/{test_ids["battle_id"]}',
                'label': 'Battle', 'children': []}, {
                'id': test_ids["raid_id"],
                'url': f'http://local.host/api/0.2/entity/{test_ids["raid_id"]}',
                'label': 'Raid', 'children': []}]}],
        'External reference': [{
            'id': test_ids["link_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["link_id"]}',
            'label': 'Link', 'children': []}],
        'External reference match': [{
            'id': test_ids["close_match_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["close_match_id"]}',
            'label': 'close match', 'children': []}, {
            'id': test_ids["exact_match_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["exact_match_id"]}',
            'label': 'exact match', 'children': []}],
        'Feature': [{
            'id': test_ids["grave_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["grave_id"]}',
            'label': 'Grave', 'children': []}, {
            'id': test_ids["pit_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["pit_id"]}',
            'label': 'Pit', 'children': []}],
        'Human remains': [{
            'id': test_ids["lower_body_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["lower_body_id"]}',
            'label': 'Lower Body', 'children': []}, {
            'id': test_ids["upper_body_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["upper_body_id"]}',
            'label': 'Upper Body', 'children': []}],
        'Involvement': [{
            'id': test_ids["creator_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["creator_id"]}',
            'label': 'Creator', 'children': []}, {
            'id': test_ids["offender_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["offender_id"]}',
            'label': 'Offender', 'children': []}, {
            'id': test_ids["sponsor_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["sponsor_id"]}',
            'label': 'Sponsor', 'children': []}, {
            'id': test_ids["victim_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["victim_id"]}',
            'label': 'Victim', 'children': []}],
        'License': [{
            'id': test_ids["open_license_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["open_license_id"]}',
            'label': 'Open license', 'children': [{
                'id': test_ids["cc_by_sa_id"],
                'url': f'http://local.host/api/0.2/entity/{test_ids["cc_by_sa_id"]}',
                'label': 'CC BY-SA 4.0', 'children': []}, {
                'id': test_ids["cc_by_id"],
                'url': f'http://local.host/api/0.2/entity/{test_ids["cc_by_id"]}',
                'label': 'CC BY 4.0', 'children': []}, {
                'id': test_ids["public_domain_id"],
                'url': f'http://local.host/api/0.2/entity/{test_ids["public_domain_id"]}',
                'label': 'Public domain', 'children': []}]}, {
            'id': test_ids["proprietary_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["proprietary_id"]}',
            'label': 'Proprietary license', 'children': []}],
        'Place': [{
            'id': test_ids["boundary_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["boundary_id"]}',
            'label': 'Boundary Mark', 'children': []}, {
            'id': test_ids["burial_site_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["burial_site_id"]}',
            'label': 'Burial Site', 'children': []}, {
            'id': test_ids["economic_site_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["economic_site_id"]}',
            'label': 'Economic Site', 'children': []}, {
            'id': test_ids["infrastructure_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["infrastructure_id"]}',
            'label': 'Infrastructure', 'children': []}, {
            'id': test_ids["military_facility_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["military_facility_id"]}',
            'label': 'Military Facility', 'children': []}, {
            'id': test_ids["ritual_site_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["ritual_site_id"]}',
            'label': 'Ritual Site', 'children': []}, {
            'id': test_ids["settlement_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["settlement_id"]}',
            'label': 'Settlement', 'children': []}, {
            'id': test_ids["topographical_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["topographical_id"]}',
            'label': 'Topographical Entity', 'children': []}],
        'Source': [{
            'id': test_ids["charter_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["charter_id"]}',
            'label': 'Charter', 'children': []}, {
            'id': test_ids["contract_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["contract_id"]}',
            'label': 'Contract', 'children': []}, {
            'id': test_ids["letter_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["letter_id"]}',
            'label': 'Letter', 'children': []}, {
            'id': test_ids["testament_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["testament_id"]}',
            'label': 'Testament', 'children': []}],
        'Stratigraphic unit': [{
            'id': test_ids["burial_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["burial_id"]}',
            'label': 'Burial', 'children': []}, {
            'id': test_ids["deposit_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["deposit_id"]}',
            'label': 'Deposit', 'children': []}]}, 'places': {
        'Administrative unit': [{
            'id': test_ids["austria_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["austria_id"]}',
            'label': 'Austria', 'children': [{
                'id': test_ids["nieder_id"],
                'url': f'http://local.host/api/0.2/entity/{test_ids["nieder_id"]}',
                'label': 'Niederösterreich', 'children': []}, {
                'id': test_ids["wien_id"],
                'url': f'http://local.host/api/0.2/entity/{test_ids["wien_id"]}',
                'label': 'Wien', 'children': []}]}, {
            'id': test_ids["germany_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["germany_id"]}',
            'label': 'Czech Republic', 'children': []}, {
            'id': test_ids["leader_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["social_id"]}',
            'label': 'Germany', 'children': []}, {
            'id': test_ids["italy_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["italy_id"]}',
            'label': 'Italy', 'children': []}, {
            'id': test_ids["slovakia_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["slovakia_id"]}',
            'label': 'Slovakia', 'children': []}, {
            'id': test_ids["slovenia_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["slovenia_id"]}',
            'label': 'Slovenia', 'children': []}],
        'Historical place': [{
            'id': test_ids["carantinia_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["carantinia_id"]}',
            'label': 'Carantania', 'children': []}, {
            'id': test_ids["comitatus_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["comitatus_id"]}',
            'label': 'Comitatus Iauntal', 'children': []}, {
            'id': test_ids["serbia_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["serbia_id"]}',
            'label': 'Kingdom of Serbia', 'children': []}, {
            'id': test_ids["marcha_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["marcha_id"]}',
            'label': 'Marcha Orientalis', 'children': []}]},
    'custom': {
        'Sex': [{
            'id': test_ids["female_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["female_id"]}',
            'label': 'Female', 'children': []}, {
            'id': test_ids["male_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["male_id"]}',
            'label': 'Male', 'children': []}],
        'Source translation': [{
            'id': test_ids["original_text_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["original_text_id"]}',
            'label': 'Original Text', 'children': []}, {
            'id': test_ids["translation_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["translation_id"]}',
            'label': 'Translation', 'children': []}, {
            'id': test_ids["transliteration_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["transliteration_id"]}0',
            'label': 'Transliteration', 'children': []}]},
    'value': {
        'Dimensions': [{
            'id': test_ids["height_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["height_id"]}2',
            'label': 'Height', 'children': []}, {
            'id': test_ids["weight_id"],
            'url': f'http://local.host/api/0.2/entity/{test_ids["weight_id"]}',
            'label': 'Weight', 'children': []}]}}]}
