from __future__ import annotations  # Needed for Python 4.0 type annotations

import ast
from typing import Any, Dict, Optional as Optional_Type, Optional, Union

from flask import g, session
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm

from openatlas.forms.field import TreeField
from openatlas.forms.setting import ProfileForm
from openatlas.models.date import form_to_datetime64
from openatlas.models.entity import Entity
from openatlas.models.type import Type
from openatlas.util.util import uc_first


def get_link_type(form: Any) -> Optional_Type[Entity]:
    # Returns base type of a link form, e.g. involvement between actor and event
    for field in form:
        if isinstance(field, TreeField) and field.data:
            return g.types[int(field.data)]
    return None


def get_form_settings(form: Any, profile: bool = False) -> Dict[str, str]:
    if isinstance(form, ProfileForm):
        return {
            _('name'): current_user.real_name,
            _('email'): current_user.email,
            _('show email'): str(_('on') if current_user.settings['show_email']
                                 else _('off')),
            _('newsletter'): str(_('on') if current_user.settings['newsletter']
                                 else _('off'))}
    settings = {}
    for field in form:
        if field.type in ['CSRFTokenField', 'HiddenField', 'SubmitField']:
            continue
        label = uc_first(field.label.text)
        if profile and field.name in current_user.settings:
            value = current_user.settings[field.name]
        elif field.name in session['settings']:
            value = session['settings'][field.name]
        else:  # pragma: no cover
            value = ''  # In case of a missing setting after an update
        if field.type in ['StringField', 'IntegerField']:
            settings[label] = value
        if field.type == 'BooleanField':
            # str() needed for templates
            settings[label] = str(_('on')) if value else str(_('off'))
        if field.type == 'SelectField':
            if isinstance(value, str) and value.isdigit():
                value = int(value)
            settings[label] = dict(field.choices).get(value)
        if field.name in ['mail_recipients_feedback',
                          'file_upload_allowed_extension']:
            settings[label] = ' '.join(value)
    return settings


def set_form_settings(form: Any, profile: bool = False) -> None:
    for field in form:
        if field.type in ['CSRFTokenField', 'HiddenField', 'SubmitField']:
            continue
        if profile and field.name == 'name':
            field.data = current_user.real_name
            continue
        if profile and field.name == 'email':
            field.data = current_user.email
            continue
        if profile and field.name in current_user.settings:
            field.data = current_user.settings[field.name]
            continue
        if field.name in ['log_level']:
            field.data = int(session['settings'][field.name])
            continue
        if field.name in \
                ['mail_recipients_feedback', 'file_upload_allowed_extension']:
            field.data = ' '.join(session['settings'][field.name])
            continue
        if field.name not in session['settings']:  # pragma: no cover
            field.data = ''  # In case of a missing setting after an update
            continue
        field.data = session['settings'][field.name]


def process_form_data(
        form: FlaskForm,
        entity: Entity,
        origin: Optional[Entity] = None) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        'attributes': process_form_dates(form),
        'links': [],
        'administrative_units': [],
        'types': [],
        'value_types': []}
    for key, value in form.data.items():
        field_type = getattr(form, key).type
        if field_type in ['CSRFTokenField', 'HiddenField', 'SubmitField'] \
                or key.startswith(('begin_', 'end_')):
            continue
        if field_type in [
                'TreeField', 'TreeMultiField', 'TableField', 'TableMultiField']:
            if value:
                ids = ast.literal_eval(value)
                value = ids if isinstance(ids, list) else [int(ids)]
            else:
                value = []

        # Data mapping
        if key in ['name', 'description']:
            data['attributes'][key] = form.data[key]
        elif key == 'alias':
            data['aliases'] = value
        elif field_type in ['TreeField', 'TreeMultiField']:
            if g.types[int(getattr(form, key).id)].class_.name \
                    == 'administrative_unit':
                data['administrative_units'] += value
            else:
                data['types'] += value
        elif field_type == 'ValueFloatField':
            data['value_types'].append({'id': int(key), 'value': value})
        else:  # pragma: no cover # Todo: throw an exception and log it
            print('unknown form field type', field_type, key, value)

    return data

    #     def save_entity_types(entity: Entity, form: Any) -> None:
    #         entity_location.delete_links(['P89'])
    #         entity.link('P89', range_)
    #     elif entity.class_.view == 'type':
    #         type_ = origin if isinstance(origin, Type) else entity
    #         root = g.types[type_.root[0]] if type_.root else type_
    #         super_id = g.types[type_.root[-1]] if type_.root else type_
    #         new_super_id = getattr(form, str(root.id)).data
    #         new_super = g.types[int(new_super_id)] if new_super_id else root
    #         if super_id != new_super.id:
    #             property_code = 'P127' if entity.class_.name == 'type' else
    #             'P89'
    #             entity.delete_links([property_code])
    #             entity.link(property_code, new_super)


