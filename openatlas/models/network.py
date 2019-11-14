# Created by Alexander Watzinger and others. Please see README.md for licensing information
from typing import Optional

from flask import g

from openatlas.util.util import truncate_string


class Network:

    @staticmethod
    def get_network_json(params: dict) -> Optional[str]:
        """ Returns JSON data for d3.js"""
        properties = [code for code, param in params['properties'].items() if param['active']]
        classes = [code for code, param in params['classes'].items() if param['active']]
        if not classes:
            return None

        # Get edges
        entities = set()
        edges = ''
        if properties:
            sql = """
                SELECT l.domain_id, l.range_id FROM model.link l
                JOIN model.entity e ON l.domain_id = e.id
                WHERE property_code IN %(properties)s
                    AND (e.system_type IS NULL OR e.system_type != 'file');"""
            g.execute(sql, {'properties': tuple(properties)})
            for row in g.cursor.fetchall():
                edges += "{{'source':'{domain_id}','target':'{range_id}'}},".format(
                    domain_id=row.domain_id, range_id=row.range_id)
                entities.update([row.domain_id, row.range_id])

        # Get entities
        sql = "SELECT id, class_code, name FROM model.entity WHERE class_code IN %(classes)s;"
        g.execute(sql, {'classes': tuple(classes)})
        nodes = ''
        entities_already = set()
        for row in g.cursor.fetchall():
            if params['options']['orphans'] or row.id in entities:
                entities_already.add(row.id)
                nodes += """{{'id':'{id}','name':'{name}','color':'{color}'}},""".format(
                    id=row.id,
                    name=truncate_string(row.name.replace("'", ""), span=False),
                    color=params['classes'][row.class_code]['color'])

        # Get entities of links which weren't present in class selection
        array_diff = [item for item in entities if item not in entities_already]
        if array_diff:
            sql = "SELECT id, class_code, name FROM model.entity WHERE id IN %(array_diff)s;"
            g.execute(sql, {'array_diff': tuple(array_diff)})
            result = g.cursor.fetchall()
            for row in result:
                color = ''
                if row.class_code in params['classes']:  # pragma: no cover
                    color = params['classes'][row.class_code]['color']
                nodes += """{{'id':'{id}','name':'{name}','color':'{color}'}},""".format(
                    id=row.id, color=color,
                    name=truncate_string(row.name.replace("'", ""), span=False))

        return "graph = {'nodes': [" + nodes + "],  links: [" + edges + "]};" if nodes else None
