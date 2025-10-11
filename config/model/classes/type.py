from flask_babel import lazy_gettext as _

from config.model.class_groups import standard_relations

type_ = {
    'label': _('type'),
    'attributes': {
        'name': {
            'required': True},
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
               'buttons': ['insert']}},
        'entities': {
            'label': _('entities'),
            'classes': [],
            'property': 'P2',
            'inverse': True,
            'multiple': True},
        'reference': standard_relations['reference'],
        'file': standard_relations['file']},
    'display': {
        'buttons': ['selectable'],
        'form': {
            'insert_and_continue': True},
        'additional_tabs': {
            'note': {}}}}
