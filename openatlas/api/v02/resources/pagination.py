import itertools
from typing import Any, Dict, List

from openatlas.api.v02.resources.error import EntityDoesNotExistError, NoEntityAvailable
from openatlas.api.v02.resources.geojson import Geojson
from openatlas.api.v02.resources.linked_places import LinkedPlaces
from openatlas.api.v02.resources.util import get_all_links, get_all_links_inverse
from openatlas.models.entity import Entity
from openatlas.models.link import Link


class Pagination:

    @staticmethod
    def get_shown_entities(total: List[int], parser: Dict[str, Any]) -> List[Any]:
        if parser['last'] and int(parser['last']) in total:
            return list(itertools.islice(total, total.index(int(parser['last'])) + 1, None))
        if parser['first'] and int(parser['first']) in total:
            return list(itertools.islice(total, total.index(int(parser['first'])), None))
        raise EntityDoesNotExistError

    @staticmethod
    def pagination(entities: List[Entity], parser: Dict[str, Any]) -> Dict[str, Any]:
        if not entities:
            raise NoEntityAvailable
        index = []
        total = [e.id for e in entities]
        count = len(total)
        for num, i in enumerate(list(itertools.islice(total, 0, None, int(parser['limit'])))):
            index.append(({'page': num + 1, 'startId': i}))
        if parser['last'] or parser['first']:
            total = Pagination.get_shown_entities(total, parser)
        h = [i for i, x in enumerate(entities) if x.id == total[0]]
        entity_limit = [e for idx, e in enumerate(entities[h[0]:])]
        links = get_all_links([e.id for e in entity_limit[:int(parser['limit'])]])
        links_inverse = get_all_links_inverse([e.id for e in entity_limit[:int(parser['limit'])]])

        result = []
        if parser['format'] == 'lp':
            result = Pagination.linked_places_result(links, links_inverse, entity_limit, parser)
        if parser['format'] == 'geojson':
            result = Pagination.get_geojson(entity_limit)
        print(result)
        return {
            "results": result,
            "pagination": {
                'entitiesPerPage': int(parser['limit']),
                'entities': count,
                'index': index,
                'totalPages': len(index)}}

    @staticmethod
    def linked_places_result(links: List[Link], links_inverse: List[Link], entity_limit,
                             parser: Dict[str, str]) -> List[Dict[str, Any]]:
        return [LinkedPlaces.get_entity(
            entity,
            [link.id for link in links if link.domain == entity.id],
            [link.id for link in links_inverse if link.range == entity.id],
            parser)
            for entity in entity_limit[:int(parser['limit'])]]

    @staticmethod
    def get_geojson(entity_limit: List[Entity]) -> Dict[str, Any]:
        class_json = [Geojson.check_if_geometry(entity) for entity in entity_limit]
        return Geojson.return_output(class_json)
