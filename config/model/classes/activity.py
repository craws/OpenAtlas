from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups

model = {
    'attributes': {
        'name': {'required': True},
        'description': {'label': _('content'), 'annotated': True}},
    'relations': {
        'actor': {
            'class': class_groups['actor'],
            'property': ['P11', 'P14', 'P22', 'P23'],
            'multiple': True
        },
        'subs': {
            'class': class_groups['event'],
            'property': 'P9',
            'multiple': True},
        'source': {
            'class': 'source',
            'property': 'P67',
            'inverse': True,
            'multiple': True}
    },
    'display': {
        'buttons': ['copy', 'network'],
        'form': {'insert_and_continue': True},
        'tabs': {
            'subs': {
                'class': class_groups['event'],
                'property': 'P67',
                'multiple': True},
            'source': {
                'class': 'source',
                'property': 'P67',
                'inverse': True,
                'multiple': True},
            'actor': {},
            'reference': {},
            'file': {'additional_columns': ['main image', 'remove']},
            'note': {}}}}
