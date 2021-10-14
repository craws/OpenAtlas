import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_params import test_ids

test_type_tree = {'typeTree': [{
    test_ids["abbot_id"]: {
        'id': test_ids["abbot_id"], 'name': 'Abbot', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_function_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["actor_r_id"]: {
        'id': test_ids["actor_r_id"], 'name': 'Actor actor relation',
        'description': 'Categories for the relationship between two actors. This may be a mutual relationship (e.g. actor A is friend of actor B and vice versa), or a directional relationship (e.g. actor A is the child of actor B, while actor B is the parent of actor A).',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [test_ids["economical_id"], 54, test_ids["political_id"], 56],
        'count': 0, 'count_subs': 1,
        'locked': False, 'standard': True}}, {
    test_ids["actor_function_id"]: {
        'id': test_ids["actor_function_id"], 'name': 'Actor function',
        'description': 'Definitions of an actor\'s function within a group. An actor can for example be member of a group and this membership is defined by a certain function during a certain period of time. E.g. actor "Charlemagne" is member of the group "Frankish Reign" from 768 to 814 in the function of "King" and he is member of the group "Roman Empire" from 800 to 814 in the function "Emperor".',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [test_ids["abbot_id"], test_ids["bishop_id"],
                 test_ids["count_id"], test_ids["emperor_id"], 22, 19],
        'count': 0, 'count_subs': 0,
        'locked': False, 'standard': True}}, {
    test_ids["ally_id"]: {
        'id': test_ids["ally_id"], 'name': 'Ally of', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["political_id"], test_ids["actor_r_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["article_id"]: {
        'id': test_ids["article_id"], 'name': 'Article', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["bibliography_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["artifact_id"]: {
        'id': test_ids["artifact_id"], 'name': 'Artifact', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [test_ids["coin_id"], 25], 'count': 0, 'count_subs': 0,
        'locked': False,
        'standard': True}}, {
    test_ids["battle_id"]: {
        'id': test_ids["battle_id"], 'name': 'Battle', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["conflict_id"], test_ids["event_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["bibliography_id"]: {
        'id': test_ids["bibliography_id"], 'name': 'Bibliography',
        'description': 'Categories for bibliographical entries as used for example in BibTeX, e.g. Book, Inbook, Article etc.',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [test_ids["article_id"], test_ids["book_id"],
                 test_ids["inbook_id"]], 'count': 0,
        'count_subs': 0, 'locked': False,
        'standard': True}}, {
    test_ids["bishop_id"]: {
        'id': test_ids["bishop_id"], 'name': 'Bishop', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_function_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["book_id"]: {
        'id': test_ids["book_id"], 'name': 'Book', 'description': None,
        'origin_id': None,
        'first': None, 'last': None, 'root': [test_ids["bibliography_id"]],
        'subs': [],
        'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    test_ids["boundary_id"]: {
        'id': test_ids["boundary_id"], 'name': 'Boundary Mark',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["place_id"]],
        'subs': [], 'count': 1, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["burial_id"]: {
        'id': test_ids["burial_id"], 'name': 'Burial', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["stratigraphic_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["burial_site_id"]: {
        'id': test_ids["burial_site_id"], 'name': 'Burial Site',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["place_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["cc_by_sa_id"]: {
        'id': test_ids["cc_by_sa_id"],
        'name': 'CC BY-SA test_ids["inbook_id"].0', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [49, test_ids["license_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["cc_by_id"]: {
        'id': test_ids["cc_by_id"], 'name': 'CC BY test_ids["inbook_id"].0',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [49, test_ids["license_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["change_id"]: {
        'id': test_ids["change_id"], 'name': 'Change of Property',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["event_id"]],
        'subs': [test_ids["donation_id"], test_ids["exchange_id"],
                 test_ids["sale_id"]], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    test_ids["charter_id"]: {
        'id': test_ids["charter_id"], 'name': 'Charter', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["source_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["charter_edition_id"]: {
        'id': test_ids["charter_edition_id"], 'name': 'Charter Edition',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["edition_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["chronicle_edition_id"]: {
        'id': test_ids["chronicle_edition_id"], 'name': 'Chronicle Edition',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["edition_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["close_match_id"]: {
        'id': test_ids["close_match_id"], 'name': 'close match',
        'description': 'Concepts are sufficiently similar that they can be used interchangeably in some information retrieval applications.',
        'origin_id': None, 'first': None,
        'last': None, 'root': [test_ids["external_match_id"]],
        'subs': [], 'count': 1,
        'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["coin_id"]: {
        'id': test_ids["coin_id"], 'name': 'Coin', 'description': None,
        'origin_id': None,
        'first': None, 'last': None, 'root': [test_ids["artifact_id"]],
        'subs': [],
        'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["conflict_id"]: {
        'id': test_ids["conflict_id"], 'name': 'Conflict', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["event_id"]],
        'subs': [test_ids["battle_id"], 41], 'count': 0, 'count_subs': 0,
        'locked': False,
        'standard': False}}, {
    test_ids["contract_id"]: {
        'id': test_ids["contract_id"], 'name': 'Contract', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["source_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["count_id"]: {
        'id': test_ids["count_id"], 'name': 'Count', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_function_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["creator_id"]: {
        'id': test_ids["creator_id"], 'name': 'Creator', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [26],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["deposit_id"]: {
        'id': test_ids["deposit_id"], 'name': 'Deposit', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["stratigraphic_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["dimensions_id"]: {
        'id': test_ids["dimensions_id"], 'name': 'Dimensions',
        'description': 'Physical dimensions like weight and height.',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [test_ids["height_id"], 103], 'count': 0,
        'count_subs': 1, 'locked': False,
        'standard': False}}, {
    test_ids["donation_id"]: {
        'id': test_ids["donation_id"], 'name': 'Donation', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["change_id"], test_ids["event_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["economic_site_id"]: {
        'id': test_ids["economic_site_id"], 'name': 'Economic Site',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["place_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["economical_id"]: {
        'id': test_ids["economical_id"], 'name': 'Economical',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_r_id"]],
        'subs': [test_ids["provider_id"]], 'count': 1, 'count_subs': 0,
        'locked': False,
        'standard': False}}, {
    test_ids["edition_id"]: {
        'id': test_ids["edition_id"], 'name': 'Edition',
        'description': "Categories for the classification of written sources' editions like charter editions, chronicle edition etc.",
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [test_ids["charter_edition_id"],
                 test_ids["chronicle_edition_id"],
                 test_ids["letter_edition_id"]], 'count': 0,
        'count_subs': 0, 'locked': False,
        'standard': True}}, {
    test_ids["emperor_id"]: {
        'id': test_ids["emperor_id"], 'name': 'Emperor', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_function_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["enemy_id"]: {
        'id': test_ids["enemy_id"], 'name': 'Enemy of', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [56, test_ids["actor_r_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["event_id"]: {
        'id': test_ids["event_id"], 'name': 'Event',
        'description': 'Categories for the type of events like Change of property, Conflict, Movement, Attendance etc.',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [test_ids["change_id"], test_ids["conflict_id"]], 'count': 0,
        'count_subs': 0, 'locked': False,
        'standard': True}}, {
    test_ids["exact_match_id"]: {
        'id': test_ids["exact_match_id"], 'name': 'exact match',
        'description': 'High degree of confidence that the concepts can be used interchangeably.',
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["external_match_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["exchange_id"]: {
        'id': test_ids["exchange_id"], 'name': 'Exchange', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["change_id"], test_ids["event_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["external_reference_id"]: {
        'id': test_ids["external_reference_id"], 'name': 'External reference',
        'description': 'Categories for the classification of external references like a link to Wikipedia',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [12], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': True}}, {
    test_ids["external_match_id"]: {
        'id': test_ids["external_match_id"], 'name': 'External reference match',
        'description': 'SKOS based definition of the confidence degree that concepts can be used interchangeable.',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [test_ids["close_match_id"], test_ids["exact_match_id"]],
        'count': 0, 'count_subs': 1, 'locked': True,
        'standard': True}}, {
    test_ids["feature_id"]: {
        'id': test_ids["feature_id"], 'name': 'Feature',
        'description': 'Classification of the archaeological feature e.g. grave, pit, ...',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [test_ids["grave_id"], 76], 'count': 0,
        'count_subs': 0, 'locked': False,
        'standard': True}}, {
    test_ids["female_id"]: {
        'id': test_ids["female_id"], 'name': 'Female', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [31],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["friend_id"]: {
        'id': test_ids["friend_id"], 'name': 'Friend of', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [56, test_ids["actor_r_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["grave_id"]: {
        'id': test_ids["grave_id"], 'name': 'Grave', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["feature_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["height_id"]: {
        'id': test_ids["height_id"], 'name': 'Height',
        'description': 'centimeter',
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["dimensions_id"]],
        'subs': [], 'count': 1, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["human_remains_id"]: {
        'id': test_ids["human_remains_id"], 'name': 'Human remains',
        'description': 'Human remains, that for example were discovered during archaeological excavations. They are associated with a stratigraphic unit (in most cases a skeleton) that is composed of (P46) one or multiple parts (in most cases bones) that are classified as biological objects (E20). From a hierarchical point of view the human remains are one level below the stratigraphic unit respectively the entity whose sum of parts resembles the individual/skeleton. This way individual bones or body parts can be treated individually and be connected with separate classifications (e.g. Injuries of the right upper arm or caries on a certain tooth).',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [82, 81], 'count': 0,
        'count_subs': 0, 'locked': False,
        'standard': True}}, {
    test_ids["inbook_id"]: {
        'id': test_ids["inbook_id"], 'name': 'Inbook', 'description': None,
        'origin_id': None,
        'first': None, 'last': None, 'root': [test_ids["bibliography_id"]],
        'subs': [],
        'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    '70': {  # todo: weitermachen
        'id': 70, 'name': 'Infrastructure', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["place_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '26': {
        'id': 26, 'name': 'Involvement',
        'description': 'Categories to define the involvement of an actor within an event. E.g. "Napoleon" participated in the event "Invasion of Russia" as "Commander" or "Michelangelo" performed the event "painting of the Sistine chapel" as "Artist".',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [test_ids["creator_id"], 30, 28, 29],
        'count': 0, 'count_subs': 0,
        'locked': False, 'standard': True}}, {
    '54': {
        'id': 54, 'name': 'Kindredship', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_r_id"]],
        'subs': [55], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '22': {
        'id': 22, 'name': 'King', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_function_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '62': {
        'id': 62, 'name': 'Leader of (Retinue of)',
        'description': None, 'origin_id': None, 'first': None,
        'last': None,
        'root': [test_ids["political_id"], test_ids["actor_r_id"]], 'subs': [],
        'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    '45': {
        'id': 45, 'name': 'Letter', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["source_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    'test_ids["letter_edition_id"]': {
        'id': test_ids["letter_edition_id"], 'name': 'Letter Edition',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["edition_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    'test_ids["license_id"]': {
        'id': test_ids["license_id"], 'name': 'License',
        'description': 'Types for the licensing of a file',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [49, 48], 'count': 0,
        'count_subs': 1, 'locked': False,
        'standard': True}}, {
    '12': {
        'id': 12, 'name': 'Link', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["external_reference_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '82': {
        'id': 82, 'name': 'Lower Body', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["human_remains_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '33': {
        'id': 33, 'name': 'Male', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [31],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '59': {
        'id': 59, 'name': 'Mentor of (Student of)',
        'description': None, 'origin_id': None, 'first': None,
        'last': None, 'root': [56, test_ids["actor_r_id"]], 'subs': [],
        'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    '67': {
        'id': 67, 'name': 'Military Facility', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["place_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '30': {
        'id': 30, 'name': 'Offender', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [26],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '49': {
        'id': 49, 'name': 'Open license', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["license_id"]],
        'subs': [test_ids["cc_by_sa_id"], test_ids["cc_by_id"], 50], 'count': 1,
        'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '98': {
        'id': 98, 'name': 'Original Text', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [97],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '55': {
        'id': 55, 'name': 'Parent of (Child of)',
        'description': None, 'origin_id': None, 'first': None,
        'last': None, 'root': [54, test_ids["actor_r_id"]], 'subs': [],
        'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    '76': {
        'id': 76, 'name': 'Pit', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["feature_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["place_id"]: {
        'id': test_ids["place_id"], 'name': 'Place',
        'description': 'Types for non-moveable entities (i.e. places) with a certain extent and/or location like Settlement, Burial site, Ritual site, Fortification etc.',
        'origin_id': None,
        'first': None, 'last': None,
        'root': [],
        'subs': [test_ids["boundary_id"], test_ids["burial_site_id"],
                 test_ids["economic_site_id"], 70, 67,
                 test_ids["ritual_site_id"],
                 66, 73], 'count': 1,
        'count_subs': 1,
        'locked': False,
        'standard': True}}, {
    'test_ids["political_id"]': {
        'id': test_ids["political_id"], 'name': 'Political',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_r_id"]],
        'subs': [test_ids["ally_id"], 62], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '19': {
        'id': 19, 'name': 'Pope', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_function_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '48': {
        'id': 48, 'name': 'Proprietary license', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["license_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    'test_ids["provider_id"]': {
        'id': test_ids["provider_id"], 'name': 'Provider of (Customer of)',
        'description': None, 'origin_id': None, 'first': None,
        'last': None,
        'root': [test_ids["economical_id"], test_ids["actor_r_id"]], 'subs': [],
        'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    '50': {
        'id': 50, 'name': 'Public domain', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [49, test_ids["license_id"]], 'subs': [], 'count': 0,
        'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '41': {
        'id': 41, 'name': 'Raid', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["conflict_id"], test_ids["event_id"]], 'subs': [],
        'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    'test_ids["ritual_site_id"]': {
        'id': test_ids["ritual_site_id"], 'name': 'Ritual Site',
        'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["place_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    test_ids["sale_id"]: {
        'id': test_ids["sale_id"], 'name': 'Sale', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["change_id"], test_ids["event_id"]], 'subs': [],
        'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '66': {
        'id': 66, 'name': 'Settlement', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["place_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '31': {
        'id': 31, 'name': 'Sex',
        'description': 'Categories for sex like female, male.',
        'origin_id': None,
        'first': None, 'last': None,
        'root': [], 'subs': [test_ids["female_id"], 33],
        'count': 0, 'count_subs': 0,
        'locked': False,
        'standard': False}}, {
    '56': {
        'id': 56, 'name': 'Social', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["actor_r_id"]],
        'subs': [test_ids["enemy_id"], test_ids["friend_id"], 59], 'count': 0,
        'count_subs': 0,
        'locked': False, 'standard': False}}, {
    test_ids["source_id"]: {
        'id': test_ids["source_id"], 'name': 'Source',
        'description': 'Types for historical sources like charter, chronicle, letter etc.',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [test_ids["charter_id"], test_ids["contract_id"], 45, 44],
        'count': 0, 'count_subs': 0,
        'locked': False, 'standard': True}}, {
    '97': {
        'id': 97, 'name': 'Source translation', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [98, 99, 100], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '28': {
        'id': 28, 'name': 'Sponsor', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [26],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '25': {
        'id': 25, 'name': 'Statue', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["artifact_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    'test_ids["stratigraphic_id"]': {
        'id': test_ids["stratigraphic_id"], 'name': 'Stratigraphic unit',
        'description': 'Classification of the archaeological SU e.g. burial, deposit, ...',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [test_ids["burial_id"], test_ids["deposit_id"]], 'count': 0,
        'count_subs': 0,
        'locked': False, 'standard': True}}, {
    '44': {
        'id': 44, 'name': 'Testament', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["source_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '73': {
        'id': 73, 'name': 'Topographical Entity',
        'description': None, 'origin_id': None, 'first': None,
        'last': None, 'root': [test_ids["place_id"]], 'subs': [], 'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    '99': {
        'id': 99, 'name': 'Translation', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [97],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '100': {
        'id': 100, 'name': 'Transliteration', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [97], 'subs': [], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '81': {
        'id': 81, 'name': 'Upper Body', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["human_remains_id"]],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '29': {
        'id': 29, 'name': 'Victim', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [26],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '103': {
        'id': 103, 'name': 'Weight', 'description': 'gram',
        'origin_id': None, 'first': None, 'last': None,
        'root': [test_ids["dimensions_id"]], 'subs': [], 'count': 0,
        'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '83': {
        'id': 83, 'name': 'Administrative unit',
        'description': 'Hierarchy of administrative units like "Austria", "Germany", "Italy" and their respective subunits like "Lower Austria", "Styria" and their subunits etc.',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [84, 89, 87, 88, 90, 91], 'count': test_ids["book_id"],
        'count_subs': 2, 'locked': False, 'standard': True}}, {
    '84': {
        'id': 84, 'name': 'Austria', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [83],
        'subs': [86, 85], 'count': 2, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '93': {
        'id': 93, 'name': 'Carantania', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [92],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '95': {
        'id': 95, 'name': 'Comitatus Iauntal', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [92],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '89': {
        'id': 89, 'name': 'Czech Republic', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [83],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '87': {
        'id': 87, 'name': 'Germany', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [83],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '92': {
        'id': 92, 'name': 'Historical place',
        'description': 'Hierarchy of historical places respectively historical administrative units like: Duchy of Bavaria, Lombard Kingdom etc.',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [93, 95, 96, 94], 'count': test_ids["inbook_id"],
        'count_subs': 0,
        'locked': False, 'standard': True}}, {
    '88': {
        'id': 88, 'name': 'Italy', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [83],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '96': {
        'id': 96, 'name': 'Kingdom of Serbia', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [92],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '94': {
        'id': 94, 'name': 'Marcha Orientalis', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [92],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '86': {
        'id': 86, 'name': 'Niederösterreich', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [84, 83], 'subs': [], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '90': {
        'id': 90, 'name': 'Slovakia', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [83],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '91': {
        'id': 91, 'name': 'Slovenia', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [83],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '85': {
        'id': 85, 'name': 'Wien', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [84, 83], 'subs': [], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}]}
