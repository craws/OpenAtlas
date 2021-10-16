import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_params import test_ids

test_type_tree = {'typeTree': [{
    f'{test_ids["abbot_id"]}': {
        'id': test_ids["abbot_id"], 'name': 'Abbot', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_function_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["actor_r_id"]}': {
        'id': test_ids["actor_r_id"], 'name': 'Actor actor relation',
        'description': 'Categories for the relationship between two actors. This may be a mutual relationship (e.g. actor A is friend of actor B and vice versa), or a directional relationship (e.g. actor A is the child of actor B, while actor B is the parent of actor A).',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [test_ids["economical_id"], test_ids["kindredship_id"],
                 test_ids["political_id"], test_ids["social_id"]],
        'count': 0, 'count_subs': 1,
        'locked': False, 'standard': True}}, {
    f'{test_ids["actor_function_id"]}': {
        'id': test_ids["actor_function_id"], 'name': 'Actor function',
        'description': 'Definitions of an actor\'s function within a group. An actor can for example be member of a group and this membership is defined by a certain function during a certain period of time. E.g. actor "Charlemagne" is member of the group "Frankish Reign" from 768 to 814 in the function of "King" and he is member of the group "Roman Empire" from 800 to 814 in the function "Emperor".',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [test_ids["abbot_id"], test_ids["bishop_id"],
                 test_ids["count_id"], test_ids["emperor_id"],
                 test_ids["king_id"], test_ids["pope_id"]],
        'count': 0, 'count_subs': 0,
        'locked': False, 'standard': True}}, {
    f'{test_ids["ally_id"]}': {
        'id': test_ids["ally_id"], 'name': 'Ally of', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["political_id"], test_ids["actor_r_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["article_id"]}': {
        'id': test_ids["article_id"], 'name': 'Article', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["bibliography_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["artifact_id"]}': {
        'id': test_ids["artifact_id"], 'name': 'Artifact', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [test_ids["coin_id"], test_ids["statue_id"]], 'count': 0,
        'count_subs': 0,
        'locked': False,
        'standard': True}}, {
    f'{test_ids["battle_id"]}': {
        'id': test_ids["battle_id"], 'name': 'Battle', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["conflict_id"], test_ids["event_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["bibliography_id"]}': {
        'id': test_ids["bibliography_id"], 'name': 'Bibliography',
        'description': 'Categories for bibliographical entries as used for example in BibTeX, e.g. Book, Inbook, Article etc.',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [test_ids["article_id"], test_ids["book_id"],
                 test_ids["inbook_id"]], 'count': 0,
        'count_subs': 0, 'locked': False,
        'standard': True}}, {
    f'{test_ids["bishop_id"]}': {
        'id': test_ids["bishop_id"], 'name': 'Bishop', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_function_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["book_id"]}': {
        'id': test_ids["book_id"], 'name': 'Book', 'description': None,
        'origin_id': None,
        'first': None, 'last': None, 'root': [test_ids["bibliography_id"]],
        'subs': [],
        'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    f'{test_ids["boundary_id"]}': {
        'id': test_ids["boundary_id"], 'name': 'Boundary Mark',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["place_id"]],
        'subs': [], 'count': 1, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["burial_id"]}': {
        'id': test_ids["burial_id"], 'name': 'Burial', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["stratigraphic_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["burial_site_id"]}': {
        'id': test_ids["burial_site_id"], 'name': 'Burial Site',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["place_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["cc_by_sa_id"]}': {
        'id': test_ids["cc_by_sa_id"],
        'name': 'CC BY-SA 4.0', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["open_license_id"], test_ids["license_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["cc_by_id"]}': {
        'id': test_ids["cc_by_id"], 'name': 'CC BY 4.0',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["open_license_id"], test_ids["license_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["change_id"]}': {
        'id': test_ids["change_id"], 'name': 'Change of Property',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["event_id"]],
        'subs': [test_ids["donation_id"], test_ids["exchange_id"],
                 test_ids["sale_id"]], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    f'{test_ids["charter_id"]}': {
        'id': test_ids["charter_id"], 'name': 'Charter', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["source_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["charter_edition_id"]}': {
        'id': test_ids["charter_edition_id"], 'name': 'Charter Edition',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["edition_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["chronicle_edition_id"]}': {
        'id': test_ids["chronicle_edition_id"], 'name': 'Chronicle Edition',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["edition_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["close_match_id"]}': {
        'id': test_ids["close_match_id"], 'name': 'close match',
        'description': 'Concepts are sufficiently similar that they can be used interchangeably in some information retrieval applications.',
        'origin_id': None, 'first': None,
        'last': None, 'root': [test_ids["external_match_id"]],
        'subs': [], 'count': 1,
        'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["coin_id"]}': {
        'id': test_ids["coin_id"], 'name': 'Coin', 'description': None,
        'origin_id': None,
        'first': None, 'last': None, 'root': [test_ids["artifact_id"]],
        'subs': [],
        'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["conflict_id"]}': {
        'id': test_ids["conflict_id"], 'name': 'Conflict', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["event_id"]],
        'subs': [test_ids["battle_id"], test_ids["raid_id"]], 'count': 0,
        'count_subs': 0,
        'locked': False,
        'standard': False}}, {
    f'{test_ids["contract_id"]}': {
        'id': test_ids["contract_id"], 'name': 'Contract', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["source_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["count_id"]}': {
        'id': test_ids["count_id"], 'name': 'Count', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_function_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["creator_id"]}': {
        'id': test_ids["creator_id"], 'name': 'Creator', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["involvement_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["deposit_id"]}': {
        'id': test_ids["deposit_id"], 'name': 'Deposit', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["stratigraphic_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["dimensions_id"]}': {
        'id': test_ids["dimensions_id"], 'name': 'Dimensions',
        'description': 'Physical dimensions like weight and height.',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [test_ids["height_id"], test_ids["weight_id"]], 'count': 0,
        'count_subs': 1, 'locked': False,
        'standard': False}}, {
    f'{test_ids["donation_id"]}': {
        'id': test_ids["donation_id"], 'name': 'Donation', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["change_id"], test_ids["event_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["economic_site_id"]}': {
        'id': test_ids["economic_site_id"], 'name': 'Economic Site',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["place_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["economical_id"]}': {
        'id': test_ids["economical_id"], 'name': 'Economical',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_r_id"]],
        'subs': [test_ids["provider_id"]], 'count': 1, 'count_subs': 0,
        'locked': False,
        'standard': False}}, {
    f'{test_ids["edition_id"]}': {
        'id': test_ids["edition_id"], 'name': 'Edition',
        'description': "Categories for the classification of written sources' editions like charter editions, chronicle edition etc.",
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [test_ids["charter_edition_id"],
                 test_ids["chronicle_edition_id"],
                 test_ids["letter_edition_id"]], 'count': 0,
        'count_subs': 0, 'locked': False,
        'standard': True}}, {
    f'{test_ids["emperor_id"]}': {
        'id': test_ids["emperor_id"], 'name': 'Emperor', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_function_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["enemy_id"]}': {
        'id': test_ids["enemy_id"], 'name': 'Enemy of', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["social_id"], test_ids["actor_r_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["event_id"]}': {
        'id': test_ids["event_id"], 'name': 'Event',
        'description': 'Categories for the type of events like Change of property, Conflict, Movement, Attendance etc.',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [test_ids["change_id"], test_ids["conflict_id"]], 'count': 0,
        'count_subs': 0, 'locked': False,
        'standard': True}}, {
    f'{test_ids["exact_match_id"]}': {
        'id': test_ids["exact_match_id"], 'name': 'exact match',
        'description': 'High degree of confidence that the concepts can be used interchangeably.',
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["external_match_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["exchange_id"]}': {
        'id': test_ids["exchange_id"], 'name': 'Exchange', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["change_id"], test_ids["event_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["external_reference_id"]}': {
        'id': test_ids["external_reference_id"], 'name': 'External reference',
        'description': 'Categories for the classification of external references like a link to Wikipedia',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [test_ids["link_id"]], 'count': 0, 'count_subs': 0,
        'locked': False,
        'standard': True}}, {
    f'{test_ids["external_match_id"]}': {
        'id': test_ids["external_match_id"], 'name': 'External reference match',
        'description': 'SKOS based definition of the confidence degree that concepts can be used interchangeable.',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [test_ids["close_match_id"], test_ids["exact_match_id"]],
        'count': 0, 'count_subs': 1, 'locked': True,
        'standard': True}}, {
    f'{test_ids["feature_id"]}': {
        'id': test_ids["feature_id"], 'name': 'Feature',
        'description': 'Classification of the archaeological feature e.g. grave, pit, ...',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [test_ids["grave_id"], test_ids["pit_id"]], 'count': 0,
        'count_subs': 0, 'locked': False,
        'standard': True}}, {
    f'{test_ids["female_id"]}': {
        'id': test_ids["female_id"], 'name': 'Female', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["sex_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["friend_id"]}': {
        'id': test_ids["friend_id"], 'name': 'Friend of', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["social_id"], test_ids["actor_r_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["grave_id"]}': {
        'id': test_ids["grave_id"], 'name': 'Grave', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["feature_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["height_id"]}': {
        'id': test_ids["height_id"], 'name': 'Height',
        'description': 'centimeter',
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["dimensions_id"]],
        'subs': [], 'count': 1, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["human_remains_id"]}': {
        'id': test_ids["human_remains_id"], 'name': 'Human remains',
        'description': 'Human remains, that for example were discovered during archaeological excavations. They are associated with a stratigraphic unit (in most cases a skeleton) that is composed of (P46) one or multiple parts (in most cases bones) that are classified as biological objects (E20). From a hierarchical point of view the human remains are one level below the stratigraphic unit respectively the entity whose sum of parts resembles the individual/skeleton. This way individual bones or body parts can be treated individually and be connected with separate classifications (e.g. Injuries of the right upper arm or caries on a certain tooth).',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [test_ids["lower_body_id"], test_ids["upper_body_id"]],
        'count': 0,
        'count_subs': 0, 'locked': False,
        'standard': True}}, {
    f'{test_ids["inbook_id"]}': {
        'id': test_ids["inbook_id"], 'name': 'Inbook', 'description': None,
        'origin_id': None,
        'first': None, 'last': None, 'root': [test_ids["bibliography_id"]],
        'subs': [],
        'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    f'{test_ids["infrastructure_id"]}': {
        'id': test_ids["infrastructure_id"], 'name': 'Infrastructure',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["place_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["involvement_id"]}': {
        'id': test_ids["involvement_id"], 'name': 'Involvement',
        'description': 'Categories to define the involvement of an actor within an event. E.g. "Napoleon" participated in the event "Invasion of Russia" as "Commander" or "Michelangelo" performed the event "painting of the Sistine chapel" as "Artist".',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [test_ids["creator_id"], test_ids["offender_id"],
                 test_ids["sponsor_id"], test_ids["victim_id"]],
        'count': 0, 'count_subs': 0,
        'locked': False, 'standard': True}}, {
    f'{test_ids["kindredship_id"]}': {
        'id': test_ids["kindredship_id"], 'name': 'Kindredship',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_r_id"]],
        'subs': [test_ids["parent_id"]], 'count': 0, 'count_subs': 0,
        'locked': False,
        'standard': False}}, {
    f'{test_ids["king_id"]}': {
        'id': test_ids["king_id"], 'name': 'King', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_function_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["leader_id"]}': {
        'id': test_ids["leader_id"], 'name': 'Leader of (Retinue of)',
        'description': None, 'origin_id': None, 'first': None,
        'last': None,
        'root': [test_ids["political_id"], test_ids["actor_r_id"]], 'subs': [],
        'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    f'{test_ids["letter_id"]}': {
        'id': test_ids["letter_id"], 'name': 'Letter', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["source_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["letter_edition_id"]}': {
        'id': test_ids["letter_edition_id"], 'name': 'Letter Edition',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["edition_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["license_id"]}': {
        'id': test_ids["license_id"], 'name': 'License',
        'description': 'Types for the licensing of a file',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [test_ids["open_license_id"], test_ids["proprietary_id"]],
        'count': 0,
        'count_subs': 1, 'locked': False,
        'standard': True}}, {
    f'{test_ids["link_id"]}': {
        'id': test_ids["link_id"], 'name': 'Link', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["external_reference_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["lower_body_id"]}': {
        'id': test_ids["lower_body_id"], 'name': 'Lower Body',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["human_remains_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["male_id"]}': {
        'id': test_ids["male_id"], 'name': 'Male', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["sex_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["mentor_id"]}': {
        'id': test_ids["mentor_id"], 'name': 'Mentor of (Student of)',
        'description': None, 'origin_id': None, 'first': None,
        'last': None, 'root': [test_ids["social_id"], test_ids["actor_r_id"]],
        'subs': [],
        'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    f'{test_ids["military_facility_id"]}': {
        'id': test_ids["military_facility_id"], 'name': 'Military Facility',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["place_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["offender_id"]}': {
        'id': test_ids["offender_id"], 'name': 'Offender', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["involvement_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["open_license_id"]}': {
        'id': test_ids["open_license_id"], 'name': 'Open license',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["license_id"]],
        'subs': [test_ids["cc_by_sa_id"], test_ids["cc_by_id"],
                 test_ids["public_domain_id"]], 'count': 1,
        'count_subs': 0,
        'locked': False, 'standard': False}}, {
    f'{test_ids["original_text_id"]}': {
        'id': test_ids["original_text_id"], 'name': 'Original Text',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["source_translation_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["parent_id"]}': {
        'id': test_ids["parent_id"], 'name': 'Parent of (Child of)',
        'description': None, 'origin_id': None, 'first': None,
        'last': None,
        'root': [test_ids["kindredship_id"], test_ids["actor_r_id"]],
        'subs': [],
        'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    f'{test_ids["pit_id"]}': {
        'id': test_ids["pit_id"], 'name': 'Pit', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["feature_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["place_id"]}': {
        'id': test_ids["place_id"], 'name': 'Place',
        'description': 'Types for non-moveable entities (i.e. places) with a certain extent and/or location like Settlement, Burial site, Ritual site, Fortification etc.',
        'origin_id': None,
        'first': None, 'last': None,
        'root': [],
        'subs': [test_ids["boundary_id"], test_ids["burial_site_id"],
                 test_ids["economic_site_id"], test_ids["infrastructure_id"],
                 test_ids["military_facility_id"],
                 test_ids["ritual_site_id"],
                 test_ids["settlement_id"], test_ids["topographical_id"]],
        'count': 1,
        'count_subs': 1,
        'locked': False,
        'standard': True}}, {
    f'{test_ids["political_id"]}': {
        'id': test_ids["political_id"], 'name': 'Political',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_r_id"]],
        'subs': [test_ids["ally_id"], test_ids["leader_id"]], 'count': 0,
        'count_subs': 0,
        'locked': False, 'standard': False}}, {
    f'{test_ids["pope_id"]}': {
        'id': test_ids["pope_id"], 'name': 'Pope', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_function_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["proprietary_id"]}': {
        'id': test_ids["proprietary_id"], 'name': 'Proprietary license',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["license_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["provider_id"]}': {
        'id': test_ids["provider_id"], 'name': 'Provider of (Customer of)',
        'description': None, 'origin_id': None, 'first': None,
        'last': None,
        'root': [test_ids["economical_id"], test_ids["actor_r_id"]], 'subs': [],
        'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    f'{test_ids["public_domain_id"]}': {
        'id': test_ids["public_domain_id"], 'name': 'Public domain',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["open_license_id"], test_ids["license_id"]],
        'subs': [], 'count': 0,
        'count_subs': 0,
        'locked': False, 'standard': False}}, {
    f'{test_ids["raid_id"]}': {
        'id': test_ids["raid_id"], 'name': 'Raid', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["conflict_id"], test_ids["event_id"]], 'subs': [],
        'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    f'{test_ids["ritual_site_id"]}': {
        'id': test_ids["ritual_site_id"], 'name': 'Ritual Site',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["place_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["sale_id"]}': {
        'id': test_ids["sale_id"], 'name': 'Sale', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["change_id"], test_ids["event_id"]], 'subs': [],
        'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    f'{test_ids["settlement_id"]}': {
        'id': test_ids["settlement_id"], 'name': 'Settlement',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["place_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["sex_id"]}': {
        'id': test_ids["sex_id"], 'name': 'Sex',
        'description': 'Categories for sex like female, male.',
        'origin_id': None,
        'first': None, 'last': None,
        'root': [], 'subs': [test_ids["female_id"], test_ids["male_id"]],
        'count': 0, 'count_subs': 0,
        'locked': False,
        'standard': False}}, {
    f'{test_ids["social_id"]}': {
        'id': test_ids["social_id"], 'name': 'Social', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_r_id"]],
        'subs': [test_ids["enemy_id"], test_ids["friend_id"],
                 test_ids["mentor_id"]], 'count': 0,
        'count_subs': 0,
        'locked': False, 'standard': False}}, {
    f'{test_ids["source_id"]}': {
        'id': test_ids["source_id"], 'name': 'Source',
        'description': 'Types for historical sources like charter, chronicle, letter etc.',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [test_ids["charter_id"], test_ids["contract_id"],
                 test_ids["letter_id"], test_ids["testament_id"]],
        'count': 0, 'count_subs': 0,
        'locked': False, 'standard': True}}, {
    f'{test_ids["source_translation_id"]}': {
        'id': test_ids["source_translation_id"], 'name': 'Source translation',
        'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [test_ids["original_text_id"], test_ids["translation_id"],
                 test_ids["transliteration_id"]], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    f'{test_ids["sponsor_id"]}': {
        'id': test_ids["sponsor_id"], 'name': 'Sponsor', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["involvement_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["statue_id"]}': {
        'id': test_ids["statue_id"], 'name': 'Statue', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["artifact_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["stratigraphic_id"]}': {
        'id': test_ids["stratigraphic_id"], 'name': 'Stratigraphic unit',
        'description': 'Classification of the archaeological SU e.g. burial, deposit, ...',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [test_ids["burial_id"], test_ids["deposit_id"]], 'count': 0,
        'count_subs': 0,
        'locked': False, 'standard': True}}, {
    f'{test_ids["testament_id"]}': {
        'id': test_ids["testament_id"], 'name': 'Testament',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["source_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["topographical_id"]}': {
        'id': test_ids["topographical_id"], 'name': 'Topographical Entity',
        'description': None, 'origin_id': None, 'first': None,
        'last': None, 'root': [test_ids["place_id"]], 'subs': [], 'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    f'{test_ids["translation_id"]}': {
        'id': test_ids["translation_id"], 'name': 'Translation',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["source_translation_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["transliteration_id"]}': {
        'id': test_ids["transliteration_id"], 'name': 'Transliteration',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["source_translation_id"]], 'subs': [], 'count': 0,
        'count_subs': 0,
        'locked': False, 'standard': False}}, {
    f'{test_ids["upper_body_id"]}': {
        'id': test_ids["upper_body_id"], 'name': 'Upper Body',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["human_remains_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["victim_id"]}': {
        'id': test_ids["victim_id"], 'name': 'Victim', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["involvement_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["weight_id"]}': {
        'id': test_ids["weight_id"], 'name': 'Weight', 'description': 'gram',
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["dimensions_id"]], 'subs': [], 'count': 0,
        'count_subs': 0,
        'locked': False, 'standard': False}}, {
    f'{test_ids["administrative_id"]}': {
        'id': test_ids["administrative_id"], 'name': 'Administrative unit',
        'description': 'Hierarchy of administrative units like "Austria", "Germany", "Italy" and their respective subunits like "Lower Austria", "Styria" and their subunits etc.',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [test_ids["austria_id"], test_ids["czech_id"],
                 test_ids["germany_id"], test_ids["italy_id"],
                 test_ids["slovakia_id"], test_ids["slovenia_id"]],
        'count': test_ids["book_id"],
        'count_subs': 2, 'locked': False, 'standard': True}}, {
    f'{test_ids["austria_id"]}': {
        'id': test_ids["austria_id"], 'name': 'Austria', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["administrative_id"]],
        'subs': [test_ids["nieder_id"], test_ids["wien_id"]], 'count': 2,
        'count_subs': 0,
        'locked': False, 'standard': False}}, {
    f'{test_ids["carantinia_id"]}': {
        'id': test_ids["carantinia_id"], 'name': 'Carantania',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["historical_place_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["comitatus_id"]}': {
        'id': test_ids["comitatus_id"], 'name': 'Comitatus Iauntal',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["historical_place_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["czech_id"]}': {
        'id': test_ids["czech_id"], 'name': 'Czech Republic',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["administrative_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["germany_id"]}': {
        'id': test_ids["germany_id"], 'name': 'Germany', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["administrative_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["historical_place_id"]}': {
        'id': test_ids["historical_place_id"], 'name': 'Historical place',
        'description': 'Hierarchy of historical places respectively historical administrative units like: Duchy of Bavaria, Lombard Kingdom etc.',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [test_ids["carantinia_id"], test_ids["comitatus_id"],
                 test_ids["serbia_id"], test_ids["marcha_id"]],
        'count': test_ids["inbook_id"],
        'count_subs': 0,
        'locked': False, 'standard': True}}, {
    f'{test_ids["italy_id"]}': {
        'id': test_ids["italy_id"], 'name': 'Italy', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["administrative_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["serbia_id"]}': {
        'id': test_ids["serbia_id"], 'name': 'Kingdom of Serbia',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["historical_place_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["marcha_id"]}': {
        'id': test_ids["marcha_id"], 'name': 'Marcha Orientalis',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["historical_place_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["nieder_id"]}': {
        'id': test_ids["nieder_id"], 'name': 'Niederösterreich',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["austria_id"], test_ids["administrative_id"]],
        'subs': [], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    f'{test_ids["slovakia_id"]}': {
        'id': test_ids["slovakia_id"], 'name': 'Slovakia', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["administrative_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["slovenia_id"]}': {
        'id': test_ids["slovenia_id"], 'name': 'Slovenia', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["administrative_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    f'{test_ids["wien_id"]}': {
        'id': test_ids["wien_id"], 'name': 'Wien', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["austria_id"], test_ids["administrative_id"]],
        'subs': [], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}]}
