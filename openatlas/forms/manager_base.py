from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

from flask import g
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectMultipleField, StringField, widgets

from openatlas.display.util import link
from openatlas.forms.add_fields import add_reference_systems
from openatlas.forms.field import TableField, TreeField
from openatlas.forms.populate import populate_dates, populate_reference_systems
from openatlas.forms.process import (
    process_dates, process_origin, process_standard_fields)
from openatlas.forms.util import convert
from openatlas.forms.validation import hierarchy_name_exists, validate
from openatlas.models.entity import Entity, Link
from openatlas.models.gis import Gis
from openatlas.models.overlay import Overlay

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.openatlas_class import OpenatlasClass


class BaseManager:
    fields: list[str] = []
    continue_link_id: Optional[int] = None
    data: dict[str, Any] = {}

    def __init__(
            self,
            class_: OpenatlasClass,
            entity: Optional[Entity],
            origin: Optional[Entity],
            link_: Optional[Link],
            copy: Optional[bool] = False) -> None:

        self.class_ = class_
        self.entity: Any = entity
        self.origin: Any = origin
        self.link_: Any = link_
        self.copy = copy
        self.crumbs: list[Any] = []
        self.insert = bool(not self.entity and not self.link_)
        self.place_info: dict[str, Any] = {}
        self.aliases = current_user.settings['table_show_aliases']
        self.table_items: dict[str, list[Entity]] = {}

        if self.insert:
            self.get_place_info_for_insert()
        else:
            self.get_place_info_for_update()

        class Form(FlaskForm):
            opened = HiddenField()
            validate = validate

        self.form_class = Form
        add_reference_systems(self)
        if self.entity:
            setattr(Form, 'entity_id', HiddenField())
        if 'map' in self.fields:
            setattr(Form, 'gis_points', HiddenField(default='[]'))
            setattr(Form, 'gis_polygons', HiddenField(default='[]'))
            setattr(Form, 'gis_lines', HiddenField(default='[]'))
        self.form: Any = Form(obj=self.link_ or self.entity)
        self.customize_labels()

    def get_place_info_for_insert(self) -> None:
        self.place_info = {
            'structure': None,
            'gis_data': None,
            'overlays': None}

    def get_place_info_for_update(self) -> None:
        self.place_info = {
            'structure': None,
            'gis_data': None,
            'overlays': None,
            'location': None}

    def update_entity(self, new: bool = False) -> None:
        self.continue_link_id = self.entity.update(self.data, new)

    def customize_labels(self) -> None:
        pass

    def get_link_type(self) -> Optional[Entity]:
        # Returns base type of link, e.g. involvement between actor and event
        for field in self.form:
            if isinstance(field, TreeField) and field.data:
                return g.types[int(field.data)]
        return None

    def populate_insert(self) -> None:
        pass

    def populate_update(self) -> None:
        if self.entity and not self.copy:
            self.form.entity_id.data = self.entity.id
        populate_reference_systems(self)
        if 'date' in self.fields:
            populate_dates(self)
        if hasattr(self.form, 'alias'):
            for alias in self.entity.aliases.values():
                self.form.alias.append_entry(alias)
            self.form.alias.append_entry('')

    def add_link(
            self,
            property_: str,
            range_: str | Entity,
            description: Optional[str] = None,
            inverse: bool = False,
            return_link_id: bool = False,
            type_id: Optional[int] = None) -> None:
        if not range_:
            return
        self.data['links']['insert'].append({
            'property': property_,
            'range': convert(range_)
            if isinstance(range_, str) else range_,
            'description': description,
            'inverse': inverse,
            'return_link_id': return_link_id,
            'type_id': type_id})

    def process_form(self) -> None:
        self.data: dict[str, Any] = {
            'attributes': process_dates(self),
            'links': {
                'insert': [],
                'delete': set(),
                'delete_inverse': set()}}
        process_standard_fields(self)
        if self.origin:
            process_origin(self)
        if 'map' in self.fields:
            self.data['gis'] = {
                shape: getattr(self.form, f'gis_{shape}s').data
                for shape in ['point', 'line', 'polygon']}

    def insert_entity(self) -> None:
        self.entity = Entity.insert(self.class_.name, self.form.name.data)

    def update_link(self) -> None:
        self.data['attributes_link'] = self.data['attributes']
        self.origin.update_links(self.data, new=True)

    def process_link_form(self) -> None:
        self.link_.description = self.form.description.data
        self.link_.set_dates(process_dates(self))


