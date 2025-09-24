import copy

from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups, standard_relations

# Todo: Needed for translation, to be removed after implemented
_('first'), _('last')  # event dates in grey in case no relation dates
_('administrative unit')
_('feature')
_('involvement')
_('object location')
_('type tools')

group = {
    'label': _('group'),
    'attributes': {
        'name': {
            'required': True},
        'alias': {},
        'description': {},
        'dates': {}},
    'relations': {
        'residence': {
            'label': _('residence'),
            'classes': 'object_location',
            'property': 'P74',
            'mode': 'direct'},
        'begins_in': {
            'label': _('born in'),
            'classes': 'object_location',
            'property': 'OA8',
            'mode': 'direct'},
        'ends_in': {
            'label': _('died in'),
            'classes': 'object_location',
            'property': 'OA9',
            'mode': 'direct'},
        'source': standard_relations['source'],
        'performed': {
            'label': _('performed'),
            'classes': class_groups['event']['classes'],
            'property': 'P14',
            'inverse': True,
            'multiple': True,
            'type': 'Involvement',
            'additional_fields': ['dates', 'description'],
            'tab': {
                'columns': [
                    'name',
                    'class',
                    'involvement',
                    'begin',
                    'end',
                    'description'],
                'buttons': ['link']}},
        'participated': {
            'label': _('participated'),
            'classes': class_groups['event']['classes'],
            'property': 'P11',
            'inverse': True,
            'multiple': True,
            'type': 'Involvement',
            'additional_fields': ['dates', 'description'],
            'tab': {
                'columns': [
                    'name',
                    'class',
                    'involvement',
                    'begin',
                    'end',
                    'description'],
                'buttons': ['link']}},
        'relative': {
            'label': _('relation'),
            'classes': 'person',
            'property': 'OA7',
            'type': 'Actor relation',
            'additional_fields': ['domain', 'dates', 'description'],
            'tab': {
                'buttons': ['link', 'insert'],
                'columns': [
                    'name',
                    'relation',
                    'begin',
                    'end',
                    'description']}},
        'member_of': {
            'label': _('member of'),
            'classes': 'group',
            'property': 'P107',
            'inverse': True,
            'type': 'Actor function',
            'additional_fields': ['dates', 'description'],
            'tab': {
                'buttons': ['link', 'insert'],
                'columns': [
                    'name',
                    'function',
                    'begin',
                    'end',
                    'description']}},
        'member': {
            'label': _('member'),
            'classes': class_groups['actor']['classes'],
            'property': 'P107',
            'type': 'Actor function',
            'additional_fields': ['dates', 'description'],
            'tab': {
                'buttons': ['link', 'insert'],
                'columns': [
                    'name',
                    'function',
                    'begin',
                    'end',
                    'description']}},
        'artifact': {
            'label': class_groups['artifact']['label'],
            'classes': class_groups['artifact']['classes'],
            'property': 'P52',
            'inverse': True,
            'tab': {
                'buttons': ['insert'],
                'columns': [
                    'name',
                    'class',
                    'type',
                    'begin',
                    'end',
                    'description']}},
        'reference': standard_relations['reference'],
        'file': standard_relations['file']},
    'display': {
        'buttons': ['copy', 'network'],
        'form': {
            'insert_and_continue': True},
        'additional_tabs': {
            'note': {}}}}

person = copy.deepcopy(group)
person['label'] = _('person')
del person['relations']['member']
