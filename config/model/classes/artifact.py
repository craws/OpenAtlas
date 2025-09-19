from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups, standard_relations

artifact = {
    'attributes': {
        'name': {
            'required': True},
        'description': {},
        'dates': {}},
    'relations': {
        'actor': {
            'label': _('owned by'),
            'classes': class_groups['actor']['classes'],
            'properties': 'P52',
            'mode': 'direct',
            'tab': {
                'buttons': ['insert']}},
        'super': {
            'label': _('super'),
            'classes': ['artifact'] + class_groups['place']['classes'],
            'properties': 'P46',
            'inverse': True,
            'mode': 'direct'},
        'source': standard_relations['source'],
        'event': {
            'classes': ['acquisition', 'modification', 'move', 'production'],
            'properties': ['P24', 'P25', 'P31', 'P108'],
            'inverse': True,
            'multiple': True,
            'tab': {
                'buttons': ['insert']}},
        'subs': {
            'label': _('subs'),
            'classes': 'artifact',
            'properties': 'P46',
            'multiple': True,
            'tab': {
                'buttons': ['link', 'insert']}},
        'reference': standard_relations['reference'],
        'file': standard_relations['file']},
    'display': {
        'buttons': ['copy', 'network'],
        'form': {
            'insert_and_continue': True},
        'additional_tabs': {
            'note': {}}}}
