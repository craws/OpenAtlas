# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import g

from openatlas import debug_model
from openatlas.util.util import truncate_string


class Network:

    @staticmethod
    def get_network_json(params):
        """ Returns JSON data for d3.js"""
        properties = [code for code, param in params['properties'].items() if param['active']]
        classes = [code for code, param in params['classes'].items() if param['active']]
        if not classes:
            return None  # Return nothing if no classes are selected

        # Get edges
        entities = set()
        edges = ''
        if properties:
            sql = """
                SELECT l.domain_id, l.range_id FROM model.link l
                JOIN model.entity e ON l.domain_id = e.id
                WHERE property_code IN %(properties)s
                    AND (e.system_type IS NULL OR e.system_type != 'file');"""
            g.cursor.execute(sql, {'properties': tuple(properties)})
            debug_model['div sql'] += 1
            for row in g.cursor.fetchall():
                edges += "{{'source':'{domain_id}','target':'{range_id}'}},".format(
                    domain_id=row.domain_id, range_id=row.range_id)
                entities.update([row.domain_id, row.range_id])

        # Get entities
        sql = "SELECT id, class_code, name FROM model.entity WHERE class_code IN %(classes)s;"
        g.cursor.execute(sql, {'classes': tuple(classes)})
        debug_model['div sql'] += 1
        nodes = ''
        entities_already = set()
        for row in g.cursor.fetchall():
            if params['options']['orphans'] or row.id in entities:
                entities_already.add(row.id)
                nodes += """{{'id':'{id}','name':'{name}','color':'{color}'}},""".format(
                    id=row.id, name=truncate_string(row.name.replace("'", ""), span=False),
                    color=params['classes'][row.class_code]['color'])

        # Get entities of links which weren't present in class selection
        array_diff = [item for item in entities if item not in entities_already]
        if array_diff:
            sql = "SELECT id, class_code, name FROM model.entity WHERE id IN %(array_diff)s;"
            g.cursor.execute(sql, {'array_diff': tuple(array_diff)})
            debug_model['div sql'] += 1
            result = g.cursor.fetchall()
            for row in result:
                color = ''
                if row.class_code in params['classes']:  # pragma: no cover
                    color = params['classes'][row.class_code]['color']
                nodes += """{{'id':'{id}','name':'{name}','color':'{color}'}},""".format(
                    id=row.id, color=color,
                    name=truncate_string(row.name.replace("'", ""), span=False))

        return "graph = {'nodes': [" + nodes + "],  links: [" + edges + "]};" if nodes else None
