# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import openatlas
from openatlas.util.util import truncate_string


class Network(object):

    @staticmethod
    def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]

    @staticmethod
    def get_network_json(params):

        classes = []
        for code, param in params['classes'].items():
            if param['active']:
                classes.append(code)
        properties = []
        for code, param in params['properties'].items():
            if param['active']:
                properties.append(code)
        sql = """
            SELECT l.domain_id, l.range_id FROM model.link l
            JOIN model.property p ON l.property_id = p.id
            WHERE p.code IN %(properties)s;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'properties': tuple(properties)})
        entities = []
        edges = ''
        for row in cursor.fetchall():
            edges += "{'source': '" + str(row.domain_id)
            edges += "', 'target': '" + str(row.range_id) + "' },"
            entities.append(row.domain_id)
            entities.append(row.range_id)
        edges = " links: [" + edges + "]"
        nodes = ''
        entities_already = []
        sql = """
            SELECT e.id, e.class_id, e.name, c.code
            FROM model.entity e
            JOIN model.class c ON e.class_id = c.id
            WHERE c.code IN %(classes)s;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'classes': tuple(classes)})
        for row in cursor.fetchall():
            if row.name == 'History of the World':
                continue
            name = truncate_string(row.name.replace("'", "").replace('Location of ', ''), 40, False)
            if params['options']['orphans'] or row.id in entities:
                entities_already.append(row.id)
                nodes += "{'id':'" + str(row.id) + "', 'name':'" + name
                nodes += "', 'color':'" + params['classes'][row.code]['color'] + "'},"
        # Get elements of links which weren't present in class selection
        array_diff = Network.diff(entities, entities_already)
        if array_diff:
            sql = """
                SELECT e.id, e.class_id, e.name, c.code FROM model.entity e
                JOIN model.class c ON e.class_id = c.id
                WHERE e.id IN %(array_diff)s;"""
            cursor = openatlas.get_cursor()
            cursor.execute(sql, {'array_diff': tuple(array_diff)})
            for row in cursor.fetchall():
                name = truncate_string(row.name.replace("'", "").replace('Location of ', ''), 40, False)
                nodes += "{'id':'" + str(row.id) + "', 'name':'" + name
                nodes += "', 'color':'" + params['classes'][row.code]['color'] if row.code in params['classes'] else ''
                nodes += "'},"
        return "graph = {'nodes': [" + nodes + "], " + edges + "};"
