from typing import Any, Dict, List, Tuple, Union

from flasgger import swag_from
from flask import Response, g, url_for
from flask_restful import Resource, marshal

from openatlas.api.v03.resources.parser import default
from openatlas.api.v03.resources.resolve_endpoints import download
from openatlas.api.v03.templates.types_overview import TypeOverviewTemplate
from openatlas.models.entity import Entity
from openatlas.models.type import Type


class GetTypeOverview(Resource):
    @staticmethod
    @swag_from("../swagger/type_overview.yml", endpoint="api_03.type_overview")
    def get() -> Union[Tuple[Resource, int], Response]:
        parser = default.parse_args()
        node = GetTypeOverview.get_node_overview()
        template = TypeOverviewTemplate.type_overview_template()
        if parser['download']:
            return download(node, template, 'types')
        return marshal(node, template), 200

    @staticmethod
    def get_node_overview() -> Dict[str, Dict[Entity, str]]:
        nodes: Dict[str, Any] = {
            'standard': [],
            'custom': [],
            'place': [],
            'value': [],
            'system': []}
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
    def walk_tree(nodes: List[int]) -> List[Dict[str, Any]]:
        items = []
        for id_ in nodes:
            item = g.types[id_]
            items.append({
                'id': item.id,
                'url': url_for('api_03.entity', id_=item.id, _external=True),
                'label': item.name.replace("'", "&apos;"),
                'children': GetTypeOverview.walk_tree(item.subs)})
        return items
