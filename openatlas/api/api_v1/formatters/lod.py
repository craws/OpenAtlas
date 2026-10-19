from typing import Any, Final

from flask import url_for

from openatlas.models.entity import Entity

LOD_CONTEXT: Final[str] = 'https://linked.art/ns/v1/linked-art.json'
LOD_SEARCH_CONTEXT: Final[str] = 'https://linked.art/ns/v1/search.json'


def format_lod_entity(entity: Entity) -> dict[str, Any]:
    return {'@context': LOD_CONTEXT} | stub(entity)


def format_lod_entities(
        entities: list[Entity],
        pagination: dict[str, Any] | None = None) -> dict[str, Any]:
    items = [stub(entity) for entity in entities]
    if pagination is None:
        return {
            '@context': [LOD_CONTEXT, LOD_SEARCH_CONTEXT],
            'type': 'OrderedCollection',
            'totalItems': len(items),
            'orderedItems': items}
    result: dict[str, Any] = {
        '@context': [LOD_CONTEXT, LOD_SEARCH_CONTEXT],
        'id': pagination['id'],
        'type': 'OrderedCollectionPage',
        'partOf': {
            'id': pagination['collection_url'],
            'type': 'OrderedCollection',
            'totalItems': pagination['total_items'],
            'first': {
                'id': pagination['first'],
                'type': 'OrderedCollectionPage'},
            'last': {
                'id': pagination['last'],
                'type': 'OrderedCollectionPage'}},
        'startIndex': pagination['start_index'],
        'orderedItems': items}
    if 'previous' in pagination:
        result['prev'] = {
            'id': pagination['previous'],
            'type': 'OrderedCollectionPage'}
    if 'next' in pagination:
        result['next'] = {
            'id': pagination['next'],
            'type': 'OrderedCollectionPage'}
    return result


def stub(entity: Entity) -> dict[str, Any]:
    return {
        'id': url_for(
            'api.entity_uuid',
            uuid=entity.uuid,
            _external=True),
        'type': entity.cidoc_class.i18n['en'],
        '_label': entity.name}
