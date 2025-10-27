from __future__ import annotations

import ast
from typing import Any, Optional, TYPE_CHECKING

from flask import g, request
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import BooleanField, HiddenField, SelectField
from wtforms.validators import InputRequired, Optional

from openatlas.forms.field import TableMultiField, TreeField
from openatlas.forms.util import convert
from openatlas.forms.validation import validate
from openatlas.models.entity import Entity, Link

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

        class Form(FlaskForm):
            opened = HiddenField()
            validate = validate

        self.form_class = Form
        if self.entity:
            setattr(Form, 'entity_id', HiddenField())
        self.form: Any = Form(obj=self.link_ or self.entity)

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


class ActorBaseManager(BaseManager):

    def process_form(self) -> None:
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
        type_id = getattr(
            self.form,
            str(g.classes['involvement'].standard_type_id)).data
        self.link_.type = g.types[int(type_id)] if type_id else None
        self.link_.property = g.properties[self.form.activity.data]
