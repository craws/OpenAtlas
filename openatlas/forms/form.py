from __future__ import annotations  # Needed for Python 4.0 type annotations

from collections import OrderedDict
from typing import Any, Optional, Union

from flask import g, render_template, request
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, FieldList, HiddenField, IntegerField, MultipleFileField,
    SelectField, SelectMultipleField, StringField, SubmitField, TextAreaField,
    widgets)
from wtforms.validators import (
    InputRequired, NoneOf, NumberRange, Optional as OptionalValidator, URL)

from openatlas import app
from openatlas.forms.field import (
    TableField, TableMultiField, TreeField, TreeMultiField, ValueFloatField,
    RemovableListField)
from openatlas.forms.populate import pre_populate_form
from openatlas.forms.validation import validate
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.openatlas_class import view_class_mapping
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type
from openatlas.util.table import Table
from openatlas.util.util import get_base_table_data, uc_first

FORMS = {
    'acquisition': ['name', 'date', 'description', 'continue'],
    'activity': ['name', 'date', 'description', 'continue'],
    'actor_function': ['date', 'description', 'continue'],
    'actor_actor_relation': ['date', 'description', 'continue'],
    'administrative_unit': ['name', 'description', 'continue'],
    'artifact': ['name', 'date', 'description', 'continue', 'map'],
    'bibliography': ['name', 'description', 'continue'],
    'edition': ['name', 'description', 'continue'],
    'event': ['name', 'date', 'description', 'continue'],
    'external_reference': ['name', 'description', 'continue'],
    'feature': ['name', 'date', 'description', 'continue', 'map'],
    'file': ['name', 'description'],
    'group': ['name', 'alias', 'date', 'description', 'continue'],
    'hierarchy': ['name', 'description'],
    'human_remains': ['name', 'date', 'description', 'continue', 'map'],
    'involvement': ['date', 'description', 'continue'],
    'move': ['name', 'date', 'description', 'continue'],
    'note': ['description'],
    'person': ['name', 'alias', 'date', 'description', 'continue'],
    'place': ['name', 'alias', 'date', 'description', 'continue', 'map'],
    'production': ['name', 'date', 'description', 'continue'],
    'reference_system': ['name', 'description'],
    'source': ['name', 'description', 'continue'],
    'source_translation': ['name', 'description', 'continue'],
    'stratigraphic_unit': ['name', 'date', 'description', 'continue', 'map'],
    'type': ['name', 'date', 'description', 'continue']}


def get_form(
        class_: str,
        entity: Optional[Union[Entity, Link, Type]] = None,
        code: Optional[str] = None,
        origin: Union[Entity, Type, None] = None,
        location: Optional[Entity] = None) -> FlaskForm:
    class Form(FlaskForm):
        opened = HiddenField()
        validate = validate

    if class_ == 'note':
        setattr(Form, 'public', BooleanField(_('public'), default=False))
    if 'name' in FORMS[class_]:
        setattr(Form, 'name', StringField(
            _('URL') if class_ == 'external_reference' else _('name'),
            [InputRequired(), URL()] if class_ == 'external_reference'
            else [InputRequired()],
            render_kw={'autofocus': True}))
    if 'alias' in FORMS[class_]:
        setattr(Form, 'alias', FieldList(RemovableListField('')))
    if class_ in g.classes and g.classes[class_].hierarchies:
        add_types(Form, class_)
    add_fields(Form, class_, code, entity, origin)
    add_reference_systems(Form, class_)
    if 'date' in FORMS[class_]:
        add_date_fields(Form)
    if 'description' in FORMS[class_]:
        label = _('content') if class_ == 'source' else _('description')
        setattr(Form, 'description', TextAreaField(label))
        if class_ == 'type':
            type_ = entity if entity else origin
            if isinstance(type_, Type):
                root = g.types[type_.root[0]] if type_.root else type_
                if root.category == 'value':
                    del Form.description
                    setattr(Form, 'description', StringField(_('unit')))
    if 'map' in FORMS[class_]:
        setattr(Form, 'gis_points', HiddenField(default='[]'))
        setattr(Form, 'gis_polygons', HiddenField(default='[]'))
        setattr(Form, 'gis_lines', HiddenField(default='[]'))
    add_buttons(Form, class_, entity, origin)
    if not entity or (request and request.method != 'GET'):
        form = Form()
    else:
        form = pre_populate_form(Form(obj=entity), entity, location)
    customize_labels(class_, form, entity, origin)
    return form


