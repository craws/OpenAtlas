from __future__ import annotations

import time
from typing import Any, Optional, TYPE_CHECKING

from flask import g, request, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    FieldList, HiddenField, SelectMultipleField, StringField, TextAreaField,
    widgets)
from wtforms.validators import InputRequired

from openatlas.forms.add_fields import (
    add_date_fields, add_reference_systems, add_types)
from openatlas.forms.field import (
    RemovableListField, SubmitField, TableField, TreeField)
from openatlas.forms.populate import (
    populate_dates, populate_reference_systems, populate_types)
from openatlas.forms.process import (
    process_dates, process_origin, process_standard_fields)
from openatlas.forms.util import (
    check_if_entity_has_time, string_to_entity_list)
from openatlas.forms.validation import hierarchy_name_exists, validate
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.link import Link
from openatlas.models.overlay import Overlay
from openatlas.models.type import Type

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

        if self.insert:
            self.get_place_info_for_insert()
        else:
            self.get_place_info_for_update()

        class Form(FlaskForm):
            opened = HiddenField()
            origin_id = HiddenField()
            validate = validate

        self.form_class = Form
        self.add_name_fields()
        add_types(self)
        for id_, field in self.additional_fields().items():
            setattr(Form, id_, field)
        add_reference_systems(self)
        if self.entity:
            setattr(Form, 'entity_id', HiddenField())
        if 'date' in self.fields:
            add_date_fields(self.form_class, bool(
                current_user.settings['module_time']
                or (entity and check_if_entity_has_time(entity))))
        if 'description' in self.fields:
            self.add_description()
        if 'map' in self.fields:
            setattr(Form, 'gis_points', HiddenField(default='[]'))
            setattr(Form, 'gis_polygons', HiddenField(default='[]'))
            setattr(Form, 'gis_lines', HiddenField(default='[]'))
        if 'annotation' in self.fields:
            setattr(Form, 'annotation', HiddenField(default='[]'))
        self.add_buttons()
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

    def get_crumbs(self) -> list[Any]:
        if not self.crumbs:
            label = self.origin.class_.name if self.origin \
                else g.classes[self.class_.name].view
            if label in g.class_view_mapping:
                label = g.class_view_mapping[label]
            self.crumbs = [[
                _(label.replace('_', ' ')),
                url_for(
                    'index',
                    view=self.origin.class_.view if self.origin
                    else g.classes[self.class_.name].view)]]
        if self.place_info['structure']:
            self.crumbs += self.place_info['structure']['supers']
        elif self.origin:
            self.crumbs.append(self.origin)
        if self.insert:
            self.crumbs.append(f'+ {g.classes[self.class_.name].label}')
        else:
            self.crumbs.append(self.entity)
            self.crumbs.append(
                _('copy') if 'copy_' in request.path else _('edit'))
        return self.crumbs

    def add_description(self) -> None:
        setattr(
            self.form_class,
            'description',
            TextAreaField(_('description')))

    def add_name_fields(self) -> None:
        if 'name' in self.fields:
            setattr(
                self.form_class,
                'name',
                StringField(
                    _('name'),
                    [InputRequired()],
                    render_kw={'autofocus': True}))
        if 'alias' in self.fields:
            setattr(self.form_class, 'alias', FieldList(RemovableListField()))

    def update_entity(self, new: bool = False) -> None:
        self.continue_link_id = self.entity.update(self.data, new)

    def customize_labels(self) -> None:
        pass

    def add_buttons(self) -> None:
        setattr(
            self.form_class,
            'save',
            SubmitField(_('insert') if self.insert else _('save')))
        if self.insert and 'continue' in self.fields:
            setattr(
                self.form_class,
                'insert_and_continue',
                SubmitField(_('insert and continue')))
            setattr(self.form_class, 'continue_', HiddenField())

    def additional_fields(self) -> dict[str, Any]:
        return {}

    def get_link_type(self) -> Optional[Entity]:
        # Returns base type of link, e.g. involvement between actor and event
        for field in self.form:
            if isinstance(field, TreeField) and field.data:
                return g.types[int(field.data)]
        return None

    def populate_insert(self) -> None:
        pass

    def populate_update(self) -> None:
        self.form.opened.data = time.time()
        if self.entity and not self.copy:
            self.form.entity_id.data = self.entity.id
        populate_types(self)
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
            'range': string_to_entity_list(range_)
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
        if 'annotation' in self.fields:
            self.data['annotation'] = getattr(self.form, 'annotation').data

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

    def additional_fields(self) -> dict[str, Any]:
        return {
            'residence': TableField(
                _('residence'),
                add_dynamic=['place'],
                related_tables=['begins_in', 'ends_in']),
            'begins_in': TableField(
                _('begins in'),
                add_dynamic=['place'],
                related_tables=['residence', 'ends_in']),
            'ends_in': TableField(
                _('ends in'),
                add_dynamic=['place'],
                related_tables=['begins_in', 'residence'])}

    def populate_insert(self) -> None:
        self.form.alias.append_entry('')
        if self.origin and self.origin.class_.name == 'place':
            self.form.residence.data = self.origin.id

    def populate_update(self) -> None:
        super().populate_update()
        if residence := self.entity.get_linked_entity('P74'):
            self.form.residence.data = \
                residence.get_linked_entity_safe('P53', True).id
        if first := self.entity.get_linked_entity('OA8'):
            self.form.begins_in.data = \
                first.get_linked_entity_safe('P53', True).id
        if last := self.entity.get_linked_entity('OA9'):
            self.form.ends_in.data = \
                last.get_linked_entity_safe('P53', True).id

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
        if self.origin:
            structure = self.origin.get_structure_for_insert()
            self.place_info['structure'] = structure
            self.place_info['gis_data'] = Gis.get_all([self.origin], structure)
            if current_user.settings['module_map_overlay'] \
                    and self.origin.class_.view == 'place':
                self.place_info['overlay'] = Overlay.get_by_object(self.origin)
        else:
            self.place_info['gis_data'] = Gis.get_all()

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
        return {
            'actor':
                TableField(_('owned by'), add_dynamic=['person', 'group'])}

    def get_crumbs(self) -> list[Any]:
        crumbs = super().get_crumbs()
        if self.place_info['structure'] and self.origin:
            if count := len([
                    i for i in self.place_info['structure']['siblings'] if
                    i.class_.name == self.class_.name]):
                crumbs[-1] = crumbs[-1] + f' ({count} {_("exists")})'
        return crumbs

    def populate_insert(self) -> None:
        if self.origin and self.origin.class_.view == 'actor':
            self.form.actor.data = self.origin.id

    def populate_update(self) -> None:
        super().populate_update()
        if owner := self.entity.get_linked_entity('P52'):
            self.form.actor.data = owner.id

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P52')
        self.data['links']['delete_inverse'].add('P46')
        if self.form.actor.data:
            self.add_link('P52', self.form.actor.data)


