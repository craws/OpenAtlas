import copy
from typing import Any

from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups


def get_relation(classes: str | list[str]) -> dict[str, Any]:
    _('page')  # Needed for translations
    return {
        'classes': classes,
        'property': 'P67',
        'multiple': True,
        'additional_fields': ['page'],
        'tab': {
            'columns': ['name', 'class', 'type', 'page', 'description'],
            'buttons': ['link', 'insert']}}


bibliography = {
    'label': _('bibliography'),
    'attributes': {
        'name': {
            'required': True},
        'description': {}},
    'relations': {
        'source': get_relation('source'),
        'event': get_relation(class_groups['event']['classes']),
        'actor': get_relation(class_groups['actor']['classes']),
        'place': get_relation('place'),
        'artifact': get_relation(class_groups['artifact']['classes']),
        'type': {
            'label': class_groups['type']['label'],
            'classes': class_groups['type']['classes'],
            'property': 'P67',
            'multiple': True,
            'additional_fields': ['page'],
            'tab': {
                'columns': ['name', 'class', 'page', 'description']}},
        'file': {
            'label': class_groups['file']['label'],
            'classes': class_groups['file']['classes'],
            'property': 'P67',
            'multiple': True,
            'additional_fields': ['page'],
            'tab': {
                'buttons': ['link', 'insert'],
                'columns': ['name', 'type', 'page', 'description']}}},
    'display': {
        'buttons': ['copy'],
        'form_buttons': ['insert_and_continue'],
        'additional_tabs': {
            'note': {}}}}

edition = copy.deepcopy(bibliography)
edition['label'] = _('edition')

external_reference = copy.deepcopy(bibliography)
external_reference['label'] = _('external reference')
external_reference['attributes']['name'] = {
    'label': _('URL'),
    'format': 'url',
    'required': True}
