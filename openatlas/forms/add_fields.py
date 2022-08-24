from collections import OrderedDict
from typing import Any

from flask import g
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, TextAreaField
from wtforms.validators import (
    NoneOf, NumberRange, Optional as OptionalValidator)

from openatlas.forms.field import TreeField, TreeMultiField, ValueFloatField
from openatlas.models.openatlas_class import OpenatlasClass
from openatlas.models.type import Type
from openatlas.util.util import is_authorized, uc_first


def add_reference_systems(class_: OpenatlasClass, form: Any) -> None:
    if hasattr(form, 'classes'):
        return  # Skip hierarchies
    precisions = [('', '')] + [
        (str(g.types[id_].id), g.types[id_].name)
        for id_ in Type.get_hierarchy('External reference match').subs]
    systems = list(g.reference_systems.values())
    systems.sort(key=lambda x: x.name.casefold())
    for system in systems:
        if class_.name not in system.classes:
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


def add_date_fields(form_class: Any, has_time: bool) -> None:
    validator_second = [OptionalValidator(), NumberRange(min=0, max=59)]
    validator_minute = [OptionalValidator(), NumberRange(min=0, max=59)]
    validator_hour = [OptionalValidator(), NumberRange(min=0, max=23)]
    validator_day = [OptionalValidator(), NumberRange(min=1, max=31)]
    validator_month = [OptionalValidator(), NumberRange(min=1, max=12)]
    validator_year = [
        OptionalValidator(),
        NumberRange(min=-4713, max=9999),
        NoneOf([0])]

    setattr(
        form_class,
        'begin_year_from',
        IntegerField(
            render_kw={'placeholder': _('YYYY')},
            validators=validator_year))
    setattr(
        form_class,
        'begin_month_from',
        IntegerField(
            render_kw={'placeholder': _('MM')},
            validators=validator_month))
    setattr(
        form_class,
        'begin_day_from',
        IntegerField(
            render_kw={'placeholder': _('DD')},
            validators=validator_day))
    if has_time:
        setattr(
            form_class,
            'begin_hour_from',
            IntegerField(
                render_kw={'placeholder': _('hh')},
                validators=validator_hour))
        setattr(
            form_class,
            'begin_minute_from',
            IntegerField(
                render_kw={'placeholder': _('mm')},
                validators=validator_minute))
        setattr(
            form_class,
            'begin_second_from',
            IntegerField(
                render_kw={'placeholder': _('ss')},
                validators=validator_second))
    setattr(
        form_class,
        'begin_year_to',
        IntegerField(
            render_kw={'placeholder': _('YYYY')},
            validators=validator_year))
    setattr(
        form_class,
        'begin_month_to',
        IntegerField(
            render_kw={'placeholder': _('MM')},
            validators=validator_month))
    setattr(
        form_class,
        'begin_day_to',
        IntegerField(
            render_kw={'placeholder': _('DD')},
            validators=validator_day))
    if has_time:
        setattr(
            form_class,
            'begin_hour_to',
            IntegerField(
                render_kw={'placeholder': _('hh')},
                validators=validator_hour))
        setattr(
            form_class,
            'begin_minute_to',
            IntegerField(
                render_kw={'placeholder': _('mm')},
                validators=validator_minute))
        setattr(
            form_class,
            'begin_second_to',
            IntegerField(
                render_kw={'placeholder': _('ss')},
                validators=validator_second))
    setattr(
        form_class,
        'begin_comment',
        StringField(render_kw={'placeholder': _('comment')}))
    setattr(
        form_class,
        'end_year_from',
        IntegerField(
            render_kw={'placeholder': _('YYYY')},
            validators=validator_year))
    setattr(
        form_class,
        'end_month_from',
        IntegerField(
            render_kw={'placeholder': _('MM')},
            validators=validator_month))
    setattr(
        form_class,
        'end_day_from',
        IntegerField(
            render_kw={'placeholder': _('DD')},
            validators=validator_day))
    if has_time:
        setattr(
            form_class,
            'end_hour_from',
            IntegerField(
                render_kw={'placeholder': _('hh')},
                validators=validator_hour))
        setattr(
            form_class,
            'end_minute_from',
            IntegerField(
                render_kw={'placeholder': _('mm')},
                validators=validator_minute))
        setattr(
            form_class,
            'end_second_from',
            IntegerField(
                render_kw={'placeholder': _('ss')},
                validators=validator_second))
    setattr(
        form_class,
        'end_year_to',
        IntegerField(
            render_kw={'placeholder': _('YYYY')},
            validators=validator_year))
    setattr(
        form_class,
        'end_month_to',
        IntegerField(
            render_kw={'placeholder': _('MM')},
            validators=validator_month))
    setattr(
        form_class,
        'end_day_to',
        IntegerField(
            render_kw={'placeholder': _('DD')},
            validators=validator_day))
    if has_time:
        setattr(
            form_class,
            'end_hour_to',
            IntegerField(
                render_kw={'placeholder': _('hh')},
                validators=validator_hour))
        setattr(
            form_class,
            'end_minute_to',
            IntegerField(
                render_kw={'placeholder': _('mm')},
                validators=validator_minute))
        setattr(
            form_class,
            'end_second_to',
            IntegerField(
                render_kw={'placeholder': _('ss')},
                validators=validator_second))
    setattr(
        form_class,
        'end_comment',
        StringField(render_kw={'placeholder': _('comment')}))


def add_value_type_fields(form_class: FlaskForm, subs: list[int]) -> None:
    for sub_id in subs:
        sub = g.types[sub_id]
        setattr(
            form_class,
            str(sub.id),
            ValueFloatField(sub.name, [OptionalValidator()]))
        add_value_type_fields(form_class, sub.subs)


def add_types(manager: Any) -> None:
    if manager.class_.name in g.classes \
            and g.classes[manager.class_.name].hierarchies:
        types = OrderedDict({
            id_: g.types[id_] for id_ in
            g.classes[manager.class_.name].hierarchies})
        if g.classes[
                manager.class_.name].standard_type_id in types:
            types.move_to_end(  # Standard type to top
                g.classes[manager.class_.name].standard_type_id,
                last=False)
        for type_ in types.values():

            class AddDynamicType(FlaskForm):
                pass

            setattr(AddDynamicType, 'name-dynamic', StringField(_('name')))
            setattr(
                AddDynamicType,
                f'{type_.id}-dynamic',
                TreeField(str(type_.id), type_id=str(type_.id)))
            setattr(
                AddDynamicType,
                'description-dynamic',
                TextAreaField(_('description')))
            form = AddDynamicType() if is_authorized('editor') else None
            getattr(form, f'{type_.id}-dynamic').label.text = 'super'
            if type_.multiple:
                setattr(
                    manager.form_class,
                    str(type_.id),
                    TreeMultiField(str(type_.id), form=form))
            else:
                setattr(
                    manager.form_class,
                    str(type_.id),
                    TreeField(str(type_.id), form=form))
            if type_.category == 'value':
                add_value_type_fields(manager.form_class, type_.subs)
