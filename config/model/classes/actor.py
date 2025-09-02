from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups, standard_relations

# Todo: Needed for translation, used to differentiate special case to show
# event dates in grey in case no relation dates - should be solved differently
_('first')
_('last')

person = {
    'attributes': {
        'name': {
            'required': True},
        'alias': {},
        'description': {},
        'dates': {}},
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
            'mode': 'tab_directed',
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
            'mode': 'tab_directed',
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
        'residence': {
            'label': _('residence'),
            'classes': 'object_location',
            'properties': 'P74',
            'mode': 'direct'},
        'reference': standard_relations['reference'],
        'file': standard_relations['file']},
    'display': {
        'buttons': ['copy', 'network'],
        'form': {
            'insert_and_continue': True},
        'additional_tabs': {
            'note': {}}}}
