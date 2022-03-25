from __future__ import annotations  # Needed for Python 4.0 type annotations

import ast
from typing import Any, Optional

from flask import g

from openatlas import app
from openatlas.database.type import Type as Db
from openatlas.models.entity import Entity


class Type(Entity):
    count = 0
    count_subs = 0
    category = ''
    multiple = False
    directional = False

    def __init__(self, row: dict[str, Any]) -> None:
        super().__init__(row)
        self.root: list[int] = []
        self.subs: list[int] = []
        self.classes: list[str] = []

    @staticmethod
    def get_all() -> dict[int, Type]:
        types = {}
        for row in \
                Db.get_types('type', 'P127') + \
                Db.get_types('type_anthropology', 'P127') + \
                Db.get_types('administrative_unit', 'P89'):
            type_ = Type(row)
            types[type_.id] = type_
            type_.count = row['count'] if row['count'] \
                else row['count_property']
            type_.count_subs = 0
            type_.subs = []
            type_.root = [row['super_id']] if row['super_id'] else []
        Type.populate_subs(types)
        return types

    @staticmethod
    def populate_subs(types: dict[int, Type]) -> None:
        hierarchies = {row['id']: row for row in Db.get_hierarchies()}
        for type_ in types.values():
            if type_.root:
                super_ = types[type_.root[-1]]
                super_.subs.append(type_.id)
                type_.root = Type.get_root_path(
                    types,
                    type_,
                    type_.root[-1],
                    type_.root)
                type_.category = hierarchies[type_.root[0]]['category']
            else:
                type_.category = hierarchies[type_.id]['category']
                type_.multiple = hierarchies[type_.id]['multiple']
                type_.directional = hierarchies[type_.id]['directional']
                for class_ in g.classes.values():
                    if class_.hierarchies and type_.id in class_.hierarchies:
                        type_.classes.append(class_.name)

    @staticmethod
    def get_root_path(
            types: dict[int, Type],
            type_: Type,
            super_id: int,
            root: list[int]) -> list[int]:
        super_ = types[super_id]
        super_.count_subs += type_.count
        if not super_.root:
            return root
        type_.root.insert(0, super_.root[-1])
        return Type.get_root_path(types, type_, super_.root[-1], root)

    @staticmethod
    def get_types(name: str) -> list[int]:
        for type_ in g.types.values():
            if type_.name == name and not type_.root:
                return type_.subs
        return []  # pragma: no cover

    @staticmethod
    def check_hierarchy_exists(name: str) -> list[Type]:
        hierarchies = [
            root for root in g.types.values()
            if root.name == name and not root.root]
        return hierarchies

    @staticmethod
    def get_hierarchy(name: str) -> Type:
        return [
            root for root in g.types.values()
            if root.name == name and not root.root][0]

    @staticmethod
    def get_tree_data(
            type_id: int,
            selected_ids: list[int]) -> list[dict[str, Any]]:
        return Type.walk_tree(g.types[type_id].subs, selected_ids)

    @staticmethod
    def walk_tree(
            types: list[Type],
            selected_ids: list[int]) -> list[dict[str, Any]]:
        items = []
        for id_ in types:
            item = g.types[id_]
            items.append({
                'id': item.id,
                'text': item.name.replace("'", "&apos;"),
                'state':
                    {'selected': 'true'} if item.id in selected_ids else '',
                'children': Type.walk_tree(item.subs, selected_ids)})
        return items

    @staticmethod
    def get_class_choices(root: Optional[Type] = None) -> list[tuple[int, str]]:
        choices = []
        for class_ in g.classes.values():
            if class_.new_types_allowed \
                    and (not root or class_.name not in root.classes):
                choices.append((class_.name, class_.label))
        return choices

    @staticmethod
    def insert_hierarchy(
            type_: Type,
            category: str,
            classes: list[str],
            multiple: bool) -> None:
        Db.insert_hierarchy({
            'id': type_.id,
            'name': type_.name,
            'multiple': multiple,
            'category': category})
        Db.add_classes_to_hierarchy(type_.id, classes)

    @staticmethod
    def update_hierarchy(
            type_: Type,
            name: str,
            classes: list[str],
            multiple: bool) -> None:
        Db.update_hierarchy({
            'id': type_.id,
            'name': name,
            'multiple': multiple})
        Db.add_classes_to_hierarchy(type_.id, classes)

    @staticmethod
    def get_type_orphans() -> list[Type]:
        return [
            n for key, n in g.types.items()
            if n.root and n.count < 1 and not n.subs]

    @staticmethod
    def move_entities(
            old_type: Type,
            new_type_id: int,
            checkbox_values: str) -> None:
        root = g.types[old_type.root[0]]
        entity_ids = ast.literal_eval(checkbox_values)
        delete_ids = []
        if new_type_id:  # A new type was selected
            if root.multiple:
                cleaned_entity_ids = []
                for entity in Entity.get_by_ids(entity_ids, types=True):
                    if any(type_.id == int(new_type_id)
                           for type_ in entity.types):
                        delete_ids.append(entity.id)
                    else:
                        cleaned_entity_ids.append(entity.id)
                entity_ids = cleaned_entity_ids
            if entity_ids:
                data = {
                    'old_type_id': old_type.id,
                    'new_type_id': new_type_id,
                    'entity_ids': tuple(entity_ids)}
                if root.name in app.config['PROPERTY_TYPES']:
                    Db.move_link_type(data)
                else:
                    Db.move_entity_type(data)
        else:
            delete_ids = entity_ids  # No new type selected so delete all links

        if delete_ids:
            if root.name in app.config['PROPERTY_TYPES']:
                Db.remove_link_type(old_type.id, delete_ids)
            else:
                Db.remove_entity_type(old_type.id, delete_ids)

    @staticmethod
    def get_all_sub_ids(
            type_: Type,
            subs: Optional[list[int]] = None) -> list[int]:
        subs = (subs if subs else []) + type_.subs
        for sub_id in type_.subs:
            Type.get_all_sub_ids(g.types[sub_id], subs)
        return subs

    @staticmethod
    def get_form_count(root_type: Type, class_name: str) -> Optional[int]:
        if type_ids := Type.get_all_sub_ids(root_type):
            return Db.get_form_count(class_name, type_ids)
        return None

    @staticmethod
    def remove_class_from_hierarchy(class_name: str, hierarchy_id: int) -> None:
        Db.remove_class_from_hierarchy(class_name, hierarchy_id)

    @staticmethod
    def remove_by_entity_and_type(entity_id: int, type_id: int) -> None:
        Db.remove_by_entity_and_type(entity_id, type_id)

    @staticmethod
    def get_untyped(hierarchy_id: int) -> list[Entity]:
        hierarchy = g.types[hierarchy_id]
        classes = hierarchy.classes
        if hierarchy.name in ('Administrative unit', 'Historical place'):
            classes = 'object_location'  # pragma: no cover
        untyped = []
        for entity in Entity.get_by_class(classes, types=True):
            linked = False
            for type_ in entity.types:
                if type_.root[0] == hierarchy_id:
                    linked = True
                    break
            if not linked:
                if classes == 'object_location':  # pragma: no cover
                    if entity.get_linked_entity('P53', True):
                        untyped.append(entity)
                else:
                    untyped.append(entity)
        return untyped
