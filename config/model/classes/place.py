from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups, standard_relations

relations = {
    'artifact': {
        'label': _('artifact'),
        'classes': class_groups['artifact']['classes'],
        'property': 'P46',
        'multiple': True,
        'tab': {
            'buttons': ['link', 'insert']}}}

place = {
    'label': _('place'),
    'attributes': {
        'name': {
            'required': True},
        'alias': {},
        'dates': {},
        'description': {},
        'location': {}},
    'extra': ['reference_system'],
    'relations': {
        'source': standard_relations['source'],
        'artifact': relations['artifact'],
        'reference': standard_relations['reference'],
        'file': standard_relations['file']},
    'display': {
        'buttons': ['copy', 'network'],
        'form': {
            'insert_and_continue': True},
        'additional_tabs': {
            'note': {}}}}

feature = {
    'label': _('feature'),
    'attributes': {
        'name': {
            'required': True},
        'dates': {},
        'description': {},
        'location': {}},
    'extra': ['reference_system'],
    'relations': {
        'source': standard_relations['source'],
        'artifact': relations['artifact'],
        'reference': standard_relations['reference'],
        'file': standard_relations['file']},
    'display': {
        'buttons': ['copy', 'network'],
        'form': {
            'insert_and_continue': True},
        'additional_tabs': {
            'note': {}}}}
