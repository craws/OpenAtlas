import copy
from typing import Any

from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups, standard_relations


def get_relation(classes: str | list[str]) -> dict[str, Any]:
    return {
        'classes': classes,
        'properties': 'P67',
        'multiple': True,
        'additional_fields': ['page'],
        'tab': {
            'columns': ['name', 'class', 'type', 'page', 'description'],
            'buttons': ['link', 'insert']}}


bibliography = {
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
            'classes': class_groups['type']['classes'],
            'properties': 'P67',
            'multiple': True,
            'additional_fields': ['page'],
            'tab': {
                'columns': ['name', 'class', 'type', 'page', 'description'],
                'buttons': ['link']}},
        'file': standard_relations['file']},
    'display': {
        'buttons': ['copy'],
        'form': {
            'insert_and_continue': True},
        'additional_tabs': {
            'note': {}}}}

edition = copy.deepcopy(bibliography)

# Todo: solve URL field with validatior instead name field
external_reference = copy.deepcopy(bibliography)
external_reference['attributes']['name'] = {
    'label': _('URL'),
    'required': True}
