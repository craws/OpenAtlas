from collections import defaultdict
from typing import Any, Union

from flasgger import swag_from
from flask import Response, g, url_for
from flask_restful import Resource, marshal

from openatlas.api.resources.error import NotAPlaceError
from openatlas.api.resources.formats.subunits import get_subunits_from_id
from openatlas.api.resources.parser import default, entity_
from openatlas.api.resources.resolve_endpoints import (
    download, resolve_subunits)
from openatlas.api.resources.templates import (
    type_by_view_class_template, type_overview_template, type_tree_template)
from openatlas.api.resources.model_mapper import get_entity_by_id
from openatlas.models.entity import Entity
from openatlas.models.type import Type


def walk_type_tree(types: list[int]) -> list[dict[str, Any]]:
    items = []
    for id_ in types:
        item = g.types[id_]
        items.append({
            'id': item.id,
            'url': url_for('api_03.entity', id_=item.id, _external=True),
            'label': item.name.replace("'", "&apos;"),
            'children': walk_type_tree(item.subs)})
    return items


class GetTypeByViewClass(Resource):
    @staticmethod
    @swag_from("../swagger/type_by_view_class.yml",
               endpoint="api_03.type_by_view_class")
    def get() -> Union[tuple[Resource, int], Response]:
        types = GetTypeByViewClass.get_type_by_view()
        if default.parse_args()['download']:
            return download(types, type_by_view_class_template(types), 'types')
        return marshal(types, type_by_view_class_template(types)), 200

    @staticmethod
    def get_type_by_view() -> dict[str, dict[Entity, str]]:
        types: dict[str, Any] = defaultdict(list)
        for type_ in g.types.values():
            if type_.root:
                continue
            for class_ in type_.classes:
                types[class_].append({
                    "id": type_.id,
                    "name": type_.name,
                    "category": type_.category,
                    "children": walk_type_tree(Type.get_types(type_.name))})
        return types


class GetTypeOverview(Resource):
    @staticmethod
    @swag_from("../swagger/type_overview.yml", endpoint="api_03.type_overview")
    def get() -> Union[tuple[Resource, int], Response]:
        types = GetTypeOverview.get_type_overview()
        if default.parse_args()['download']:
            return download(types, type_overview_template(), 'types')
        return marshal(types, type_overview_template()), 200

    @staticmethod
    def get_type_overview() -> dict[str, dict[Entity, str]]:
        types: dict[str, Any] = {
            'standard': [],
            'custom': [],
            'place': [],
            'value': [],
            'system': [],
            'anthropology': []}
        for type_ in g.types.values():
            if type_.root:
                continue
            types[type_.category].append({
                "id": type_.id,
                "name": type_.name,
                "viewClass": type_.classes,
                "children": walk_type_tree(Type.get_types(type_.name))})
        return types


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
    def serialize_to_json(type_: Type) -> dict[str, Any]:
        return {
            'id': type_.id,
            'name': type_.name,
            'description': type_.description,
            'origin_id': type_.origin_id,
            'first': type_.first,
            'last': type_.last,
            'root': type_.root,
            'subs': type_.subs,
            'count': type_.count,
            'count_subs': type_.count_subs,
            'category': type_.category}


class GetSubunits(Resource):
    @staticmethod
    @swag_from("../swagger/subunits.yml", endpoint="api_03.subunits")
    def get(id_: int) -> Union[tuple[Resource, int], Response, dict[str, Any]]:
        parser = entity_.parse_args()
        entity = get_entity_by_id(id_)
        if not entity.class_.name == 'place':
            raise NotAPlaceError
        subunits = get_subunits_from_id(entity, parser)
        return resolve_subunits(subunits, parser, str(id_))
