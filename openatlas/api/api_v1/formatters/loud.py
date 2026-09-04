from typing import Any

from openatlas.api.api_v1.formatters.lod import (
    format_lod_entities as base_format_lod_entities,
    format_lod_entity as base_format_lod_entity)
from openatlas.models.entity import Entity


def clean_linked_art(data: Any) -> Any:
    if isinstance(data, dict):
        _clean_object(data)
        for value in data.values():
            clean_linked_art(value)
    elif isinstance(data, list):
        for item in data:
            clean_linked_art(item)
    return data


def _clean_object(data: dict[str, Any]) -> None:
    type_ = data.get('type')
    if type_ in {'Name', 'Identifier', 'Dimension', 'TimeSpan'}:
        data.pop('id', None)

    _clean_references(data)
    _clean_part_of(data, type_)
    _remove_nested_property(data, 'classified_as', 'attributed_by')
    data.pop('refers_to', None)

    if type_ == 'DigitalObject':
        data.pop('right_held_by', None)
    _clean_actors(data)
    _move_visual_items(data)

    if type_ in {'Place', 'Site'}:
        data.pop('timespan', None)
        data.pop('former_or_current_location', None)


def _clean_references(data: dict[str, Any]) -> None:
    references = data.get('referred_to_by')
    if not isinstance(references, list):
        return

    references_with_content = []
    for reference in references:
        if isinstance(reference, dict):
            reference.pop('id', None)
            if 'content' in reference:
                references_with_content.append(reference)

    if references_with_content:
        data['referred_to_by'] = references_with_content
    else:
        data.pop('referred_to_by')


def _clean_part_of(data: dict[str, Any], type_: Any) -> None:
    parts = data.get('part_of')
    if not isinstance(parts, list):
        return
    if type_ == 'Type':
        data.pop('part_of')
        return
    _remove_nested_property(data, 'part_of', 'identified_by')


def _remove_nested_property(
        data: dict[str, Any], property_: str, nested_property: str) -> None:
    items = data.get(property_)
    if not isinstance(items, list):
        return
    for item in items:
        if isinstance(item, dict):
            item.pop(nested_property, None)


def _clean_actors(data: dict[str, Any]) -> None:
    creation = data.get('created_by')
    if not isinstance(creation, dict):
        return
    actors = creation.get('carried_out_by')
    if not isinstance(actors, list):
        return
    for actor in actors:
        if isinstance(actor, dict) and actor.get('type') not in {
                'Person', 'Group'}:
            actor['type'] = 'Group'


def _move_visual_items(data: dict[str, Any]) -> None:
    carried_items = data.get('digitally_carries')
    if not isinstance(carried_items, list):
        return

    digital_objects = []
    visual_items = []
    for item in carried_items:
        if not isinstance(item, dict):
            continue
        if item.get('type') == 'VisualItem':
            item.pop('represents', None)
            visual_items.append(item)
        else:
            digital_objects.append(item)

    if visual_items:
        data['digitally_shows'] = (
            data.get('digitally_shows', []) + visual_items)
    if digital_objects:
        data['digitally_carries'] = digital_objects
    else:
        data.pop('digitally_carries')


def format_loud_entity(entity: Entity) -> dict[str, Any]:
    graph = base_format_lod_entity(entity)
    return clean_linked_art(graph)


def format_loud_entities(
        entities: list[Entity],
        pagination: dict[str, Any] | None = None) -> dict[str, Any]:
    graph = base_format_lod_entities(entities, pagination=pagination)
    return clean_linked_art(graph)
