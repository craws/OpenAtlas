class NodeOverview:
    @staticmethod
    def get_test_node_overview(params):
        return {'types': [{
            'standard': {
                'Actor actor relation': [{
                    'id': params["economical_id"],
                    'url': f'http://local.host/api/entity/{params["economical_id"]}',
                    'label': 'Economical', 'children': [{
                        'id': params["provider_of_(customer_of)_id"],
                        'url': f'http://local.host/api/entity/{params["provider_of_(customer_of)_id"]}',
                        'label': 'Provider of (Customer of)', 'children': []}]},
                    {
                        'id': params["kindredship_id"],
                        'url': f'http://local.host/api/entity/{params["kindredship_id"]}',
                        'label': 'Kindredship', 'children': [{
                        'id': params["parent_of_(child_of)_id"],
                        'url': f'http://local.host/api/entity/{params["parent_of_(child_of)_id"]}',
                        'label': 'Parent of (Child of)', 'children': []}]}, {
                        'id': params["political_id"],
                        'url': f'http://local.host/api/entity/{params["political_id"]}',
                        'label': 'Political', 'children': [{
                            'id': params["ally_of_id"],
                            'url': f'http://local.host/api/entity/{params["ally_of_id"]}',
                            'label': 'Ally of', 'children': []}, {
                            'id': params["leader_of_(retinue_of)_id"],
                            'url': f'http://local.host/api/entity/{params["leader_of_(retinue_of)_id"]}',
                            'label': 'Leader of (Retinue of)',
                            'children': []}]}, {
                        'id': params["social_id"],
                        'url': f'http://local.host/api/entity/{params["social_id"]}',
                        'label': 'Social', 'children': [{
                            'id': params["enemy_of_id"],
                            'url': f'http://local.host/api/entity/{params["enemy_of_id"]}',
                            'label': 'Enemy of', 'children': []}, {
                            'id': params["friend_of_id"],
                            'url': f'http://local.host/api/entity/{params["friend_of_id"]}',
                            'label': 'Friend of', 'children': []}, {
                            'id': params["mentor_of_(student_of)_id"],
                            'url': f'http://local.host/api/entity/{params["mentor_of_(student_of)_id"]}',
                            'label': 'Mentor of (Student of)',
                            'children': []}]}],
                'Actor function': [{
                    'id': params["abbot_id"],
                    'url': f'http://local.host/api/entity/{params["abbot_id"]}',
                    'label': 'Abbot', 'children': []}, {
                    'id': params["bishop_id"],
                    'url': f'http://local.host/api/entity/{params["bishop_id"]}',
                    'label': 'Bishop', 'children': []}, {
                    'id': params["count_id"],
                    'url': f'http://local.host/api/entity/{params["count_id"]}',
                    'label': 'Count', 'children': []}, {
                    'id': params["emperor_id"],
                    'url': f'http://local.host/api/entity/{params["emperor_id"]}',
                    'label': 'Emperor', 'children': []}, {
                    'id': params["king_id"],
                    'url': f'http://local.host/api/entity/{params["king_id"]}',
                    'label': 'King', 'children': []}, {
                    'id': params["pope_id"],
                    'url': f'http://local.host/api/entity/{params["pope_id"]}',
                    'label': 'Pope', 'children': []}],
                'Artifact': [{
                    'id': params["coin_id"],
                    'url': f'http://local.host/api/entity/{params["coin_id"]}',
                    'label': 'Coin', 'children': []}, {
                    'id': params["statue_id"],
                    'url': f'http://local.host/api/entity/{params["statue_id"]}',
                    'label': 'Statue', 'children': []}],
                'Bibliography': [{
                    'id': params["article_id"],
                    'url': f'http://local.host/api/entity/{params["article_id"]}',
                    'label': 'Article', 'children': []}, {
                    'id': params["book_id"],
                    'url': f'http://local.host/api/entity/{params["book_id"]}',
                    'label': 'Book', 'children': []}, {
                    'id': params["inbook_id"],
                    'url': f'http://local.host/api/entity/{params["inbook_id"]}',
                    'label': 'Inbook', 'children': []}],
                'Edition': [{
                    'id': params["charter_edition_id"],
                    'url': f'http://local.host/api/entity/{params["charter_edition_id"]}',
                    'label': 'Charter Edition', 'children': []}, {
                    'id': params["chronicle_edition_id"],
                    'url': f'http://local.host/api/entity/{params["chronicle_edition_id"]}',
                    'label': 'Chronicle Edition', 'children': []}, {
                    'id': params["letter_edition_id"],
                    'url': f'http://local.host/api/entity/{params["letter_edition_id"]}',
                    'label': 'Letter Edition', 'children': []}],
                'Event': [{
                    'id': params["change_of_property_id"],
                    'url': f'http://local.host/api/entity/{params["change_of_property_id"]}',
                    'label': 'Change of Property', 'children': [{
                        'id': params["donation_id"],
                        'url': f'http://local.host/api/entity/{params["donation_id"]}',
                        'label': 'Donation', 'children': []}, {
                        'id': params["exchange_id"],
                        'url': f'http://local.host/api/entity/{params["exchange_id"]}',
                        'label': 'Exchange', 'children': []}, {
                        'id': params["sale_id"],
                        'url': f'http://local.host/api/entity/{params["sale_id"]}',
                        'label': 'Sale', 'children': []}]}, {
                    'id': params["conflict_id"],
                    'url': f'http://local.host/api/entity/{params["conflict_id"]}',
                    'label': 'Conflict', 'children': [{
                        'id': params["battle_id"],
                        'url': f'http://local.host/api/entity/{params["battle_id"]}',
                        'label': 'Battle', 'children': []}, {
                        'id': params["raid_id"],
                        'url': f'http://local.host/api/entity/{params["raid_id"]}',
                        'label': 'Raid', 'children': []}]}],
                'External reference': [{
                    'id': params["link_id"],
                    'url': f'http://local.host/api/entity/{params["link_id"]}',
                    'label': 'Link', 'children': []}],
                'Feature': [{
                    'id': params["grave_id"],
                    'url': f'http://local.host/api/entity/{params["grave_id"]}',
                    'label': 'Grave', 'children': []}, {
                    'id': params["pit_id"],
                    'url': f'http://local.host/api/entity/{params["pit_id"]}',
                    'label': 'Pit', 'children': []}],
                'Human remains': [{
                    'id': params["lower_body_id"],
                    'url': f'http://local.host/api/entity/{params["lower_body_id"]}',
                    'label': 'Lower Body', 'children': []}, {
                    'id': params["upper_body_id"],
                    'url': f'http://local.host/api/entity/{params["upper_body_id"]}',
                    'label': 'Upper Body', 'children': []}],
                'Involvement': [{
                    'id': params["creator_id"],
                    'url': f'http://local.host/api/entity/{params["creator_id"]}',
                    'label': 'Creator', 'children': []}, {
                    'id': params["offender_id"],
                    'url': f'http://local.host/api/entity/{params["offender_id"]}',
                    'label': 'Offender', 'children': []}, {
                    'id': params["sponsor_id"],
                    'url': f'http://local.host/api/entity/{params["sponsor_id"]}',
                    'label': 'Sponsor', 'children': []}, {
                    'id': params["victim_id"],
                    'url': f'http://local.host/api/entity/{params["victim_id"]}',
                    'label': 'Victim', 'children': []}],
                'License': [{
                    'id': params["open_license_id"],
                    'url': f'http://local.host/api/entity/{params["open_license_id"]}',
                    'label': 'Open license', 'children': [{
                        'id': params["cc_by-sa_4.0_id"],
                        'url': f'http://local.host/api/entity/{params["cc_by-sa_4.0_id"]}',
                        'label': 'CC BY-SA 4.0', 'children': []}, {
                        'id': params["cc_by_4.0_id"],
                        'url': f'http://local.host/api/entity/{params["cc_by_4.0_id"]}',
                        'label': 'CC BY 4.0', 'children': []}, {
                        'id': params["public_domain_id"],
                        'url': f'http://local.host/api/entity/{params["public_domain_id"]}',
                        'label': 'Public domain', 'children': []}]}, {
                    'id': params["proprietary_license_id"],
                    'url': f'http://local.host/api/entity/{params["proprietary_license_id"]}',
                    'label': 'Proprietary license', 'children': []}],
                'Place': [{
                    'id': params["boundary_mark_id"],
                    'url': f'http://local.host/api/entity/{params["boundary_mark_id"]}',
                    'label': 'Boundary Mark', 'children': []}, {
                    'id': params["burial_site_id"],
                    'url': f'http://local.host/api/entity/{params["burial_site_id"]}',
                    'label': 'Burial Site', 'children': []}, {
                    'id': params["economic_site_id"],
                    'url': f'http://local.host/api/entity/{params["economic_site_id"]}',
                    'label': 'Economic Site', 'children': []}, {
                    'id': params["infrastructure_id"],
                    'url': f'http://local.host/api/entity/{params["infrastructure_id"]}',
                    'label': 'Infrastructure', 'children': []}, {
                    'id': params["military_facility_id"],
                    'url': f'http://local.host/api/entity/{params["military_facility_id"]}',
                    'label': 'Military Facility', 'children': []}, {
                    'id': params["ritual_site_id"],
                    'url': f'http://local.host/api/entity/{params["ritual_site_id"]}',
                    'label': 'Ritual Site', 'children': []}, {
                    'id': params["settlement_id"],
                    'url': f'http://local.host/api/entity/{params["settlement_id"]}',
                    'label': 'Settlement', 'children': []}, {
                    'id': params["topographical_entity_id"],
                    'url': f'http://local.host/api/entity/{params["topographical_entity_id"]}',
                    'label': 'Topographical Entity', 'children': []}],
                'Source': [{
                    'id': params["charter_id"],
                    'url': f'http://local.host/api/entity/{params["charter_id"]}',
                    'label': 'Charter', 'children': []}, {
                    'id': params["contract_id"],
                    'url': f'http://local.host/api/entity/{params["contract_id"]}',
                    'label': 'Contract', 'children': []}, {
                    'id': params["letter_id"],
                    'url': f'http://local.host/api/entity/{params["letter_id"]}',
                    'label': 'Letter', 'children': []}, {
                    'id': params["testament_id"],
                    'url': f'http://local.host/api/entity/{params["testament_id"]}',
                    'label': 'Testament', 'children': []}],
                'Source translation': [{
                    'id': params["original_text_id"],
                    'url': f'http://local.host/api/entity/{params["original_text_id"]}',
                    'label': 'Original Text', 'children': []}, {
                    'id': params["translation_id"],
                    'url': f'http://local.host/api/entity/{params["translation_id"]}',
                    'label': 'Translation', 'children': []}, {
                    'id': params["transliteration_id"],
                    'url': f'http://local.host/api/entity/{params["transliteration_id"]}',
                    'label': 'Transliteration', 'children': []}],
                'Stratigraphic unit': [{
                    'id': params["burial_id"],
                    'url': f'http://local.host/api/entity/{params["burial_id"]}',
                    'label': 'Burial', 'children': []}, {
                    'id': params["deposit_id"],
                    'url': f'http://local.host/api/entity/{params["deposit_id"]}',
                    'label': 'Deposit', 'children': []}]},
            'place': {
                'Administrative unit': [{
                    'id': params["austria_id"],
                    'url': f'http://local.host/api/entity/{params["austria_id"]}',
                    'label': 'Austria', 'children': [{
                        'id': params["niederösterreich_id"],
                        'url': f'http://local.host/api/entity/{params["niederösterreich_id"]}',
                        'label': 'Niederösterreich', 'children': []}, {
                        'id': params["wien_id"],
                        'url': f'http://local.host/api/entity/{params["wien_id"]}',
                        'label': 'Wien', 'children': []}]}, {
                    'id': params["czech_republic_id"],
                    'url': f'http://local.host/api/entity/{params["czech_republic_id"]}',
                    'label': 'Czech Republic', 'children': []}, {
                    'id': params["germany_id"],
                    'url': f'http://local.host/api/entity/{params["germany_id"]}',
                    'label': 'Germany', 'children': []}, {
                    'id': params["italy_id"],
                    'url': f'http://local.host/api/entity/{params["italy_id"]}',
                    'label': 'Italy', 'children': []}, {
                    'id': params["slovakia_id"],
                    'url': f'http://local.host/api/entity/{params["slovakia_id"]}',
                    'label': 'Slovakia', 'children': []}, {
                    'id': params["slovenia_id"],
                    'url': f'http://local.host/api/entity/{params["slovenia_id"]}',
                    'label': 'Slovenia', 'children': []}],
                'Historical place': [{
                    'id': params["carantania_id"],
                    'url': f'http://local.host/api/entity/{params["carantania_id"]}',
                    'label': 'Carantania', 'children': []}, {
                    'id': params["comitatus_iauntal_id"],
                    'url': f'http://local.host/api/entity/{params["comitatus_iauntal_id"]}',
                    'label': 'Comitatus Iauntal', 'children': []}, {
                    'id': params["kingdom_of_serbia_id"],
                    'url': f'http://local.host/api/entity/{params["kingdom_of_serbia_id"]}',
                    'label': 'Kingdom of Serbia', 'children': []}, {
                    'id': params["marcha_orientalis_id"],
                    'url': f'http://local.host/api/entity/{params["marcha_orientalis_id"]}',
                    'label': 'Marcha Orientalis', 'children': []}]},
            'custom': {
                'Sex': [{
                    'id': params["female_id"],
                    'url': f'http://local.host/api/entity/{params["female_id"]}',
                    'label': 'Female', 'children': []}, {
                    'id': params["male_id"],
                    'url': f'http://local.host/api/entity/{params["male_id"]}',
                    'label': 'Male', 'children': []}]},
            'system': {'External reference match': [{
                'children': [],
                'id': params["close_match_id"],
                'label': 'close match',
                'url': f'http://local.host/api/entity/{params["close_match_id"]}'},
                {'children': [],
                 'id': params["exact_match_id"],
                 'label': 'exact match',
                 'url': f'http://local.host/api/entity/{params["exact_match_id"]}'}]},
            'value': {
                'Dimensions': [{
                    'id': params["height_id"],
                    'url': f'http://local.host/api/entity/{params["height_id"]}',
                    'label': 'Height', 'children': []}, {
                    'id': params["weight_id"],
                    'url': f'http://local.host/api/entity/{params["weight_id"]}',
                    'label': 'Weight', 'children': []}]}}]}
