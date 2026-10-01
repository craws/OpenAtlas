from typing import Any, Final

from openatlas.api.api_v1.formatters.loud_formatter import LoudFormatter
from openatlas.api.api_v1.formatters.lod_util import (
    get_links_for_entities, get_type_references)
from openatlas.models.entity import Entity

LOUD_CONTEXT: Final[str] = 'https://linked.art/ns/v1/linked-art.json'


def format_loud_entity(entity: Entity) -> dict[str, Any]:
    result = format_loud_entities([entity])
    return {'@context': result['@context']} | result['@graph'][0]


def format_loud_entities(
        entities: list[Entity],
        pagination: dict[str, Any] | None = None) -> dict[str, Any]:
    if not entities and pagination is None:
        return {'@context': LOUD_CONTEXT, '@graph': []}
    links_data = get_links_for_entities(entities) if entities else {}
    formatter = LoudFormatter(type_references=get_type_references())
    graph = [formatter.format_entity(item) for item in links_data.values()]
    if pagination is None:
        return {'@context': LOUD_CONTEXT, '@graph': graph}
    result: dict[str, Any] = {
        '@context': [
            LOUD_CONTEXT,
            {'hydra': 'http://www.w3.org/ns/hydra/core#'}],
        'id': pagination['id'],
        'type': 'hydra:PartialCollectionView',
        'hydra:totalItems': pagination['total_items'],
        'hydra:first': pagination['first']}
    if 'previous' in pagination:
        result['hydra:previous'] = pagination['previous']
    if 'next' in pagination:
        result['hydra:next'] = pagination['next']
    result['hydra:last'] = pagination['last']
    result['@graph'] = graph
    return result
