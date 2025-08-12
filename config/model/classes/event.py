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
            'label': _('actor'),
            'classes': class_groups['actor']['classes'],
            'properties': ['P11', 'P14', 'P22', 'P23'],
            'multiple': True},
        'subs': {
            'label': _('subs'),
            'classes': class_groups['event']['classes'],
            'properties': 'P9',
            'multiple': True},
        'source': {
            'label': _('source'),
            'classes': 'source',
            'properties': 'P67',
            'inverse': True,
            'multiple': True},
        'file': {
            'label': _('file'),
            'classes': class_groups['file']['classes'],
            'properties': 'P67',
            'inverse': True,
            'multiple': True,
            'additional_fields': ['page']},
        'reference': {
            'label': _('reference'),
            'classes': class_groups['reference']['classes'],
            'properties': 'P67',
            'inverse': True,
            'multiple': True},
        'sub_event': {
            'label': _('sub event'),
            'classes': class_groups['event']['classes'],
            'properties': 'P9'},
        'sub_event_of': {
            'label': _('sub event of'),
            'classes': class_groups['event']['classes'],
            'properties': 'P9',
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
                    'name', 'classes', 'activity', 'involvement', 'first',
                    'last', 'comment', 'update', 'remove']},
            'reference': {
                'mode': 'link',
                'additional_columns': ['page', 'update', 'remove'],
                'buttons': ['link', 'insert']},
            'file': {
                'additional_columns': ['main image', 'remove'],
                'buttons': ['link', 'insert']},
            'note': {}}}}

additional_relations = {
    'succeeding_event': {
        'label': _('succeeding event'),
        'classes': class_groups['event']['classes'],
        'properties': 'P134',
        'inverse': True,
        'mode': 'display'},
    'preceding_event': {
        'label': _('preceding event'),
        'classes': class_groups['event']['classes'],
        'properties': 'P134',
        'mode': 'direct'},
    'location': {
        'label': _('location'),
        'classes': 'object_location',
        'properties': 'P7',
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
        'classes': class_groups['actor'],
        'properties': 'P22',
        'mode': 'display',
        'multiple': True},
    'donor': {
        'label': _('donor'),
        'classes': class_groups['actor'],
        'properties': 'P23',
        'mode': 'display',
        'multiple': True},
    'given_place': {
        'label': _('given place'),
        'classes': 'place',
        'properties': 'P24',
        'mode': 'direct',
        'multiple': True},
    'given_artifact': {
        'label': _('given artifact'),
        'classes': 'artifact',
        'properties': 'P24',
        'mode': 'direct',
        'multiple': True}}

creation = copy.deepcopy(model)
creation['relations'] = creation['relations'] | {
    'succeeding_event': additional_relations['succeeding_event'],
    'preceding_event': additional_relations['preceding_event'],
    'location': additional_relations['location'],
    'document': {
        'label': _('file'),
        'classes': 'file',
        'properties': 'P94',
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
        'classes': class_groups['artifact'],
        'properties': 'P31',
        'multiple': True,
        'mode': 'direct'},
    'modified_place': {
        'label': _('modified place'),
        'classes': 'place',
        'properties': 'P31',
        'multiple': True,
        'mode': 'direct'}}

move = copy.deepcopy(model)
move['relations'] = move['relations'] | {
    'succeeding_event': additional_relations['succeeding_event'],
    'preceding_event': additional_relations['preceding_event'],
    'place_from': {
        'label': _('place from'),
        'classes': 'object_location',
        'properties': 'P27',
        'mode': 'direct'},
    'place_to': {
        'label': _('place to'),
        'classes': 'object_location',
        'properties': 'P26',
        'mode': 'direct'},
    'moved_person': {
        'label': _('moved person'),
        'classes': 'person',
        'properties': 'P25',
        'multiple': True,
        'mode': 'direct'},
    'moved_object': {
        'label': _('moved object'),
        'classes': class_groups['artifact'],
        'properties': 'P25',
        'multiple': True,
        'mode': 'direct'}}

production = copy.deepcopy(model)
production['relations'] = production['relations'] | {
    'succeeding_event': additional_relations['succeeding_event'],
    'preceding_event': additional_relations['preceding_event'],
    'location': additional_relations['location'],
    'produced_artifact': {
        'label': _('produced artifact'),
        'classes': 'artifact',
        'properties': 'P108',
        'multiple': True,
        'mode': 'direct'}}
