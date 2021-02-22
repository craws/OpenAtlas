from typing import Any, Dict, Iterator, Optional

from flask import flash, g
from flask_wtf import FlaskForm
from psycopg2.extras import NamedTupleCursor

from openatlas.util.display import truncate


class Network:

    properties = ['P7', 'P11', 'P14', 'P22', 'P23', 'P24', 'P25', 'P67', 'P74', 'P107', 'OA7',
                  'OA8', 'OA9']
    classes = ['E7', 'E8', 'E9', 'E18', 'E20', 'E21', 'E22',  'E31', 'E33', 'E40', 'E53', 'E74',
               'E84']
    sql_where = """
        AND ((e.system_type IS NULL AND e.class_code != 'E53')
                OR (e.system_class NOT IN ('feature', 'stratigraphic_unit', 'find', 'file',
                                            'source_translation'))) AND e.class_code != 'E32'"""
    sql_where2 = """
        AND ((e2.system_type IS NULL AND e2.class_code != 'E53')
                OR (e2.system_class NOT IN ('feature', 'stratigraphic_unit', 'find', 'file',
                                            'source_translation'))) AND e2.class_code != 'E32'"""

    @staticmethod
    def get_edges() -> Iterator[NamedTupleCursor.Record]:
        sql = """
            SELECT l.id, l.domain_id, l.range_id FROM model.link l
            JOIN model.entity e ON l.domain_id = e.id
            JOIN model.entity e2 ON l.range_id = e2.id
            WHERE property_code IN %(properties)s """ + Network.sql_where + Network.sql_where2
        g.execute(sql, {'properties': tuple(Network.properties)})
        return g.cursor.fetchall()

    @staticmethod
    def get_entities() -> Iterator[NamedTupleCursor.Record]:
        sql = """
            SELECT e.id, e.class_code, e.name
            FROM model.entity e
            WHERE class_code IN %(classes)s """ + Network.sql_where
        g.execute(sql, {'classes': tuple(Network.classes)})
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
    def get_network_json(form: FlaskForm,
                         params: Dict[str, Any],
                         dimensions: Optional[int]) -> Optional[str]:
        mapping = Network.get_object_mapping()
        linked_entity_ids = set()

        edges = []
        for row in Network.get_edges():
            domain_id = mapping[row.domain_id] if row.domain_id in mapping else row.domain_id
            range_id = mapping[row.range_id] if row.range_id in mapping else row.range_id
            linked_entity_ids.add(domain_id)
            linked_entity_ids.add(range_id)
            edges.append({'id': int(row.id), 'source': domain_id, 'target': range_id})
        nodes = []

        entities = set()
        for row in Network.get_entities():
            if row.id in mapping:  # pragma: no cover - Locations will be mapped to objects
                continue
            if not form.orphans.data and row.id not in linked_entity_ids:  # Hide orphans
                continue
            entities.add(row.id)
            name = truncate(row.name.replace("'", ""), span=False)
            nodes.append({'id': row.id,
                          'label' if dimensions else 'name': name,
                          'color': params['classes'][row.class_code]['color']})
        if not linked_entity_ids.issubset(entities):  # pragma: no cover
            flash('Missing nodes for links', 'error')
            return ''
        return str({'nodes': nodes, 'edges' if dimensions else 'links': edges}) if nodes else None
