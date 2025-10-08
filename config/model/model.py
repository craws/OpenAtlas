from typing import Any

from flask_babel import lazy_gettext as _

from config.model.classes import (
    actor, artifact, event, file, reference, reference_system, source, type)

# Todo: Needed for translation, to be removed after implemented
_('first'), _('last')  # event dates in grey in case no relation dates
_('administrative unit')
_('feature')
_('involvement')
_('object location')
_('type tools')
_('page')

model: dict[str, Any] = {
    'acquisition': event.acquisition,
    'activity': event.activity,
    'administrative_unit': {
        'attributes': {}},
    'appellation': {
        'attributes': {}},
    'artifact': artifact.artifact,
    'bibliography': reference.bibliography,
    'edition': reference.edition,
    'external_reference': reference.external_reference,
    'feature': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'file': file.file,
    'group': actor.group,
    'human_remains': artifact.human_remains,
    'modification': event.modification,
    'move': event.move,
    'object_location': {
        'attributes': {}},
    'person': actor.person,
    'place': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'production': event.production,
    'reference_system': reference_system.reference_system,
    'source': source.source,
    'source_translation': source.source_translation,
    'stratigraphic_unit': {
        'attributes': {},
        'display': {'buttons': ['network']}},
    'type': type.type_,
    'type_tools': {
        'attributes': {}}}