class EventBaseManager(BaseManager):
    fields = ['name', 'date', 'description', 'continue']

    def get_sub_ids(self, entity: Entity, ids: list[int]) -> list[int]:
        for sub in entity.get_linked_entities('P9'):
            ids.append(sub.id)
            self.get_sub_ids(sub, ids)
        return ids

    def additional_fields(self) -> dict[str, Any]:
        filter_ids = []
        if self.entity:
            filter_ids = self.get_sub_ids(self.entity, [self.entity.id])
        fields = {
            'event': TableField(
                _('sub event of'),
                filter_ids=filter_ids,
                add_dynamic=[
                    'activity',
                    'acquisition',
                    'event',
                    'modification',
                    'move',
                    'production'],
                related_tables=['event_preceding'])}
        if self.class_.name != 'event':
            fields['event_preceding'] = TableField(
                _('preceding event'),
                filter_ids=filter_ids,
                add_dynamic=[
                    'activity',
                    'acquisition',
                    'modification',
                    'move',
                    'production'],
                related_tables=['event'])
        if self.class_.name != 'move':
            fields['place'] = \
                TableField(_('location'), add_dynamic=['place'])
        return fields

    def populate_insert(self) -> None:
        if self.origin:
            if self.origin.class_.view == 'artifact':
                self.form.artifact.data = [self.origin.id]
            elif self.origin.class_.view == 'place':
                if self.class_.name == 'move':
                    self.form.place_from.data = self.origin.id
                else:
                    self.form.place.data = self.origin.id

    def populate_update(self) -> None:
        super().populate_update()
        if super_ := self.entity.get_linked_entity('P9', inverse=True):
            self.form.event.data = super_.id
        if preceding_ := self.entity.get_linked_entity('P134'):
            self.form.event_preceding.data = preceding_.id
        if self.class_.name != 'move':
            if place := self.entity.get_linked_entity('P7'):
                self.form.place.data = \
                    place.get_linked_entity_safe('P53', True).id

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete_inverse'].add('P9')
        self.add_link('P9', self.form.event.data, inverse=True)
        if self.class_.name != 'event':
            self.data['links']['delete'].add('P134')
            self.add_link('P134', self.form.event_preceding.data)
        if self.class_.name != 'move':
            self.data['links']['delete'].add('P7')
            if self.form.place.data:
                self.add_link(
                    'P7',
                    Entity.get_linked_entity_safe_static(
                        int(self.form.place.data),
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
                choices=Type.get_class_choices(self.entity),
                option_widget=widgets.CheckboxInput(),
                widget=widgets.ListWidget(prefix_label=False))}


class TypeBaseManager(BaseManager):
    fields = ['name', 'date', 'description', 'continue']
    super_id: int

    def additional_fields(self) -> dict[str, Any]:
        root = self.get_root()
        fields = {
            'is_type_form': HiddenField(),
            str(root.id): TreeField(
                str(root.id),
                filter_ids=[self.entity.id] if self.entity else [])}
        if root.directional:
            fields['name_inverse'] = StringField(_('inverse'))
        return fields

    def customize_labels(self) -> None:
        getattr(self.form, str(self.get_root().id)).label.text = 'super'

    def get_crumbs(self) -> list[Any]:
        self.crumbs = [[_('types'), url_for('type_index')]]
        type_ = self.origin or self.entity
        self.crumbs += [g.types[type_id] for type_id in type_.root]
        return super().get_crumbs()

    def get_root(self) -> Type:
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
            self.form.name.data = name_parts[0]
            if len(name_parts) > 1:
                self.form.name_inverse.data = name_parts[1][:-1]
        super_ = g.types[self.entity.root[-1]]
        root = g.types[self.entity.root[0]]
        if super_.id != root.id:
            getattr(self.form, str(root.id)).data = super_.id

    def process_form(self) -> None:
        super().process_form()
        self.super_id = self.get_root().id
        if new_id := getattr(self.form, str(self.super_id)).data:
            self.super_id = int(new_id)
