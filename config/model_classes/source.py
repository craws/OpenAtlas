from flask_babel import lazy_gettext as _


def source_model(mapping):
    return {
        'attributes': {
            'name': {'required': True},
            'description': {'label': _('content'), 'annotated': True}},
        'relations': {
            'text': {
                'class': 'source_translation',
                'property': 'P73',
                'multiple': True},
            'actor': {
                'class': mapping['actor'],
                'property': 'P67',
                'multiple': True},
            'artifact': {
                'class': mapping['artifact'],
                'property': 'P67',
                'multiple': True},
            'information_carrier': {
                'class': ['artifact'],
                'property': 'P128',
                'inverse': True,
                'multiple': True,
                'mode': 'direct',
                'label': _('information carrier'),
                'description': _(
                    'Link artifacts as the information carrier of the source')
            },
            'event': {
                'class': mapping['event'],
                'property': 'P67',
                'multiple': True},
            'place': {
                'class': mapping['place'],
                'property': 'P67',
                'multiple': True},
            'reference': {
                'class': mapping['reference'],
                'property': 'P67',
                'inverse': True,
                'multiple': True},
            'file': {
                'class': mapping['file'],
                'property': 'P67',
                'inverse': True,
                'multiple': True}},
        'display': {
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
                    'additional_columns': ['page', 'remove', 'update']},
                'file': {'additional_columns': ['main image', 'remove']},
                'note': {}}}}
