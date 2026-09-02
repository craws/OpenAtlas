from typing import Any

from openatlas.api.api_v1.formatters.lod import (
    format_lod_entities as base_format_lod_entities,
    format_lod_entity as base_format_lod_entity)
from openatlas.models.entity import Entity


def clean_linked_art(d: Any) -> Any:
    if isinstance(d, dict):
        t = d.get('type')
        if t in ['Name', 'Identifier', 'Dimension', 'TimeSpan'] and 'id' in d:
            del d['id']

        if 'referred_to_by' in d and isinstance(d['referred_to_by'], list):
            new_refs = []
            for item in d['referred_to_by']:
                if isinstance(item, dict):
                    if 'id' in item:
                        del item['id']
                    if 'content' in item:
                        new_refs.append(item)
            if new_refs:
                d['referred_to_by'] = new_refs
            else:
                del d['referred_to_by']

        if 'part_of' in d and isinstance(d['part_of'], list):
            if t == 'Type':
                del d['part_of']
            else:
                for item in d['part_of']:
                    if isinstance(item, dict) and 'identified_by' in item:
                        del item['identified_by']

        if 'classified_as' in d and isinstance(d['classified_as'], list):
            for item in d['classified_as']:
                if isinstance(item, dict) and 'attributed_by' in item:
                    del item['attributed_by']

        if 'refers_to' in d:
            del d['refers_to']

        if 'right_held_by' in d and t == 'DigitalObject':
            del d['right_held_by']

        if 'created_by' in d and isinstance(d['created_by'], dict):
            cb = d['created_by']
            if 'carried_out_by' in cb and isinstance(cb['carried_out_by'], list):
                for actor in cb['carried_out_by']:
                    if isinstance(actor, dict) and actor.get('type') not in ['Person', 'Group']:
                        actor['type'] = 'Group'

        if 'digitally_carries' in d and isinstance(d['digitally_carries'], list):
            new_carries = []
            new_shows = []
            for item in d['digitally_carries']:
                if isinstance(item, dict):
                    if item.get('type') == 'VisualItem':
                        if 'represents' in item:
                            del item['represents']
                        new_shows.append(item)
                    else:
                        new_carries.append(item)

            if new_shows:
                d['digitally_shows'] = d.get('digitally_shows', []) + new_shows

            if new_carries:
                d['digitally_carries'] = new_carries
            else:
                del d['digitally_carries']

        if t in ['Place', 'Site']:
            if 'timespan' in d:
                del d['timespan']
            if 'former_or_current_location' in d:
                del d['former_or_current_location']

        for k, v in list(d.items()):
            clean_linked_art(v)
    elif isinstance(d, list):
        for item in d:
            clean_linked_art(item)
    return d


def format_loud_entity(entity: Entity) -> dict[str, Any]:
    graph = base_format_lod_entity(entity)
    return clean_linked_art(graph)


def format_loud_entities(
        entities: list[Entity],
        pagination: dict[str, Any] | None = None) -> dict[str, Any]:
    graph = base_format_lod_entities(entities, pagination=pagination)
    return clean_linked_art(graph)
