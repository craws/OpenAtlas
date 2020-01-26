from __future__ import annotations  # Needed for Python 4.0 type annotations

import ast
from typing import Any, Dict, List, Optional, Tuple

from flask import g
from flask_wtf import FlaskForm
from psycopg2.extras import NamedTupleCursor

from openatlas import app
from openatlas.models.entity import Entity


class Node(Entity):

    count = 0
    count_subs = 0
    locked = False
    multiple = False
    system = False
    value_type = False
    directional = False

    def __init__(self, row: NamedTupleCursor.Record) -> None:
        super().__init__(row)
        self.root: List[int] = []
        self.subs: List[int] = []
        self.forms: Dict[int, Any] = {}

    @staticmethod
    def get_all_nodes() -> Dict[int, Node]:
        """ Get and return all type and place nodes"""
        sql = """
            SELECT e.id, e.name, e.class_code, e.description, e.system_type, e.created, e.modified,
                es.id AS super_id, COUNT(l2.id) AS count, COUNT(l3.id) AS count_property
            FROM model.entity e                

            -- Get super
            LEFT JOIN model.link l ON e.id = l.domain_id AND l.property_code = %(property_code)s
            LEFT JOIN model.entity es ON l.range_id = es.id

            -- Get count
            LEFT JOIN model.link l2 ON e.id = l2.range_id AND l2.property_code IN ('P2', 'P89')
            LEFT JOIN model.link l3 ON e.id = l3.type_id
            
            WHERE e.class_code = %(class_code)s
                AND (e.system_type IS NULL OR e.system_type != 'place location')
            GROUP BY e.id, es.id                        
            ORDER BY e.name;"""
        g.execute(sql, {'class_code': 'E55', 'property_code': 'P127'})
        types = g.cursor.fetchall()
        g.execute(sql, {'class_code': 'E53', 'property_code': 'P89'})
        places = g.cursor.fetchall()
        nodes = {}

        for row in types + places:
            node = Node(row)
            nodes[node.id] = node
            node.count = row.count + row.count_property
            node.count_subs = 0
            node.subs = []
            node.locked = False
            node.root = [row.super_id] if row.super_id else []
        Node.populate_subs(nodes)
        return nodes

    @staticmethod
    def populate_subs(nodes: Dict[int, Node]) -> None:
        g.execute("SELECT id, name, extendable FROM web.form ORDER BY name ASC;")
        forms = {}
        for row in g.cursor.fetchall():
            forms[row.id] = {'id': row.id, 'name': row.name, 'extendable': row.extendable}
        sql = """
            SELECT h.id, h.name, h.multiple, h.system, h.directional, h.value_type, h.locked,
                (SELECT ARRAY(
                    SELECT f.id FROM web.form f JOIN web.hierarchy_form hf ON f.id = hf.form_id
                    AND hf.hierarchy_id = h.id)) AS form_ids
            FROM web.hierarchy h;"""
        g.execute(sql)
        hierarchies = {row.id: row for row in g.cursor.fetchall()}
        for id_, node in nodes.items():
            if node.root:
                super_ = nodes[node.root[0]]
                super_.subs.append(id_)
                node.root = Node.get_root_path(nodes, node, node.root[0], node.root)
                node.system = False
                node.locked = nodes[node.root[0]].locked
            else:
                node.value_type = hierarchies[node.id].value_type
                node.directional = hierarchies[node.id].directional
                node.multiple = hierarchies[node.id].multiple
                node.system = hierarchies[node.id].system
                node.locked = hierarchies[node.id].locked
                node.forms = {form_id: forms[form_id] for form_id in hierarchies[node.id].form_ids}

    @staticmethod
    def get_root_path(nodes: Dict[int, Node],
                      node: Node,
                      super_id: int,
                      root: List[int]) -> List[int]:
        super_ = nodes[super_id]
        super_.count_subs += node.count
        if not super_.root:
            return root
        node.root.append(super_.root[0])
        return Node.get_root_path(nodes, node, super_.root[0], root)

    @staticmethod
    def get_nodes(name: str) -> List[int]:
        for id_, node in g.nodes.items():
            if node.name == name and not node.root:
                return node.subs
        return []

    @staticmethod
    def get_hierarchy(name: str) -> Node:
        return [root for id_, root in g.nodes.items() if root.name == name.replace('_', ' ')][0]

    @staticmethod
    def get_tree_data(node_id: int, selected_ids: List[int]) -> List[Dict[str, Any]]:
        return Node.walk_tree(g.nodes[node_id].subs, selected_ids)

    @staticmethod
    def walk_tree(nodes: List[Node], selected_ids: List[int]) -> List[Dict[str, Any]]:
        items = []
        for id_ in nodes:
            item = g.nodes[id_]
            items.append({'id': item.id,
                          'text': item.name.replace("'", "&apos;"),
                          'state': {'selected': 'true'} if item.id in selected_ids else '',
                          'children': Node.walk_tree(item.subs, selected_ids)})
        return items

    @staticmethod
    def get_nodes_for_form(form_name: str) -> Dict[int, Node]:
        sql = """
            SELECT h.id FROM web.hierarchy h
            JOIN web.hierarchy_form hf ON h.id = hf.hierarchy_id
            JOIN web.form f ON hf.form_id = f.id AND f.name = %(form_name)s
            ORDER BY h.name;"""
        g.execute(sql, {'form_name': form_name})
        return {row.id: g.nodes[row.id] for row in g.cursor.fetchall()}

    @staticmethod
    def get_form_choices(root: Optional[Node] = None) -> List[Tuple[int, str]]:
        g.execute("SELECT f.id, f.name FROM web.form f WHERE f.extendable = True ORDER BY name ASC")
        return [(r.id, r.name) for r in g.cursor.fetchall() if not root or r.id not in root.forms]

    @staticmethod
    def save_entity_nodes(entity: Entity, form: Any) -> None:
        from openatlas.forms.forms import TreeField, TreeMultiField, ValueFloatField
        if hasattr(entity, 'nodes'):
            entity.delete_links(['P2', 'P89'])
        for field in form:
            if type(field) is ValueFloatField and entity.class_.code != 'E53':
                if field.data is not None:  # Allow to save 0 but not empty
                    entity.link('P2', g.nodes[int(field.name)], field.data)
            elif type(field) in (TreeField, TreeMultiField) and field.data:
                root = g.nodes[int(field.id)]
                try:
                    range_ = [g.nodes[int(field.data)]]
                except ValueError:  # Form value was a list string e.g. '[97,2798]'
                    range_ = [g.nodes[int(range_id)] for range_id in ast.literal_eval(field.data)]
                if root.name in ['Administrative Unit', 'Historical Place']:
                    if entity.class_.code == 'E53':
                        entity.link('P89', range_)
                elif entity.class_.code != 'E53':
                    entity.link('P2', range_)

    @staticmethod
    def insert_hierarchy(node: Node, form: FlaskForm, value_type: bool) -> None:
        sql = """
            INSERT INTO web.hierarchy (id, name, multiple, value_type)
            VALUES (%(id)s, %(name)s, %(multiple)s, %(value_type)s);"""
        multiple = False
        if value_type or (hasattr(form, 'multiple') and form.multiple and form.multiple.data):
            multiple = True
        g.execute(sql, {'id': node.id,
                        'name': node.name,
                        'multiple': multiple,
                        'value_type': value_type})
        Node.add_forms_to_hierarchy(node, form)

    @staticmethod
    def update_hierarchy(node: Node, form: FlaskForm) -> None:
        sql = "UPDATE web.hierarchy SET name = %(name)s, multiple = %(multiple)s WHERE id = %(id)s;"
        multiple = False
        if node.multiple or (hasattr(form, 'multiple') and form.multiple and form.multiple.data):
            multiple = True
        g.execute(sql, {'id': node.id, 'name': form.name.data, 'multiple': multiple})
        Node.add_forms_to_hierarchy(node, form)

    @staticmethod
    def add_forms_to_hierarchy(node: Node, form: FlaskForm) -> None:
        for form_id in form.forms.data:
            sql = """
                INSERT INTO web.hierarchy_form (hierarchy_id, form_id)
                VALUES (%(node_id)s, %(form_id)s);"""
            g.execute(sql, {'node_id': node.id, 'form_id': form_id})

    @staticmethod
    def get_node_orphans() -> List[Node]:
        return[n for key, n in g.nodes.items() if n.root and n.count < 1 and not n.subs]

    @staticmethod
    def move_entities(old_node: Node, new_type_id: int, checkbox_values: str) -> None:
        root = g.nodes[old_node.root[-1]]
        entity_ids = ast.literal_eval(checkbox_values)
        delete_ids = []
        if new_type_id:  # A new type was selected
            if root.multiple:
                cleaned_entity_ids = []
                for entity in Entity.get_by_ids(entity_ids, nodes=True):
                    if any(node.id == int(new_type_id) for node in entity.nodes):
                        delete_ids.append(entity.id)  # If already linked add to delete ids
                    else:
                        cleaned_entity_ids.append(entity.id)
                entity_ids = cleaned_entity_ids
            if entity_ids:
                if root.name in app.config['PROPERTY_TYPES']:
                    sql = """
                        UPDATE model.link SET type_id = %(new_type_id)s
                        WHERE type_id = %(old_type_id)s AND id IN %(entity_ids)s;"""
                else:
                    sql = """
                        UPDATE model.link SET range_id = %(new_type_id)s
                        WHERE range_id = %(old_type_id)s AND domain_id IN %(entity_ids)s;"""
                g.execute(sql, {'old_type_id': old_node.id,
                                'new_type_id': new_type_id,
                                'entity_ids': tuple(entity_ids)})
        else:
            delete_ids = entity_ids  # No new type was selected so delete all links

        if delete_ids:
            if root.name in app.config['PROPERTY_TYPES']:
                sql = """
                    Update model.link SET type_id = NULL
                    WHERE type_id = %(old_type_id)s AND id IN %(delete_ids)s;"""
            else:
                sql = """
                    DELETE FROM model.link
                    WHERE range_id = %(old_type_id)s AND domain_id IN %(delete_ids)s;"""
            g.execute(sql, {'old_type_id': old_node.id, 'delete_ids': tuple(delete_ids)})

    @staticmethod
    def get_all_sub_ids(node: Node, subs: Optional[List[int]] = None) -> List[int]:
        # Recursive function to return a list with all sub node ids
        subs = subs if subs else []
        subs += node.subs
        for sub_id in node.subs:
            Node.get_all_sub_ids(g.nodes[sub_id], subs)
        return subs

    @staticmethod
    def get_form_count(root_node: Node, form_id: int) -> NamedTupleCursor.Record:
        # Check if nodes are already linked to entities before offering to remove a node from form
        node_ids = Node.get_all_sub_ids(root_node)
        if not node_ids:  # There are no sub nodes so skipping test
            return
        g.execute("SELECT name FROM web.form WHERE id = %(form_id)s;", {'form_id': form_id})
        form_name = g.cursor.fetchone()[0]
        system_type = ''
        class_code: List[str] = []
        if form_name == 'Source':
            system_type = 'source content'
        elif form_name == 'Event':
            class_code = app.config['CLASS_CODES']['event']
        elif form_name == 'Person':
            class_code = ['E21']
        elif form_name == 'Group':
            class_code = ['E74']
        elif form_name == 'Legal Body':
            class_code = ['E40']
        else:
            system_type = form_name.lower()
        sql = """
            SELECT count(*) FROM model.link l
            JOIN model.entity e ON l.domain_id = e.id AND l.range_id IN %(node_ids)s
            WHERE l.property_code = 'P2' AND {sql_where} %(params)s;""".format(
                sql_where='e.system_type =' if system_type else 'e.class_code IN')
        g.execute(sql, {'node_ids': tuple(node_ids),
                        'params': system_type if system_type else tuple(class_code)})
        return g.cursor.fetchone()[0]

    @staticmethod
    def remove_form_from_hierarchy(root_node: Node, form_id: int) -> None:
        sql = """
            DELETE FROM web.hierarchy_form
            WHERE hierarchy_id = %(hierarchy_id)s AND form_id = %(form_id)s;"""
        g.execute(sql, {'hierarchy_id': root_node.id, 'form_id': form_id})

    @staticmethod
    def remove_by_entity_and_node(entity_id: int, node_id: int) -> None:
        sql = """
            DELETE FROM model.link
            WHERE domain_id = %(entity_id)s AND range_id = %(node_id)s AND property_code = 'P2';"""
        g.execute(sql, {'entity_id': entity_id, 'node_id': node_id})
