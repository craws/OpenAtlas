# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import ast

import openatlas
from collections import OrderedDict

from openatlas.forms import TreeField, TreeMultiField
from .entity import Entity, EntityMapper


class NodeMapper(EntityMapper):

    @staticmethod
    def get_all_nodes():
        """Get and return all type and place nodes"""
        sql = """
            SELECT
                e.id,
                e.name,
                e.class_id,
                e.description,
                e.created,
                e.modified,
                es.id AS super_id,
                COUNT(p2.id) AS count
            FROM model.entity e
            JOIN model.class c ON e.class_id = c.id AND c.code = '{class_code}' {class_condition}

            -- get super
            LEFT JOIN model.link l
                ON e.id = l.domain_id AND
                l.property_id = (SELECT id FROM model.property WHERE code = '{property_code}')
            LEFT JOIN model.entity es ON l.range_id = es.id

            -- get count
            LEFT JOIN model.link l2 ON l2.range_id = e.id
            LEFT JOIN model.property p2 ON
                l2.property_id = p2.id AND
                p2.code IN ('P2', 'P89')
            GROUP BY e.id, es.id
            ORDER BY e.name;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql.format(class_code='E55', property_code='P127', class_condition=''))
        types = cursor.fetchall()
        cursor.execute(sql.format(
            class_code='E53',
            property_code='P89',
            class_condition="AND e.name NOT LIKE 'Location of %'"))
        places = cursor.fetchall()
        nodes = OrderedDict()
        for row in types + places:
            node = Entity(row)
            nodes[node.id] = node
            node.count = row.count
            node.count_subs = 0
            node.subs = []
            node.root = [row.super_id] if row.super_id else []
        return nodes

    @staticmethod
    def populate_subs():
        forms = {}
        cursor = openatlas.get_cursor()
        cursor.execute("SELECT id, name, extendable FROM web.form ORDER BY name ASC;")
        for row in cursor.fetchall():
            forms[row.id] = {'id': row.id, 'name': row.name, 'extendable': row.extendable}
        sql = """
            SELECT h.id, h.name, h.multiple, h.system, h.extendable, h.directional,
                (SELECT ARRAY(
                    SELECT f.id FROM web.form f JOIN web.hierarchy_form hf ON f.id = hf.form_id
                    AND hf.hierarchy_id = h.id)) AS form_ids
            FROM web.hierarchy h;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql)
        hierarchies = {}
        for row in cursor.fetchall():
            hierarchies[row.id] = row
        for id_, node in openatlas.nodes.items():
            if node.root:
                super_ = openatlas.nodes[node.root[0]]
                super_.subs.append(id_)
                node.root = NodeMapper.get_root_path(node, node.root[0], node.root)
            else:
                node.directional = hierarchies[node.id].directional
                node.extendable = hierarchies[node.id].extendable
                node.multiple = hierarchies[node.id].multiple
                node.system = hierarchies[node.id].system
                node.forms = {}
                for form_id in hierarchies[node.id].form_ids:
                    node.forms[form_id] = forms[form_id]

    @staticmethod
    def get_root_path(node, super_id, root):
        super_ = openatlas.nodes[super_id]
        super_.count_subs += node.count
        if not super_.root:
            return root
        node.root.append(super_.root[0])
        return NodeMapper.get_root_path(node, super_.root[0], root)

    @staticmethod
    def get_nodes(name):
        for id_, node in openatlas.nodes.items():
            if node.name == name:
                return node.subs

    @staticmethod
    def get_hierarchy_by_name(name):
        for id_, node in openatlas.nodes.items():
            if node.name == name and not node.root:
                return node

    @staticmethod
    def move_entities(old_id, new_id, entity_ids):
        sql = """
            UPDATE model.link SET range_id = %(new_id)s
            WHERE range_id = %(old_id)s AND domain_id = ANY(%(entity_ids)s);"""
        params = {'old_id': old_id, 'new_id': new_id, 'entity_ids': list(map(int, entity_ids))}
        openatlas.get_cursor().execute(sql, params)

    @staticmethod
    def get_tree_data(node_id, selected_ids):
        node = openatlas.nodes[node_id]
        return "'core':{'data':[" + NodeMapper.walk_tree(node.subs, selected_ids) + "]}"

    @staticmethod
    def walk_tree(param, selected_ids):
        items = param if isinstance(param, list) else [param]
        string = ''
        for id_ in items:
            item = openatlas.nodes[id_]
            selected = ",'state' : {'selected' : true}" if item.id in selected_ids else ''
            string += "{'text':'" + item.name + "', 'id':'" + str(item.id) + "'" + selected
            if item.subs:
                string += ",'children' : ["
                for sub in item.subs:
                    string += NodeMapper.walk_tree(sub, selected_ids)
                string += "]"
            string += "},"
        return string

    @staticmethod
    def get_nodes_for_form(form_id):
        sql = """
            SELECT h.id FROM web.hierarchy h
            JOIN web.hierarchy_form hf ON h.id = hf.hierarchy_id
            JOIN web.form f ON hf.form_id = f.id AND f.name = %(form_name)s
            ORDER BY h.name;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'form_name': form_id})
        nodes = OrderedDict()
        for row in cursor.fetchall():
            nodes[row.id] = openatlas.nodes[row.id]
        return nodes

    @staticmethod
    def save_entity_nodes(entity, form):
        # Todo: don't delete/save if not changed
        if hasattr(entity, 'nodes'):
            sql = """
                    DELETE FROM model.link
                    WHERE domain_id = %(entity_id)s AND property_id = %(property_id)s"""
            openatlas.get_cursor().execute(sql, {
                'entity_id': entity.id,
                'property_id': openatlas.has_type_id})
        for field in form:
            if isinstance(field, (TreeField, TreeMultiField)) and field.data:
                try:
                    range_param = int(field.data)
                    node_class = openatlas.classes[openatlas.nodes[range_param].class_.id].code
                except ValueError:
                    range_param = ast.literal_eval(field.data)
                    if range_param:
                        node_class = openatlas.classes[openatlas.nodes[range_param].class_.id].code
                    else:
                        node_class = ''
                entity.link('P2' if node_class == 'E55' else 'P127', range_param)
