import time
from typing import Any, Optional, Union

from flask import g
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    FieldList, HiddenField, SelectMultipleField, StringField, SubmitField,
    TextAreaField, widgets)
from wtforms.validators import InputRequired, URL

from openatlas.display.util import uc_first
from openatlas.forms.add_fields import (
    add_date_fields, add_reference_systems, add_types)
from openatlas.forms.field import RemovableListField, TableField, TreeField
from openatlas.forms.populate import (
    populate_dates, populate_reference_systems, populate_types)
from openatlas.forms.process import (
    process_dates, process_origin, process_standard_fields)
from openatlas.forms.util import (
    check_if_entity_has_time, string_to_entity_list)
from openatlas.forms.validation import hierarchy_name_exists, validate
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.openatlas_class import OpenatlasClass
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type


class BaseManager:
    class_: OpenatlasClass
    fields: list[str] = []
    form: Any = None
    entity: Any = None
    origin: Any = None
    link_: Any = None
    continue_link_id: Optional[int] = None
    data: dict[str, Any] = {}

    def __init__(
            self,
            class_: OpenatlasClass,
            entity: Union[Entity, None],
            origin: Union[Entity, None],
            link_: Union[Link, None]):

        self.class_ = class_
        self.entity = entity
        self.origin = origin
        self.link_ = link_

        class Form(FlaskForm):
            opened = HiddenField()
            origin_id = HiddenField()
            validate = validate

        self.form_class = Form
        self.add_name_fields()
        add_types(self)
        for id_, field in self.additional_fields().items():
            setattr(Form, id_, field)
        add_reference_systems(self.class_, self.form_class)
        if self.entity:
            setattr(Form, 'entity_id', HiddenField())
        if 'date' in self.fields:
            add_date_fields(self.form_class, bool(
                current_user.settings['module_time']
                or check_if_entity_has_time(entity)))
        if 'description' in self.fields:
            setattr(Form, 'description', TextAreaField(
                _('content') if class_.name == 'source' else _('description')))
            if class_.name == 'type':
                type_ = entity or origin
                if isinstance(type_, Type):
                    root = g.types[type_.root[0]] if type_.root else type_
                    if root.category == 'value':
                        del Form.description
                        setattr(Form, 'description', StringField(_('unit')))
        if 'map' in self.fields:
            setattr(Form, 'gis_points', HiddenField(default='[]'))
            setattr(Form, 'gis_polygons', HiddenField(default='[]'))
            setattr(Form, 'gis_lines', HiddenField(default='[]'))
        self.add_buttons()
        self.form = Form(obj=self.link_ or self.entity)
        self.customize_labels()

    def add_name_fields(self) -> None:
        if 'name' in self.fields:
            readonly = bool(
                isinstance(self.entity, ReferenceSystem)
                and self.entity.system)
            setattr(self.form_class, 'name', StringField(
                _('name'),
                [InputRequired()],
                render_kw={'autofocus': True, 'readonly': readonly}))
        if 'url' in self.fields:
            setattr(self.form_class, 'name', StringField(
                _('URL'),
                [InputRequired(), URL()],
                render_kw={'autofocus': True}))
        if 'alias' in self.fields:
            setattr(
                self.form_class,
                'alias', FieldList(
                    RemovableListField(),
                    render_kw={'class': 'no-label'},))

    def update_entity(self, new: bool = False) -> None:
        self.continue_link_id = self.entity.update(self.data, new)

    def customize_labels(self) -> None:
        if self.class_.name in ('administrative_unit', 'type') \
                and 'classes' not in self.form:
            type_ = self.entity or self.origin
            if isinstance(type_, Type):
                root = g.types[type_.root[0]] if type_.root else type_
                getattr(self.form, str(root.id)).label.text = 'super'

    def add_buttons(self) -> None:
        setattr(
            self.form_class,
            'save',
            SubmitField(
                _('save') if self.entity or self.link_ else _('insert')))
        if not self.entity and not self.link_ and 'continue' in self.fields:
            setattr(
                self.form_class,
                'insert_and_continue',
                SubmitField(_('insert and continue')))
            setattr(self.form_class, 'continue_', HiddenField())

    def additional_fields(self) -> dict[str, Any]:
        return {}

    def get_root_type(self) -> Type:
        type_ = self.entity if isinstance(self.entity, Type) else self.origin
        return g.types[type_.root[0]] if type_.root else type_

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
        if self.entity:
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
            range_: Union[str, Entity],
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

    def insert_entity(self) -> None:
        if self.entity:
            return
        if self.class_.name == 'reference_system':
            self.entity = ReferenceSystem.insert_system({
                'name': self.form.name.data,
                'description': self.form.description.data,
                'website_url': self.form.website_url.data,
                'resolver_url': self.form.resolver_url.data})
            return
        self.entity = Entity.insert(self.class_.name, self.form.name.data)
        if self.class_.view in ['artifact', 'place']:
            self.entity.link(
                'P53',
                Entity.insert(
                    'object_location',
                    f'Location of {self.form.name.data}'))
        return

    def update_link(self) -> None:
        self.data['attributes_link'] = self.data['attributes']
        self.origin.update_links(self.data, new=True)

    def process_link_form(self) -> None:
        self.link_.description = self.form.description.data
        self.link_.set_dates(process_dates(self))


class ActorBaseManager(BaseManager):
    fields = ['name', 'alias', 'date', 'description', 'continue']

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


class ArtifactBaseManager(BaseManager):
    fields = ['name', 'date', 'description', 'continue', 'map']

    def additional_fields(self) -> dict[str, Any]:
        return {
            'actor':
                TableField(_('owned by'), add_dynamic=['person', 'group'])}

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
        for sub in entity.get_linked_entities('P9', inverse=True):
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
                    'move',
                    'production'],
                related_tables=['event'])
        if self.class_.name != 'move':
            fields['place'] = \
                TableField(_('location'), add_dynamic=['place'])
        return fields

    def populate_update(self) -> None:
        super().populate_update()
        if super_ := self.entity.get_linked_entity('P9'):
            self.form.event.data = super_.id
        if preceding_ := self.entity.get_linked_entity('P134', True):
            self.form.event_preceding.data = preceding_.id
        if self.class_.name != 'move':
            if place := self.entity.get_linked_entity('P7'):
                self.form.place.data = \
                    place.get_linked_entity_safe('P53', True).id

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P9')
        self.add_link('P9', self.form.event.data)
        if self.class_.name != 'event':
            self.data['links']['delete_inverse'].add('P134')
            self.add_link('P134', self.form.event_preceding.data, inverse=True)
        if self.class_.name != 'move':
            self.data['links']['delete'].add('P7')
            if self.form.place.data:
                self.add_link(
                    'P7',
                    Link.get_linked_entity_safe(
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
                render_kw={'disabled': True},
                description=_('tooltip hierarchy forms'),
                choices=Type.get_class_choices(self.entity),
                option_widget=widgets.CheckboxInput(),
                widget=widgets.ListWidget(prefix_label=False))}
