from __future__ import annotations

import ast
from typing import Any, Optional, TYPE_CHECKING

from flask import g, request
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, HiddenField, SelectField, SelectMultipleField, StringField,
    widgets)
from wtforms.validators import InputRequired, Optional, URL

from openatlas.forms.field import (
    SubmitField, TableField, TableMultiField, TreeField)
from openatlas.forms.util import convert
from openatlas.forms.validation import hierarchy_name_exists, validate
from openatlas.models.entity import Entity, Link
from openatlas.models.gis import Gis
from openatlas.models.overlay import Overlay

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.openatlas_class import OpenatlasClass


def process_standard_fields(manager: Any) -> None:
    for key, value in manager.form.data.items():
        field_type = getattr(manager.form, key).type
        if key == 'name':
            name = manager.form.data['name']
            if hasattr(manager.form, 'name_inverse'):
                name = manager.form.name.data.replace(
                    '(', '').replace(')', '').strip()
                if manager.form.name_inverse.data.strip():
                    inverse = manager.form.name_inverse.data. \
                        replace('(', ''). \
                        replace(')', '').strip()
                    name += f' ({inverse})'
            # if isinstance(manager.entity, ReferenceSystem) \
            #        and manager.entity.system:
            #    name = manager.entity.name  # Prevent changing a system name
            manager.data['attributes']['name'] = name
        elif field_type == 'ValueTypeField':
            if value is not None:  # Allow the number zero
                manager.add_link('P2', g.types[int(key)], value)


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
        if self.entity:
            setattr(Form, 'entity_id', HiddenField())
        self.form: Any = Form(obj=self.link_ or self.entity)

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

    def get_link_type(self) -> Optional[Entity]:
        # Returns base type of link, e.g. involvement between actor and event
        for field in self.form:
            if isinstance(field, TreeField) and field.data:
                return g.types[int(field.data)]
        return None

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
        process_standard_fields(self)

    def process_link_form(self) -> None:
        self.link_.description = self.form.description.data
        # self.link_.set_dates(process_dates(self))


class ActorBaseManager(BaseManager):
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
    def get_crumbs(self) -> list[Any]:
        crumbs = []
        if self.place_info['structure'] and self.origin:
            if count := len([
                i for i in self.place_info['structure']['siblings']
                    if i.class_.name == self.class_.name]):
                crumbs[-1] = crumbs[-1] + f' ({count} {_("exists")})'
        return crumbs


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

    def get_root(self) -> Entity:
        type_ = self.origin or self.entity
        return g.types[type_.root[0]] if type_.root else type_

    def populate_insert(self) -> None:
        root_id = self.origin.root[0] if self.origin.root else self.origin.id
        getattr(self.form, str(root_id)).data = self.origin.id \
            if self.origin.id != root_id else None

    def populate_update(self) -> None:
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


class ActorFunctionManager(BaseManager):
    fields = ['date', 'description', 'continue']

    def top_fields(self) -> dict[str, Any]:
        if self.link_:
            return {}
        if 'membership' in request.url:
            field_name = 'group'
            entities = Entity.get_by_class('group', aliases=self.aliases)
        else:
            field_name = 'actor'
            entities = Entity.get_by_class('actor', aliases=self.aliases)
        return {
            'member_origin_id': HiddenField(),
            field_name:
                TableMultiField(
                    entities,
                    filter_ids=[self.origin.id],
                    validators=[InputRequired()])}

    def populate_insert(self) -> None:
        self.form.member_origin_id.data = self.origin.id

    def process_form(self) -> None:
        super().process_form()
        link_type = self.get_link_type()
        class_ = 'group' if hasattr(self.form, 'group') else 'actor'
        for actor in Entity.get_by_ids(
                ast.literal_eval(getattr(self.form, class_).data)):
            self.add_link(
                'P107',
                actor,
                self.form.description.data,
                inverse=(class_ == 'group'),
                type_id=link_type.id if link_type else None)

    def process_link_form(self) -> None:
        super().process_link_form()
        type_id = getattr(
            self.form,
            str(g.classes['actor_function'].standard_type_id)).data
        self.link_.type = g.types[int(type_id)] if type_id else None


