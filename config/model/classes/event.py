import copy

from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups

model = {
    'attributes': {
        'name': {
            'required': True},
        'description': {},
        'date': {}},
    'relations': {
        'actor': {
            'class': class_groups['actor'],
            'property': ['P11', 'P14', 'P22', 'P23'],
            'multiple': True},
        'subs': {
            'class': class_groups['event'],
            'property': 'P9',
            'multiple': True},
        'source': {
            'class': 'source',
            'property': 'P67',
            'inverse': True,
            'multiple': True},
        'file': {
            'class': class_groups['file'],
            'property': 'P67',
            'inverse': True,
            'multiple': True},
        'reference': {
            'class': class_groups['reference'],
            'property': 'P67',
            'inverse': True,
            'multiple': True},
        'sub_event': {
            'label': _('sub event'),
            'class': class_groups['event'],
            'property': 'P9'},
        'sub_event_of': {
            'label': _('sub event of'),
            'class': class_groups['event'],
            'property': 'P9',
            'inverse': True,
            'mode': 'direct'}},
    'display': {
        'buttons': ['copy', 'network'],
        'form': {'insert_and_continue': True},
        'tabs': {
            'subs': {},
            'source': {
                'additional_columns': ['remove']},
            'actor': {
                'mode': 'link',
                'columns': [
                    'name', 'class', 'activity', 'involvement', 'first',
                    'last', 'comment', 'update', 'remove']},
            'reference': {
                'mode': 'link',
                'additional_columns': ['page', 'update', 'remove']},
            'file': {
                'additional_columns': ['main image', 'remove']},
            'note': {}}}}

additional_relations = {
    'succeeding_event': {
        'label': _('succeeding event'),
        'class': class_groups['event'],
        'property': 'P134',
        'inverse': True,
        'mode': 'display'},
    'preceding_event': {
        'label': _('preceding event'),
        'class': class_groups['event'],
        'property': 'P134',
        'mode': 'direct'},
    'location': {
        'label': _('location'),
        'class': 'object_location',
        'property': 'P7',
        'mode': 'direct'}}

activity = copy.deepcopy(model)
activity['relations'] = activity['relations'] | {
    'succeeding_event': additional_relations['succeeding_event'],
    'preceding_event': additional_relations['preceding_event'],
    'location': additional_relations['location']}

acquisition = copy.deepcopy(model)
acquisition['relations'] = acquisition['relations'] | {
    'succeeding_event': additional_relations['succeeding_event'],
    'preceding_event': additional_relations['preceding_event'],
    'location': additional_relations['location'],
    'recipient': {
        'label': _('recipient'),
        'class': class_groups['actor'],
        'property': 'P22',
        'mode': 'display',
        'multiple': True},
    'donor': {
        'label': _('donor'),
        'class': class_groups['actor'],
        'property': 'P23',
        'mode': 'display',
        'multiple': True},
    'given_place': {
        'label': _('given place'),
        'class': 'place',
        'property': 'P24',
        'mode': 'direct',
        'multiple': True},
    'given_artifact': {
        'label': _('given artifact'),
        'class': 'artifact',
        'property': 'P24',
        'mode': 'direct',
        'multiple': True}}

creation = copy.deepcopy(model)
creation['relations'] = creation['relations'] | {
    'succeeding_event': additional_relations['succeeding_event'],
    'preceding_event': additional_relations['preceding_event'],
    'location': additional_relations['location'],
    'document': {
        'label': _('file'),
        'class': 'file',
        'property': 'P94',
        'multiple': True,
        'mode': 'direct'}}

event = copy.deepcopy(model)
event['relations'] = event['relations'] | {
    'location': additional_relations['location']}

modification = copy.deepcopy(model)
modification['relations'] = modification['relations'] | {
    'succeeding_event': additional_relations['succeeding_event'],
    'preceding_event': additional_relations['preceding_event'],
    'location': additional_relations['location'],
    'modified_object': {
        'label': _('modified object'),
        'class': class_groups['artifact'],
        'property': 'P31',
        'multiple': True,
        'mode': 'direct'},
    'modified_place': {
        'label': _('modified place'),
        'class': 'place',
        'property': 'P31',
        'multiple': True,
        'mode': 'direct'}}

move = copy.deepcopy(model)
move['relations'] = move['relations'] | {
    'succeeding_event': additional_relations['succeeding_event'],
    'preceding_event': additional_relations['preceding_event'],
    'place_from': {
        'label': _('place from'),
        'class': 'object_location',
        'property': 'P27',
        'mode': 'direct'},
    'place_to': {
        'label': _('place to'),
        'class': 'object_location',
        'property': 'P26',
        'mode': 'direct'},
    'moved_person': {
        'label': _('moved person'),
        'class': 'person',
        'property': 'P25',
        'multiple': True,
        'mode': 'direct'},
    'moved_object': {
        'label': _('moved object'),
        'class': class_groups['artifact'],
        'property': 'P25',
        'multiple': True,
        'mode': 'direct'}}

production = copy.deepcopy(model)
production['relations'] = production['relations'] | {
    'succeeding_event': additional_relations['succeeding_event'],
    'preceding_event': additional_relations['preceding_event'],
    'location': additional_relations['location'],
    'produced_artifact': {
        'label': _('produced artifact'),
        'class': 'artifact',
        'property': 'P108',
        'multiple': True,
        'mode': 'direct'}}
