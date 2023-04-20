from typing import Optional

from flask import g

from openatlas.database.network import Network as Db
from openatlas.models.entity import Entity


class Network:

    properties = [
        'P7', 'P11', 'P14', 'P22', 'P23', 'P24', 'P25', 'P52', 'P67',
        'P74', 'P107', 'OA7', 'OA8', 'OA9']

    @staticmethod
    def get_ego_network_json(
            colors: dict[str, str],
            id_: int) -> Optional[str]:
        mapping = Db.get_object_mapping()
        print(mapping)
        entity_ids: set[int] = set()
        nodes = []
        for row in Db.get_ego_network(id_):
            if row['property_code'] in Network.properties:
                if row['domain_id'] not in mapping:
                    entity_ids.add(row['domain_id'])
                if row['range_id'] not in mapping:
                    entity_ids.add(row['range_id'])
        for entity in Entity.get_by_ids(entity_ids):
            nodes.append({
                'id': entity.id,
                'name': Network.truncate(entity.name.replace("'", "")),
                'color': colors[entity.class_.name]})
        edges = []
        return str({
            'nodes': nodes,
            'links': edges}) if nodes else None

    @staticmethod
    def get_network_json(
            colors: dict[str, str],
            show_orphans: bool,
            dimensions: Optional[int]) -> Optional[str]:
        mapping = Db.get_object_mapping()
        print(mapping)
        classes = [c.name for c in g.classes.values() if c.network_color]
        entities: set[int] = set()
        nodes = []
        for row in Db.get_entities(classes):
            if row['id'] not in mapping and row['id'] not in entities:
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
        return str({
            'nodes': nodes,
            'edges' if dimensions else 'links': edges}) if nodes else None

    @staticmethod
    def truncate(string: str = '', length: int = 40) -> str:
        return string if len(string) < length + 1 else string[:length] + '..'