def process_form_dates(form: FlaskForm) -> Dict[str, Any]:
    data = {
        'begin_from': None, 'begin_to': None, 'begin_comment': None,
        'end_from': None, 'end_to': None, 'end_comment': None}
    if form.begin_year_from.data:
        data['begin_comment'] = form.begin_comment.data
        data['begin_from'] = form_to_datetime64(
            form.begin_year_from.data,
            form.begin_month_from.data,
            form.begin_day_from.data)
        data['begin_to'] = form_to_datetime64(
            form.begin_year_to.data,
            form.begin_month_to.data,
            form.begin_day_to.data,
            to_date=True)
    if form.end_year_from.data:
        data['end_comment'] = form.end_comment.data
        data['end_from'] = form_to_datetime64(
            form.end_year_from.data,
            form.end_month_from.data,
            form.end_day_from.data)
        data['end_to'] = form_to_datetime64(
            form.end_year_to.data,
            form.end_month_to.data,
            form.end_day_to.data,
            to_date=True)
    return data


def populate_insert_form(
        form: FlaskForm,
        class_: str,
        origin: Union[Entity, Type, None]) -> None:
    if hasattr(form, 'alias'):
        form.alias.append_entry('')
    if not origin:
        return
    view = g.classes[class_].view
    if view == 'actor' and origin.class_.name == 'place':
        form.residence.data = origin.id
    if view == 'artifact' and origin.class_.view == 'actor':
        form.actor.data = origin.id
    if view == 'event':
        if origin.class_.view == 'artifact':
            form.artifact.data = [origin.id]
        elif origin.class_.view in ['artifact', 'place']:
            if class_ == 'move':
                form.place_from.data = origin.id
            else:
                form.place.data = origin.id
    if view == 'source' and origin.class_.name == 'artifact':
        form.artifact.data = [origin.id]
    if view == 'type':
        root_id = origin.root[0] if origin.root else origin.id
        getattr(form, str(root_id)).data = origin.id \
            if origin.id != root_id else None


def populate_update_form(form: FlaskForm, entity: Union[Entity, Type]) -> None:
    if hasattr(form, 'alias'):
        for alias in entity.aliases.values():
            form.alias.append_entry(alias)
        form.alias.append_entry('')
    if entity.class_.view == 'actor':
        residence = entity.get_linked_entity('P74')
        form.residence.data = residence.get_linked_entity_safe('P53', True).id \
            if residence else ''
        first = entity.get_linked_entity('OA8')
        form.begins_in.data = first.get_linked_entity_safe('P53', True).id \
            if first else ''
        last = entity.get_linked_entity('OA9')
        form.ends_in.data = last.get_linked_entity_safe('P53', True).id \
            if last else ''
    elif entity.class_.name == 'artifact':
        owner = entity.get_linked_entity('P52')
        form.actor.data = owner.id if owner else None
    elif entity.class_.view == 'event':
        super_event = entity.get_linked_entity('P117')
        form.event.data = super_event.id if super_event else ''
        if entity.class_.name == 'move':
            place_from = entity.get_linked_entity('P27')
            form.place_from.data = place_from.get_linked_entity_safe(
                'P53', True).id if place_from else ''
            place_to = entity.get_linked_entity('P26')
            form.place_to.data = \
                place_to.get_linked_entity_safe('P53', True).id \
                if place_to else ''
            person_data = []
            object_data = []
            for linked_entity in entity.get_linked_entities('P25'):
                if linked_entity.class_.name == 'person':
                    person_data.append(linked_entity.id)
                elif linked_entity.class_.view == 'artifact':
                    object_data.append(linked_entity.id)
            form.person.data = person_data
            form.artifact.data = object_data
        else:
            place = entity.get_linked_entity('P7')
            form.place.data = place.get_linked_entity_safe('P53', True).id \
                if place else ''
        if entity.class_.name == 'acquisition':
            form.given_place.data = \
                [entity.id for entity in entity.get_linked_entities('P24')]
        if entity.class_.name == 'production':
            form.artifact.data = \
                [entity.id for entity in entity.get_linked_entities('P108')]
    elif isinstance(entity, Type):
        if hasattr(form, 'name_inverse'):  # Directional, e.g. actor relation
            name_parts = entity.name.split(' (')
            form.name.data = name_parts[0]
            if len(name_parts) > 1:
                form.name_inverse.data = name_parts[1][:-1]  # remove the ")"
        root = g.types[entity.root[0]] if entity.root else entity
        if root:  # Set super if exists and is not same as root
            super_ = g.types[entity.root[-1]]
            getattr(
                form,
                str(root.id)).data = super_.id \
                if super_.id != root.id else None
    elif entity.class_.view == 'source':
        form.artifact.data = [
            item.id for item in
            entity.get_linked_entities('P128', inverse=True)]
