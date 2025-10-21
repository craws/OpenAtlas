import copy
from typing import Any

from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups, standard_relations

artifact: dict[str, Any] = {
    'label': _('artifact'),
    'attributes': {
        'name': {
            'required': True},
        'dates': {},
        'description': {},
        'location': {}},
    'extra': ['reference_system'],
    'relations': {
        'actor': {
            'label': _('owned by'),
            'classes': class_groups['actor']['classes'],
            'property': 'P52',
            'mode': 'direct',
            'tab': {
                'buttons': ['insert']}},
        'super': {
            'label': _('super'),
            'classes': ['artifact'] + class_groups['place']['classes'],
            'property': 'P46',
            'inverse': True,
            'mode': 'direct'},
        'source': standard_relations['source'],
        'subs': {
            'label': _('subs'),
            'classes': 'artifact',
            'property': 'P46',
            'multiple': True,
            'tab': {
                'buttons': ['link', 'insert']}},
        'acquisition': {
            'classes': 'acquisition',
            'property': 'P24',
            'inverse': True,
            'multiple': True,
            'tab': {
                'buttons': ['link', 'insert']}},
        'modification': {
            'classes': 'modification',
            'property': 'P31',
            'inverse': True,
            'multiple': True,
            'tab': {
                'buttons': ['link', 'insert']}},
        'move': {
            'classes':  'move',
            'property': 'P25',
            'inverse': True,
            'multiple': True,
            'tab': {
                'buttons': ['link', 'insert']}},
        'production': {
            'classes':  'production',
            'property': 'P108',
            'inverse': True,
            'multiple': True,
            'tab': {
                'buttons': ['link','insert']}},
        'reference': standard_relations['reference'],
        'file': standard_relations['file']},
    'display': {
        'buttons': ['copy', 'network'],
        'form_buttons': ['insert_and_continue'],
        'additional_tabs': {
            'note': {}}}}

human_remains = copy.deepcopy(artifact)
human_remains['label'] = _('human remains')
human_remains['relations']['super']['classes'] = \
    ['human_remains'] + class_groups['place']['classes']
human_remains['relations']['subs']['classes'] = 'human_remains'
