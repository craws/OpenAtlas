import itertools
from typing import Any, Dict, List

from openatlas.api.v02.resources.error import EntityDoesNotExistError, \
    NoEntityAvailable, TypeIDError
from openatlas.api.v02.resources.geojson import Geojson
from openatlas.api.v02.resources.linked_places import LinkedPlaces
from openatlas.api.v02.resources.util import get_all_links, \
    get_all_links_inverse, get_entity_by_id
from openatlas.models.entity import Entity
from openatlas.models.link import Link


class Pagination:

    @staticmethod
    def get_start_entity(total: List[int], parser: Dict[str, Any]) -> List[Any]:
        if parser['last'] and int(parser['last']) in total:
            return list(itertools.islice(
                total,
                total.index(int(parser['last'])) + 1,
                None))
        if parser['first'] and int(parser['first']) in total:
            return list(itertools.islice(
                total,
                total.index(int(parser['first'])),
                None))
        raise EntityDoesNotExistError  # pragma: no cover

    @staticmethod
    def pagination(
            entities: List[Entity],
            parser: Dict[str, Any]) -> Dict[str, Any]:
        if not entities:
            raise NoEntityAvailable  # pragma: no cover
        if parser['type_id']:
            entities = Pagination.get_entities_by_type(entities, parser)
            if not entities:
                raise TypeIDError
        index = []
        total = [e.id for e in entities]
        count = len(total)
        e_list = list(itertools.islice(total, 0, None, int(parser['limit'])))
        for num, i in enumerate(e_list):
            index.append(({'page': num + 1, 'startId': i}))
        if parser['last'] or parser['first']:
            total = Pagination.get_start_entity(total, parser)
        j = [i for i, x in enumerate(entities) if x.id == total[0]]
        new_entities = [e for idx, e in enumerate(entities[j[0]:])]
        return {
            "results": Pagination.get_results(new_entities, parser),
            "pagination": {
                'entitiesPerPage': int(parser['limit']),
                'entities': count,
                'index': index,
                'totalPages': len(index)}}

    @staticmethod
    def get_results(
            new_entities: List[Entity],
            parser: Dict[str, Any]) -> List[Dict[str, Any]]:
        if parser['format'] == 'geojson':
            return [Pagination.get_geojson(new_entities, parser)]
        return Pagination.linked_places_result(
            new_entities[:int(parser['limit'])],
            parser,
            Pagination.link_builder(new_entities, parser),
            Pagination.link_builder(new_entities, parser, True))

    @staticmethod
    def get_entities_by_type(
            entities: List[Entity],
            parser: Dict[str, Any]) -> List[Entity]:
        new_entities = []
        for entity in entities:
            if any(ids in [key.id for key in entity.nodes]
                   for ids in parser['type_id']):
                new_entities.append(entity)
        return new_entities

    @staticmethod
    def link_builder(
            new_entities: List[Entity],
            parser: Dict[str, Any],
            inverse: bool = False) -> List[Link]:
        if any(i in ['relations', 'types', 'depictions', 'links', 'geometry']
               for i in parser['show']):
            entities = [e.id for e in new_entities[:int(parser['limit'])]]
            return get_all_links_inverse(entities) \
                if inverse else get_all_links(entities)
        return []

    @staticmethod
    def linked_places_result(
            entities: List[Entity],
            parser: Dict[str, str],
            links: List[Link],
            links_inverse: List[Link]) -> List[Dict[str, Any]]:
        return [
            LinkedPlaces.get_entity(
                get_entity_by_id(entity.id) if 'names' in parser['show']
                else entity,
                [link_ for link_ in links if link_.domain.id == entity.id],
                [link_ for link_ in links_inverse if
                 link_.range.id == entity.id],
                parser)
            for entity in entities]

    @staticmethod
    def get_geojson(
            entity_limit: List[Entity],
            parser: Dict[str, str]) -> Dict[str, Any]:
        return Geojson.return_output(
            Geojson.get_geojson(entity_limit[:int(parser['limit'])]))