def customize_labels(
        name: str,
        form: FlaskForm,
        item: Optional[Union[Entity, Link]] = None,
        origin: Union[Entity, Type, None] = None, ) -> None:
    if name == 'source_translation':
        form.description.label.text = _('content')
    if name in ('administrative_unit', 'type'):
        type_ = item if item else origin
        if isinstance(type_, Type):
            root = g.types[type_.root[0]] if type_.root else type_
            getattr(form, str(root.id)).label.text = 'super'


def add_buttons(
        form: Any,
        name: str,
        entity: Union[Entity, Type, Link, None],
        origin: Optional[Entity] = None) -> FlaskForm:
    setattr(form, 'save', SubmitField(_('save') if entity else _('insert')))
    if entity:
        return form
    if 'continue' in FORMS[name] and (
            name in ['involvement', 'artifact', 'human_remains',
                     'source_translation', 'type']
            or not origin):
        setattr(
            form,
            'insert_and_continue',
            SubmitField(uc_first(_('insert and continue'))))
        setattr(form, 'continue_', HiddenField())
    insert_add = uc_first(_('insert and add')) + ' '
    if name == 'place':
        setattr(
            form,
            'insert_and_continue',
            SubmitField(uc_first(_('insert and continue'))))
        setattr(form, 'continue_', HiddenField())
        setattr(
            form,
            'insert_continue_sub',
            SubmitField(insert_add + _('feature')))
    elif name == 'feature' and origin and origin.class_.name == 'place':
        setattr(
            form,
            'insert_and_continue',
            SubmitField(uc_first(_('insert and continue'))))
        setattr(form, 'continue_', HiddenField())
        setattr(
            form,
            'insert_continue_sub',
            SubmitField(insert_add + _('stratigraphic unit')))
    elif name == 'stratigraphic_unit':
        setattr(
            form,
            'insert_and_continue',
            SubmitField(uc_first(_('insert and continue'))))
        setattr(form, 'continue_', HiddenField())
        setattr(
            form,
            'insert_continue_sub',
            SubmitField(insert_add + _('artifact')))
        setattr(
            form,
            'insert_continue_human_remains',
            SubmitField(insert_add + _('human remains')))
    return form


def add_reference_systems(form: Any, class_: str) -> None:
    precisions = [('', '')] + [
        (str(g.types[id_].id), g.types[id_].name)
        for id_ in Type.get_hierarchy('External reference match').subs]
    systems = list(g.reference_systems.values())
    systems.sort(key=lambda x: x.name.casefold())
    for system in systems:
        if class_ not in system.classes:
            continue
        setattr(
            form,
            f'reference_system_id_{system.id}',
            StringField(
                uc_first(system.name),
                [OptionalValidator()],
                description=system.description,
                render_kw={
                    'autocomplete': 'off',
                    'placeholder': system.placeholder}))
        setattr(
            form,
            f'reference_system_precision_{system.id}',
            SelectField(
                _('precision'),
                choices=precisions,
                default=system.precision_default_id))


def add_value_type_fields(form: Any, subs: list[int]) -> None:
    for sub_id in subs:
        sub = g.types[sub_id]
        setattr(
            form,
            str(sub.id),
            ValueFloatField(sub.name, [OptionalValidator()]))
        add_value_type_fields(form, sub.subs)


def add_types(form: Any, class_: str) -> None:
    types = OrderedDict(
        {id_: g.types[id_] for id_ in g.classes[class_].hierarchies})
    if g.classes[class_].standard_type_id in types:  # Standard type to top
        types.move_to_end(g.classes[class_].standard_type_id, last=False)
    for type_ in types.values():
        if type_.multiple:
            setattr(form, str(type_.id), TreeMultiField(str(type_.id)))
        else:
            setattr(form, str(type_.id), TreeField(str(type_.id)))
        if type_.category == 'value':
            add_value_type_fields(form, type_.subs)


