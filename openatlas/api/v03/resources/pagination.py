import itertools
from typing import Any

from openatlas.api.v03.resources.error import EntityDoesNotExistError, \
    LastEntityError
from openatlas.api.v03.resources.formats.geojson import get_geojson
from openatlas.api.v03.resources.formats.linked_places import get_entity
from openatlas.api.v03.resources.util import get_entity_by_id, link_parser_check
from openatlas.models.entity import Entity
from openatlas.models.link import Link


def get_start_entity(total: list[int], parser: dict[str, Any]) -> list[Any]:
    if parser['first'] and int(parser['first']) in total:
        return list(itertools.islice(
            total,
            total.index(int(parser['first'])),
            None))
    if parser['last'] and int(parser['last']) in total:
        if not (out := list(itertools.islice(
                total,
                total.index(int(parser['last'])) + 1,
                None))):
            raise LastEntityError
        return out
    raise EntityDoesNotExistError


def get_by_page(
        index: list[dict[str, Any]],
        parser: dict[str, Any]) -> dict[str, Any]:
    page = parser['page'] \
        if parser['page'] < index[-1]['page'] else index[-1]['page']
    return [entry['startId'] for entry in index if entry['page'] == page][0]


def pagination(
        entities: list[Entity],
        parser: dict[str, Any]) -> dict[str, Any]:
    total = [e.id for e in entities]
    count = len(total)
    e_list = list(itertools.islice(total, 0, None, int(parser['limit'])))
    index = [{'page': num + 1, 'startId': i} for num, i in enumerate(e_list)]
    parser['first'] = get_by_page(index, parser) \
        if parser['page'] else parser['first']
    total = get_start_entity(total, parser) \
        if parser['last'] or parser['first'] else total
    j = [i for i, x in enumerate(entities) if x.id == total[0]]
    new_entities = [e for idx, e in enumerate(entities[j[0]:])]
    return {
        "results": get_entities_formatted(new_entities, parser),
        "pagination": {
            'entitiesPerPage': int(parser['limit']),
            'entities': count,
            'index': index,
            'totalPages': len(index)}}


def get_entities_formatted(
        new_entities: list[Entity],
        parser: dict[str, Any]) -> list[dict[str, Any]]:
    limited_entities = new_entities[:int(parser['limit'])]
    if parser['format'] == 'geojson':
        return [get_geojson(limited_entities)]
    return linked_places_result(
        limited_entities,
        parser,
        link_parser_check(limited_entities, parser),
        link_parser_check(limited_entities, parser, True))


def linked_places_result(
        entities: list[Entity],
        parser: dict[str, str],
        links: list[Link],
        links_inverse: list[Link]) -> list[dict[str, Any]]:
    return [
        get_entity(
            get_entity_by_id(entity.id) if 'names' in parser['show']
            else entity,
            [link_ for link_ in links if link_.domain.id == entity.id],
            [link_ for link_ in links_inverse if
             link_.range.id == entity.id],
            parser)
        for entity in entities]
