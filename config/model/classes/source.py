from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups

model = {
    'attributes': {
        'name': {
            'required': True},
        'description': {
            'label': _('content'),
            'annotated': True}},
    'relations': {
        'text': {
            'label': _('text'),
            'class': 'source_translation',
            'property': 'P73',
            'multiple': True},
        'actor': {
            'class': class_groups['actor'],
            'property': 'P67',
            'multiple': True},
        'artifact': {
            'class': class_groups['artifact'],
            'property': 'P67',
            'multiple': True},
        'information_carrier': {
            'label': _('information carrier'),
            'class': 'artifact',
            'property': 'P128',
            'inverse': True,
            'multiple': True,
            'mode': 'direct',
            'tooltip': _(
                'Link artifacts as the information carrier of the source')},
        'event': {
            'class': class_groups['event'],
            'property': 'P67',
            'multiple': True},
        'place': {
            'class': class_groups['place'],
            'property': 'P67',
            'multiple': True},
        'reference': {
            'class': class_groups['reference'],
            'property': 'P67',
            'inverse': True,
            'multiple': True},
        'document': {
            'label': _('file'),
            'class': class_groups['file'],
            'property': 'P67',
            'inverse': True,
            'multiple': True}},
    'display': {
        'buttons': ['copy'],
        'form': {
            'insert_and_continue': True},
        'tabs': {
            'text': {},
            'actor': {
                'additional_columns': ['remove'],
                'tooltip': _('mentioned in the source')},
            'artifact': {
                'additional_columns': ['remove'],
                'tooltip': _('mentioned in the source')},
            'event': {
                'additional_columns': ['remove'],
                'tooltip': _('mentioned in the source')},
            'place': {
                'additional_columns': ['remove'],
                'tooltip': _('mentioned in the source')},
            'reference': {
                'additional_columns': ['page', 'update', 'remove'],
                'mode': 'link'},
            'file': {
                'additional_columns': ['main image', 'remove']},
            'note': {}}}}