class ActorRelationManager(BaseManager):
    fields = ['date', 'description', 'continue']

    def top_fields(self) -> dict[str, Any]:
        fields = {}
        if not self.link_:
            fields['actor'] = TableMultiField(
                Entity.get_by_class('person', aliases=self.aliases),
                filter_ids=[self.origin.id],
                validators=[InputRequired()])
            fields['relation_origin_id'] = HiddenField()
        return fields

    def additional_fields(self) -> dict[str, Any]:
        return {'inverse': BooleanField(_('inverse'))}

    def populate_insert(self) -> None:
        self.form.relation_origin_id.data = self.origin.id

    def process_form(self) -> None:
        super().process_form()
        for actor in Entity.get_by_ids(
                ast.literal_eval(self.form.actor.data)):
            link_type = self.get_link_type()
            self.add_link(
                'OA7',
                actor,
                self.form.description.data,
                inverse=bool(self.form.inverse.data),
                type_id=link_type.id if link_type else None)

    def process_link_form(self) -> None:
        super().process_link_form()
        type_id = getattr(
            self.form,
            str(g.classes['actor_relation'].standard_type_id)).data
        self.link_.type = g.types[int(type_id)] if type_id else None
        inverse = self.form.inverse.data
        if (self.origin.id == self.link_.domain.id and inverse) or \
                (self.origin.id == self.link_.range.id and not inverse):
            new_range = self.link_.domain
            self.link_.domain = self.link_.range
            self.link_.range = new_range

    def populate_update(self) -> None:
        if self.origin.id == self.link_.range.id:
            self.form.inverse.data = True


class AdministrativeUnitManager(TypeBaseManager):
    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P89')
        self.add_link('P89', g.types[self.super_id])


class ArtifactManager(ArtifactBaseManager):
    def additional_fields(self) -> dict[str, Any]:
        filter_ids = []
        if self.entity:
            filter_ids = [self.entity.id] + [
                e.id for e in self.entity.get_linked_entities_recursive('P46')]
        if self.insert:
            selection = self.origin if self.origin \
                and self.origin.class_.view in ['artifact', 'place'] else None
        else:
            selection = self.entity.get_linked_entity('P46', inverse=True)
        return {
            'super': TableField(
                Entity.get_by_class(
                    g.class_groups['place']['classes'] + ['artifact'],
                    types=True,
                    aliases=self.aliases),
                selection,
                filter_ids,
                add_dynamic=['place'])}

    def process_form(self) -> None:
        super().process_form()
        if self.form.super.data:
            self.add_link('P46', self.form.super.data, inverse=True)


class ExternalReferenceManager(BaseManager):
    fields = ['url', 'description', 'continue']

    def add_name_fields(self) -> None:
        setattr(
            self.form_class,
            'name',
            StringField(
                _('URL'),
                [InputRequired(), URL()],
                render_kw={'autofocus': True}))


class FeatureManager(PlaceBaseManager):
    fields = ['name', 'date', 'description', 'continue', 'map']

    def add_buttons(self) -> None:
        if self.entity:
            return
        setattr(
            self.form_class,
            'insert_continue_sub',
            SubmitField(_('insert and add') + ' ' + _('stratigraphic unit')))

    def additional_fields(self) -> dict[str, Any]:
        if self.insert:
            selection = self.origin if (
                self.origin  and self.origin.class_.name == 'place') else None
        else:
            selection = self.entity.get_linked_entity('P46', inverse=True)
        return {
            'super':
                TableField(
                    Entity.get_by_class('place', True, self.aliases),
                    selection,
                    validators=[InputRequired()],
                    add_dynamic=['place'])}

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete_inverse'].add('P46')
        self.add_link(
            'P46',
            Entity.get_by_id(int(self.form.super.data)),
            inverse=True)


class HumanRemainsManager(ArtifactBaseManager):
    def additional_fields(self) -> dict[str, Any]:
        filter_ids = []
        if self.entity:
            filter_ids = [self.entity.id] + [
                e.id for e in self.entity.get_linked_entities_recursive('P46')]
        if self.insert:
            selection = self.origin if self.origin \
                                       and self.origin.class_.view in [
                                           'artifact', 'place'] else None
        else:
            selection = self.entity.get_linked_entity('P46', inverse=True)
        return {
            'super': TableField(
                Entity.get_by_class(
                    g.class_groups['place']['classes'] + ['human remains'],
                    types=True,
                    aliases=self.aliases),
                selection,
                filter_ids,
                add_dynamic=['place'])}

    def process_form(self) -> None:
        super().process_form()
        if self.form.super.data:
            self.add_link('P46', self.form.super.data, inverse=True)


