from typing import Any

from flask_babel import lazy_gettext as _

view_class_mapping = {
    'actor': ['person', 'group'],
    'event': [
        'activity', 'acquisition', 'creation', 'event', 'modification', 'move',
        'production'],
    'file': ['file'],
    'artifact': ['artifact', 'human_remains'],
    'place': ['feature', 'place', 'stratigraphic_unit'],
    'reference': ['bibliography', 'edition', 'external_reference'],
    'reference_system': ['reference_system'],
    'source': ['source'],
    'type': ['administrative_unit', 'type'],
    'source_translation': ['source_translation']}

model: dict[str, Any] = {
    'acquisition': {
        'attributes': {
            'name': {'required': True},
            'info': {},
            'end': {'label': 'readout', 'required': True},
            'begin': {'label': 'published'}},
        'relations': {},
        'display': {'buttons': ['network']}},
    'activity': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'actor_function': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'actor_relation': {
        'attributes': {}},
    'administrative_unit': {
        'attributes': {}},
    'appellation': {
        'attributes': {}},
    'artifact': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'bibliography': {
        'attributes': {}},
    'creation': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'edition': {
        'attributes': {}},
    'event': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'external_reference': {
        'attributes': {}},
    'feature': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'file': {
        'attributes': {}},
    'group': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'human_remains': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'involvement': {
        'attributes': {}},
    'modification': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'move': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'object_location': {
        'attributes': {}},
    'person': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'place': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'production': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'reference_system': {
        'attributes': {}},
    'source': {
        'attributes': {
            'name': {'required': True},
            'description': {'label': _('content'), 'annotated': True}},
        'relations': {
            'text': {
                'class': 'source_translation',
                'property': 'P73',
                'multiple': True},
            'actor': {
                'class': view_class_mapping['actor'],
                'property': 'P67',
                'multiple': True},
            'artifact': {
                'class': view_class_mapping['artifact'],
                'property': 'P67',
                'multiple': True},
            'event': {
                'class': view_class_mapping['event'],
                'property': 'P67',
                'multiple': True},
            'place': {
                'class': view_class_mapping['place'],
                'property': 'P67',
                'multiple': True},
        },
        'display': {
            'tabs': {
                'text': {},
                'actor': {
                    'additional_columns': ['remove'],
                    'tooltip': _('mentioned in the source')},
                'artifact': {
                    'additional_columns': ['remove'],
                    'tooltip': _('mentioned in the source')},
                'event': {
                    'additional_columns': ['remove'],
                    'tooltip': _('mentioned in the source')},
                'place': {
                    'additional_columns': ['remove'],
                    'tooltip': _('mentioned in the source')},
                'reference': {},
                'file': {},
                'note': {}}}},
    'source_translation': {
        'attributes': {}},
    'stratigraphic_unit': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'type': {
        'attributes': {}},
    'type_tools': {
        'attributes': {}}}
