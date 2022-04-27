from typing import Any, Union

from flasgger import swag_from
from flask import Response, g, url_for
from flask_restful import Resource, marshal

from openatlas.api.v03.resources.formats.subunits import get_subunits_from_id
from openatlas.api.v03.resources.parser import default, entity_
from openatlas.api.v03.resources.resolve_endpoints import (
    download, resolve_subunits)
from openatlas.api.v03.resources.templates import (
    type_overview_template, type_tree_template)
from openatlas.api.v03.resources.util import (
    get_entity_by_id)
from openatlas.models.entity import Entity
from openatlas.models.type import Type


class GetTypeOverview(Resource):
    @staticmethod
    @swag_from("../swagger/type_overview.yml", endpoint="api_03.type_overview")
    def get() -> Union[tuple[Resource, int], Response]:
        types = GetTypeOverview.get_node_overview()
        if default.parse_args()['download']:
            return download(types, type_overview_template(), 'types')
        return marshal(types, type_overview_template()), 200

    @staticmethod
    def get_node_overview() -> dict[str, dict[Entity, str]]:
        nodes: dict[str, Any] = {
            'standard': [],
            'custom': [],
            'place': [],
            'value': [],
            'system': [],
            'anthropology': []}
        for node in g.types.values():
            if node.root:
                continue
            nodes[node.category].append({
                "id": node.id,
                "name": node.name,
                "viewClass": node.classes,
                "children":
                    GetTypeOverview.walk_tree(Type.get_types(node.name))})
        return nodes

    @staticmethod
    def walk_tree(nodes: list[int]) -> list[dict[str, Any]]:
        items = []
        for id_ in nodes:
            item = g.types[id_]
            items.append({
                'id': item.id,
                'url': url_for('api_03.entity', id_=item.id, _external=True),
                'label': item.name.replace("'", "&apos;"),
                'children': GetTypeOverview.walk_tree(item.subs)})
        return items


class GetTypeTree(Resource):
    @staticmethod
    @swag_from("../swagger/type_tree.yml", endpoint="api_03.type_tree")
    def get() -> Union[tuple[Resource, int], Response]:
        type_tree = {'typeTree': GetTypeTree.get_type_tree()}
        if entity_.parse_args()['download']:
            return download(type_tree, type_tree_template(), 'type_tree')
        return marshal(type_tree, type_tree_template()), 200

    @staticmethod
    def get_type_tree() -> dict[int, Any]:
        return {id_: GetTypeTree.serialize_to_json(type_)
                for id_, type_ in Type.get_all().items()}

    @staticmethod
    def serialize_to_json(node: Type) -> dict[str, Any]:
        return {
            'id': node.id,
            'name': node.name,
            'description': node.description,
            'origin_id': node.origin_id,
            'first': node.first,
            'last': node.last,
            'root': node.root,
            'subs': node.subs,
            'count': node.count,
            'count_subs': node.count_subs,
            'category': node.category}


class GetSubunits(Resource):
    @staticmethod
    @swag_from("../swagger/subunits.yml", endpoint="api_03.subunits")
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        parser = entity_.parse_args()
        subunits = get_subunits_from_id(get_entity_by_id(id_), parser)
        return resolve_subunits(subunits, parser, str(id_))
