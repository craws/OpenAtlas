from typing import Any, Dict, Optional

from flask import g

from openatlas.util.util import truncate_string


class Network:

    properties = ['P7', 'P11', 'P14', 'P23', 'P24', 'P67', 'P74', 'P107', 'OA7', 'OA8', 'OA9']
    classes = ['E7', 'E8', 'E18', 'E21', 'E31', 'E33', 'E40', 'E53', 'E74', 'E84']
    sql_where = """
        AND ((e.system_type IS NULL AND e.class_code != 'E53')
                OR (e.system_type NOT IN ('file', 'source translation')
                    AND e.system_type NOT LIKE 'external reference%%'));"""

    @staticmethod
    def get_edges():
        sql = """
            SELECT l.id, l.domain_id, l.range_id FROM model.link l
            JOIN model.entity e ON l.domain_id = e.id
            WHERE property_code IN %(properties)s """ + Network.sql_where
        g.execute(sql, {'properties': tuple(Network.properties)})
        return g.cursor.fetchall()

    @staticmethod
    def get_entities():
        sql = """
            SELECT e.id, e.class_code, e.name
            FROM model.entity e
            WHERE class_code IN %(classes)s """ + Network.sql_where
        g.execute(sql, {'classes': tuple(Network.classes)})
        return g.cursor.fetchall()

    @staticmethod
    def get_object_mapping():
        # Get mapping between location and objects to join them into one entity
        sql = """
            SELECT e.id, l.range_id
            FROM model.entity e
            JOIN model.link l ON e.id = domain_id AND l.property_code = 'P53';"""
        g.execute(sql)
        return {row.range_id: row.id for row in g.cursor.fetchall()}

    @staticmethod
    def get_network_json(params: Dict[str, Any]) -> Optional[str]:
        mapping = Network.get_object_mapping()
        entities = set()
        nodes = ''
        for row in Network.get_entities():
            if row.id in mapping:  # pragma: no cover - Locations will be mapped to objects
                continue
            entities.add(row.id)
            nodes += """{{'id':'{id}','name':'{name}','color':'{color}'}},""".format(
                id=row.id,
                name=truncate_string(row.name.replace("'", ""), span=False),
                color=params['classes'][row.class_code]['color'])

        edges = ''
        for row in Network.get_edges():
            domain_id = mapping[row.domain_id] if row.domain_id in mapping else row.domain_id
            range_id = mapping[row.range_id] if row.range_id in mapping else row.range_id
            if domain_id not in entities:  # pragma: no cover
                # print('Missing entity id: ' + str(domain_id))
                continue
            if range_id not in entities:  # pragma: no cover
                # print('Missing entity id: ' + str(range_id))
                continue
            edges += "{{'source':'{source}','target':'{target}'}},".format(source=domain_id,
                                                                           target=range_id)

        return "graph = {'nodes': [" + nodes + "],  links: [" + edges + "]};" if nodes else None

    @staticmethod
    def get_network_json2(params: Dict[str, Any]) -> Optional[str]:
        mapping = Network.get_object_mapping()
        entities = set()
        nodes = ''
        for row in Network.get_entities():
            if row.id in mapping:  # pragma: no cover - Locations will be mapped to objects
                continue
            entities.add(row.id)
            nodes += """{{'id':'{id}','label':'{name}','color':'{color}'}},""".format(
                id=row.id,
                name=truncate_string(row.name.replace("'", ""), span=False),
                color=params['classes'][row.class_code]['color'])

        edges = ''
        for row in Network.get_edges():
            domain_id = mapping[row.domain_id] if row.domain_id in mapping else row.domain_id
            range_id = mapping[row.range_id] if row.range_id in mapping else row.range_id
            if domain_id not in entities:  # pragma: no cover
                # print('Missing entity id: ' + str(domain_id))
                continue
            if range_id not in entities:  # pragma: no cover
                # print('Missing entity id: ' + str(range_id))
                continue
            edges += "{{'source':'{source}', 'target':'{target}', 'id':'{id}'}},".format(
                source=domain_id, target=range_id, id=row.id)

        return "{{nodes: [{nodes}], edges: [{edges}], types: {{nodes: [], edges: []}} }};".format(
            nodes=nodes, edges=edges)
