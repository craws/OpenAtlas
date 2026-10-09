from typing import Any, Final

from openatlas.api.api_v1.formatters.la_formatter import LaFormatter
from openatlas.api.api_v1.formatters.lod_util import (
    get_links_for_entities, get_type_references)
from openatlas.api.api_v1.util.files import prefetch_files
from openatlas.models.entity import Entity

LA_CONTEXT: Final[str] = 'https://linked.art/ns/v1/linked-art.json'


def format_la_entity(entity: Entity) -> dict[str, Any]:
    result = format_la_entities([entity])
    return {'@context': result['@context']} | result['@graph'][0]


def format_la_entities(
        entities: list[Entity],
        pagination: dict[str, Any] | None = None) -> dict[str, Any]:
    if not entities and pagination is None:
        return {'@context': LA_CONTEXT, '@graph': []}
    links_data = get_links_for_entities(entities) if entities else {}
    prefetch_files(links_data)
    formatter = LaFormatter(type_references=get_type_references())
    graph = [formatter.format_entity(item) for item in links_data.values()]
    if pagination is None:
        return {'@context': LA_CONTEXT, '@graph': graph}
    result: dict[str, Any] = {
        '@context': [
            LA_CONTEXT,
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
