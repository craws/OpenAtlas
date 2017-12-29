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
        """
            Returns JavaScript data string for d3.js
        """
        classes = []
        for code, param in params['classes'].items():
            if param['active']:
                classes.append(code)
        properties = []
        for code, param in params['properties'].items():
            if param['active']:
                properties.append(code)
        sql = "SELECT domain_id, range_id FROM model.link WHERE property_code IN %(properties)s;"
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'properties': tuple(properties)})
        entities = []
        edges = ''
        for row in cursor.fetchall():
            if row.domain_id != row.range_id:  # prevent circular dependencies
                edges += "{'source': '" + str(row.domain_id)
                edges += "', 'target': '" + str(row.range_id) + "' },"
                entities.append(row.domain_id)
                entities.append(row.range_id)
        edges = " links: [" + edges + "]"
        nodes = ''
        entities_already = []
        sql = "SELECT id, class_code, name FROM model.entity WHERE class_code IN %(classes)s;"
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'classes': tuple(classes)})
        for row in cursor.fetchall():
            if params['options']['orphans'] or row.id in entities:
                name = row.name.replace("'", "").replace('Location of ', '')
                entities_already.append(row.id)
                nodes += "{'id':'" + str(row.id) + "', 'name':'" + truncate_string(name, 40, False)
                nodes += "', 'color':'" + params['classes'][row.class_code]['color'] + "'},"

        # Get elements of links which weren't present in class selection
        array_diff = Network.diff(entities, entities_already)
        if array_diff:
            sql = "SELECT id, class_code, name FROM model.entity WHERE id IN %(array_diff)s;"
            cursor = openatlas.get_cursor()
            cursor.execute(sql, {'array_diff': tuple(array_diff)})
            for row in cursor.fetchall():
                color = ''
                if row.class_code in params['classes']:
                    color = params['classes'][row.class_code]['color']
                name = row.name.replace("'", "").replace('Location of ', '')
                nodes += "{'id':'" + str(row.id) + "', 'name':'" + truncate_string(name, 40, False)
                nodes += "', 'color':'" + color + "'},"
        return "graph = {'nodes': [" + nodes + "], " + edges + "};"
