from typing import Any, Dict, List, Optional

from flask import g, url_for

from openatlas.api.error import APIError
from openatlas.models.entity import Entity
from openatlas.models.place import get_structure


class APINode:

    @staticmethod
    def get_node(id_: int) -> List[Dict[str, Any]]:
        if id_ not in g.nodes:
            raise APIError('Entity ID doesn\'t exist', status_code=404, payload="404a")

        entities = g.nodes[id_].get_linked_entities(['P2', 'P89'], inverse=True)
        data = []
        for e in entities:
            data.append({'id': e.id, 'label': e.name,
                         'url': url_for('api_entity', id_=e.id, _external=True)})

        return data

    @staticmethod
    def get_node_all(id_: int) -> List[Dict[str, Any]]:
        if id_ not in g.nodes:
            raise APIError('Entity ID doesn\'t exist', status_code=404, payload="404a")

        return APINode.get_recursiv_node_entities(id_, [])

    @staticmethod
    def get_recursiv_node_entities(id_: int, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        entities = g.nodes[id_].get_linked_entities(['P2', 'P89'], inverse=True)
        for e in entities:
            data.append({'id': e.id, 'label': e.name,
                         'url': url_for('api_entity', id_=e.id, _external=True)})
        node = g.nodes[id_]
        for sub_id in node.subs:
            APINode.get_recursiv_node_entities(sub_id, data)
        return data

    @staticmethod
    def get_stratographic_node(id_: int) -> List[Dict[str, Any]]:
        try:
            entity = Entity.get_by_id(id_, nodes=True, aliases=True)
        except Exception:
            raise APIError('Entity ID doesn\'t exist', status_code=404, payload="404a")
        try:
            structure = get_structure(entity)
        except Exception:
            raise APIError('Stratographic node doesn\'t exist', status_code=404, payload="404a")
        data = []
        for n in structure['subunits']:
            data.append({'id': n.id, 'label': n.name,
                         'url': url_for('api_entity', id_=n.id, _external=True)})
        return data

    @staticmethod
    def get_stratographic_node_all(id_: int) -> List[Dict[str, Any]]:
        try:
            entity = Entity.get_by_id(id_, nodes=True, aliases=True)
        except Exception:
            raise APIError('Entity ID doesn\'t exist', status_code=404, payload="404a")
        return APINode.get_recursiv_stratographic_node_all(entity, [])

    @staticmethod
    def get_recursiv_stratographic_node_all(entity: Optional[Entity], data: List[Dict[str, Any]]) \
            -> List[Dict[str, Any]]:
        structure = get_structure(entity)
        for n in structure['subunits']:
            data.append({'id': n.id, 'label': n.name,
                         'url': url_for('api_entity', id_=n.id, _external=True)})
        node = get_structure(entity)
        for sub_id in node['subunits']:
            APINode.get_recursiv_stratographic_node_all(sub_id, data)
        return data
