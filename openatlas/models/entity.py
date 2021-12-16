from __future__ import annotations  # Needed for Python 4.0 type annotations

import ast
from typing import (
    Any, Dict, Iterable, List, Optional, Set, TYPE_CHECKING, Union)

from flask import g, request
from flask_wtf import FlaskForm
from fuzzywuzzy import fuzz
from werkzeug.exceptions import abort

from openatlas import app
from openatlas.database.date import Date
from openatlas.database.entity import Entity as Db
from openatlas.forms.date import format_date
from openatlas.models.date import (
    datetime64_to_timestamp, timestamp_to_datetime64)
from openatlas.models.link import Link
from openatlas.util.util import get_base_table_data, sanitize

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.type import Type
    from openatlas.models.reference_system import ReferenceSystem


class Entity:

    def __init__(self, data: Dict[str, Any]) -> None:

        self.id = data['id']
        self.standard_type = None
        self.types: Dict['Type', str] = {}
        self.name = data['name']

        if 'types' in data and data['types']:
            for item in data['types']:
                type_ = g.types[item['f1']]  # f1 = type id, f2 = value
                self.types[type_] = item['f2']
                if type_.category == 'standard':
                    self.standard_type = type_

        self.aliases: Dict[int, str] = {}
        if 'aliases' in data and data['aliases']:
            for alias in data['aliases']:
                # f1 = alias id, f2 = alias name
                self.aliases[alias['f1']] = alias['f2']
            self.aliases = {k: v for k, v in sorted(
                self.aliases.items(),
                key=lambda item_: item_[1])}
        self.description = data['description']
        self.created = data['created']
        self.modified = data['modified']
        self.cidoc_class = g.cidoc_classes[data['cidoc_class_code']]
        self.class_ = g.classes[data['openatlas_class_name']]
        self.reference_systems: List[Link] = []
        self.origin_id: Optional[int] = None  # When coming from another entity
        self.image_id: Optional[int] = None  # Profile image
        self.linked_places: List[Entity] = []  # Related places for map
        self.location: Optional[Entity] = None  # Respective location if a place
        self.info_data: Dict[str, Union[str, List[str], None]]

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
            self.first = format_date(self.begin_from, 'year') \
                if self.begin_from else None
            self.last = format_date(self.end_from, 'year') \
                if self.end_from else None
            self.last = format_date(self.end_to, 'year') \
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
            code: Union[str, List[str]],
            inverse: bool = False,
            types: bool = False) -> List[Entity]:
        return Link.get_linked_entities(
            self.id,
            code,
            inverse=inverse,
            types=types)

    def link(self,
             code: str,
             range_: Union[Entity, List[Entity]],
             description: Optional[str] = None,
             inverse: bool = False,
             type_id: Optional[int] = None) -> List[int]:
        return Link.insert(self, code, range_, description, inverse, type_id)

    def link_string(
            self,
            code: str,
            range_: str,
            description: Optional[str] = None,
            inverse: bool = False) -> None:
        if not range_:
            return  # pragma: no cover
        # range_ = string value from a form, can be empty, int or int list
        # e.g. '', '1', '[]', '[1, 2]'
        ids = ast.literal_eval(range_)
        ids = [int(id_) for id_ in ids] if isinstance(ids, list) else [int(ids)]
        Link.insert(self, code, Entity.get_by_ids(ids), description, inverse)

    def get_links(
            self,
            codes: Union[str, List[str]],
            inverse: bool = False) -> List[Link]:
        return Link.get_links(self.id, codes, inverse)

    def delete(self) -> None:
        Entity.delete_(self.id)

    def delete_links(self, codes: List[str], inverse: bool = False) -> None:
        Link.delete_by_codes(self, codes, inverse)

    def update(
            self,
            data: Dict[str, Any],
            new: Optional[bool] = False,) -> Optional[int]:
        from openatlas.models.reference_system import ReferenceSystem
        if not new and 'links' in data:
            self.delete_links(['P2'] + data['links']['delete'])
            if data['links']['delete_inverse']:
                self.delete_links(data['links']['delete_inverse'], True)
            if 'delete_reference_system_links' in data \
                    and data['delete_reference_system_links']:
                ReferenceSystem.delete_links_from_entity(self)
        if 'attribute' in data:
            for key, value in data['attributes'].items():
                setattr(self, key, value)
        if 'aliases' in data:
            self.update_aliases(data['aliases'])
        if 'types' in data and self.class_.name != 'type':
            self.update_types(data)
        redirect_link_id = None
        if 'links' in data:
            for link_ in data['links']['insert']:
                ids = self.link(
                    link_['property'],
                    link_['range'],
                    link_['description'] if 'description' in link_ else None,
                    type_id=link_['type_id'] if 'type_id' in link_ else None,
                    inverse=('inverse' in link_ and link_['inverse']))
                if 'return_link_id' in link_ and link_['return_link_id']:
                    redirect_link_id = ids[0]
        if 'gis' in data:
            from openatlas.models.gis import Gis
            location = self.get_linked_entity_safe('P53')
            if not new:
                Db.update({
                    'id': location.id,
                    'name': f'Location of {str(self.name).strip()}',
                    'begin_from': None,
                    'begin_to': None,
                    'end_from': None,
                    'end_to': None,
                    'begin_comment': None,
                    'end_comment': None,
                    'description': None})
                Gis.delete_by_entity(location)
            Gis.insert(location, data['gis'])
        Db.update({
            'id': self.id,
            'name': str(self.name).strip(),
            'begin_from': datetime64_to_timestamp(self.begin_from),
            'begin_to': datetime64_to_timestamp(self.begin_to),
            'end_from': datetime64_to_timestamp(self.end_from),
            'end_to': datetime64_to_timestamp(self.end_to),
            'begin_comment':
                str(self.begin_comment).strip() if self.begin_comment else None,
            'end_comment':
                str(self.end_comment).strip() if self.end_comment else None,
            'description':
                sanitize(self.description, 'text') if self.description else None
        })
        if isinstance(self, ReferenceSystem):
            self.update_system(data)
        return redirect_link_id

    def update_types(self, data):
        self.link('P2', [g.types[id_] for id_ in data['types']])
        for type_ in data['value_types']:
            if type_['value'] is not None:  # Allow the number zero
                self.link('P2', g.types[type_['id']], type_['value'])
        if 'administrative_units' in data:
            if not self.location:
                self.location = self.get_linked_entity_safe('P53')
            self.location.delete_links(['P89'])
            if data['administrative_units']:
                self.location.link(
                    'P89',
                    [g.types[id_] for id_ in data['administrative_units']])

    def update_aliases(self, aliases) -> None:
        delete_ids = []
        for id_, alias in self.aliases.items():
            if alias in aliases:
                aliases.remove(alias)
            else:
                delete_ids.append(id_)
        Entity.delete_(delete_ids)
        for alias in aliases:
            if alias.strip():
                if self.class_.view == 'actor':
                    self.link('P131', Entity.insert('actor_appellation', alias))
                else:
                    self.link('P1', Entity.insert('appellation', alias))

    def set_image_for_places(self) -> None:
        self.image_id = self.get_profile_image_id()
        if not self.image_id:
            for link_ in self.get_links('P67', inverse=True):
                domain = link_.domain
                if domain.class_.view == 'file':  # pragma: no cover
                    data = get_base_table_data(domain)
                    if data[3] in app.config['DISPLAY_FILE_EXTENSIONS']:
                        self.image_id = domain.id
                        break

    def get_profile_image_id(self) -> Optional[int]:
        return Db.get_profile_image_id(self.id)

    def remove_profile_image(self) -> None:
        Db.remove_profile_image(self.id)

    def get_name_directed(self, inverse: bool = False) -> str:
        """Returns name part of a directed type e.g. parent of (child of)"""
        name_parts = self.name.split(' (')
        if inverse and len(name_parts) > 1:  # pragma: no cover
            return sanitize(name_parts[1][:-1], 'type')  # remove close bracket
        return name_parts[0]

    @staticmethod
    def get_invalid_dates() -> List[Entity]:
        return [
            Entity.get_by_id(row['id'], types=True)
            for row in Date.get_invalid_dates()]

    @staticmethod
    def delete_(id_: Union[int, List[int]]) -> None:
        if not id_:
            return
        Db.delete(id_ if isinstance(id_, list) else [id_])

    @staticmethod
    def get_by_class(
            classes: Union[str, List[str]],
            types: bool = False,
            aliases: bool = False) -> List[Entity]:
        if aliases:  # For performance: check classes if they can have an alias
            aliases = False
            for class_ in classes if isinstance(classes, list) \
                    else [classes]:
                if g.classes[class_].alias_allowed:
                    aliases = True
                    break
        return [Entity(row) for row in Db.get_by_class(classes, types, aliases)]

    @staticmethod
    def get_by_view(
            view: str,
            types: bool = False,
            aliases: bool = False) -> List[Entity]:
        return Entity.get_by_class(g.view_class_mapping[view], types, aliases)

    @staticmethod
    def get_display_files() -> List[Entity]:
        entities = []
        for row in Db.get_by_class('file', types=True):
            ext = g.file_stats[row['id']]['ext'] \
                if row['id'] in g.file_stats else 'N/A'
            if ext in app.config['DISPLAY_FILE_EXTENSIONS']:
                entities.append(Entity(row))
        return entities

    @staticmethod
    def insert(
            class_name: str,
            name: str,
            description: Optional[str] = None) -> Union[Entity, Type]:
        if not name:  # pragma: no cover
            from openatlas import logger
            logger.log('error', 'model', 'Insert entity without name')
            abort(422)
        id_ = Db.insert({
            'name': str(name).strip(),
            'code': g.classes[class_name].cidoc_class.code,
            'openatlas_class_name': class_name,
            'description':
                sanitize(description, 'text') if description else None})
        return Entity.get_by_id(id_)

    @staticmethod
    def get_by_cidoc_class(
            code: Union[str, List[str]],
            types: bool = False,
            aliases: bool = False) -> List[Entity]:
        return [Entity(row) for row in
                Db.get_by_cidoc_class(code, types, aliases)]

    @staticmethod
    def get_by_id(
            id_: int,
            types: bool = False,
            aliases: bool = False) -> Union[Entity, Type, 'ReferenceSystem']:
        if id_ in g.types:
            return g.types[id_]
        if id_ in g.reference_systems:
            return g.reference_systems[id_]
        data = Db.get_by_id(id_, types, aliases)
        if not data:
            if 'activity' in request.path:  # Re-raise if in user activity view
                raise AttributeError  # pragma: no cover
            abort(418)
        return Entity(data)

    @staticmethod
    def get_by_ids(
            ids: Iterable[int],
            types: bool = False,
            aliases: bool = False) -> List[Entity]:
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
    def get_by_project_id(project_id: int) -> List[Entity]:
        entities = []
        for row in Db.get_by_project_id(project_id):
            entity = Entity(row)
            entity.origin_id = row['origin_id']
            entities.append(entity)
        return entities

    @staticmethod
    def get_by_link_property(code: str, class_: str) -> List[Entity]:
        return [Entity(row) for row in Db.get_by_link_property(code, class_)]

    @staticmethod
    def get_similar_named(form: FlaskForm) -> Dict[int, Any]:
        similar: Dict[int, Any] = {}
        already_added: Set[int] = set()
        entities = Entity.get_by_class(form.classes.data)
        for sample in filter(lambda x: x.id not in already_added, entities):
            similar[sample.id] = {'entity': sample, 'entities': []}
            for entity in filter(lambda x: x.id != sample.id, entities):
                if fuzz.ratio(sample.name, entity.name) >= form.ratio.data:
                    already_added.add(sample.id)
                    already_added.add(entity.id)
                    similar[sample.id]['entities'].append(entity)
        return {
            similar: data
            for similar, data in similar.items() if data['entities']}

    @staticmethod
    def get_overview_counts() -> Dict[str, int]:
        return Db.get_overview_counts(g.class_view_mapping.keys())

    @staticmethod
    def get_orphans() -> List[Entity]:
        return [Entity.get_by_id(row['id']) for row in Db.get_orphans()]

    @staticmethod
    def get_latest(limit: int) -> List[Entity]:
        return [
            Entity(row)
            for row in Db.get_latest(g.class_view_mapping.keys(), limit)]

    @staticmethod
    def set_profile_image(id_: int, origin_id: int) -> None:
        Db.set_profile_image(id_, origin_id)

    @staticmethod
    def get_entities_linked_to_itself() -> List[Entity]:
        return [Entity.get_by_id(row['domain_id']) for row in Db.get_circular()]