class ActorBaseManager(BaseManager):
    fields = ['name', 'alias', 'date', 'description', 'continue']
    _('begins in')
    _('ends in')

    def additional_fields(self) -> dict[str, Any]:
        residence = None
        begins_in = None
        ends_in = None
        self.table_items['place'] = \
            Entity.get_by_class('place', types=True, aliases=self.aliases)
        if self.insert:
            if self.origin and self.origin.class_.name == 'place':
                residence = self.origin
        else:
            if residence := self.entity.get_linked_entity('P74'):
                residence = residence.get_linked_entity_safe('P53', True)
            if first := self.entity.get_linked_entity('OA8'):
                begins_in = first.get_linked_entity_safe('P53', True)
            if last := self.entity.get_linked_entity('OA9'):
                ends_in = last.get_linked_entity_safe('P53', True)
        return {
            'residence': TableField(
                self.table_items['place'],
                residence,
                add_dynamic=['place']),
            'begins_in': TableField(
                self.table_items['place'],
                begins_in,
                add_dynamic=['place']),
            'ends_in': TableField(
                self.table_items['place'],
                ends_in,
                add_dynamic=['place'])}

    def populate_insert(self) -> None:
        self.form.alias.append_entry('')

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].update(['P74', 'OA8', 'OA9'])
        if self.form.residence.data:
            residence = Entity.get_by_id(int(self.form.residence.data))
            self.add_link('P74', residence.get_linked_entity_safe('P53'))
        if self.form.begins_in.data:
            begin_place = Entity.get_by_id(int(self.form.begins_in.data))
            self.add_link('OA8', begin_place.get_linked_entity_safe('P53'))
        if self.form.ends_in.data:
            end_place = Entity.get_by_id(int(self.form.ends_in.data))
            self.add_link('OA9', end_place.get_linked_entity_safe('P53'))
        if self.origin:
            if self.origin.class_.view == 'event':
                self.add_link(
                    'P11',
                    self.origin,
                    return_link_id=True,
                    inverse=True)
            if self.origin.class_.view == 'actor':
                self.add_link(
                    'OA7',
                    self.origin,
                    return_link_id=True,
                    inverse=True)


class PlaceBaseManager(BaseManager):
    def insert_entity(self) -> None:
        super().insert_entity()
        self.entity.link(
            'P53',
            Entity.insert(
                'object_location',
                f'Location of {self.form.name.data}'))

    def get_place_info_for_insert(self) -> None:
        super().get_place_info_for_insert()
        if not self.origin:
            self.place_info['gis_data'] = Gis.get_all()
            return
        structure = self.origin.get_structure_for_insert()
        self.place_info['structure'] = structure
        self.place_info['gis_data'] = Gis.get_all([self.origin], structure)
        if current_user.settings['module_map_overlay'] \
                and self.origin.class_.view == 'place':
            self.place_info['overlay'] = Overlay.get_by_object(self.origin)

    def get_place_info_for_update(self) -> None:
        super().get_place_info_for_update()
        structure = self.entity.get_structure()
        self.place_info['structure'] = structure
        self.place_info['gis_data'] = Gis.get_all([self.entity], structure)
        if current_user.settings['module_map_overlay']:
            self.place_info['overlays'] = Overlay.get_by_object(self.entity)
        self.place_info['location'] = \
            self.entity.get_linked_entity_safe('P53', types=True)


class ArtifactBaseManager(PlaceBaseManager):
    fields = ['name', 'date', 'description', 'continue', 'map']

    def additional_fields(self) -> dict[str, Any]:
        if self.insert:
            owner = self.origin if self.origin \
                and self.origin.class_.view == 'actor' else None
        else:
            owner = self.entity.get_linked_entity('P52')
        self.table_items['actor'] = \
            Entity.get_by_view('actor', aliases=self.aliases)
        return {
            'owned_by':
                TableField(
                    self.table_items['actor'],
                    owner,
                    add_dynamic=['person', 'group'])}

    def get_crumbs(self) -> list[Any]:
        crumbs = []
        if self.place_info['structure'] and self.origin:
            if count := len([
                i for i in self.place_info['structure']['siblings']
                    if i.class_.name == self.class_.name]):
                crumbs[-1] = crumbs[-1] + f' ({count} {_("exists")})'
        return crumbs

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P52')
        self.data['links']['delete_inverse'].add('P46')
        if self.form.owned_by.data:
            self.add_link('P52', self.form.owned_by.data)


