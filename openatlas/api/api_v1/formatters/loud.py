from typing import Any

from openatlas.api.api_v1.formatters.lod import (
    format_lod_entities as base_format_lod_entities,
    format_lod_entity as base_format_lod_entity)
from openatlas.models.entity import Entity


def clean_linked_art(data: Any) -> Any:
    if isinstance(data, dict):
        type_ = data.get('type')
        if type_ in [
                'Name',
                'Identifier',
                'Dimension',
                'TimeSpan'] and 'id' in data:
            del data['id']

        if 'referred_to_by' in data \
                and isinstance(data['referred_to_by'], list):
            new_refs = []
            for item in data['referred_to_by']:
                if isinstance(item, dict):
                    if 'id' in item:
                        del item['id']
                    if 'content' in item:
                        new_refs.append(item)
            if new_refs:
                data['referred_to_by'] = new_refs
            else:
                del data['referred_to_by']

        if 'part_of' in data and isinstance(data['part_of'], list):
            if type_ == 'Type':
                del data['part_of']
            else:
                for item in data['part_of']:
                    if isinstance(item, dict) and 'identified_by' in item:
                        del item['identified_by']

        if 'classified_as' in data and isinstance(data['classified_as'], list):
            for item in data['classified_as']:
                if isinstance(item, dict) and 'attributed_by' in item:
                    del item['attributed_by']

        if 'refers_to' in data:
            del data['refers_to']

        if 'right_held_by' in data and type_ == 'DigitalObject':
            del data['right_held_by']

        if 'created_by' in data and isinstance(data['created_by'], dict):
            cb = data['created_by']
            if 'carried_out_by' in cb and isinstance(cb['carried_out_by'], list):
                for actor in cb['carried_out_by']:
                    if isinstance(actor, dict) \
                            and actor.get('type') not in ['Person', 'Group']:
                        actor['type'] = 'Group'

        if 'digitally_carries' in data \
                and isinstance(data['digitally_carries'], list):
            new_carries = []
            new_shows = []
            for item in data['digitally_carries']:
                if isinstance(item, dict):
                    if item.get('type') == 'VisualItem':
                        if 'represents' in item:
                            del item['represents']
                        new_shows.append(item)
                    else:
                        new_carries.append(item)

            if new_shows:
                data['digitally_shows'] = data.get('digitally_shows', []) \
                                          + new_shows

            if new_carries:
                data['digitally_carries'] = new_carries
            else:
                del data['digitally_carries']

        if type_ in ['Place', 'Site']:
            if 'timespan' in data:
                del data['timespan']
            if 'former_or_current_location' in data:
                del data['former_or_current_location']

        for k, v in list(data.items()):
            clean_linked_art(v)
    elif isinstance(data, list):
        for item in data:
            clean_linked_art(item)
    return data


def format_loud_entity(entity: Entity) -> dict[str, Any]:
    graph = base_format_lod_entity(entity)
    return clean_linked_art(graph)


def format_loud_entities(
        entities: list[Entity],
        pagination: dict[str, Any] | None = None) -> dict[str, Any]:
    graph = base_format_lod_entities(entities, pagination=pagination)
    return clean_linked_art(graph)
