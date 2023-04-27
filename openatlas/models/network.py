from typing import Optional

from flask import g

from openatlas.database.network import Network as Db
from openatlas.models.entity import Entity


class Network:

    properties = [
        'P7', 'P11', 'P14', 'P22', 'P23', 'P24', 'P25', 'P27', 'P52', 'P74',
        'P107', 'OA7', 'OA8', 'OA9']

    @staticmethod
    def get_ego_network_json(
            colors: dict[str, str],
            id_: int,
            depth: int,
            dimensions: int) -> str:
        mapping = Db.get_object_mapping()
        entity_ids = {id_}
        location_id = 0
        if id_ in mapping.values():
            location_id = \
                list(mapping.keys())[list(mapping.values()).index(id_)]
            entity_ids.add(location_id)
        edges = []
        for _ in range(depth):
            for row in Db.get_ego_network(entity_ids):
                if row['property_code'] in Network.properties:
                    domain_id = mapping[row['domain_id']] \
                        if row['domain_id'] in mapping else row['domain_id']
                    range_id = mapping[row['range_id']] \
                        if row['range_id'] in mapping else row['range_id']
                    entity_ids.add(domain_id)
                    entity_ids.add(range_id)
                    edges.append({
                        'id': row['id'],
                        'source': domain_id,
                        'target': range_id})
        nodes = []
        if location_id in entity_ids:
            entity_ids.remove(location_id)
        for entity in Entity.get_by_ids(entity_ids):
            nodes.append({
                'id': entity.id,
                'label' if dimensions else
                'name': Network.truncate(entity.name.replace("'", "")),
                'color': colors[entity.class_.name]
                if entity.class_.name in colors else '#333333'})
        return str({
            'nodes': nodes,
            'edges' if dimensions else 'links': edges}) if nodes else None

    @staticmethod
    def get_network_json(
            colors: dict[str, str],
            show_orphans: bool,
            dimensions: Optional[int]) -> Optional[str]:
        mapping = Db.get_object_mapping()
        classes = [c.name for c in g.classes.values() if c.network_color]
        entities: set[int] = set()
        nodes = []
        for row in Db.get_entities(classes):
            if row['id'] not in mapping \
                    and row['id'] not in entities \
                    and row['openatlas_class_name'] != 'source':
                nodes.append({
                    'id': row['id'],
                    'label' if dimensions else
                    'name': Network.truncate(row['name'].replace("'", "")),
                    'color': colors[row['openatlas_class_name']]})
                entities.add(row['id'])
        edges = []
        edge_entity_ids = set()
        for row in Db.get_edges(classes, Network.properties):
            domain_id = mapping[row['domain_id']] \
                if row['domain_id'] in mapping else row['domain_id']
            range_id = mapping[row['range_id']] \
                if row['range_id'] in mapping else row['range_id']
            edges.append({
                'id': int(row['id']),
                'source': domain_id,
                'target': range_id})
            edge_entity_ids.add(domain_id)
            edge_entity_ids.add(range_id)
        if not show_orphans:
            nodes[:] = [d for d in nodes if int(d['id']) in edge_entity_ids]
        else:
            nodes[:] = [
                d for d in nodes if int(d['id']) in edge_entity_ids
                or (not d['name'].startswith('Location of'))]
        return str({
            'nodes': nodes,
            'edges' if dimensions else 'links': edges}) if nodes else None

    @staticmethod
    def truncate(string: str = '', length: int = 40) -> str:
        return string if len(string) < length + 1 else string[:length] + '..'
