from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups, standard_relations

source = {
    'label': _('source'),
    'attributes': {
        'name': {
            'required': True},
        'description': {
            'label': _('content'),
            'annotated': True}},
    'extra': ['reference_system'],
    'relations': {
        'text': {
            'label': _('text'),
            'classes': 'source_translation',
            'property': 'P73',
            'multiple': True,
            'tab':{
                'buttons': ['insert']}},
        'actor': {
            'label': class_groups['actor']['label'],
            'classes': class_groups['actor']['classes'],
            'property': 'P67',
            'multiple': True,
            'tab': {
                'buttons': ['link', 'insert'],
                'tooltip': _('mentioned in the source')}},
        'artifact': {
            'label': class_groups['artifact']['label'],
            'classes': class_groups['artifact']['classes'],
            'property': 'P67',
            'multiple': True,
            'tab': {
                'buttons': ['link', 'insert'],
                'tooltip': _('mentioned in the source')}},
        'information_carrier': {
            'label': _('information carrier'),
            'classes': 'artifact',
            'property': 'P128',
            'inverse': True,
            'multiple': True,
            'mode': 'direct',
            'tooltip': _(
                'Link artifacts as the information carrier of the source')},
        'event': {
            'label': class_groups['event']['label'],
            'classes': class_groups['event']['classes'],
            'property': 'P67',
            'multiple': True,
            'tab': {
                'buttons': ['link', 'insert'],
                'tooltip': _('mentioned in the source')}},
        'place': {
            'label': class_groups['place']['label'],
            'classes': class_groups['place']['classes'],
            'property': 'P67',
            'multiple': True,
            'tab': {
                'buttons': ['link', 'insert'],
                'tooltip': _('mentioned in the source')}},
        'reference': standard_relations['reference'],
        'file': standard_relations['file']},
    'display': {
        'buttons': ['copy'],
        'form': {
            'insert_and_continue': True},
        'additional_tabs': {
            'note': {}}}}

source_translation = {
    'label': _('source translation'),
    'attributes': {
        'name': {
            'required': True},
        'description': {
            'label': _('content'),
            'annotated': True}},
    'relations': {
        'source': {
            'classes': 'source',
            'property': 'P73',
            'inverse': True,
            'required': True,
            'mode': 'direct'}},
    'display': {
        'form': {
            'insert_and_continue': True},
        'additional_tabs': {
            'note': {}}}}
