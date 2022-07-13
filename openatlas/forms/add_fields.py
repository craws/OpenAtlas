from collections import OrderedDict

from flask import g
from flask_babel import lazy_gettext as _
from wtforms import IntegerField, SelectField, StringField
from wtforms.validators import (
    NoneOf, NumberRange, Optional as OptionalValidator)
from openatlas.forms.field import TreeField, TreeMultiField, ValueFloatField
from openatlas.models.type import Type
from openatlas.util.util import uc_first


def add_reference_systems(class_, form_class) -> None:
    precisions = [('', '')] + [
        (str(g.types[id_].id), g.types[id_].name)
        for id_ in Type.get_hierarchy('External reference match').subs]
    systems = list(g.reference_systems.values())
    systems.sort(key=lambda x: x.name.casefold())
    for system in systems:
        if class_.name not in system.classes:
            continue
        setattr(
            form_class,
            f'reference_system_id_{system.id}',
            StringField(
                uc_first(system.name),
                [OptionalValidator()],
                description=system.description,
                render_kw={
                    'autocomplete': 'off',
                    'placeholder': system.placeholder}))
        setattr(
            form_class,
            f'reference_system_precision_{system.id}',
            SelectField(
                _('precision'),
                choices=precisions,
                default=system.precision_default_id))


def add_date_fields(form_class, has_time: bool) -> None:
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


def add_value_type_fields(form_class, subs: list[int]) -> None:
    for sub_id in subs:
        sub = g.types[sub_id]
        setattr(
            form_class,
            str(sub.id),
            ValueFloatField(sub.name, [OptionalValidator()]))
        add_value_type_fields(form_class, sub.subs)


def add_types(manager):
    if manager.class_.name in g.classes \
            and g.classes[manager.class_.name].hierarchies:
        types = OrderedDict(
            {id_: g.types[id_] for id_ in
             g.classes[manager.class_.name].hierarchies})
        if g.classes[
                manager.class_.name].standard_type_id in types:
            types.move_to_end(  # Standard type to top
                g.classes[manager.class_.name].standard_type_id,
                last=False)
        for type_ in types.values():
            if type_.multiple:
                setattr(
                    manager.form_class,
                    str(type_.id),
                    TreeMultiField(str(type_.id)))
            else:
                setattr(
                    manager.form_class,
                    str(type_.id),
                    TreeField(str(type_.id)))
            if type_.category == 'value':
                add_value_type_fields(manager.form_class, type_.subs)
