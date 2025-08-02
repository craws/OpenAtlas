from typing import Any

from config.model.classes import (
    event, source, source_translation)

model: dict[str, Any] = {
    'acquisition': event.acquisition,
    'activity': event.activity,
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
    'creation': event.creation,
    'edition': {
        'attributes': {}},
    'event': event.event,
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
    'modification': event.modification,
    'move': event.move,
    'object_location': {
        'attributes': {}},
    'person': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'place': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'production': event.production,
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
