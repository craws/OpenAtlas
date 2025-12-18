import copy
from typing import Any

from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups, standard_relations

class_ = {
    'attributes': {
        'name': {
            'required': True},
        'dates': {},
        'description': {}},
    'extra': ['reference_system'],
    'relations': {
        'source': standard_relations['source'],
        'performer': {
            'label': _('performer'),
            'classes': class_groups['actor']['classes'],
            'property': 'P14',
            'multiple': True,
            'type': 'Involvement',
            'additional_fields': ['dates', 'description'],
            'tab': {
                'buttons': ['link', 'insert'],
                'columns': [
                    'name', 'class', 'type_link',
                    'begin', 'end', 'description']}},
        'participant': {
            'label': _('participant'),
            'classes': class_groups['actor']['classes'],
            'property': 'P11',
            'multiple': True,
            'type': 'Involvement',
            'additional_fields': ['dates', 'description'],
            'tab': {
                'buttons': ['link', 'insert'],
                'columns': [
                    'name', 'class', 'type_link',
                    'begin', 'end', 'description']}},
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
        'file': standard_relations['file'],
        'preceding_event': {
            'label': _('preceding event'),
            'classes': class_groups['event']['classes'],
            'property': 'P134',
            'mode': 'direct',
            'add_dynamic': True},
        'succeeding_event': {
            'label': _('succeeding event'),
            'classes': class_groups['event']['classes'],
            'property': 'P134',
            'inverse': True,
            'mode': 'display'},
        'location': {
            'label': _('location'),
            'classes': ['object_location'],
            'property': 'P7',
            'mode': 'direct',
            'add_dynamic': True}},
    'display': {
        'buttons': ['copy', 'network'],
        'form_buttons': ['insert_and_continue'],
        'additional_tabs': {'note': {}},
        'network_color': '#0000FF'}}

activity: dict[str, Any] = copy.deepcopy(class_)
activity['label'] = _('activity')
activity['display']['tooltip'] = \
    _('the most common, e.g. a battle, a meeting or a wedding')

acquisition: dict[str, Any] = copy.deepcopy(class_)
acquisition['label'] = _('acquisition')
acquisition['display']['tooltip'] = _('mapping a change of property')
acquisition['relations'] = acquisition['relations'] | {
    'donor': {
        'label': _('donor'),
        'classes': class_groups['actor']['classes'],
        'property': 'P23',
        'mode': 'direct',
        'multiple': True},
    'recipient': {
        'label': _('recipient'),
        'classes': class_groups['actor']['classes'],
        'property': 'P22',
        'mode': 'direct',
        'multiple': True},
    'given_place': {
        'label': _('given place'),
        'classes': ['place'],
        'property': 'P24',
        'mode': 'direct',
        'multiple': True},
    'given_artifact': {
        'label': _('given artifact'),
        'classes': class_groups['artifact']['classes'],
        'property': 'P24',
        'mode': 'direct',
        'multiple': True}}

modification: dict[str, Any] = copy.deepcopy(class_)
modification['label'] = _('modification')
modification['display']['tooltip'] = _('modification of artifacts')
modification['relations'] = modification['relations'] | {
    'modified_object': {
        'label': _('modified object'),
        'classes': class_groups['artifact']['classes'],
        'property': 'P31',
        'multiple': True,
        'mode': 'direct'},
    'modified_place': {
        'label': _('modified place'),
        'classes': ['place'],
        'property': 'P31',
        'multiple': True,
        'mode': 'direct'}}

move: dict[str, Any] = copy.deepcopy(class_)
del move['relations']['location']
move['label'] = _('move')
move['display']['tooltip'] = _('movement of artifacts or persons')
move['relations'] = move['relations'] | {
    'place_from': {
        'label': _('place from'),
        'classes': ['object_location'],
        'property': 'P27',
        'mode': 'direct',
        'add_dynamic': True},
    'place_to': {
        'label': _('place to'),
        'classes': ['object_location'],
        'property': 'P26',
        'mode': 'direct',
        'add_dynamic': True},
    'moved_person': {
        'label': _('moved person'),
        'classes': ['person'],
        'property': 'P25',
        'multiple': True,
        'mode': 'direct'},
    'moved_object': {
        'label': _('moved object'),
        'classes': class_groups['artifact']['classes'],
        'property': 'P25',
        'multiple': True,
        'mode': 'direct'}}

production: dict[str, Any] = copy.deepcopy(class_)
production['production'] = _('production')
production['display']['tooltip'] = _('creation of artifacts')
production['relations'] = production['relations'] | {
    'produced_artifact': {
        'label': _('produced artifact'),
        'classes': ['artifact'],
        'property': 'P108',
        'multiple': True,
        'mode': 'direct'}}
