import itertools
from typing import Any, Dict, List

from flask import g

from openatlas.api.v01.apifunction import Api
from openatlas.api.v01.error import APIError
from openatlas.api.v01.sql import Query
from openatlas.models.content import Content
from openatlas.models.entity import Entity


class Path:

    @staticmethod
    def get_entities_by_menu_item(code_: str, validation: Dict[str, Any]) -> List[Entity]:
        entities = []
        if code_ not in ['actor', 'event', 'place', 'reference', 'source', 'object']:
            raise APIError('Invalid code: ' + code_, status_code=404, payload="404c")
        for entity in Query.get_by_menu_item_api(code_, validation):
            entities.append(entity)
        return entities

    @staticmethod
    def get_entities_by_class(class_code: str, validation: Dict[str, Any]) -> List[Entity]:
        entities = []
        if class_code not in g.classes:
            raise APIError('Invalid CIDOC CRM class code: ' + class_code, status_code=404,
                           payload="404d")
        for entity in Query.get_by_class_code_api(class_code, validation):
            entities.append(entity)
        return entities

    @staticmethod
    def get_entities_get_latest(limit_: int, validation: Dict[str, Any]) -> List[Dict[str, Any]]:
        entities = []
        try:
            limit_ = int(limit_)
        except Exception:
            raise APIError('Invalid limit.', status_code=404, payload="404e")
        if 1 < limit_ < 101:
            for entity in Entity.get_latest(limit_):
                entities.append(Api.get_entity(entity, meta=validation))
            return entities
        else:
            raise APIError('Invalid limit.', status_code=404, payload="404e")

    @staticmethod
    def pagination(entities: List[Entity], validation: Dict[str, Any]) -> List[List[Dict[str, Any]]]:
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
        entities_result=[]
        for r in entity_limit[:int(validation['limit'])]:
            entities_result.append(Api.get_entity(r, validation))
        result.append(entities_result)
        result.append([{'entity_per_page': int(validation['limit']), 'entities': len(total),
                        'index': index, 'total_pages': len(index)}])
        return result

    @staticmethod
    def get_content(validation: Dict[str, Any]) -> Dict[str, str]:
        content = {'intro': Content.get_translation('intro_for_frontend', validation['lang']),
                   'contact': Content.get_translation('contact_for_frontend', validation['lang']),
                   'legal-notice': Content.get_translation('legal_notice_for_frontend',
                                                           validation['lang'])}
        return content
