from __future__ import annotations

import ast
import json
from typing import Any, Iterable, Optional

from flask import g, request
from werkzeug.exceptions import abort

from openatlas import app
from openatlas.database import (
    date, entity as db, link as db_link, tools as db_tools)
from openatlas.display.util2 import convert_size, sanitize
from openatlas.models.annotation import AnnotationText
from openatlas.models.dates import Dates
from openatlas.models.gis import Gis
from openatlas.models.tools import get_carbon_link

# Todo: remove? Property types work differently, e.g. no move functionality
app.config['PROPERTY_TYPES'] = [
    'Actor relation',
    'Actor function',
    'External reference match',
    'Involvement']


class Entity:
    count = 0
    count_subs = 0
    category = ''
    multiple = False
    required = False
    directional = False
    selectable = True
    system = False

    def __init__(self, data: dict[str, Any]) -> None:
        self.class_ = g.classes[data['openatlas_class_name']]
        self.cidoc_class = self.class_.cidoc_class
        self.id = 0
        self.name = None
        self.aliases = {}
        self.description = None
        self.created = None
        self.modified = None
        self.origin_id: Optional[int] = None  # When coming from another entity
        self.image_id: Optional[int] = None  # Profile image
        self.location: Optional[Entity] = None  # Respective location if place
        self.types = {}
        self.standard_type = None
        self.root: list[int] = []
        self.subs: list[int] = []
        self.classes: list[str] = []
        self.dates = Dates(data)

        for name, value in data.items():
            if not value and value != 0:
                continue
            match name:
                case 'types':
                    for item in value:  # f1 = type id, f2 = value
                        type_ = g.types[item['f1']]
                        if type_.class_.name == 'type_tools':
                            continue
                        self.types[type_] = item['f2']
                        if type_.category == 'standard':
                            self.standard_type = type_
                case 'aliases':
                    for alias in data['aliases']:  # f1 = id, f2 = name
                        self.aliases[alias['f1']] = alias['f2']
                    self.aliases = dict(
                        sorted(
                            self.aliases.items(),
                            key=lambda item_: item_[1]))
                case _:
                    setattr(self, name, value)
        if self.class_.name == 'file':
            self.public = False
            self.creator = None
            self.license_holder = None
            if self.id in g.file_info:
                self.public = g.file_info[self.id]['public']
                self.creator = g.file_info[self.id]['creator']
                self.license_holder = g.file_info[self.id]['license_holder']
        if self.class_.name == 'reference_system' and 'website_url' in data:
            self.website_url = data['website_url']
            self.resolver_url = data['resolver_url']
            self.example_id = data['identifier_example']
            self.system = data['system']
            self.classes: list[str] = []

    def get_linked_entity(
            self,
            code: str,
            classes: Optional[list[str]] = None,
            inverse: bool = False,
            types: bool = False) -> Optional[Entity]:
        return Entity.get_linked_entity_static(
            self.id,
            code,
            classes,
            inverse=inverse,
            types=types)

    def get_linked_entity_safe(
            self,
            code: str,
            inverse: bool = False,
            types: bool = False) -> Entity:
        return Entity.get_linked_entity_safe_static(
            self.id,
            code,
            inverse=inverse,
            types=types)

    def get_linked_entities(
            self,
            code: str | list[str],
            classes: Optional[list[str]] = None,
            inverse: bool = False,
            types: bool = False,
            sort: bool = False) -> list[Entity]:
        return Entity.get_linked_entities_static(
            self.id,
            code,
            classes,
            inverse=inverse,
            types=types,
            sort=sort)

    def get_linked_entity_ids_recursive(
            self,
            codes: list[str] | str,
            inverse: bool = False) -> list[int]:
        return db.get_linked_entities_recursive(self.id, codes, inverse)

    def get_linked_entities_recursive(
            self,
            codes: list[str] | str,
            inverse: bool = False,
            types: bool = False) -> list[Entity]:
        return Entity.get_by_ids(
            db.get_linked_entities_recursive(self.id, codes, inverse),
            types=types)

    def link(self,
             code: str,
             range_: Entity | list[Entity],
             description: Optional[str] = None,
             inverse: bool = False,
             type_id: Optional[int] = None,
             dates: Optional[dict] = None) -> list[int]:
        property_ = g.properties[code]
        entities = range_ if isinstance(range_, list) else [range_]
        new_link_ids = []
        for linked_entity in entities:
            domain = linked_entity if inverse else self
            range_ = self if inverse else linked_entity
            domain_error = True
            range_error = True
            if property_.find_object(
                    'domain_class_code',
                    domain.class_.cidoc_class.code):
                domain_error = False
            if property_.find_object(
                    'range_class_code',
                    range_.class_.cidoc_class.code):
                range_error = False
            if domain_error or range_error:  # pragma: no cover
                text = \
                    f"invalid CIDOC link {domain.class_.cidoc_class.code}" \
                    f" > {code} > {range_.class_.cidoc_class.code}"
                g.logger.log('error', 'model', text)
                abort(400, text)
            data = {
                'property_code': code,
                'domain_id': domain.id,
                'range_id': range_.id,
                'description': sanitize(description)
                if isinstance(description, str) else description,
                'type_id': type_id}
            data.update(dates or {
                'begin_from': None,
                'begin_to': None,
                'begin_comment': None,
                'end_from': None,
                'end_to': None,
                'end_comment': None})
            id_ = db.link(data)
            new_link_ids.append(id_)
        return new_link_ids

    def link_string(
            self,
            code: str,
            range_: str,  # int or list[int] form string value, e.g. '1', '[1]'
            description: Optional[str] = None,
            inverse: bool = False) -> None:
        ids = ast.literal_eval(range_)
        ids = [int(i) for i in ids] if isinstance(ids, list) else [int(ids)]
        self.link(code, Entity.get_by_ids(ids), sanitize(description), inverse)

    def get_links(
            self,
            codes: str | list[str],
            classes: Optional[list[str]] = None,
            inverse: bool = False) -> list[Link]:
        return Entity.get_links_of_entities(self.id, codes, classes, inverse)

    def delete(self) -> None:
        db.delete(self.id)

    def delete_links(
            self,
            property_: str,
            classes: list[str],
            inverse: bool = False) -> None:
        db.delete_links_by_property_and_class(
            self.id,
            property_,
            classes,
            inverse)

    def delete_links_old(
            self,
            codes: list[str],
            inverse: bool = False) -> None:
        # Todo: remove this function after new classes
        if self.class_.name == 'stratigraphic_unit' \
                and 'P2' in codes \
                and not inverse:
            exclude_ids = g.sex_type.get_sub_ids_recursive()
            exclude_ids.append(g.radiocarbon_type.id)
            if db_tools.get_sex_types(self.id) or get_carbon_link(self):
                db.remove_types(self.id, exclude_ids)
                codes.remove('P2')
                if not codes:
                    return
        db.delete_links_by_codes(self.id, codes, inverse)

    def save_file_info(self, data: dict[str, Any]) -> None:
        db.update_file_info({
            'entity_id': self.id,
            'creator': data.get('creator'),
            'license_holder': data.get('license_holder'),
            'public': data.get('public', False)})

    def update(self, data: dict[str, Any]) -> None:
        data['id'] = self.id
        annotation_data = []
        if self.class_.attributes.get('description', []).get('annotated'):
            result = AnnotationText.extract_annotations(data['description'])
            data['description'] = result['text']
            annotation_data = result['data']
            AnnotationText.delete_annotations_text(self.id)
        for item in ['name', 'description']:
            data[item] = sanitize(data.get(item, getattr(self, item)))
        db.update(data)
        for annotation in annotation_data:
            annotation['source_id'] = self.id
            AnnotationText.insert(annotation)
        for attribute in self.class_.attributes:
            match attribute:
                case 'alias':
                    self.update_aliases(data.get('alias', []))
                case 'location':
                    self.update_gis(data['gis'])
                case 'file':
                    self.save_file_info(data)
                case 'resolver_url':
                    db.update_reference_system({
                        'entity_id': self.id,
                        'name': self.name,
                        'website_url': data['website_url'],
                        'resolver_url': data['resolver_url'],
                        'identifier_example': sanitize(data['example_id'])})
                    if data['reference_system_classes']:
                        db.add_reference_system_classes(
                            self.id,
                            data['reference_system_classes'])

        # continue_link_id = None
        # if 'administrative_units' in data \
        #        and self.class_.name != 'administrative_unit':
        #   self.update_administrative_units(data['administrative_units'], new)
        # if 'links' in data:
        #    continue_link_id = self.update_links(data, new)
        # return continue_link_id

    def update_administrative_units(
            self,
            units: dict[str, list[int]],
            new: bool) -> None:
        if not self.location:
            self.location = self.get_linked_entity_safe('P53')
        if not new:
            self.location.delete_links_old(['P89'])
        if units:
            self.location.link('P89', [g.types[id_] for id_ in units])

    def get_annotated_text(self) -> str:
        offset = 0
        text = self.description
        for annotation in AnnotationText.get_by_source_id(self.id):
            dict_ = {'annotationId': f'a-{annotation.id}'}
            if annotation.entity_id:
                dict_['entityId'] = annotation.entity_id
            if annotation.text:
                dict_['comment'] = annotation.text
            inner_text = text[
                annotation.link_start + offset: annotation.link_end + offset]
            meta = str(json.dumps(dict_)).replace('"', '&quot;')
            mark = f'<mark meta="{meta}">{inner_text}</mark>'
            start = annotation.link_start + offset
            end = annotation.link_end + offset
            text = text[:start] + mark + text[end:]
            offset += (len(mark) - len(inner_text))
        return text.replace('\n', '<br>') if text else text

    def update_aliases(self, aliases: list[str]) -> None:
        for id_, alias in self.aliases.items():
            if alias in aliases:
                aliases.remove(alias)
            else:
                Entity.get_by_id(int(id_)).delete()
        for alias in aliases:
            if alias.strip():
                self.link(
                    'P1',
                    insert({
                        'name': alias,
                        'openatlas_class_name': 'appellation'}))

    # Todo: Only used for imports. Has to be adapted and maybe move there?
    def update_links(self, data: dict[str, Any], new: bool) -> Optional[int]:
        if not new:
            if 'delete' in data['links'] and data['links']['delete']:
                self.delete_links_old(data['links']['delete'])
            if 'delete_inverse' in data['links'] \
                    and data['links']['delete_inverse']:
                self.delete_links_old(data['links']['delete_inverse'], True)
            if 'delete_reference_system' in data['links'] \
                    and data['links']['delete_reference_system']:
                db.delete_reference_system_links(self.id)
        continue_link_id = None
        for link_ in data['links']['insert']:
            ids = self.link(
                link_['property'],
                link_['range'],
                link_['description'],
                link_['inverse'],
                link_['type_id'])
            if 'attributes_link' in data:
                for id_ in ids:
                    item = Link.get_by_id(id_)
                    item.begin_from = data['attributes_link']['begin_from']
                    item.begin_to = data['attributes_link']['begin_to']
                    item.begin_comment = \
                        data['attributes_link']['begin_comment']
                    item.end_from = data['attributes_link']['end_from']
                    item.end_to = data['attributes_link']['end_to']
                    item.end_comment = data['attributes_link']['end_comment']
                    # item.update()
            if link_['return_link_id']:
                continue_link_id = ids[0]
        return continue_link_id

    def update_gis(self, gis_data: dict[str, Any], new: bool = False) -> None:
        if new:
            location = insert({
                'name': f'Location of {self.name}',
                'openatlas_class_name': 'object_location'})
            self.link('P53', location)
        else:
            location = self.get_linked_entity_safe('P53')
            db.update({
                'id': location.id,
                'name': f"Location of {sanitize(self.name)}"})
            Gis.delete_by_entity(location)
        if gis_data:
            Gis.insert(location, gis_data)

    def get_profile_image_id(self) -> Optional[int]:
        return db.get_profile_image_id(self.id)

    def remove_profile_image(self) -> None:
        db.remove_profile_image(self.id)

    def get_name_directed(self, inverse: bool = False) -> str | None:
        """Returns name part of a directed type e.g. parent of (child of)"""
        name_parts = self.name.split(' (')
        if inverse and len(name_parts) > 1:  # Remove closing bracket
            return sanitize(name_parts[1][:-1])  # pragma: no cover
        return name_parts[0]

    def check_too_many_single_type_links(self) -> bool:
        type_dict: dict[int, int] = {}
        for type_ in self.types:
            if type_.root[0] in type_dict:
                type_dict[type_.root[0]] += 1
                continue
            type_dict[type_.root[0]] = 1
        for id_, count in type_dict.items():
            if count > 1 and not g.types[id_].multiple:
                return True
        return False

    def get_structure(self) -> dict[str, list[Entity]]:
        structure: dict[str, list[Entity]] = {
            'siblings': [],
            'supers': self.get_linked_entities_recursive('P46', inverse=True),
            'subunits': self.get_linked_entities('P46', types=True)}
        if structure['supers']:
            structure['siblings'] = \
                structure['supers'][-1].get_linked_entities('P46')
        return structure

    def get_structure_for_insert(self) -> dict[str, list[Entity]]:
        return {
            'siblings': self.get_linked_entities('P46'),
            'subunits': [],
            'supers':
                self.get_linked_entities_recursive('P46', inverse=True) +
                [self]}

    def get_file_size(self) -> str:
        return convert_size(g.files[self.id].stat().st_size) \
            if self.id in g.files else 'N/A'

    def get_file_ext(self) -> str:
        return g.files[self.id].suffix if self.id in g.files else 'N/A'

    def get_sub_ids_recursive(
            self,
            subs: Optional[list[int]] = None) -> list[int]:
        subs = subs or []
        for sub_id in self.subs:
            subs.append(sub_id)
            Entity.get_sub_ids_recursive(g.types[sub_id], subs)
        return subs

    def get_count_by_class(self, name: str) -> Optional[int]:
        if type_ids := self.get_sub_ids_recursive():
            return db.get_class_count(name, type_ids)
        return None

    def set_required(self) -> None:
        db.set_required(self.id)

    def unset_required(self) -> None:
        db.unset_required(self.id)

    def set_selectable(self) -> None:
        db.set_selectable(self.id)

    def unset_selectable(self) -> None:
        if not self.count and self.category != 'value':
            db.unset_selectable(self.id)

    def remove_class(self, name: str) -> None:
        db.remove_class(self.id, name)

    def remove_reference_system_class(self, name: str) -> None:
        db.remove_reference_system_class(self.id, name)

    def remove_entity_links(self, entity_id: int) -> None:
        db.remove_entity_links(self.id, entity_id)

    def get_untyped(self) -> list[Entity]:
        untyped = []
        for entity in Entity.get_by_class(self.classes, types=True):
            linked = False
            to_check = entity
            if self.name in ('Administrative unit', 'Historical place'):
                to_check = entity.get_linked_entity_safe('P53', types=True)
            for type_ in to_check.types:
                if type_.root[0] == self.id:
                    linked = True
                    break
            if not linked:
                untyped.append(entity)
        return untyped

    def update_hierarchy(
            self,
            name: str,
            classes: list[str],
            multiple: bool) -> None:
        db.update_hierarchy({
            'id': self.id,
            'name': sanitize(name),
            'multiple': multiple})
        db.add_classes_to_hierarchy(self.id, classes)

    def move_entities(self, new_type_id: int, checkbox_values: str) -> None:
        root = g.types[self.root[0]]
        entity_ids = ast.literal_eval(checkbox_values)
        delete_ids = []
        if new_type_id:  # A new type was selected
            if root.multiple:
                cleaned_entity_ids = []
                for e in Entity.get_by_ids(entity_ids, types=True):
                    if any(type_.id == int(new_type_id) for type_ in e.types):
                        delete_ids.append(e.id)
                        continue
                    cleaned_entity_ids.append(e.id)
                entity_ids = cleaned_entity_ids
            if entity_ids:
                data = {
                    'old_type_id': self.id,
                    'new_type_id': new_type_id,
                    'entity_ids': tuple(entity_ids)}
                if root.name in app.config['PROPERTY_TYPES']:
                    db.move_link_type(data)
                else:
                    db.move_entity_type(data)
        else:
            delete_ids = entity_ids  # No new type selected so delete all links

        if delete_ids:
            if root.name in app.config['PROPERTY_TYPES']:
                db.remove_link_type(self.id, delete_ids)
            else:
                db.remove_entity_type(self.id, delete_ids)

    @staticmethod
    def get_file_info() -> dict[int, Any]:
        return db.get_file_info()

    @staticmethod
    def get_by_class(
            classes: str | list[str],
            types: bool = False,
            aliases: bool = False) -> list[Entity]:
        if aliases:  # For performance: check classes if they can have an alias
            aliases = False
            for class_ in classes if isinstance(classes, list) else [classes]:
                if g.classes[class_].attributes.get('alias'):
                    aliases = True
                    break
        return [
            Entity(row) for row in db.get_by_class(classes, types, aliases)]

    @staticmethod
    def get_display_files() -> list[Entity]:
        entities = []
        for row in db.get_by_class('file', types=True):
            ext = g.files[row['id']].suffix if row['id'] in g.files else 'N/A'
            if ext in app.config['DISPLAY_FILE_EXT']:
                entities.append(Entity(row))
        return entities

    @staticmethod
    def get_by_cidoc_class(
            code: str | list[str],
            types: bool = False,
            aliases: bool = False) -> list[Entity]:
        return [
            Entity(row) for row in db.get_by_cidoc_class(code, types, aliases)]

    @staticmethod
    def get_by_id(
            id_: int,
            types: bool = False,
            aliases: bool = False,
            with_location: bool = True) -> Entity:
        if id_ in g.types:
            return g.types[id_]
        if id_ in g.reference_systems:
            return g.reference_systems[id_]
        data = db.get_by_id(id_, types, aliases)
        if not data:
            if 'activity' in request.path:  # Re-raise if in user activity view
                raise AttributeError
            abort(418)
        entity = Entity(data)
        if entity.class_.name == 'place' and with_location:
            entity.location = entity.get_linked_entity_safe('P53', types=True)
            if types:
                entity.types.update(entity.location.types)
        return entity

    @staticmethod
    def get_by_ids(
            ids: Iterable[int],
            types: bool = False,
            aliases: bool = False, ) -> list[Entity]:
        entities = []
        for row in db.get_by_ids(ids, types, aliases):
            if row['id'] in g.types:
                entities.append(g.types[row['id']])
            elif row['id'] in g.reference_systems:
                entities.append(g.reference_systems[row['id']])
            else:
                entities.append(Entity(row))
        return entities

    @staticmethod
    def get_by_project_id(project_id: int) -> list[Entity]:
        entities = []
        for row in db.get_by_project_id(project_id):
            entity = Entity(row)
            entity.origin_id = row['origin_id']
            entities.append(entity)
        return entities

    @staticmethod
    def get_overview_counts() -> dict[str, int]:
        return db.get_overview_counts(g.classes)

    @staticmethod
    def get_overview_counts_by_type(ids: list[int]) -> dict[str, int]:
        return db.get_overview_counts_by_type(ids, g.classes.keys())

    @staticmethod
    def get_latest(limit: int) -> list[Entity]:
        classes = []
        for class_ in g.classes.values():
            if class_.group and class_.name != 'reference_system':
                classes.append(class_.name)
        return [Entity(r) for r in db.get_latest(classes, limit)]

    @staticmethod
    def set_profile_image(id_: int, origin_id: int) -> None:
        db.set_profile_image(id_, origin_id)

    @staticmethod
    def get_roots(
            property_code: str,
            ids: list[int],
            inverse: bool = False) -> dict[int, Any]:
        return db.get_roots(property_code, ids, inverse)

    @staticmethod
    def get_links_of_entities(
            entity_ids: int | list[int],
            codes: str | list[str] | None = None,
            classes: Optional[list[str]] = None,
            inverse: bool = False) -> list[Link]:
        result = set()
        if codes:
            codes = codes if isinstance(codes, list) else [str(codes)]
        rows = db.get_links_of_entities(entity_ids, codes, classes, inverse)
        for row in rows:
            result.add(row['domain_id'])
            result.add(row['range_id'])
        linked_entities = {
            e.id: e for e in Entity.get_by_ids(result, types=True)}
        links = []
        for row in rows:
            links.append(
                Link(
                    row,
                    domain=linked_entities[row['domain_id']],
                    range_=linked_entities[row['range_id']]))
        return links

    @staticmethod
    def get_linked_entity_static(
            id_: int,
            code: str,
            classes: Optional[list[str]] = None,
            inverse: bool = False,
            types: bool = False) -> Optional[Entity]:
        result = Entity.get_linked_entities_static(
            id_,
            code,
            classes,
            inverse=inverse,
            types=types)
        if len(result) > 1:  # pragma: no cover
            g.logger.log(
                'error',
                'model',
                f'Multiple linked entities found for {code}')
            abort(400, 'Multiple linked entities found')
        return result[0] if result else None

    @staticmethod
    def get_linked_entities_static(
            id_: int,
            codes: str | list[str],
            classes: Optional[list[str]] = None,
            inverse: bool = False,
            types: bool = False,
            sort: bool = False) -> list[Entity]:
        codes = codes if isinstance(codes, list) else [codes]
        entities = Entity.get_by_ids(
            db.get_linked_entities_inverse(id_, codes, classes) if inverse
            else db.get_linked_entities(id_, codes, classes),
            types=types)
        if sort and entities:
            entities.sort(key=lambda x: x.name)
        return entities

    @staticmethod
    def get_linked_entity_safe_static(
            id_: int,
            code: str,
            classes: Optional[list[str]] = None,
            inverse: bool = False,
            types: bool = False) -> Entity:
        entity = Entity.get_linked_entity_static(
            id_,
            code,
            classes,
            inverse,
            types)
        if not entity:  # pragma: no cover
            g.logger.log(
                'error',
                'model',
                'missing linked',
                f'id: {id_}, code: {code}')
            abort(418, f'Missing linked {code} for {id_}')
        return entity

    @staticmethod
    def get_all_types(with_count: bool) -> dict[int, Entity]:
        types = {}
        for row in db.get_types(with_count):
            type_ = Entity(row)
            types[type_.id] = type_
            type_.count = row['count'] or row['count_property']
            type_.count_subs = 0
            type_.subs = []
            type_.root = [row['super_id']] if row['super_id'] else []
            type_.selectable = not row['non_selectable']
        Entity.populate_subs(types)
        return types

    @staticmethod
    def populate_subs(types: dict[int, Entity]) -> None:
        hierarchies = {row['id']: row for row in db.get_hierarchies()}
        for type_ in types.values():
            if type_.root:
                super_ = types[type_.root[-1]]
                super_.subs.append(type_.id)
                type_.root = Entity.get_root_path(
                    types,
                    type_,
                    type_.root[-1],
                    type_.root)
                type_.category = hierarchies[type_.root[0]]['category']
                continue
            type_.category = hierarchies[type_.id]['category']
            type_.multiple = hierarchies[type_.id]['multiple']
            type_.required = hierarchies[type_.id]['required']
            type_.directional = hierarchies[type_.id]['directional']
            for class_ in g.classes.values():
                if class_.hierarchies and type_.id in class_.hierarchies:
                    type_.classes.append(class_.name)

    @staticmethod
    def get_root_path(
            types: dict[int, Entity],
            type_: Entity,
            super_id: int,
            root: list[int]) -> list[int]:
        super_ = types[super_id]
        super_.count_subs += type_.count
        if not super_.root:
            return root
        type_.root.insert(0, super_.root[-1])
        return Entity.get_root_path(types, type_, super_.root[-1], root)

    @staticmethod
    def check_hierarchy_exists(name: str) -> list[Entity]:
        return [x for x in g.types.values() if x.name == name and not x.root]

    @staticmethod
    def get_hierarchy(name: str) -> Entity:
        return \
            [x for x in g.types.values() if x.name == name and not x.root][0]

    @staticmethod
    def get_tree_data(
            type_id: Optional[int],
            selected_ids: list[int],
            filtered_ids: Optional[list[int]] = None,
            is_type_form: Optional[bool] = False) -> list[dict[str, Any]]:
        return Entity.walk_tree(
            g.types[type_id].subs,
            selected_ids,
            filtered_ids or [],
            is_type_form or False)

    @staticmethod
    def walk_tree(
            types: list[int],
            selected_ids: list[int],
            filtered_ids: list[int],
            is_type_form: bool) -> list[dict[str, Any]]:
        items = []
        for id_ in [id_ for id_ in types if id_ not in filtered_ids]:
            item = g.types[id_]
            state = {}
            if item.id in selected_ids:
                state['selected'] = 'true'
            if not is_type_form and not item.selectable:
                state['disabled'] = 'true'
            items.append({
                'id': item.id,
                'text': item.name.replace("'", "&apos;"),
                'state': state or '',
                'children':
                    Entity.walk_tree(
                        item.subs,
                        selected_ids,
                        filtered_ids,
                        is_type_form)})
        return items

    @staticmethod
    def get_class_choices(
            root: Optional[Entity] = None) -> list[tuple[int, str]]:
        choices = []
        for class_ in g.classes.values():
            if class_.new_types_allowed \
                    and (not root or class_.name not in root.classes):
                choices.append((class_.name, class_.label))
        return choices

    @staticmethod
    def insert_hierarchy(
            type_: Entity,
            category: str,
            classes: list[str],
            multiple: bool) -> None:
        db.insert_hierarchy({
            'id': type_.id,
            'name': type_.name,
            'multiple': multiple,
            'category': category})
        db.add_classes_to_hierarchy(type_.id, classes)

    @staticmethod
    def get_type_orphans() -> list[Entity]:
        return [
            node for key, node in g.types.items()
            if node.root
            and node.category not in ['system', 'tools']
            and node.count < 1
            and not node.subs]

    @staticmethod
    def reference_system_counts() -> dict[str, int]:
        return db.reference_system_counts()

    @staticmethod
    def get_reference_systems() -> dict[int, Entity]:
        systems = {}
        for row in db.get_reference_systems():
            system = Entity(row)
            for class_ in g.classes.values():
                if system.id in class_.reference_systems:
                    system.classes.append(class_.name)
            systems[system.id] = system
            if system.system:
                setattr(g, system.name.lower(), system)
        return systems


