import copy

from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups, standard_relations

model = {
    'attributes': {
        'name': {
            'required': True},
        'description': {},
        'dates': {}},
    'relations': {
        'source': standard_relations['source'],
        'actor': {
            'label': _('actor'),
            'classes': class_groups['actor']['classes'],
            'property': 'P11', # Todo: 'P14', 'P22', 'P23'
            'multiple': True,
            'type': 'Involvement',
            'additional_fields': [
                'domain',
                'dates',
                'description'],
            'tab': {
                'buttons': ['link', 'insert'],
                'columns': [
                    'name', 'class', 'activity', 'involvement', 'first',
                    'last', 'description']}},
        'subs': {
            'label': _('subs'),
            'classes': class_groups['event']['classes'],
            'property': 'P9',
            'multiple': True,
            'tab': {
                'buttons': ['link', 'insert']}},
        'super': {
            'label': _('sub event of'),
            'classes': class_groups['event']['classes'],
            'property': 'P9',
            'inverse': True,
            'mode': 'direct'},
        'reference': standard_relations['reference'],
        'file': standard_relations['file']},
    'display': {
        'buttons': ['copy', 'network'],
        'form': {'insert_and_continue': True},
        'additional_tabs': {'note': {}}}}

additional_relations = {
    'succeeding_event': {
        'label': _('succeeding event'),
        'classes': class_groups['event']['classes'],
        'property': 'P134',
        'inverse': True,
        'mode': 'display'},
    'preceding_event': {
        'label': _('preceding event'),
        'classes': class_groups['event']['classes'],
        'property': 'P134',
        'mode': 'direct'},
    'location': {
        'label': _('location'),
        'classes': 'object_location',
        'property': 'P7',
        'mode': 'direct'}}

activity = copy.deepcopy(model)
activity['display']['tooltip'] = \
    _('the most common, e.g. a battle, a meeting or a wedding')
activity['relations'] = activity['relations'] | {
    'succeeding_event': additional_relations['succeeding_event'],
    'preceding_event': additional_relations['preceding_event'],
    'location': additional_relations['location']}

acquisition = copy.deepcopy(model)
acquisition['display']['tooltip'] = _('mapping a change of property')
acquisition['relations'] = acquisition['relations'] | {
    'succeeding_event': additional_relations['succeeding_event'],
    'preceding_event': additional_relations['preceding_event'],
    'location': additional_relations['location'],
    'recipient': {
        'label': _('recipient'),
        'classes': class_groups['actor']['classes'],
        'property': 'P22',
        'mode': 'display',
        'multiple': True},
    'donor': {
        'label': _('donor'),
        'classes': class_groups['actor']['classes'],
        'property': 'P23',
        'mode': 'display',
        'multiple': True},
    'given_place': {
        'label': _('given place'),
        'classes': 'place',
        'property': 'P24',
        'mode': 'direct',
        'multiple': True},
    'given_artifact': {
        'label': _('given artifact'),
        'classes': 'artifact',
        'property': 'P24',
        'mode': 'direct',
        'multiple': True}}

creation = copy.deepcopy(model)
creation['display']['tooltip'] = _('creation of documents (files)')
creation['relations'] = creation['relations'] | {
    'succeeding_event': additional_relations['succeeding_event'],
    'preceding_event': additional_relations['preceding_event'],
    'location': additional_relations['location'],
    'document': {
        'label': _('file'),
        'classes': 'file',
        'property': 'P94',
        'multiple': True,
        'mode': 'direct'}}

event = copy.deepcopy(model)
event['display']['tooltip'] = \
    _('events not performed by actors, e.g. a natural disaster')
event['relations'] = event['relations'] | {
    'location': additional_relations['location']}

modification = copy.deepcopy(model)
modification['display']['tooltip'] = _('modification of artifacts')
modification['relations'] = modification['relations'] | {
    'succeeding_event': additional_relations['succeeding_event'],
    'preceding_event': additional_relations['preceding_event'],
    'location': additional_relations['location'],
    'modified_object': {
        'label': _('modified object'),
        'classes': class_groups['artifact']['classes'],
        'property': 'P31',
        'multiple': True,
        'mode': 'direct'},
    'modified_place': {
        'label': _('modified place'),
        'classes': 'place',
        'property': 'P31',
        'multiple': True,
        'mode': 'direct'}}

move = copy.deepcopy(model)
move['display']['tooltip'] = _('movement of artifacts or persons')
move['relations'] = move['relations'] | {
    'succeeding_event': additional_relations['succeeding_event'],
    'preceding_event': additional_relations['preceding_event'],
    'place_from': {
        'label': _('place from'),
        'classes': 'object_location',
        'property': 'P27',
        'mode': 'direct'},
    'place_to': {
        'label': _('place to'),
        'classes': 'object_location',
        'property': 'P26',
        'mode': 'direct'},
    'moved_person': {
        'label': _('moved person'),
        'classes': 'person',
        'property': 'P25',
        'multiple': True,
        'mode': 'direct'},
    'moved_object': {
        'label': _('moved object'),
        'classes': class_groups['artifact']['classes'],
        'property': 'P25',
        'multiple': True,
        'mode': 'direct'}}

production = copy.deepcopy(model)
production['display']['tooltip'] = _('creation of artifacts')
production['relations'] = production['relations'] | {
    'succeeding_event': additional_relations['succeeding_event'],
    'preceding_event': additional_relations['preceding_event'],
    'location': additional_relations['location'],
    'produced_artifact': {
        'label': _('produced artifact'),
        'classes': 'artifact',
        'property': 'P108',
        'multiple': True,
        'mode': 'direct'}}
