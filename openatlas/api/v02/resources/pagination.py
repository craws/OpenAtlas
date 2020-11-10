import itertools
from typing import Any, Dict, List

from openatlas.api.v02.resources.geojson_entity import GeoJsonEntity
from openatlas.api.v01.error import APIError
from openatlas.models.entity import Entity


class Pagination:

    @staticmethod
    def pagination(entities: List[Entity], validation: Dict[str, Any]) -> List[
        List[Dict[str, Any]]]:
        result = []
        index = []
        total = []
        for e in entities:
            total.append(e.id)
        for num, i in enumerate(
                list(itertools.islice(total, 0, None, int(validation['limit'])))):
            index.append(({'page': num + 1, 'start_id': i}))
        if validation['last'] or validation['first']:
            if validation['last'] and int(validation['last']) in total:
                total = list(
                    itertools.islice(total, total.index(int(validation['last'])) + 1, None))
            elif validation['first'] and int(validation['first']) in total:
                total = list(
                    itertools.islice(total, total.index(int(validation['first'])), None))
            else:
                raise APIError('Entity ID doesn\'t exist', status_code=404, payload="404a")
        else:
            pass
        # Finding the entity with the wanted id
        h = [i for i, x in enumerate(entities) if x.id == total[0]]
        entity_limit = []
        for idx, e in enumerate(entities[h[0]:]):
            entity_limit.append(e)
        entities_result = []
        for r in entity_limit[:int(validation['limit'])]:
            entities_result.append(GeoJsonEntity.get_entity(r, validation))
        result.append(entities_result)
        result.append([{'entity_per_page': int(validation['limit']), 'entities': len(total),
                        'index': index, 'total_pages': len(index)}])
        return result