def insert(data: dict[str, Any]) -> Entity:
    annotation_data = []
    attributes = g.classes[data['openatlas_class_name']].attributes
    if 'description' in attributes \
            and 'annotated' in attributes['description']:
        result = AnnotationText.extract_annotations(data['description'])
        data['description'] = result['text']
        annotation_data = result['data']
    for item in [
            'begin_from', 'begin_to', 'begin_comment',
            'end_from', 'end_to', 'end_comment', 'description']:
        data[item] = data.get(item)
    for item in ['name', 'description']:
        data[item] = sanitize(data[item])
    entity = Entity.get_by_id(db.insert(data), with_location=False)
    for attribute in attributes:
        match attribute:
            case 'alias' if 'alias' in data:
                entity.update_aliases(data['alias'])
            case 'location':
                entity.update_gis(data.get('gis', {}), new=True)
            case 'file':
                entity.save_file_info(data)
            case 'resolver_url':
                db.insert_reference_system({
                    'entity_id': entity.id,
                    'name': entity.name,
                    'website_url': data['website_url'],
                    'resolver_url': data['resolver_url'],
                    'identifier_example': sanitize(data['example_id'])})
                if data['reference_system_classes']:
                    db.add_reference_system_classes(
                        entity.id,
                        data['reference_system_classes'])
    for annotation in annotation_data:
        annotation['source_id'] = entity.id
        AnnotationText.insert(annotation)
    return entity


