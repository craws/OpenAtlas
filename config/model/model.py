from typing import Any

from flask_babel import lazy_gettext as _

from config.model.classes import (
    actor, event, file, item, place, reference, reference_system, source,
    type_)

model: dict[str, Any] = {
    'acquisition': event.acquisition,
    'activity': event.activity,
    'administrative_unit': type_.administrative_unit,
    'alias': {'attributes': {}},
    'artifact': item.artifact,
    'bibliography': reference.bibliography,
    'creation': event.creation,
    'edition': reference.edition,
    'external_reference': reference.external_reference,
    'feature': place.feature,
    'file': file.file,
    'group': actor.group,
    'human_remains': item.human_remains,
    'modification': event.modification,
    'move': event.move,
    'object_location': {'label': _('object location'), 'attributes': {}},
    'person': actor.person,
    'place': place.place,
    'production': event.production,
    'reference_system': reference_system.reference_system,
    'source': source.source,
    'stratigraphic_unit': place.stratigraphic_unit,
    'text': source.text,
    'type': type_.type_,
    'type_tools': {'label': _('type tools'), 'attributes': {}}}
