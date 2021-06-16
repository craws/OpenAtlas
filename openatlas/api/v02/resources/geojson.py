from typing import Any, Dict, List, Optional

from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.link import Link


class Geojson:
    @staticmethod
    def get_geoms_by_entity(entity: Entity) -> List[Dict[str, Any]]:
        return Gis.get_by_id(entity.id)

    @staticmethod
    def check_if_geometry(entity: Entity):
        geoms = None
        if entity.class_.view == 'place' or entity.class_.name in ['find', 'artifact']:
            geoms = Geojson.get_geoms_by_entity(Link.get_linked_entity(entity.id, 'P53'))
        elif entity.class_.name == 'object_location':
            geoms = Geojson.get_geoms_by_entity(entity)
        out = []
        if geoms:
            for geom in geoms:
                out.append(Geojson.get_entity(entity,  geom))
        else:
            out.append(Geojson.get_entity(entity))
        return out

    @staticmethod
    def get_entity(entity: Entity,  geom: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        features = {
            'type': 'Feature',
            'geometry': geom,
            'properties': {
                '@id': entity.id,
                'systemClass': entity.class_.name,
                'name': entity.name,
                'description': entity.description,
                'begin_earliest': entity.begin_from,
                'begin_latest': entity.begin_to,
                'begin_comment': entity.begin_comment,
                'end_earliest': entity.end_from,
                'end_latest': entity.end_to,
                'end_comment': entity.end_comment,
                'types': Geojson.get_node(entity)
            }}
        return features

    @staticmethod
    def get_node(entity: Entity) -> Optional[List[Dict[str, Any]]]:
        nodes = []
        for node in entity.nodes:
            out = [node.name]
            # for link in links:
            #     link_out = []
            #     if link.range.id == node.id and link.description:
            #         link_out.append(link.description)
            #         if link.range.id == node.id and node.description:
            #             link_out.append(node.description)
            #         out.append(' '.join(link_out))
            nodes.append(': '.join(out))
        return nodes if nodes else None

    @staticmethod
    def return_output(output: List[Any]) -> Dict[str, Any]:
        return {'type': 'FeatureCollection', 'features': output}


