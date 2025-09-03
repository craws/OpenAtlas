import copy

from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups, standard_relations

# Todo: Needed for translation, used to differentiate special case to show
# event dates in grey in case no relation dates - should be solved differently
_('first')
_('last')

group = {
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
            'properties': 'P74',
            'mode': 'direct'},
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
        'source': standard_relations['source'],
        'event': {
            'label': _('event'),
            'classes': class_groups['event']['classes'],
            'properties': ['P11', 'P14', 'P22', 'P23'],
            'inverse': True,
            'multiple': True,
            'tab': {
                'columns': [
                    'name',
                    'class',
                    'activity',
                    'involvement',
                    'first',
                    'last',
                    'description'],
                'buttons': ['link']}},
        'relative': {
            'label': _('relation'),
            'classes': 'person',
            'properties': 'OA7',
            'type': 'Actor relation',
            'additional_fields': [
                'domain',
                'dates',
                'description'],
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
            'properties': 'P107',
            'inverse': True,
            'type': 'Actor function',
            'additional_fields': [
                'domain',
                'dates',
                'description'],
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
            'properties': 'P107',
            'type': 'Actor function',
            'additional_fields': [
                'domain',
                'dates',
                'description'],
            'tab': {
                'buttons': ['link', 'insert'],
                'columns': [
                    'name',
                    'function',
                    'begin',
                    'end',
                    'description']}},
        'artifact': {
            'label': _('artifact'),
            'classes': class_groups['artifact']['classes'],
            'properties': 'P52',
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
del person['relations']['member']
