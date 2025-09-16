from typing import Any

from config.model.classes import (
    actor, artifact, event, reference, source, type)

model: dict[str, Any] = {
    'acquisition': event.acquisition,
    'activity': event.activity,
    'administrative_unit': {
        'attributes': {}},
    'appellation': {
        'attributes': {}},
    'artifact': artifact.artifact,
    'bibliography': reference.bibliography,
    'creation': event.creation,
    'edition': reference.edition,
    'event': event.event,
    'external_reference': reference.external_reference,
    'feature': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'file': {
        'attributes': {}},
    'group': actor.group,
    'human_remains': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'modification': event.modification,
    'move': event.move,
    'object_location': {
        'attributes': {}},
    'person': actor.person,
    'place': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'production': event.production,
    'reference_system': {
        'attributes': {}},
    'source': source.source,
    'source_translation': source.source_translation,
    'stratigraphic_unit': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'type': type.type_,
    'type_tools': {
        'attributes': {}}}
