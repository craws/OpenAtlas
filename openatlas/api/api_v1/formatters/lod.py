from typing import Any, Final

from flask import url_for

from openatlas.models.entity import Entity

LOD_CONTEXT: Final[str] = 'https://linked.art/ns/v1/linked-art.json'


def format_lod_entity(entity: Entity) -> dict[str, Any]:
    return {'@context': LOD_CONTEXT} | _stub(entity)


def format_lod_entities(
        entities: list[Entity],
        pagination: dict[str, Any] | None = None) -> dict[str, Any]:
    graph = [_stub(entity) for entity in entities]
    if pagination is None:
        return {'@context': LOD_CONTEXT, '@graph': graph}
    result: dict[str, Any] = {
        '@context': [
            LOD_CONTEXT,
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


def _stub(entity: Entity) -> dict[str, Any]:
    return {
        'id': url_for(
            'api.entity_uuid',
            uuid=entity.uuid,
            _external=True),
        'type': entity.cidoc_class.i18n['en'],
        '_label': entity.name}