class Link:
    object_: Optional[Entity]  # Needed for first/last appearance

    def __init__(
            self,
            row: dict[str, Any],
            domain: Optional[Entity] = None,
            range_: Optional[Entity] = None) -> None:
        self.id = row['id']
        self.description = row['description']
        self.property = g.properties[row['property_code']]
        self.domain = domain or Entity.get_by_id(row['domain_id'])
        self.range = range_ or Entity.get_by_id(row['range_id'])
        self.type = g.types[row['type_id']] if row['type_id'] else None
        self.types: dict[Entity, None] = {}
        if 'type_id' in row and row['type_id']:
            self.types[g.types[row['type_id']]] = None
        self.dates = Dates(row)

    def update(self, data: dict[str, Any]) -> None:
        attributes = {
            'id': self.id,
            'property_code': self.property.code,
            'domain_id': self.domain.id,
            'range_id': self.range.id,
            'type_id': self.type.id if self.type else None,
            'description': sanitize(data.get('description', self.description))}
        attributes.update(self.dates.to_timestamp())
        attributes.update(data)
        db_link.update(attributes)

    @staticmethod
    def get_by_id(id_: int) -> Link:
        return Link(db_link.get_by_id(id_))

    @staticmethod
    def get_links_by_type(type_: Entity) -> list[dict[str, Any]]:
        return db_link.get_links_by_type(type_.id)

    @staticmethod
    def get_links_by_type_recursive(
            type_: Entity,
            result: list[dict[str, Any]]) -> list[dict[str, Any]]:
        result += db_link.get_links_by_type(type_.id)
        for sub_id in type_.subs:
            result = Link.get_links_by_type_recursive(g.types[sub_id], result)
        return result

    @staticmethod
    def get_entity_ids_by_type_ids(types_: list[int]) -> list[int]:
        return db_link.get_entity_ids_by_type_ids(types_)

    @staticmethod
    def delete_(id_: int) -> None:
        db_link.delete_(id_)

    @staticmethod
    def invalid_involvement_dates() -> list[Link]:
        return [
            Link.get_by_id(row['id'])
            for row in date.invalid_involvement_dates()]

    @staticmethod
    def invalid_preceding_dates() -> list[Link]:
        return [
            Link.get_by_id(row['id'])
            for row in date.invalid_preceding_dates()]

    @staticmethod
    def invalid_sub_dates() -> list[Link]:
        return [Link.get_by_id(row['id']) for row in date.invalid_sub_dates()]

    @staticmethod
    def get_invalid_link_dates() -> list[Link]:
        return [Link.get_by_id(row['id']) for row in date.invalid_link_dates()]

    @staticmethod
    def check_link_duplicates() -> list[dict[str, Any]]:
        return db_link.check_link_duplicates()

    @staticmethod
    def delete_link_duplicates() -> int:
        return db_link.delete_link_duplicates()


def get_entity_ids_with_links(
        property_: str,
        classes: list[str],
        inverse: bool) -> list[int]:
    return db.get_entity_ids_with_links(property_, classes, inverse)
