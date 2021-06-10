from typing import Any, Dict, List, Optional

from flask import g, url_for

from openatlas.api.v02.resources.util import get_all_links
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.link import Link


class Geojson:

    @staticmethod
    def check_if_geometry(entity: Entity):
        geoms = Gis.get_by_id(entity.id)
        if geoms:
            for geom in geoms:
                Geojson.get_entity(entity, geom)
        else:
            return Geojson.get_entity(entity)

    @staticmethod
    def get_entity(entity: Entity, geom: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        features = {
            'type': 'Feature',
            'geometry': geom,
            'properties': {
                '@id': url_for('entity_view', id_=entity.id, _external=True),
                'systemClass': entity.class_.name,
                'name': entity.name,
                'description': entity.description,
                'begin_earliest': entity.begin_from,
                'begin_latest': entity.begin_to,
                'begin_comment': entity.begin_comment,
                'end_earliest': entity.end_from,
                'end_latest': entity.end_to,
                'end_comment': entity.end_comment,
                'types': Geojson.get_node(entity)}}
        for node in entity.nodes:
            features[node.name] = Geojson.get_value(node, get_all_links(entity))
        return {
            'type': 'FeatureCollection',
            'features': [features]}

    @staticmethod
    def get_node(entity: Entity) -> Optional[List[Dict[str, Any]]]:
        nodes = []
        for node in entity.nodes:
            nodes.append(node.name)
            for top_level in [g.nodes[root].name for root in node.root]:
                if top_level not in nodes:
                    nodes.append(top_level)
        return nodes if nodes else None

    @staticmethod
    def get_value(node: Entity, links: List[Link]) -> Optional[str]:
        value = []
        for link in links:
            if link.range.id == node.id and link.description:
                value.append(link.description)
                if link.range.id == node.id and node.description:
                    value.append(node.description)
        return ''.join(value)
