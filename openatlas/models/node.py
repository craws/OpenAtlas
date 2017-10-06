# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import openatlas
from collections import OrderedDict

from openatlas.forms import TreeField, TreeMultiField
from .entity import Entity, EntityMapper


class NodeMapper(EntityMapper):

    @staticmethod
    def get_all_nodes():
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
            JOIN model.class c ON e.class_id = c.id AND c.code = 'E55'

            -- get super
            LEFT JOIN model.link l
                ON e.id = l.domain_id AND
                l.property_id = (SELECT id FROM model.property WHERE code IN ('P127'))
            LEFT JOIN model.entity es ON l.range_id = es.id

            -- get count
            LEFT JOIN model.link l2 ON l2.range_id = e.id
            LEFT JOIN model.property p2 ON
                l2.property_id = p2.id AND
                p2.name IN ('is located at', 'has type')
            GROUP BY e.id, es.id
            ORDER BY e.name;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql)
        nodes = OrderedDict()
        for row in cursor.fetchall():
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
    def get_tree_data(node_id):
        node = openatlas.nodes[node_id]
        return "'core':{'data':[" + NodeMapper.walk_tree(node.subs, None) + "]}"

    @staticmethod
    def walk_tree(param, selected_ids=None):
        items = param if isinstance(param, list) else [param]
        selected_ids = selected_ids if isinstance(selected_ids, list) else [selected_ids]
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
            JOIN web.form f ON hf.form_id = f.id AND f.name = %(form_name)s;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'form_name': form_id})
        nodes = {}
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
                entity.link('P2', field.data)
