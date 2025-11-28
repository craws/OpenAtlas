from typing import Any

from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups, standard_relations

artifact_relation = {
    'label': _('artifact'),
    'classes': class_groups['artifact']['classes'],
    'property': 'P46',
    'multiple': True,
    'tab': {
        'buttons': ['link', 'insert']}}

place: dict[str, Any] = {
    'label': _('place'),
    'attributes': {
        'name': {
            'required': True},
        'alias': {},
        'dates': {},
        'description': {},
        'location': {}},
    'extra': ['reference_system'],
    'relations': {
        'source': standard_relations['source'],
        'artifact': artifact_relation,
        'feature': {
            'classes': 'feature',
            'property': 'P46',
            'multiple': True,
            'tab': {
                'buttons': ['insert']}},
        'acquisition': {
            'classes': 'acquisition',
            'property': 'P24',
            'inverse': True,
            'tab': {
                'buttons': ['insert']}},
        'modification': {
            'classes': 'modification',
            'property': 'P31',
            'inverse': True,
            'tab': {
                'buttons': ['insert']}},
        'event_location': {
            'label': _('event location'),
            'classes': [
                'activity', 'acquisition', 'modification', 'production'],
            'property': 'P7',
            'inverse': True,
            'tab': {
                'buttons': ['insert']}},
        'move_from_location': {
            'label': _('move from location'),
            'classes': 'move',
            'property': 'P27',
            'inverse': True,
            'tab': {
                'buttons': ['insert']}},
        'move_to_location': {
            'label': _('move to location'),
            'classes': 'move',
            'property': 'P26',
            'inverse': True,
            'tab': {
                'buttons': ['insert']}},
        'residence': {
            'label': _('residence'),
            'classes': class_groups['actor']['classes'],
            'property': 'P74',
            'inverse': True,
            'tab': {
                'buttons': ['insert']}},
        'begins_in': {
            'label': _('begins in'),
            'classes': class_groups['actor']['classes'],
            'property': 'OA8',
            'inverse': True,
            'tab': {
                'buttons': ['insert']}},
        'ends_in': {
            'label': _('ends in'),
            'classes': class_groups['actor']['classes'],
            'property': 'OA9',
            'inverse': True,
            'tab': {
                'buttons': ['insert']}},
        'reference': standard_relations['reference'],
        'file': standard_relations['file']},
    'display': {
        'buttons': ['copy', 'network', ],
        'form_buttons': ['insert_and_continue', 'insert_continue_sub'],
        'additional_tabs': {'note': {}},
        'network_color': '#FF0000'}}
place['relations']['file']['tab']['additional_columns'] += ['overlay']

feature: dict[str, Any] = {
    'label': _('feature'),
    'attributes': {
        'name': {
            'required': True},
        'dates': {},
        'description': {},
        'location': {}},
    'extra': ['reference_system'],
    'relations': {
        'super': {
            'label': _('super'),
            'classes': 'place',
            'property': 'P46',
            'required': True,
            'inverse': True,
            'mode': 'direct'},
        'source': standard_relations['source'],
        'artifact': artifact_relation,
        'stratigraphic_unit': {
            'classes': 'stratigraphic_unit',
            'property': 'P46',
            'multiple': True,
            'tab': {
                'buttons': ['insert']}},
        'reference': standard_relations['reference'],
        'file': standard_relations['file']},
    'display': {
        'buttons': ['copy', 'network'],
        'form_buttons': ['insert_and_continue', 'insert_continue_sub'],
        'additional_tabs': {'note': {}}}}

stratigraphic_unit: dict[str, Any] = {
    'label': _('stratigraphic unit'),
    'attributes': {
        'name': {
            'required': True},
        'dates': {},
        'description': {},
        'location': {}},
    'extra': ['reference_system'],
    'relations': {
        'super': {
            'label': _('super'),
            'classes': 'feature',
            'property': 'P46',
            'required': True,
            'inverse': True,
            'mode': 'direct'},
        'source': standard_relations['source'],
        'artifact': artifact_relation,
        'reference': standard_relations['reference'],
        'file': standard_relations['file']},
    'display': {
        'buttons': ['copy', 'network', 'stratigraphic_tools'],
        'form_buttons': [
            'insert_and_continue',
            'insert_continue_sub',
            'insert_continue_human_remains'],
        'additional_tabs': {
            'note': {}}}}