def add_fields(
        form: Any,
        class_: str,
        code: Union[str, None],
        entity: Union[Entity, Link, ReferenceSystem, Type, None],
        origin: Union[Entity, Type, None]) -> None:
    if class_ == 'actor_actor_relation':
        setattr(form, 'inverse', BooleanField(_('inverse')))
        if not entity:
            setattr(
                form,
                'actor',
                TableMultiField(_('actor'), [InputRequired()]))
            setattr(form, 'relation_origin_id', HiddenField())
    elif class_ in ['artifact', 'human_remains']:
        setattr(form, 'actor', TableField(_('owned by')))
    elif class_ in view_class_mapping['event']:
        setattr(form, 'event_id', HiddenField())
        setattr(form, 'event', TableField(_('sub event of')))
        if class_ in ['activity', 'acquisition', 'move', 'production']:
            setattr(form, 'event_preceding', TableField(_('preceding event')))
        if class_ in ['activity', 'acquisition', 'production']:
            setattr(form, 'place', TableField(_('location')))
        if class_ == 'acquisition':
            setattr(form, 'given_place', TableMultiField(_('given place')))
        elif class_ == 'move':
            setattr(form, 'place_from', TableField(_('from')))
            setattr(form, 'place_to', TableField(_('to')))
            setattr(form, 'artifact', TableMultiField())
            setattr(form, 'person', TableMultiField())
        elif class_ == 'production':
            setattr(form, 'artifact', TableMultiField())
    elif class_ == 'file' and not entity:
        setattr(form, 'file', MultipleFileField(_('file'), [InputRequired()]))
        if origin and origin.class_.view == 'reference':
            setattr(form, 'page', StringField())
    elif class_ == 'group':
        setattr(form, 'residence', TableField(_('residence')))
        setattr(form, 'begins_in', TableField(_('begins in')))
        setattr(form, 'ends_in', TableField(_('ends in')))
    elif class_ == 'hierarchy':
        if code == 'custom' or (
                entity
                and isinstance(entity, Type)
                and entity.category != 'value'):
            setattr(form, 'multiple', BooleanField(
                _('multiple'),
                description=_('tooltip hierarchy multiple')))
        setattr(form, 'classes', SelectMultipleField(
            _('classes'),
            render_kw={'disabled': True},
            description=_('tooltip hierarchy forms'),
            choices=[],
            option_widget=widgets.CheckboxInput(),
            widget=widgets.ListWidget(prefix_label=False)))
    elif class_ == 'involvement':
        if not entity and origin:
            involved_with = 'actor' \
                if origin.class_.view == 'event' else 'event'
            setattr(
                form,
                involved_with,
                TableMultiField(_(involved_with), [InputRequired()]))
        setattr(form, 'activity', SelectField(_('activity')))
    elif class_ == 'actor_function' and not entity:
        setattr(form, 'member_origin_id', HiddenField())
        setattr(
            form,
            'actor' if code == 'member' else 'group',
            TableMultiField(_('actor'), [InputRequired()]))
    elif class_ in g.view_class_mapping['type']:
        setattr(form, 'is_type_form', HiddenField())
        type_ = entity if entity else origin
        if isinstance(type_, Type):
            root = g.types[type_.root[0]] if type_.root else type_
            setattr(form, str(root.id), TreeField(str(root.id)))
            if root.directional:
                setattr(form, 'name_inverse', StringField(_('inverse')))
    elif class_ == 'person':
        setattr(form, 'residence', TableField(_('residence')))
        setattr(form, 'begins_in', TableField(_('born in')))
        setattr(form, 'ends_in', TableField(_('died in')))
    elif class_ == 'reference_system':
        setattr(
            form,
            'website_url',
            StringField(_('website URL'), [OptionalValidator(), URL()]))
        setattr(
            form,
            'resolver_url',
            StringField(_('resolver URL'), [OptionalValidator(), URL()]))
        setattr(form, 'placeholder', StringField(_('example ID')))
        precision_id = str(Type.get_hierarchy('External reference match').id)
        setattr(form, precision_id, TreeField(precision_id))
        if choices := ReferenceSystem.get_class_choices(
                entity):  # type: ignore
            setattr(form, 'classes', SelectMultipleField(
                _('classes'),
                render_kw={'disabled': True},
                choices=choices,
                option_widget=widgets.CheckboxInput(),
                widget=widgets.ListWidget(prefix_label=False)))
    elif class_ == 'source':
        setattr(
            form,
            'artifact',
            TableMultiField(description=_(
                'Link artifacts as the information carrier of the source')))


def get_add_reference_form(class_: str) -> FlaskForm:
    class Form(FlaskForm):
        pass

    setattr(Form, class_, TableField(_(class_), [InputRequired()]))
    setattr(Form, 'page', StringField(_('page')))
    setattr(Form, 'save', SubmitField(uc_first(_('insert'))))
    return Form()


