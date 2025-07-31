from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups

model = {
    'attributes': {
        'name': {'required': True},
        'description': {},
        'date': {}},
    'relations': {
        'actor': {
            'class': class_groups['actor'],
            'property': ['P11', 'P14', 'P22', 'P23'],
            'multiple': True},
        'subs': {
            'class': class_groups['event'],
            'property': 'P9',
            'multiple': True},
        'source': {
            'class': 'source',
            'property': 'P67',
            'inverse': True,
            'multiple': True},
        'file': {
            'class': class_groups['file'],
            'property': 'P67',
            'inverse': True,
            'multiple': True},
        'reference': {
            'class': class_groups['reference'],
            'property': 'P67',
            'inverse': True,
            'multiple': True},
        'sub_event': {
            'class': class_groups['event'],
            'property': 'P9',
            'label': _('sub event')},
        'sub_event_of': {
            'class': class_groups['event'],
            'property': 'P9',
            'inverse': True,
            'mode': 'direct',
            'label': _('sub event of')},
        'succeeding_event': {
            'class': class_groups['event'],
            'property': 'P134',
            'inverse': True,
            'mode': 'display',
            'label': _('succeeding event')},
        'preceding_event': {
            'label': _('preceding event'),
            'class': class_groups['event'],
            'property': 'P134',
            'mode': 'direct'},
        'location': {
            'label': _('location'),
            'class': 'object_location',
            'property': 'P7',
            'mode': 'direct'},
        'object': {
            'label': _('modified object'),
            'class': class_groups['artifact'],
            'property': 'P31',
            'multiple': True,
            'mode': 'direct'},
        'place': {
            'label': _('modified place'),
            'class': 'place',
            'property': 'P31',
            'multiple': True,
            'mode': 'direct'}},
    'display': {
        'buttons': ['copy', 'network'],
        'form': {'insert_and_continue': True},
        'tabs': {
            'subs': {},
            'source': {'additional_columns': ['remove']},
            'actor': {
                'mode': 'link',
                'columns': [
                    'name', 'class', 'activity', 'involvement', 'first',
                    'last', 'comment', 'update', 'remove']},
            'reference': {
                'mode': 'link',
                'additional_columns': ['page', 'update', 'remove']},
            'file': {'additional_columns': ['main image', 'remove']},
            'note': {}}}}
