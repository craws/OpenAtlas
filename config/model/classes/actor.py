import copy

from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups

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
            'inverse': True
        }},
    'display': {
        'buttons': ['copy', 'network'],
        'form': {'insert_and_continue': True},
        'tabs': {
            'source': {
                'additional_columns': ['remove'],
                'buttons': ['link', 'insert']},
            'reference': {
                'mode': 'link',
                'additional_columns': ['page', 'update', 'remove'],
                'buttons': ['link', 'insert']},
            'file': {
                'additional_columns': ['main image', 'remove'],
                'buttons': ['link', 'insert']},
            'note': {}}}}
