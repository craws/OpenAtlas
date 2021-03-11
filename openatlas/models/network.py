from typing import Dict, Iterator, List, Optional

from flask import g
from flask_wtf import FlaskForm
from psycopg2.extras import NamedTupleCursor

from openatlas.util.display import truncate


class Network:

    @staticmethod
    def get_edges(classes: List[str]) -> Iterator[NamedTupleCursor.Record]:
        properties = [
            'P7', 'P11', 'P14', 'P22', 'P23', 'P24', 'P25', 'P67', 'P74', 'P107', 'OA7', 'OA8',
            'OA9']
        sql = """
            SELECT l.id, l.domain_id, l.range_id FROM model.link l
            JOIN model.entity e ON l.domain_id = e.id AND e.system_class IN %(classes)s
            JOIN model.entity e2 ON l.range_id = e2.id AND e2.system_class IN %(classes)s
            WHERE property_code IN %(properties)s """
        g.execute(sql, {
            'classes': tuple(classes),
            'properties': tuple(properties), })
        return g.cursor.fetchall()

    @staticmethod
    def get_entities(classes: List[str]) -> Iterator[NamedTupleCursor.Record]:
        sql = """
            SELECT e.id, e.name, e.system_class
            FROM model.entity e
            WHERE system_class IN %(classes)s """
        g.execute(sql, {'classes': tuple(classes)})
        return g.cursor.fetchall()

    @staticmethod
    def get_object_mapping() -> Dict[int, int]:
        # Get mapping between location and objects to join them into one entity
        sql = """
            SELECT e.id, l.range_id
            FROM model.entity e
            JOIN model.link l ON e.id = domain_id AND l.property_code = 'P53';"""
        g.execute(sql)
        return {row.range_id: row.id for row in g.cursor.fetchall()}

    @staticmethod
    def get_network_json(form: FlaskForm, dimensions: Optional[int]) -> Optional[str]:
        mapping = Network.get_object_mapping()
        classes = [class_.name for class_ in g.classes.values() if class_.color]
        entities = set()
        nodes = []
        for row in Network.get_entities(classes):
            if row.id in mapping or row.id in entities:  # pragma: no cover
                continue  # Locations will be mapped to objects
            name = truncate(row.name.replace("'", ""), span=False)
            nodes.append({
                'id': row.id,
                'label' if dimensions else 'name': name,
                'color': g.classes[row.system_class].color})
            entities.add(row.id)
        linked_entity_ids = set()
        edges = []
        edge_entity_ids = set()
        for row in Network.get_edges(classes):
            domain_id = mapping[row.domain_id] if row.domain_id in mapping else row.domain_id
            range_id = mapping[row.range_id] if row.range_id in mapping else row.range_id
            linked_entity_ids.add(domain_id)
            linked_entity_ids.add(range_id)
            edges.append({'id': int(row.id), 'source': domain_id, 'target': range_id})
            edge_entity_ids.add(domain_id)
            edge_entity_ids.add(range_id)
        if not form.orphans.data:
            nodes[:] = [d for d in nodes if int(d['id']) in edge_entity_ids]
        return str({'nodes': nodes, 'edges' if dimensions else 'links': edges}) if nodes else None
