from typing import Any

from config.model.classes import source, source_translation

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
    'source': source.model,
    'source_translation': source_translation.model,
    'stratigraphic_unit': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'type': {
        'attributes': {}},
    'type_tools': {
        'attributes': {}}}
