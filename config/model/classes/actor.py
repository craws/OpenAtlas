import copy
from typing import Any

from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups, standard_relations

group: dict[str, Any] = {
    'label': _('group'),
    'attributes': {
        'name': {
            'required': True},
        'alias': {},
        'dates': {},
        'description': {}},
    'extra': ['reference_system'],
    'relations': {
        'residence': {
            'label': _('residence'),
            'classes': 'object_location',
            'property': 'P74',
            'mode': 'direct',
            'add_dynamic': True},
        'begins_in': {
            'label': _('begins in'),
            'classes': 'object_location',
            'property': 'OA8',
            'mode': 'direct',
            'add_dynamic': True},
        'ends_in': {
            'label': _('ends in'),
            'classes': 'object_location',
            'property': 'OA9',
            'mode': 'direct',
            'add_dynamic': True},
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
                    'name', 'class', 'involvement',
                    'begin', 'end', 'description'],
                'buttons': ['link', 'insert']}},
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
                    'name', 'class', 'involvement',
                    'begin', 'end', 'description'],
                'buttons': ['link', 'insert']}},
        'relative': {
            'label': _('relation'),
            'classes': class_groups['actor']['classes'],
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
        'form_buttons': ['insert_and_continue'],
        'additional_tabs': {'note': {}},
        'network_color': '#34623C'}}

person = copy.deepcopy(group)
person['label'] = _('person')
person['display']['network_color'] = '#34B522'
person['relations']['begins_in']['label'] = _('born in')
person['relations']['ends_in']['label'] = _('died in')
del person['relations']['member']