def get_table_form(class_: str, linked_entities: list[Entity]) -> str:
    """Returns a form with a list of entities with checkboxes."""
    if class_ == 'place':
        entities = Entity.get_by_class('place', types=True, aliases=True)
    elif class_ == 'artifact':
        entities = Entity.get_by_class(
            ['artifact', 'human_remains'],
            types=True)
    else:
        entities = Entity.get_by_view(class_, types=True, aliases=True)
    linked_ids = [entity.id for entity in linked_entities]
    table = Table([''] + g.table_headers[class_], order=[[1, 'asc']])
    for entity in entities:
        if entity.id in linked_ids:
            continue  # Don't show already linked entries
        input_ = f"""
            <input
                id="selection-{entity.id}"
                name="values"
                type="checkbox"
                value="{entity.id}">"""
        table.rows.append(
            [input_] + get_base_table_data(entity, show_links=False))
    if not table.rows:
        return uc_first(_('no entries'))
    return render_template(
        'forms/form_table.html',
        table=table.display(class_))


def get_move_form(type_: Type) -> FlaskForm:
    class Form(FlaskForm):
        is_type_form = HiddenField()
        checkbox_values = HiddenField()
        selection = SelectMultipleField(
            '',
            [InputRequired()],
            coerce=int,
            option_widget=widgets.CheckboxInput(),
            widget=widgets.ListWidget(prefix_label=False))
        save = SubmitField(uc_first(_('move entities')))

    root = g.types[type_.root[0]]
    setattr(Form, str(root.id), TreeField(str(root.id)))
    form = Form(obj=type_)
    choices = []
    if root.class_.name == 'administrative_unit':
        for entity in type_.get_linked_entities('P89', True):
            place = entity.get_linked_entity('P53', True)
            if place:
                choices.append((entity.id, place.name))
    elif root.name in app.config['PROPERTY_TYPES']:
        for row in Link.get_links_by_type(type_):
            domain = Entity.get_by_id(row['domain_id'])
            range_ = Entity.get_by_id(row['range_id'])
            choices.append((row['id'], domain.name + ' - ' + range_.name))
    else:
        for entity in type_.get_linked_entities('P2', True):
            choices.append((entity.id, entity.name))
    form.selection.choices = choices
    return form


def add_date_fields(form: Any) -> None:
    validator_day = [OptionalValidator(), NumberRange(min=1, max=31)]
    validator_month = [OptionalValidator(), NumberRange(min=1, max=12)]
    validator_year = [
        OptionalValidator(),
        NumberRange(min=-4713, max=9999),
        NoneOf([0])]

    setattr(form, 'begin_year_from', IntegerField(
        render_kw={'placeholder': _('YYYY')}, validators=validator_year))
    setattr(form, 'begin_month_from', IntegerField(
        render_kw={'placeholder': _('MM')}, validators=validator_month))
    setattr(form, 'begin_day_from', IntegerField(
        render_kw={'placeholder': _('DD')}, validators=validator_day))
    setattr(form, 'begin_year_to', IntegerField(
        render_kw={'placeholder': _('YYYY')}, validators=validator_year))
    setattr(form, 'begin_month_to', IntegerField(
        render_kw={'placeholder': _('MM')}, validators=validator_month))
    setattr(form, 'begin_day_to', IntegerField(
        render_kw={'placeholder': _('DD')}, validators=validator_day))
    setattr(form, 'begin_comment', StringField(
        render_kw={'placeholder': _('comment')}))
    setattr(form, 'end_year_from', IntegerField(
        render_kw={'placeholder': _('YYYY')}, validators=validator_year))
    setattr(form, 'end_month_from', IntegerField(
        render_kw={'placeholder': _('MM')}, validators=validator_month))
    setattr(form, 'end_day_from', IntegerField(
        render_kw={'placeholder': _('DD')}, validators=validator_day))
    setattr(form, 'end_year_to', IntegerField(
        render_kw={'placeholder': _('YYYY')}, validators=validator_year))
    setattr(form, 'end_month_to', IntegerField(
        render_kw={'placeholder': _('MM')}, validators=validator_month))
    setattr(form, 'end_day_to', IntegerField(
        render_kw={'placeholder': _('DD')}, validators=validator_day))
    setattr(form, 'end_comment', StringField(
        render_kw={'placeholder': _('comment')}))