class EventBaseManager(BaseManager):
    fields = ['name', 'date', 'description', 'continue']

    def additional_fields(self) -> dict[str, Any]:
        location = None
        super_event = None
        preceding_event = None
        filter_ids = []
        if self.insert:
            if self.origin \
                    and self.origin.class_.view == 'place' \
                    and self.class_.name != 'move':
                location = self.origin
        else:
            super_event = self.entity.get_linked_entity('P9', inverse=True)
            preceding_event = self.entity.get_linked_entity('P134')
            filter_ids = [self.entity.id] + [
                e.id for e in self.entity.get_linked_entities_recursive('P9') +
                self.entity.get_linked_entities_recursive('P134', True)]
            if self.class_.name != 'move' \
                    and (place_ := self.entity.get_linked_entity('P7')):
                location = place_.get_linked_entity_safe('P53', True)
        self.table_items = {
            'event_view': Entity.get_by_view('event', True, self.aliases),
            'place': Entity.get_by_class('place', True, self.aliases)}
        self.table_items['preceding_event'] = [
            e for e in self.table_items['event_view']
            if e.class_.name != 'event']
        fields = {
            'sub_event_of':
                TableField(
                    self.table_items['event_view'],
                    super_event,
                    filter_ids)}
        if self.class_.name != 'event':
            fields['preceding_event'] = TableField(
                self.table_items['preceding_event'],
                preceding_event,
                filter_ids)
        if self.class_.name != 'move':
            fields['location'] = TableField(
                self.table_items['place'],
                location,
                add_dynamic=['place'])
        return fields

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete_inverse'].add('P9')
        self.add_link('P9', self.form.sub_event_of.data, inverse=True)
        if self.class_.name != 'event':
            self.data['links']['delete'].add('P134')
            self.add_link('P134', self.form.preceding_event.data)
        if self.class_.name != 'move':
            self.data['links']['delete'].add('P7')
            if self.form.location.data:
                self.add_link(
                    'P7',
                    Entity.get_linked_entity_safe_static(
                        int(self.form.location.data),
                        'P53'))
        if self.origin and self.origin.class_.view == 'actor':
            self.add_link('P11', self.origin, return_link_id=True)


class HierarchyBaseManager(BaseManager):
    fields = ['name', 'description']

    def additional_fields(self) -> dict[str, Any]:
        setattr(self.form_class, 'validate_name', hierarchy_name_exists)
        return {
            'classes': SelectMultipleField(
                _('classes'),
                description=_('tooltip hierarchy forms'),
                choices=Entity.get_class_choices(self.entity),
                option_widget=widgets.CheckboxInput(),
                widget=widgets.ListWidget(prefix_label=False))}


class TypeBaseManager(BaseManager):
    fields = ['name', 'date', 'description', 'continue']
    super_id: int

    def additional_fields(self) -> dict[str, Any]:
        root = self.get_root()
        fields = {
            str(root.id): TreeField(
                str(root.id),
                filter_ids=[self.entity.id] if self.entity else [],
                is_type_form=True)}
        if root.directional:
            fields['name_inverse'] = StringField(_('inverse'))
        return fields

    def customize_labels(self) -> None:
        getattr(self.form, str(self.get_root().id)).label.text = 'super'

    def get_crumbs(self) -> list[Any]:
        type_ = self.origin or self.entity
        self.crumbs = [link(type_, index=True)]
        self.crumbs += [g.types[type_id] for type_id in type_.root]
        return self.crumbs

    def get_root(self) -> Entity:
        type_ = self.origin or self.entity
        return g.types[type_.root[0]] if type_.root else type_

    def populate_insert(self) -> None:
        root_id = self.origin.root[0] if self.origin.root else self.origin.id
        getattr(self.form, str(root_id)).data = self.origin.id \
            if self.origin.id != root_id else None

    def populate_update(self) -> None:
        super().populate_update()
        if hasattr(self.form, 'name_inverse'):
            name_parts = self.entity.name.split(' (')
            self.form.name.data = name_parts[0].strip()
            if len(name_parts) > 1:
                self.form.name_inverse.data = name_parts[1][:-1].strip()
        super_ = g.types[self.entity.root[-1]]
        root = g.types[self.entity.root[0]]
        if super_.id != root.id:
            getattr(self.form, str(root.id)).data = super_.id

    def process_form(self) -> None:
        super().process_form()
        self.super_id = self.get_root().id
        if new_id := getattr(self.form, str(self.super_id)).data:
            self.super_id = int(new_id)
