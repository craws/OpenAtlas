import itertools
from typing import Any, Dict, List

from flask import g

from openatlas.api.api import Api
from openatlas.api.error import APIError
from openatlas.api.sql import Query
from openatlas.models.entity import Entity


class Path:

    @staticmethod
    def get_entities_by_menu_item(code_: str, validation: Dict[str, Any]) -> List[int]:
        entities = []
        for entity in Query.get_by_menu_item(code_, validation):
            entities.append(entity.id)
        return entities

    @staticmethod
    def get_entities_by_class(class_code: str, validation: Dict[str, Any]) -> List[int]:
        entities = []
        if class_code not in g.classes:
            raise APIError('Invalid CIDOC CRM class code.', status_code=404, payload="404d")
        for entity in Query.get_by_class_code(class_code, validation):
            entities.append(entity.id)
        return entities

    @staticmethod
    def get_entities_get_latest(limit_: int, validation: Dict[str, Any]) -> List[Dict[str, Any]]:
        entities = []
        for entity in Entity.get_latest(limit_):
            entities.append(Api.get_entity(entity.id, meta=validation))
        return entities

    @staticmethod
    def pagination(entities: List[int], validation: Dict[str, Any]) -> List[List[Dict[str, Any]]]:
        result = []
        index = []
        total = entities
        for num, i in enumerate(list(itertools.islice(entities, 0, None, int(validation['limit'])))):
            index.append(({'page': num + 1, 'start_id': i}))
        if validation['last'] or validation['first']:
            if validation['last'] and int(validation['last']) in entities:
                entities = list(
                    itertools.islice(entities, entities.index(int(validation['last'])) + 1, None))
            elif validation['first'] and int(validation['first']) in entities:
                entities = list(
                    itertools.islice(entities, entities.index(int(validation['first'])), None))
            else:
                raise APIError('Entity ID doesn\'t exist', status_code=404, payload="404a")
        else:
            pass
        entity_result =[]
        for entity in entities[:int(validation['limit'])]:
            entity_result.append(Api.get_entity(entity, validation))
        result.append(entity_result)
        result.append([{'entity_per_page': int(validation['limit']), 'entities': len(total),
                       'index': index, 'total_pages': len(index)}])
        return result
