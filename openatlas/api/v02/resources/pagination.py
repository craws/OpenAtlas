import itertools
from typing import Any, Dict, List

from openatlas.api.v02.resources.error import Error
from openatlas.api.v02.resources.geojson_entity import GeoJsonEntity
from openatlas.models.entity import Entity


class Pagination:

    @staticmethod
    def pagination(entities: List[Entity], parser: Dict[str, Any]) -> List[List[Dict[str, Any]]]:
        result = []
        index = []
        total = []
        for e in entities:
            total.append(e.id)
        for num, i in enumerate(
                list(itertools.islice(total, 0, None, int(parser['limit'])))):
            index.append(({'page': num + 1, 'start_id': i}))
        if parser['last'] or parser['first']:
            if parser['last'] and int(parser['last']) in total:
                total = list(
                    itertools.islice(total, total.index(int(parser['last'])) + 1, None))
            elif parser['first'] and int(parser['first']) in total:
                total = list(
                    itertools.islice(total, total.index(int(parser['first'])), None))
            else:
                # Todo: Eliminate Error
                raise Error('Entity ID doesn\'t exist', status_code=404, payload="404a")
        else:
            pass
        # Finding the entity with the wanted id
        h = [i for i, x in enumerate(entities) if x.id == total[0]]
        entity_limit = []
        for idx, e in enumerate(entities[h[0]:]):
            entity_limit.append(e)
        entities_result = []
        for r in entity_limit[:int(parser['limit'])]:
            entities_result.append(GeoJsonEntity.get_entity(r, parser))
        result.append(entities_result)
        result.append([{'entity_per_page': int(parser['limit']), 'entities': len(total),
                        'index': index, 'total_pages': len(index)}])
        return result
