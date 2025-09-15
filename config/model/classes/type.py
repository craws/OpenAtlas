from flask_babel import lazy_gettext as _

from config.model.class_groups import standard_relations

type_ = {
    'attributes': {
        'name': {
            'required': True},
        'description': {},
        'dates': {}},
    'relations': {
        'super': {
            'label': _('super'),
            'classes': 'type',
            'properties': 'P127',
            'mode': 'direct',
            'required': True},
        'subs': {
            'label': _('subs'),
            'classes': 'type',
            'properties': 'P127',
            'multiple': True,
            'inverse': True,
            'tab': {
               'buttons': ['insert']}},
        'entities': {
            'label': _('entities'),
            'classes': [],
            'properties': 'P2',
            'inverse': True,
            'multiple': True},
        'file': standard_relations['file'],
        'reference': standard_relations['reference']},
    'display': {
        'buttons': ['selectable'],
        'form': {
            'insert_and_continue': True},
        'additional_tabs': {
            'note': {}}}}
