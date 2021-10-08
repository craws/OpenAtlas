import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_params import test_ids

test_type_tree = {'typeTree': [{
    '18': {
        'id': 18, 'name': 'Abbot', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [16],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '53': {
        'id': 53, 'name': 'Actor actor relation',
        'description': 'Categories for the relationship between two actors. This may be a mutual relationship (e.g. actor A is friend of actor B and vice versa), or a directional relationship (e.g. actor A is the child of actor B, while actor B is the parent of actor A).',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [63, 54, 60, 56], 'count': 0, 'count_subs': 1,
        'locked': False, 'standard': True}}, {
    '16': {
        'id': 16, 'name': 'Actor function',
        'description': 'Definitions of an actor\'s function within a group. An actor can for example be member of a group and this membership is defined by a certain function during a certain period of time. E.g. actor "Charlemagne" is member of the group "Frankish Reign" from 768 to 814 in the function of "King" and he is member of the group "Roman Empire" from 800 to 814 in the function "Emperor".',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [18, 17, 21, 20, 22, 19], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': True}}, {
    '61': {
        'id': 61, 'name': 'Ally of', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [60, 53],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '5': {
        'id': 5, 'name': 'Article', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [3],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '23': {
        'id': 23, 'name': 'Artifact', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [24, 25], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': True}}, {
    '40': {
        'id': 40, 'name': 'Battle', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [39, 34],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '3': {
        'id': 3, 'name': 'Bibliography',
        'description': 'Categories for bibliographical entries as used for example in BibTeX, e.g. Book, Inbook, Article etc.',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [5, 6, 4], 'count': 0,
        'count_subs': 0, 'locked': False,
        'standard': True}}, {
    '17': {
        'id': 17, 'name': 'Bishop', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [16],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '6': {
        'id': 6, 'name': 'Book', 'description': None, 'origin_id': None,
        'first': None, 'last': None, 'root': [3], 'subs': [],
        'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    '72': {
        'id': 72, 'name': 'Boundary Mark', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [65],
        'subs': [], 'count': 1, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '78': {
        'id': 78, 'name': 'Burial', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [77],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '69': {
        'id': 69, 'name': 'Burial Site', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [65],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '52': {
        'id': 52, 'name': 'CC BY-SA 4.0', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [49, 47],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '51': {
        'id': 51, 'name': 'CC BY 4.0', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [49, 47],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '35': {
        'id': 35, 'name': 'Change of Property', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [34],
        'subs': [36, 38, 37], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '43': {
        'id': 43, 'name': 'Charter', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [42],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '8': {
        'id': 8, 'name': 'Charter Edition', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [7],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '10': {
        'id': 10, 'name': 'Chronicle Edition', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [7],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '15': {
        'id': 15, 'name': 'close match',
        'description': 'Concepts are sufficiently similar that they can be used interchangeably in some information retrieval applications.',
        'origin_id': None, 'first': None,
        'last': None, 'root': [13],
        'subs': [], 'count': 1,
        'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '24': {
        'id': 24, 'name': 'Coin', 'description': None,
        'origin_id': None,
        'first': None, 'last': None, 'root': [23], 'subs': [],
        'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '39': {
        'id': 39, 'name': 'Conflict', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [34],
        'subs': [40, 41], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '46': {
        'id': 46, 'name': 'Contract', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [42],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '21': {
        'id': 21, 'name': 'Count', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [16],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '27': {
        'id': 27, 'name': 'Creator', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [26],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '79': {
        'id': 79, 'name': 'Deposit', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [77],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '101': {
        'id': 101, 'name': 'Dimensions',
        'description': 'Physical dimensions like weight and height.',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [102, 103], 'count': 0,
        'count_subs': 1, 'locked': False,
        'standard': False}}, {
    '36': {
        'id': 36, 'name': 'Donation', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [35, 34],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '71': {
        'id': 71, 'name': 'Economic Site', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [65],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '63': {
        'id': 63, 'name': 'Economical', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [53],
        'subs': [64], 'count': 1, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '7': {
        'id': 7, 'name': 'Edition',
        'description': "Categories for the classification of written sources' editions like charter editions, chronicle edition etc.",
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [8, 10, 9], 'count': 0,
        'count_subs': 0, 'locked': False,
        'standard': True}}, {
    '20': {
        'id': 20, 'name': 'Emperor', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [16],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '58': {
        'id': 58, 'name': 'Enemy of', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [56, 53],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '34': {
        'id': 34, 'name': 'Event',
        'description': 'Categories for the type of events like Change of property, Conflict, Movement, Attendance etc.',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [35, 39], 'count': 0,
        'count_subs': 0, 'locked': False,
        'standard': True}}, {
    '14': {
        'id': 14, 'name': 'exact match',
        'description': 'High degree of confidence that the concepts can be used interchangeably.',
        'origin_id': None, 'first': None, 'last': None, 'root': [13],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '38': {
        'id': 38, 'name': 'Exchange', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [35, 34],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '11': {
        'id': 11, 'name': 'External reference',
        'description': 'Categories for the classification of external references like a link to Wikipedia',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [12], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': True}}, {
    '13': {
        'id': 13, 'name': 'External reference match',
        'description': 'SKOS based definition of the confidence degree that concepts can be used interchangeable.',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [15, 14], 'count': 0, 'count_subs': 1, 'locked': True,
        'standard': True}}, {
    '74': {
        'id': 74, 'name': 'Feature',
        'description': 'Classification of the archaeological feature e.g. grave, pit, ...',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [75, 76], 'count': 0,
        'count_subs': 0, 'locked': False,
        'standard': True}}, {
    '32': {
        'id': 32, 'name': 'Female', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [31],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '57': {
        'id': 57, 'name': 'Friend of', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [56, 53],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '75': {
        'id': 75, 'name': 'Grave', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [74],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '102': {
        'id': 102, 'name': 'Height', 'description': 'centimeter',
        'origin_id': None, 'first': None, 'last': None, 'root': [101],
        'subs': [], 'count': 1, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '80': {
        'id': 80, 'name': 'Human remains',
        'description': 'Human remains, that for example were discovered during archaeological excavations. They are associated with a stratigraphic unit (in most cases a skeleton) that is composed of (P46) one or multiple parts (in most cases bones) that are classified as biological objects (E20). From a hierarchical point of view the human remains are one level below the stratigraphic unit respectively the entity whose sum of parts resembles the individual/skeleton. This way individual bones or body parts can be treated individually and be connected with separate classifications (e.g. Injuries of the right upper arm or caries on a certain tooth).',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [82, 81], 'count': 0,
        'count_subs': 0, 'locked': False,
        'standard': True}}, {
    '4': {
        'id': 4, 'name': 'Inbook', 'description': None,
        'origin_id': None,
        'first': None, 'last': None, 'root': [3], 'subs': [],
        'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    '70': {
        'id': 70, 'name': 'Infrastructure', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [65],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '26': {
        'id': 26, 'name': 'Involvement',
        'description': 'Categories to define the involvement of an actor within an event. E.g. "Napoleon" participated in the event "Invasion of Russia" as "Commander" or "Michelangelo" performed the event "painting of the Sistine chapel" as "Artist".',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [27, 30, 28, 29],
        'count': 0, 'count_subs': 0,
        'locked': False, 'standard': True}}, {
    '54': {
        'id': 54, 'name': 'Kindredship', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [53],
        'subs': [55], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '22': {
        'id': 22, 'name': 'King', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [16],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '62': {
        'id': 62, 'name': 'Leader of (Retinue of)',
        'description': None, 'origin_id': None, 'first': None,
        'last': None, 'root': [60, 53], 'subs': [], 'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    '45': {
        'id': 45, 'name': 'Letter', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [42],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '9': {
        'id': 9, 'name': 'Letter Edition', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [7],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '47': {
        'id': 47, 'name': 'License',
        'description': 'Types for the licensing of a file',
        'origin_id': None, 'first': None,
        'last': None, 'root': [],
        'subs': [49, 48], 'count': 0,
        'count_subs': 1, 'locked': False,
        'standard': True}}, {
    '12': {
        'id': 12, 'name': 'Link', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [11],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '82': {
        'id': 82, 'name': 'Lower Body', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [80],
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
        'last': None, 'root': [56, 53], 'subs': [], 'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    '67': {
        'id': 67, 'name': 'Military Facility', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [65],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '30': {
        'id': 30, 'name': 'Offender', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [26],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '49': {
        'id': 49, 'name': 'Open license', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [47],
        'subs': [52, 51, 50], 'count': 1, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '98': {
        'id': 98, 'name': 'Original Text', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [97],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '55': {
        'id': 55, 'name': 'Parent of (Child of)',
        'description': None, 'origin_id': None, 'first': None,
        'last': None, 'root': [54, 53], 'subs': [], 'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    '76': {
        'id': 76, 'name': 'Pit', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [74],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '65': {
        'id': 65, 'name': 'Place',
        'description': 'Types for non-moveable entities (i.e. places) with a certain extent and/or location like Settlement, Burial site, Ritual site, Fortification etc.',
        'origin_id': None,
        'first': None, 'last': None,
        'root': [],
        'subs': [72, 69, 71, 70, 67, 68,
                 66, 73], 'count': 1,
        'count_subs': 1,
        'locked': False,
        'standard': True}}, {
    '60': {
        'id': 60, 'name': 'Political', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [53],
        'subs': [61, 62], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '19': {
        'id': 19, 'name': 'Pope', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [16],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '48': {
        'id': 48, 'name': 'Proprietary license', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [47],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '64': {
        'id': 64, 'name': 'Provider of (Customer of)',
        'description': None, 'origin_id': None, 'first': None,
        'last': None, 'root': [63, 53], 'subs': [], 'count': 0,
        'count_subs': 0, 'locked': False, 'standard': False}}, {
    '50': {
        'id': 50, 'name': 'Public domain', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [49, 47], 'subs': [], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '41': {
        'id': 41, 'name': 'Raid', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [39, 34], 'subs': [], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '68': {
        'id': 68, 'name': 'Ritual Site', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [65],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '37': {
        'id': 37, 'name': 'Sale', 'description': None,
        'origin_id': None, 'first': None, 'last': None,
        'root': [35, 34], 'subs': [], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '66': {
        'id': 66, 'name': 'Settlement', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [65],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '31': {
        'id': 31, 'name': 'Sex',
        'description': 'Categories for sex like female, male.',
        'origin_id': None,
        'first': None, 'last': None,
        'root': [], 'subs': [32, 33],
        'count': 0, 'count_subs': 0,
        'locked': False,
        'standard': False}}, {
    '56': {
        'id': 56, 'name': 'Social', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [53],
        'subs': [58, 57, 59], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '42': {
        'id': 42, 'name': 'Source',
        'description': 'Types for historical sources like charter, chronicle, letter etc.',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [43, 46, 45, 44], 'count': 0, 'count_subs': 0,
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
        'origin_id': None, 'first': None, 'last': None, 'root': [23],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '77': {
        'id': 77, 'name': 'Stratigraphic unit',
        'description': 'Classification of the archaeological SU e.g. burial, deposit, ...',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [78, 79], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': True}}, {
    '44': {
        'id': 44, 'name': 'Testament', 'description': None,
        'origin_id': None, 'first': None, 'last': None, 'root': [42],
        'subs': [], 'count': 0, 'count_subs': 0, 'locked': False,
        'standard': False}}, {
    '73': {
        'id': 73, 'name': 'Topographical Entity',
        'description': None, 'origin_id': None, 'first': None,
        'last': None, 'root': [65], 'subs': [], 'count': 0,
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
        'origin_id': None, 'first': None, 'last': None, 'root': [80],
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
        'root': [101], 'subs': [], 'count': 0, 'count_subs': 0,
        'locked': False, 'standard': False}}, {
    '83': {
        'id': 83, 'name': 'Administrative unit',
        'description': 'Hierarchy of administrative units like "Austria", "Germany", "Italy" and their respective subunits like "Lower Austria", "Styria" and their subunits etc.',
        'origin_id': None, 'first': None, 'last': None, 'root': [],
        'subs': [84, 89, 87, 88, 90, 91], 'count': 6,
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
        'subs': [93, 95, 96, 94], 'count': 4, 'count_subs': 0,
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
