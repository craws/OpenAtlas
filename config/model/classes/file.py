from typing import Any

from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups, standard_relations


def relation(name: str) -> dict[str, Any]:
    return {
        'classes': class_groups[name]['classes'],
        'property': 'P67',
        'multiple': True,
        'tab': {'buttons': ['link', 'insert']}}


file: dict[str, Any] = {
    'label': _('file'),
    'attributes': {
        'name': {
            'required': True},
        'file': {
            'required': True},
        'public': {
            'label': _('public sharing allowed')},
        'creator': {
            'label': _('creator')},
        'license_holder': {
            'label': _('license holder')},
        'description': {}},
    'extra': ['reference_system'],
    'relations': {
        'source': relation('source'),
        'event': relation('event'),
        'actor': relation('actor'),
        'place': relation('place'),
        'artifact': relation('artifact'),
        'reference': standard_relations['reference'],
        'type': relation('type')},
    'display': {
        'buttons': ['download'],
        'form_buttons': ['insert_and_continue'],
        'additional_tabs': {'note': {}},
        'additional_information': {
            'file_size': {'label': _('size')},
            'file_extension': {'label': _('extension')}}}}
