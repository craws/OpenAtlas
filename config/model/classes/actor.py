import copy

from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups

'relation', 'member_of', 'member', 'artifact'

person = {
    'attributes': {
        'name': {
            'required': True},
        'alias': {},
        'description': {},
        'date': {}},
    'relations': {
        'residence': {
            'label': _('residence'),
            'class': 'object_location',
            'property': 'P74',
            'mode': 'direct'},
        'begins_in': {
            'label': _('born in'),
            'class': 'object_location',
            'property': 'OA8',
            'mode': 'direct'},
        'ends_in': {
            'label': _('died in'),
            'class': 'object_location',
            'property': 'OA9',
            'mode': 'direct'},
        'source': {
            'class': 'source',
            'property': 'P67',
            'multiple': True,
            'inverse': True},
        'event': {
            'label': _('event'),
            'class': class_groups['event']['classes'],
            'property': ['P11', 'P14', 'P22', 'P23'],
            'inverse': True,
            'multiple': True},
        'file': {
            'label': _('file'),
            'class': class_groups['file']['classes'],
            'property': 'P67',
            'inverse': True,
            'multiple': True},
        'reference': {
            'label': _('reference'),
            'class': class_groups['reference']['classes'],
            'property': 'P67',
            'inverse': True,
            'multiple': True},
    },
    'display': {
        'buttons': ['copy', 'network'],
        'form': {'insert_and_continue': True},
        'tabs': {
            'source': {
                'additional_columns': ['remove'],
                'buttons': ['link', 'insert']},
            'event': {
                'additional_columns': ['update', 'remove'],
                'buttons': ['link']},
            'reference': {
                'mode': 'link',
                'additional_columns': ['page', 'update', 'remove'],
                'buttons': ['link', 'insert']},
            'file': {
                'additional_columns': ['main image', 'remove'],
                'buttons': ['link', 'insert']},
            'note': {}}}}
