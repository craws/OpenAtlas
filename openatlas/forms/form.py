from __future__ import annotations  # Needed for Python 4.0 type annotations

import time
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Union

from flask import g, request
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (FieldList, HiddenField, IntegerField, SelectField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import InputRequired, Optional as OptionalValidator, URL

from openatlas import app
from openatlas.forms import date
from openatlas.forms.field import (TableField, TableMultiField, TreeField, TreeMultiField,
                                   ValueFloatField)
from openatlas.models.date import Date
from openatlas.models.entity import Entity
from openatlas.models.node import Node
from openatlas.models.reference import Reference
from openatlas.util.display import uc_first

forms = {'actor': ['name', 'alias', 'date', 'wikidata', 'description', 'continue'],
         'bibliography': ['name', 'description', 'continue'],
         'edition': ['name', 'description', 'continue'],
         'external_reference': ['name', 'description', 'continue'],
         'event': ['name', 'date', 'wikidata', 'description', 'continue'],
         'feature': ['name', 'date', 'wikidata', 'description', 'continue', 'map'],
         'find': ['name', 'date', 'wikidata', 'description', 'continue', 'map'],
         'human_remains': ['name', 'date', 'wikidata', 'description', 'continue', 'map'],
         'place': ['name', 'alias', 'date', 'wikidata', 'geonames', 'description', 'continue',
                   'map'],
         'source': ['name', 'description', 'continue'],
         'stratigraphic_unit': ['name', 'date', 'wikidata', 'description', 'continue', 'map']}


def build_form(name: str,
               entity: Optional[Entity] = None,
               code: Optional[str] = None,
               origin: Optional[Entity] = None,
               location: Optional[Entity] = None) -> FlaskForm:

    # Builds a form for CIDOC CRM entities which has to be dynamic because of types, module
    # settings and class specific fields

    class Form(FlaskForm):  # type: ignore
        opened = HiddenField()

    if 'name' in forms[name]:
        label = _('URL') if name == 'external_reference' else _('name')
        validators = [InputRequired(), URL()] if name == 'external_reference' else [InputRequired()]
        setattr(Form, 'name', StringField(label,
                                          validators=validators,
                                          render_kw={'autofocus': True}))

    if 'alias' in forms[name]:
        setattr(Form, 'alias', FieldList(StringField(''), description=_('tooltip alias')))
    code = entity.class_.code if entity else code
    add_types(Form, name, code)
    add_fields(Form, name, code)
    add_external_references(Form, name)
    if 'date' in forms[name]:
        date.add_date_fields(Form)
    if 'description' in forms[name]:
        label = _('content') if name == 'source' else _('description')
        setattr(Form, 'description', TextAreaField(label))
    if 'map' in forms[name]:
        setattr(Form, 'gis_points', HiddenField(default='[]'))
        setattr(Form, 'gis_polygons', HiddenField(default='[]'))
        setattr(Form, 'gis_lines', HiddenField(default='[]'))
    add_buttons(Form, name, entity, origin)
    setattr(Form, 'validate', validate)
    return populate_form(Form(obj=entity), entity, location) if entity else Form()


def populate_form(form: FlaskForm, entity: Entity, location: Optional[Entity]) -> FlaskForm:
    form.save.label.text = uc_first(_('save'))
    if not entity or not request or request.method != 'GET':
        return form

    # Dates
    if hasattr(form, 'begin_year_from'):
        date.populate_dates(form, entity)

    # Nodes
    nodes = entity.nodes
    if location:  # Needed for administrative unit and historical place nodes
        nodes.update(location.nodes)
    form.opened.data = time.time()
    node_data: Dict[int, List[int]] = {}
    for node, node_value in nodes.items():
        root = g.nodes[node.root[-1]] if node.root else node
        if root.id not in node_data:
            node_data[root.id] = []
        node_data[root.id].append(node.id)
        if root.value_type:
            getattr(form, str(node.id)).data = node_value
    for root_id, nodes_ in node_data.items():
        if hasattr(form, str(root_id)):
            getattr(form, str(root_id)).data = nodes_

    # External references
    for name in g.external:
        if hasattr(form, name + '_id') and current_user.settings['module_' + name]:
            link_ = Reference.get_link(entity, name)
            if link_ and not getattr(form, name + '_id').data:
                reference = link_.domain
                getattr(form, name + '_id').data = reference.name if reference else ''
                getattr(form, name + '_precision').data = g.nodes[link_.type.id].name

    return form


def add_buttons(form: any, name: str, entity: Union[Entity, None], origin) -> None:
    setattr(form, 'save', SubmitField(uc_first(_('insert'))))
    if entity:
        return form
    if not origin and 'continue' in forms[name]:
        setattr(form, 'insert_and_continue', SubmitField(uc_first(_('insert and continue'))))
        setattr(form, 'continue_', HiddenField())
    insert_and_add = uc_first(_('insert and add')) + ' '
    if name == 'place':
        setattr(form, 'insert_and_continue', SubmitField(uc_first(_('insert and continue'))))
        setattr(form, 'continue_', HiddenField())
        setattr(form, 'insert_continue_sub', SubmitField(insert_and_add + _('feature')))
    elif name == 'feature' and origin and origin.system_type == 'place':
        setattr(form, 'insert_and_continue', SubmitField(uc_first(_('insert and continue'))))
        setattr(form, 'continue_', HiddenField())
        setattr(form, 'insert_continue_sub', SubmitField(insert_and_add + _('stratigraphic unit')))
    elif name == 'stratigraphic_unit':
        setattr(form, 'insert_and_continue', SubmitField(uc_first(_('insert and continue'))))
        setattr(form, 'continue_', HiddenField())
        setattr(form, 'insert_continue_sub', SubmitField(insert_and_add + _('find')))
        setattr(form,
                'insert_continue_human_remains',
                SubmitField(insert_and_add + _('human remains')))
    return form


def add_external_references(form: any, form_name: str) -> None:
    for name, ref in g.external.items():
        if name not in forms[form_name] or not current_user.settings['module_' + name]:
            continue
        if name == 'geonames':
            field = IntegerField(ref['name'] + ' Id', [OptionalValidator()])
        else:
            field = StringField(ref['name'] + ' Id', [OptionalValidator()])
        setattr(form, name + '_id', field)
        setattr(form,
                name + '_precision',
                SelectField(uc_first(_('precision')),
                            choices=app.config['REFERENCE_PRECISION'],
                            default='close match' if name == 'geonames' else ''))


def add_value_type_fields(form: any, subs: List[int]) -> None:
    for sub_id in subs:
        sub = g.nodes[sub_id]
        setattr(form, str(sub.id), ValueFloatField(sub.name, [OptionalValidator()]))
        add_value_type_fields(form, sub.subs)


def add_types(form: any, name: str, code: Union[str, None]):
    code_class = {'E21': 'Person', 'E74': 'Group', 'E40': 'Legal Body'}
    type_name = name.replace('_', ' ').title()
    if code in code_class:
        type_name = code_class[code]
    types = OrderedDict(Node.get_nodes_for_form(type_name))
    for id_, node in types.items():
        if node.name in app.config['BASE_TYPES']:
            types.move_to_end(node.id, last=False)  # Move standard type to top
            break

    for id_, node in types.items():
        setattr(form, str(id_), TreeMultiField(str(id_)) if node.multiple else TreeField(str(id_)))
        if node.value_type:
            add_value_type_fields(form, node.subs)


def add_fields(form: Any, name: str, code: Optional[str] = None) -> None:
    if name == 'actor':
        setattr(form, 'residence', TableField(_('residence')))
        setattr(form, 'begins_in', TableField(_('born in') if code == 'E21' else _('begins in')))
        setattr(form, 'ends_in', TableField(_('died in') if code == 'E21' else _('ends in')))
    elif name == 'event':
        setattr(form, 'event_id', HiddenField())
        setattr(form, 'event', TableField(_('sub event of')))
        if code == 'E7':
            setattr(form, 'place', TableField(_('location')))
        if code == 'E8':
            setattr(form, 'place', TableField(_('location')))
            setattr(form, 'given_place', TableMultiField(_('given place')))
        elif code == 'E9':
            setattr(form, 'place_from', TableField(_('from')))
            setattr(form, 'place_to', TableField(_('to')))
            setattr(form, 'object', TableMultiField())
            setattr(form, 'person', TableMultiField())
    elif name == 'source':
        setattr(form, 'information_carrier', TableMultiField())


def validate(self) -> bool:
    valid = FlaskForm.validate(self)

    # Check date format, if valid put dates into a list called "dates"
    if hasattr(self, 'begin_year_from'):
        dates = {}
        for prefix in ['begin_', 'end_']:
            if getattr(self, prefix + 'year_to').data and not getattr(self,
                                                                      prefix + 'year_from').data:
                getattr(self, prefix + 'year_from').errors.append(
                    _("Required for time span"))
                valid = False
            for postfix in ['_from', '_to']:
                if getattr(self, prefix + 'year' + postfix).data:
                    date_ = Date.form_to_datetime64(
                        getattr(self, prefix + 'year' + postfix).data,
                        getattr(self, prefix + 'month' + postfix).data,
                        getattr(self, prefix + 'day' + postfix).data)
                    if not date_:
                        getattr(self, prefix + 'day' + postfix).errors.append(
                            _('not a valid date'))
                        valid = False
                    else:
                        dates[prefix + postfix.replace('_', '')] = date_

        # Check for valid date combination e.g. begin not after end
        if valid:
            for prefix in ['begin', 'end']:
                if prefix + '_from' in dates and prefix + '_to' in dates:
                    if dates[prefix + '_from'] > dates[prefix + '_to']:
                        field = getattr(self, prefix + '_day_from')
                        field.errors.append(_('First date cannot be after second.'))
                        valid = False
        if 'begin_from' in dates and 'end_from' in dates:
            field = getattr(self, 'begin_day_from')
            if len(dates) == 4:  # All dates are used
                if dates['begin_from'] > dates['end_from'] or dates['begin_to'] > dates['end_to']:
                    field.errors.append(_('Begin dates cannot start after end dates.'))
                    valid = False
            else:
                first = dates['begin_to'] if 'begin_to' in dates else dates['begin_from']
                second = dates['end_from'] if 'end_from' in dates else dates['end_to']
                if first > second:
                    field.errors.append(_('Begin dates cannot start after end dates.'))
                    valid = False

    # Super event
    if hasattr(self, 'event'):
        """ Check if selected super event is allowed."""
        # Todo: also check if super is not a sub event of itself (recursively)
        if self.event.data:
            if str(self.event.data) == str(self.event_id.data):
                self.event.errors.append(_('error node self as super'))
                valid = False

    # External references
    if hasattr(self, 'wikidata_id') and self.wikidata_id.data:  # pragma: no cover
        if self.wikidata_id.data[0].upper() != 'Q' or not self.wikidata_id.data[1:].isdigit():
            self.wikidata_id.errors.append(uc_first(_('wrong format')))
            valid = False
        else:
            self.wikidata_id.data = uc_first(self.wikidata_id.data)
    for name in g.external:
        if hasattr(self, name + '_id'):
            if getattr(self, name + '_id').data and not getattr(self, name + '_precision').data:
                valid = False
                getattr(self, name + '_id').errors.append(uc_first(_('precision required')))
    return valid
