# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import ast

import openatlas
from collections import OrderedDict

from openatlas.forms.forms import TreeField, TreeMultiField
from openatlas.models.linkProperty import LinkPropertyMapper
from .entity import Entity, EntityMapper


class NodeMapper(EntityMapper):

    @staticmethod
    def get_all_nodes():
        """Get and return all type and place nodes"""
        sql = """
            SELECT
                e.id,
                e.name,
                e.class_code,
                e.description,
                e.system_type,
                e.created,
                e.modified,
                es.id AS super_id,
                COUNT(l2.id) AS count,
                COUNT(lp.id) AS count_property
            FROM model.entity e                

            -- get super
            LEFT JOIN model.link l ON e.id = l.domain_id AND l.property_code = %(property_code)s
            LEFT JOIN model.entity es ON l.range_id = es.id

            -- get count
            LEFT JOIN model.link l2 ON e.id = l2.range_id AND l2.property_code IN ('P2', 'P89')
            LEFT JOIN model.link_property lp ON e.id = lp.range_id AND lp.property_code = 'P2'
            
            WHERE e.class_code = %(class_code)s
                AND (e.system_type IS NULL OR e.system_type != 'place location')
            GROUP BY e.id, es.id                        
            ORDER BY e.name;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'class_code': 'E55', 'property_code': 'P127'})
        types = cursor.fetchall()
        cursor.execute(sql, {'class_code': 'E53', 'property_code': 'P89'})
        places = cursor.fetchall()
        nodes = OrderedDict()
        for row in types + places:
            node = Entity(row)
            nodes[node.id] = node
            node.count = row.count + row.count_property
            node.count_subs = 0
            node.subs = []
            node.root = [row.super_id] if row.super_id else []
        NodeMapper.populate_subs(nodes)
        return nodes

    @staticmethod
    def populate_subs(nodes):
        forms = {}
        cursor = openatlas.get_cursor()
        cursor.execute("SELECT id, name, extendable FROM web.form ORDER BY name ASC;")
        for row in cursor.fetchall():
            forms[row.id] = {'id': row.id, 'name': row.name, 'extendable': row.extendable}
        sql = """
            SELECT h.id, h.name, h.multiple, h.system, h.directional,
                (SELECT ARRAY(
                    SELECT f.id FROM web.form f JOIN web.hierarchy_form hf ON f.id = hf.form_id
                    AND hf.hierarchy_id = h.id)) AS form_ids
            FROM web.hierarchy h;"""
        cursor.execute(sql)
        hierarchies = {}
        for row in cursor.fetchall():
            hierarchies[row.id] = row
        for id_, node in nodes.items():
            if node.root:
                super_ = nodes[node.root[0]]
                super_.subs.append(id_)
                node.root = NodeMapper.get_root_path(nodes, node, node.root[0], node.root)
                node.system = False
            else:
                node.directional = hierarchies[node.id].directional
                node.multiple = hierarchies[node.id].multiple
                node.system = hierarchies[node.id].system
                node.forms = {}
                for form_id in hierarchies[node.id].form_ids:
                    node.forms[form_id] = forms[form_id]

    @staticmethod
    def get_root_path(nodes, node, super_id, root):
        super_ = nodes[super_id]
        super_.count_subs += node.count
        if not super_.root:
            return root
        node.root.append(super_.root[0])
        return NodeMapper.get_root_path(nodes, node, super_.root[0], root)

    @staticmethod
    def get_nodes(name):
        for id_, node in openatlas.nodes.items():
            if node.name == name and not node.root:
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
        return NodeMapper.walk_tree(node.subs, selected_ids)

    @staticmethod
    def walk_tree(param, selected_ids):
        string = ''
        for id_ in param if isinstance(param, list) else [param]:
            item = openatlas.nodes[id_]
            selected = ",'state' : {'selected' : true}" if item.id in selected_ids else ''
            name = item.name.replace("'", "&apos;")
            string += "{'text':'" + name + "', 'id':'" + str(item.id) + "'" + selected
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
    def get_form_choices():
        sql = "SELECT f.id, f.name FROM web.form f WHERE f.extendable = True ORDER BY name ASC;"
        cursor = openatlas.get_cursor()
        cursor.execute(sql)
        forms = []
        for row in cursor.fetchall():
            forms.append((row.id, row.name))
        return forms

    @staticmethod
    def save_entity_nodes(entity, form):
        # Todo: don't delete/save if not changed
        # Todo: just delete node ids?
        if hasattr(entity, 'nodes'):
            entity.delete_links(['P2', 'P89'])

        for field in form:
            if isinstance(field, (TreeField, TreeMultiField)) and field.data:
                try:
                    range_param = int(field.data)
                except ValueError:
                    range_param = ast.literal_eval(field.data)
                node = openatlas.nodes[int(field.id)]
                if node.name in ['Administrative Unit', 'Historical Place']:
                    if entity.class_.code == 'E53':
                        entity.link('P89', range_param)
                else:
                    if entity.class_.code != 'E53':
                        entity.link('P2', range_param)

    @staticmethod
    def save_link_nodes(link_id, form):
        for field in form:
            if isinstance(field, TreeField) and field.data:
                LinkPropertyMapper.insert(link_id, 'P2', int(field.data))

    @staticmethod
    def insert_hierarchy(node, form):
        sql = """
            INSERT INTO web.hierarchy (id, name, multiple)
            VALUES (%(id)s, %(name)s, %(multiple)s);"""
        openatlas.get_cursor().execute(sql, {
            'id': node.id,
            'name': node.name,
            'multiple': form.multiple.data})
        NodeMapper.add_forms_to_hierarchy(node, form)

    @staticmethod
    def update_hierarchy(node, form):
        sql = "UPDATE web.hierarchy SET name = %(name)s, multiple = %(multiple)s WHERE id = %(id)s;"
        multiple = True if node.multiple or form.multiple.data else False
        openatlas.get_cursor().execute(sql, {
            'id': node.id, 'name': form.name.data, 'multiple': multiple})
        NodeMapper.add_forms_to_hierarchy(node, form)

    @staticmethod
    def add_forms_to_hierarchy(node, form):
        cursor = openatlas.get_cursor()
        for form_id in form.forms.data:
            sql = """
                INSERT INTO web.hierarchy_form (hierarchy_id, form_id)
                VALUES (%(node_id)s, %(form_id)s);"""
            cursor.execute(sql, {'node_id': node.id, 'form_id': form_id})

    @staticmethod
    def get_orphans():
        nodes = []
        for key, node in openatlas.nodes.items():
            if node.root and node.count < 1 and not node.subs:
                nodes.append(node)
        return nodes
