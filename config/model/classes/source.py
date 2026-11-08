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
            'classes': ['text'],
            'property': 'P73',
            'multiple': True,
            'tab': {
                'buttons': ['insert']}},
        'actor': {
            'label': class_groups['actor']['label'],
            'classes': class_groups['actor']['classes'],
            'property': 'P67',
            'multiple': True,
            'tab': {
                'buttons': ['link', 'insert'],
                'tooltip': _('mentioned in the source')}},
        'item': {
            'label': class_groups['item']['label'],
            'classes': class_groups['item']['classes'],
            'property': 'P67',
            'multiple': True,
            'tab': {
                'buttons': ['link', 'insert'],
                'tooltip': _('mentioned in the source')}},
        'information_carrier': {
            'label': _('information carrier'),
            'classes': class_groups['item']['classes'],
            'property': 'P128',
            'inverse': True,
            'multiple': True,
            'mode': 'direct',
            'tooltip':
                _('Link items as the information carrier of the source')},
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
        'file': standard_relations['file'],
        'source_creation': {
            'label': _('creation event'),
            'classes': ['creation'],
            'property': 'P94',
            'inverse': True,
            'mode': 'direct',
            'tooltip': _('Links the creation event of the source')}},
    'display': {
        'buttons': ['copy'],
        'form_buttons': ['insert_and_continue'],
        'additional_tabs': {'note': {}},
        'network_color': '#FFA500'}}

text = {
    'label': _('text'),
    'attributes': {
        'name': {
            'required': True},
        'description': {
            'label': _('content'),
            'annotated': True}},
    'relations': {
        'source': {
            'classes': ['source'],
            'property': 'P73',
            'inverse': True,
            'required': True,
            'mode': 'direct'}},
    'display': {
        'form_buttons': ['insert_and_continue'],
        'additional_tabs': {'note': {}}}}
