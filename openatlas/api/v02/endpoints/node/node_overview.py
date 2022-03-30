from typing import Any, Union

from flasgger import swag_from
from flask import Response, g, url_for
from flask_restful import Resource, marshal

from openatlas.api.v02.resources.parser import default
from openatlas.api.v02.resources.resolve_endpoints import download
from openatlas.api.v02.templates.nodes_overview import NodesOverviewTemplate
from openatlas.models.entity import Entity
from openatlas.models.type import Type


class GetNodeOverview(Resource):
    @staticmethod
    @swag_from("../swagger/node_overview.yml", endpoint="api_02.node_overview")
    def get() -> Union[tuple[Resource, int], Response]:
        parser = default.parse_args()
        node = {"types": GetNodeOverview.get_node_overview()}
        template = NodesOverviewTemplate.node_overview_template()
        if parser['download']:
            return download(node, template, 'types')
        return marshal(node, template), 200

    @staticmethod
    def get_node_overview() -> dict[str, dict[Entity, str]]:
        nodes: dict[str, Any] = {
            'standard': {},
            'custom': {},
            'place': {},
            'value': {},
            'system': {},
            'anthropology': {}}
        for node in g.types.values():
            if node.root:
                continue
            nodes[node.category][node.name] = GetNodeOverview.walk_tree(
                Type.get_types(node.name))
        return nodes

    @staticmethod
    def walk_tree(nodes: list[int]) -> list[dict[str, Any]]:
        items = []
        for id_ in nodes:
            item = g.types[id_]
            items.append({
                'id': item.id,
                'url': url_for('api_02.entity', id_=item.id, _external=True),
                'label': item.name.replace("'", "&apos;"),
                'children': GetNodeOverview.walk_tree(item.subs)})
        return items