class HierarchyCustomManager(HierarchyBaseManager):
    def additional_fields(self) -> dict[str, Any]:
        tooltip = _('tooltip hierarchy multiple')
        return {
            **{'multiple': BooleanField(_('multiple'), description=tooltip)},
            **super().additional_fields()}


class HierarchyValueManager(HierarchyBaseManager):
    pass


class InvolvementManager(BaseManager):
    fields = ['date', 'description', 'continue']

    def top_fields(self) -> dict[str, Any]:
        event_class_name = ''
        if self.link_:
            event_class_name = self.link_.domain.class_.name
        elif self.origin and self.origin.class_.view != 'actor':
            event_class_name = self.origin.class_.name
        fields = {}
        if self.insert and self.origin:
            class_ = 'actor' if self.origin.class_.view == 'event' else 'event'
            fields[class_] = TableMultiField(
                Entity.get_by_class(class_, True, self.aliases),
                validators=[InputRequired()])
        choices = [('P11', g.properties['P11'].name)]
        if event_class_name in [
            'acquisition', 'activity', 'modification', 'production']:
            choices.append(('P14', g.properties['P14'].name))
            if event_class_name == 'acquisition':
                choices.append(('P22', g.properties['P22'].name))
                choices.append(('P23', g.properties['P23'].name))
        fields['activity'] = SelectField(_('activity'), choices=choices)
        return fields

    def populate_update(self) -> None:
        self.form.activity.data = self.link_.property.code

    def process_form(self) -> None:
        super().process_form()
        if self.origin.class_.view == 'event':
            actors = Entity.get_by_ids(ast.literal_eval(self.form.actor.data))
            for actor in actors:
                link_type = self.get_link_type()
                self.add_link(
                    self.form.activity.data,
                    actor,
                    self.form.description.data,
                    type_id=link_type.id if link_type else None)
        else:
            events = Entity.get_by_ids(ast.literal_eval(self.form.event.data))
            for event in events:
                link_type = self.get_link_type()
                self.add_link(
                    self.form.activity.data,
                    event,
                    self.form.description.data,
                    inverse=True,
                    type_id=link_type.id if link_type else None)

    def process_link_form(self) -> None:
        super().process_link_form()
        type_id = getattr(
            self.form,
            str(g.classes['involvement'].standard_type_id)).data
        self.link_.type = g.types[int(type_id)] if type_id else None
        self.link_.property = g.properties[self.form.activity.data]


class PlaceManager(PlaceBaseManager):
    fields = ['name', 'alias', 'date', 'description', 'continue', 'map']

    def add_buttons(self) -> None:
        if not self.entity:
            setattr(
                self.form_class,
                'insert_continue_sub',
                SubmitField(_('insert and add') + ' ' + _('feature')))

    def populate_insert(self) -> None:
        self.form.alias.append_entry('')


class StratigraphicUnitManager(PlaceBaseManager):
    fields = ['name', 'date', 'description', 'continue', 'map']

    def add_buttons(self) -> None:
        if not self.entity:
            setattr(
                self.form_class,
                'insert_continue_sub',
                SubmitField(_('insert and add') + ' ' + _('artifact')))
            setattr(
                self.form_class,
                'insert_continue_human_remains',
                SubmitField(_('insert and add') + ' ' + _('human remains')))

    def additional_fields(self) -> dict[str, Any]:
        selection = None
        if not self.insert and self.entity:
            selection = self.entity.get_linked_entity_safe('P46', inverse=True)
        elif self.origin and self.origin.class_.name == 'feature':
            selection = self.origin
        return {
            'super': TableField(
                Entity.get_by_class('feature', True),
                selection,
                validators=[InputRequired()])}

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete_inverse'].add('P46')
        self.add_link(
            'P46',
            Entity.get_by_id(int(self.form.super.data)),
            inverse=True)


class TypeManager(TypeBaseManager):
    def add_description(self) -> None:
        if self.get_root().category == 'value':
            del self.form_class.description  # pylint: disable=no-member
            setattr(self.form_class, 'description', StringField(_('unit')))

    def process_form(self) -> None:
        super().process_form()
        self.data['links']['delete'].add('P127')
        self.add_link('P127', g.types[self.super_id])

