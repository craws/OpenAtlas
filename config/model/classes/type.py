from flask_babel import lazy_gettext as _

from config.model.class_groups import standard_relations

type_ = {
    'label': _('type'),
    'attributes': {
        'name': {'required': True},
        'dates': {},
        'description': {}},
    'extra': ['reference_system'],
    'relations': {
        'super': {
            'label': _('super'),
            'classes': 'type',
            'property': 'P127',
            'mode': 'direct',
            'required': True},
        'subs': {
            'label': _('subs'),
            'classes': 'type',
            'property': 'P127',
            'multiple': True,
            'inverse': True,
            'tab': {
                'buttons': ['insert'],
                'columns': ['name', 'count', 'description']}},
        'entities': {
            'label': _('entities'),
            'classes': [],
            'property': 'P2',
            'inverse': True,
            'multiple': True,
            'tab': {
                'buttons': ['move']}},
        'reference': standard_relations['reference'],
        'file': standard_relations['file']},
    'display': {
        'buttons': ['selectable'],
        'form_buttons': ['insert_and_continue'],
        'additional_tabs': {'note': {}},
        'additional_information': {'type_information': {}}}}


administrative_unit = {
    'label': _('administrative unit'),
    'attributes': {
        'name': {'required': True},
        'dates': {},
        'description': {}},
    'extra': ['reference_system'],
    'relations': {
        'super': {
            'label': _('super'),
            'classes': 'administrative_unit',
            'property': 'P89',
            'mode': 'direct',
            'required': True},
        'subs': {
            'label': _('subs'),
            'classes': 'administrative_unit',
            'property': 'P89',
            'multiple': True,
            'inverse': True,
            'tab': {
                'buttons': ['insert'],
                'columns': ['name', 'count', 'description']}},
        'entities': {
            'label': _('entities'),
            'classes': 'object_location',
            'property': 'P89',
            'inverse': True,
            'multiple': True,
            'tab': {
                'buttons': ['move']}},
        'reference': standard_relations['reference'],
        'file': standard_relations['file']},
    'display': {
        'buttons': ['selectable'],
        'form_buttons': ['insert_and_continue'],
        'additional_tabs': {'note': {}},
        'additional_information': {'type_information': {}}}}
