from typing import Any

from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups, standard_relations

file: dict[str, Any] = {
    'label': _('file'),
    'attributes': {
        'name': {
            'required': True},
        'description': {},},
    'relations': {
        'actor': {
            'label': _('owned by'),
            'classes': class_groups['actor']['classes'],
            'property': 'P52',
            'mode': 'direct',
            'tab': {
                'buttons': ['insert']}},
        'reference': standard_relations['reference']},
    'display': {
        'buttons': ['download'],
        'form': {
            'insert_and_continue': True},
        'additional_tabs': {
            'note': {}}}}
