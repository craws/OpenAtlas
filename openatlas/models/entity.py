from __future__ import annotations

import ast
from typing import Any, Iterable, Optional, TYPE_CHECKING, Union

from flask import g, request
from fuzzywuzzy import fuzz
from werkzeug.exceptions import abort

from openatlas import app
from openatlas.database.date import Date
from openatlas.database.entity import Entity as Db
from openatlas.display.util import (
    datetime64_to_timestamp, format_date_part, sanitize,
    timestamp_to_datetime64)
from openatlas.models.link import Link

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.type import Type


class Entity:

    def __init__(self, data: dict[str, Any]) -> None:

        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.created = data['created']
        self.modified = data['modified']
        self.cidoc_class = g.cidoc_classes[data['cidoc_class_code']]
        self.class_ = g.classes[data['openatlas_class_name']]
        self.reference_systems: list[Link] = []
        self.origin_id: Optional[int] = None  # When coming from another entity
        self.image_id: Optional[int] = None  # Profile image
        self.location: Optional[Entity] = None  # Respective location if place

        self.standard_type = None
        self.types: dict[Type, str] = {}
        if 'types' in data and data['types']:
            for item in data['types']:  # f1 = type id, f2 = value
                type_ = g.types[item['f1']]
                if type_.class_.name == 'type_tools':
                    continue
                self.types[type_] = item['f2']
                if type_.category == 'standard':
                    self.standard_type = type_

        self.aliases = {}
        if 'aliases' in data and data['aliases']:
            for alias in data['aliases']:  # f1 = alias id, f2 = alias name
                self.aliases[alias['f1']] = alias['f2']
            self.aliases = dict(
                sorted(self.aliases.items(), key=lambda item_: item_[1]))

        # Dates
        self.begin_from = None
        self.begin_to = None
        self.begin_comment = None
        self.end_from = None
        self.end_to = None
        self.end_comment = None
        self.first = None
        self.last = None
        if 'begin_from' in data:
            self.begin_from = timestamp_to_datetime64(data['begin_from'])
            self.begin_to = timestamp_to_datetime64(data['begin_to'])
            self.begin_comment = data['begin_comment']
            self.end_from = timestamp_to_datetime64(data['end_from'])
            self.end_to = timestamp_to_datetime64(data['end_to'])
            self.end_comment = data['end_comment']
            self.first = format_date_part(self.begin_from, 'year') \
                if self.begin_from else None
            self.last = format_date_part(self.end_from, 'year') \
                if self.end_from else None
            self.last = format_date_part(self.end_to, 'year') \
                if self.end_to else self.last

    def get_linked_entity(
            self,
            code: str,
            inverse: bool = False,
            types: bool = False) -> Optional[Entity]:
        return Link.get_linked_entity(
            self.id,
            code,
            inverse=inverse,
            types=types)

    def get_linked_entity_safe(
            self,
            code: str,
            inverse: bool = False,
            types: bool = False) -> Entity:
        return Link.get_linked_entity_safe(self.id, code, inverse, types)

    def get_linked_entities(
            self,
            code: Union[str, list[str]],
            inverse: bool = False,
            types: bool = False) -> list[Entity]:
        return Link.get_linked_entities(
            self.id,
            code,
            inverse=inverse,
            types=types)

    def get_linked_entities_recursive(
            self,
            code: str,
            inverse: bool = False,
            types: bool = False) -> list[Entity]:
        return Link.get_linked_entities_recursive(
            self.id,
            code,
            inverse=inverse,
            types=types)

    def link(self,
             code: str,
             range_: Union[Entity, list[Entity]],
             description: Optional[str] = None,
             inverse: bool = False,
             type_id: Optional[int] = None) -> list[int]:
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
            id_ = Db.link({
                'property_code': code,
                'domain_id': domain.id,
                'range_id': range_.id,
                'description': description,
                'type_id': type_id})
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
        self.link(code, Entity.get_by_ids(ids), description, inverse)

    def get_links(
            self,
            codes: Union[str, list[str]],
            inverse: bool = False) -> list[Link]:
        return Link.get_links(self.id, codes, inverse)

    def delete(self) -> None:
        Entity.delete_(self.id)

    def delete_links(self, codes: list[str], inverse: bool = False) -> None:
        Link.delete_by_codes(self, codes, inverse)

    def update(
            self,
            data: dict[str, Any],
            new: bool = False) -> Optional[int]:
        continue_link_id = None
        if 'attributes' in data:
            self.update_attributes(data['attributes'])
        if 'aliases' in data:
            self.update_aliases(data['aliases'])
        if 'administrative_units' in data \
                and self.class_.name != 'administrative_unit':
            self.update_administrative_units(data['administrative_units'], new)
        if 'links' in data:
            continue_link_id = self.update_links(data, new)
        if 'gis' in data:
            self.update_gis(data['gis'], new)
        return continue_link_id

    def update_administrative_units(
            self,
            units: dict[str, list[int]],
            new: bool) -> None:
        if not self.location:
            self.location = self.get_linked_entity_safe('P53')
        if not new:
            self.location.delete_links(['P89'])
        if units:
            self.location.link('P89', [g.types[id_] for id_ in units])

    def update_attributes(self, attributes: dict[str, Any]) -> None:
        for key, value in attributes.items():
            setattr(self, key, value)
        Db.update({
            'id': self.id,
            'name': self.name.strip(),
            'begin_from': datetime64_to_timestamp(self.begin_from),
            'begin_to': datetime64_to_timestamp(self.begin_to),
            'end_from': datetime64_to_timestamp(self.end_from),
            'end_to': datetime64_to_timestamp(self.end_to),
            'begin_comment':
                str(self.begin_comment).strip()
                if self.begin_comment else None,
            'end_comment':
                str(self.end_comment).strip() if self.end_comment else None,
            'description':
                sanitize(self.description, 'text')
                if self.description else None})

    def update_aliases(self, aliases: list[str]) -> None:
        delete_ids = []
        for id_, alias in self.aliases.items():
            if alias in aliases:
                aliases.remove(alias)
            else:
                delete_ids.append(id_)
        Entity.delete_(delete_ids)
        for alias in aliases:
            if alias.strip():
                self.link('P1', Entity.insert('appellation', alias))

    def update_links(self, data: dict[str, Any], new: bool) -> Optional[int]:
        from openatlas.models.reference_system import ReferenceSystem
        if not new:
            if 'delete' in data['links'] and data['links']['delete']:
                self.delete_links(data['links']['delete'])
            if 'delete_inverse' in data['links'] \
                    and data['links']['delete_inverse']:
                self.delete_links(data['links']['delete_inverse'], True)
            if 'delete_reference_system' in data['links'] \
                    and data['links']['delete_reference_system']:
                ReferenceSystem.delete_links_from_entity(self)
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
                    item.end_comment = \
                        data['attributes_link']['end_comment']
                    item.update()
            if link_['return_link_id']:
                continue_link_id = ids[0]
        return continue_link_id

    def update_gis(self, gis_data: dict[str, Any], new: bool) -> None:
        from openatlas.models.gis import Gis
        if not self.location:
            self.location = self.get_linked_entity_safe('P53')
        if not new:
            Db.update({
                'id': self.location.id,
                'name': f'Location of {str(self.name).strip()}',
                'begin_from': None,
                'begin_to': None,
                'end_from': None,
                'end_to': None,
                'begin_comment': None,
                'end_comment': None,
                'description': None})
            Gis.delete_by_entity(self.location)
        Gis.insert(self.location, gis_data)

    def get_profile_image_id(self) -> Optional[int]:
        return Db.get_profile_image_id(self.id)

    def remove_profile_image(self) -> None:
        Db.remove_profile_image(self.id)

    def get_name_directed(self, inverse: bool = False) -> str:
        """Returns name part of a directed type e.g. parent of (child of)"""
        name_parts = self.name.split(' (')
        if inverse and len(name_parts) > 1:
            return sanitize(
                name_parts[1][:-1],  # Remove closing bracket
                'text')  # pragma: no cover
        return name_parts[0]

    def check_too_many_single_type_links(self) -> bool:
        type_dict: dict[int, int] = {}
        for type_ in self.types:
            if type_.root[0] in type_dict:
                type_dict[type_.root[0]] += 1
            else:
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

    @staticmethod
    def get_invalid_dates() -> list[Entity]:
        return [
            Entity.get_by_id(row['id'], types=True)
            for row in Date.get_invalid_dates()]

    @staticmethod
    def get_orphaned_subunits() -> list[Entity]:
        return [Entity.get_by_id(x['id']) for x in Db.get_orphaned_subunits()]

    @staticmethod
    def delete_(id_: Union[int, list[int]]) -> None:
        if id_:
            Db.delete(id_ if isinstance(id_, list) else [id_])

    @staticmethod
    def get_by_class(
            classes: Union[str, list[str]],
            types: bool = False,
            aliases: bool = False) -> list[Entity]:
        if aliases:  # For performance: check classes if they can have an alias
            aliases = False
            for class_ in classes if isinstance(classes, list) \
                    else [classes]:
                if g.classes[class_].alias_allowed:
                    aliases = True
                    break
        return [
            Entity(row) for row in Db.get_by_class(classes, types, aliases)]

    @staticmethod
    def get_by_view(
            view: str,
            types: bool = False,
            aliases: bool = False) -> list[Entity]:
        return Entity.get_by_class(g.view_class_mapping[view], types, aliases)

    @staticmethod
    def get_display_files() -> list[Entity]:
        entities = []
        for row in Db.get_by_class('file', types=True):
            ext = g.file_stats[row['id']]['ext'] \
                if row['id'] in g.file_stats else 'N/A'
            if ext in app.config['DISPLAY_FILE_EXTENSIONS']:
                entities.append(Entity(row))
        return entities

    @staticmethod
    def insert(class_: str, name: str, desc: Optional[str] = None) -> Entity:
        id_ = Db.insert({
            'name': name.strip(),
            'code': g.classes[class_].cidoc_class.code,
            'openatlas_class_name': class_,
            'description': sanitize(desc, 'text') if desc else None})
        return Entity.get_by_id(id_)

    @staticmethod
    def get_by_cidoc_class(
            code: Union[str, list[str]],
            types: bool = False,
            aliases: bool = False) -> list[Entity]:
        return [
            Entity(row) for row in Db.get_by_cidoc_class(code, types, aliases)]

    @staticmethod
    def get_by_id(
            id_: int,
            types: bool = False,
            aliases: bool = False) -> Entity:
        if id_ in g.types:
            return g.types[id_]
        if id_ in g.reference_systems:
            return g.reference_systems[id_]
        data = Db.get_by_id(id_, types, aliases)
        if not data:
            if 'activity' in request.path:  # Re-raise if in user activity view
                raise AttributeError
            abort(418)
        return Entity(data)

    @staticmethod
    def get_by_ids(
            ids: Iterable[int],
            types: bool = False,
            aliases: bool = False) -> list[Entity]:
        entities = []
        for row in Db.get_by_ids(ids, types, aliases):
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
        for row in Db.get_by_project_id(project_id):
            entity = Entity(row)
            entity.origin_id = row['origin_id']
            entities.append(entity)
        return entities

    @staticmethod
    def get_by_link_property(code: str, class_: str) -> list[Entity]:
        return [Entity(row) for row in Db.get_by_link_property(code, class_)]

    @staticmethod
    def get_similar_named(class_: str, ratio: int) -> dict[int, Any]:
        similar: dict[int, Any] = {}
        already_added: set[int] = set()
        entities = Entity.get_by_class(class_)
        for sample in filter(lambda x: x.id not in already_added, entities):
            similar[sample.id] = {'entity': sample, 'entities': []}
            for entity in entities:
                if entity.id != sample.id \
                        and fuzz.ratio(sample.name, entity.name) >= ratio:
                    already_added.add(sample.id)
                    already_added.add(entity.id)
                    similar[sample.id]['entities'].append(entity)
        return {
            item: data for item, data in similar.items() if data['entities']}

    @staticmethod
    def get_overview_counts() -> dict[str, int]:
        return Db.get_overview_counts(g.class_view_mapping)

    @staticmethod
    def get_orphans() -> list[Entity]:
        return [Entity.get_by_id(row['id']) for row in Db.get_orphans()]

    @staticmethod
    def get_latest(limit: int) -> list[Entity]:
        return [
            Entity(row) for row in Db.get_latest(g.class_view_mapping, limit)]

    @staticmethod
    def set_profile_image(id_: int, origin_id: int) -> None:
        Db.set_profile_image(id_, origin_id)

    @staticmethod
    def get_entities_linked_to_itself() -> list[Entity]:
        return [
            Entity.get_by_id(row['domain_id']) for row in Db.get_circular()]

    @staticmethod
    def get_roots(
            property_code: str,
            ids: list[int],
            inverse: bool = False) -> dict[int, Any]:
        return Db.get_roots(property_code, ids, inverse)
