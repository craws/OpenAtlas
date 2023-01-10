from typing import Optional

from flask import g

from openatlas.database.network import Network as Db


class Network:

    @staticmethod
    def get_network_json(
            colors: dict[str, str],
            show_orphans: bool,
            dimensions: Optional[int]) -> Optional[str]:
        mapping = Db.get_object_mapping()
        classes = [c.name for c in g.classes.values() if c.network_color]
        properties = [
            'P7', 'P11', 'P14', 'P22', 'P23', 'P24', 'P25', 'P52', 'P67',
            'P74', 'P107', 'OA7', 'OA8', 'OA9']
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
        linked_entity_ids = set()
        edges = []
        edge_entity_ids = set()
        for row in Db.get_edges(classes, properties):
            domain_id = mapping[row['domain_id']] \
                if row['domain_id'] in mapping else row['domain_id']
            range_id = mapping[row['range_id']] \
                if row['range_id'] in mapping else row['range_id']
            linked_entity_ids.add(domain_id)
            linked_entity_ids.add(range_id)
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
