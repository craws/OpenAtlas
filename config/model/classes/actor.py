import copy

from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups, standard_relations

person = {
    'attributes': {
        'name': {
            'required': True},
        'alias': {},
        'description': {},
        'date': {}},
    'relations': {
        'begins_in': {
            'label': _('born in'),
            'classes': 'object_location',
            'properties': 'OA8',
            'mode': 'direct'},
        'ends_in': {
            'label': _('died in'),
            'classes': 'object_location',
            'properties': 'OA9',
            'mode': 'direct'},
        'event': {
            'label': _('event'),
            'classes': class_groups['event']['classes'],
            'properties': ['P11', 'P14', 'P22', 'P23'],
            'inverse': True,
            'multiple': True},
        'residence': {
            'label': _('residence'),
            'classes': 'object_location',
            'properties': 'P74',
            'mode': 'direct'},
        'source': standard_relations['source']['relation'],
        'file': standard_relations['file']['relation'],
        'reference': standard_relations['reference']['relation']},
    'display': {
        'buttons': ['copy', 'network'],
        'form': {'insert_and_continue': True},
        'tabs': {
            'source': standard_relations['source']['tab'],
            'event': {
                'columns': [
                    'name', 'class', 'activity', 'involvement', 'first',
                    'last', 'comment', 'update', 'remove'],
                'buttons': ['link']},
            'reference': standard_relations['reference']['tab'],
            'file': standard_relations['file']['tab'],
            'note': {}}}}
