# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import g

from openatlas import debug_model
from openatlas.util.util import truncate_string


class Network:

    @staticmethod
    def get_network_json(params):
        """ Returns JSON data for d3.js"""
        classes = []
        for code, param in params['classes'].items():
            if param['active']:
                classes.append(code)
        if not classes:
            return None  # Return nothing if no classes are selected
        properties = []
        for code, param in params['properties'].items():
            if param['active']:
                properties.append(code)
        entities = set()
        edges = ''
        if properties:
            sql = """
                SELECT domain_id, range_id FROM model.link
                WHERE property_code IN %(properties)s;"""
            g.cursor.execute(sql, {'properties': tuple(properties)})
            debug_model['div sql'] += 1
            for row in g.cursor.fetchall():
                if row.domain_id == row.range_id:  # pragma no cover
                    continue  # Prevent circular dependencies
                edges += "{'source': '" + str(row.domain_id)
                edges += "', 'target': '" + str(row.range_id) + "' },"
                entities.add(row.domain_id)
                entities.add(row.range_id)
        edges = " links: [" + edges + "]"
        nodes = ''
        entities_already = set()
        sql = "SELECT id, class_code, name FROM model.entity WHERE class_code IN %(classes)s;"
        g.cursor.execute(sql, {'classes': tuple(classes)})
        debug_model['div sql'] += 1
        for row in g.cursor.fetchall():
            if params['options']['orphans'] or row.id in entities:
                name = row.name.replace("'", "").replace('Location of ', '').replace('\n', ' ')\
                    .replace('\r', ' ')
                entities_already.add(row.id)
                nodes += "{'id':'" + str(row.id) + "', 'name':'" + truncate_string(name, span=False)
                nodes += "', 'color':'" + params['classes'][row.class_code]['color'] + "'},"

        # Get elements of links which weren't present in class selection
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
                name = row.name.replace("'", "").replace('Location of ', '').replace('\n', ' ')\
                    .replace('\r', ' ')
                nodes += "{'id':'" + str(row.id) + "', 'name':'" + truncate_string(name, span=False)
                nodes += "', 'color':'" + color + "'},"
        return "graph = {'nodes': [" + nodes + "], " + edges + "};" if nodes else None
