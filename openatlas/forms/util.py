from __future__ import annotations  # Needed for Python 4.0 type annotations

import ast
from typing import Any, Dict, List, Optional, Union

from flask import g, session
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort

from openatlas.forms.field import TreeField
from openatlas.forms.setting import ProfileForm
from openatlas.models.date import form_to_datetime64
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.type import Type
from openatlas.util.util import sanitize, uc_first


def get_link_type(form: Any) -> Optional[Entity]:
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
            _('show email'): str(
                _('on') if current_user.settings['show_email'] else _('off')),
            _('newsletter'): str(
                _('on') if current_user.settings['newsletter'] else _('off'))}
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
        'links': {'insert': [], 'delete': set(), 'delete_inverse': set()}}
    for key, value in form.data.items():
        field_type = getattr(form, key).type
        if field_type in [
                'TreeField',
                'TreeMultiField',
                'TableField',
                'TableMultiField']:
            if value:
                ids = ast.literal_eval(value)
                value = ids if isinstance(ids, list) else [int(ids)]
            else:
                value = []
        if key.startswith((
                'begin_',
                'end_',
                'name_inverse',
                'multiple',
                'page',
                'reference_system_precision_',
                'website_url',
                'resolver_url',
                'placeholder',
                'classes')) \
                or field_type in [
                    'CSRFTokenField',
                    'HiddenField',
                    'MultipleFileField',
                    'SelectMultipleField',
                    'SubmitField',
                    'TableField',
                    'TableMultiField']:
            continue
        if key == 'name':
            name = form.data['name']
            if hasattr(form, 'name_inverse'):
                name = form.name.data.replace('(', '').replace(')', '').strip()
                if form.name_inverse.data.strip():
                    inverse = form.name_inverse.data.\
                        replace('(', '').\
                        replace(')', '').strip()
                    name += ' (' + inverse + ')'
            if entity.class_.name == 'type':
                name = sanitize(name, 'type')
            elif entity.class_.name == 'reference_system' \
                    and hasattr(entity, 'system') \
                    and entity.system:
                name = entity.name
            data['attributes']['name'] = name
        elif key == 'description':
            data['attributes'][key] = form.data[key]
        elif key == 'alias':
            data['aliases'] = value
        elif field_type in ['TreeField', 'TreeMultiField']:
            if g.types[int(getattr(form, key).id)].class_.name \
                    == 'administrative_unit':
                if 'administrative_units' not in data:
                    data['administrative_units'] = []
                data['administrative_units'] += value
            else:
                data['links']['delete'].add('P2')
                data['links']['insert'].append({
                    'property': 'P2',
                    'range': [g.types[id_] for id_ in value]})
        elif field_type == 'ValueFloatField':
            if value is not None:  # Allow the number zero
                data['links']['insert'].append({
                    'property': 'P2',
                    'description': value,
                    'range': g.types[int(key)]})
        elif key.startswith('reference_system_id_'):
            system = Entity.get_by_id(
                int(key.replace('reference_system_id_', '')))
            precision_field = getattr(form, key.replace('id_', 'precision_'))
            data['links']['delete_reference_system'] = True
            if value:
                data['links']['insert'].append({
                    'property': 'P67',
                    'range': system,
                    'description': value,
                    'type_id': precision_field.data,
                    'inverse': True})
        else:  # pragma: no cover
            abort(418, f'Form field error: {key}, {field_type}, value={value}')

    if entity.class_.view == 'actor':
        data['links']['delete'].update(['P74', 'OA8', 'OA9'])
        if form.residence.data:
            residence = Entity.get_by_id(int(form.residence.data))
            data['links']['insert'].append({
                'property': 'P74',
                'range': residence.get_linked_entity_safe('P53')})
        if form.begins_in.data:
            begin_place = Entity.get_by_id(int(form.begins_in.data))
            data['links']['insert'].append({
                'property': 'OA8',
                'range': begin_place.get_linked_entity_safe('P53')})
        if form.ends_in.data:
            end_place = Entity.get_by_id(int(form.ends_in.data))
            data['links']['insert'].append({
                'property': 'OA9',
                'range': end_place.get_linked_entity_safe('P53')})
    elif entity.class_.view == 'event':
        data['links']['delete'].update(['P7', 'P117'])
        if form.event.data:  # Super event
            data['links']['insert'].append({
                'property': 'P117',
                'range': form.event.data})
        if hasattr(form, 'place') and form.place.data:
            data['links']['insert'].append({
                'property': 'P7',
                'range':
                    Link.get_linked_entity_safe(int(form.place.data), 'P53')})
        if entity.class_.name == 'acquisition':
            data['links']['delete'].add('P24')
            if form.given_place.data:
                data['links']['insert'].append({
                    'property': 'P24',
                    'range': form.given_place.data})
        elif entity.class_.name == 'production':
            data['links']['delete'].add('P108')
            if form.artifact.data:
                data['links']['insert'].append({
                    'property': 'P108',
                    'range': form.artifact.data})
        elif entity.class_.name == 'move':
            data['links']['delete'].update(['P25', 'P26', 'P27'])
            if form.artifact.data:
                data['links']['insert'].append({
                    'property': 'P25',
                    'range': form.artifact.data})
            if form.person.data:
                data['links']['insert'].append({
                    'property': 'P25',
                    'range': form.person.data})
            if form.place_from.data:
                data['links']['insert'].append({
                    'property': 'P27',
                    'range':  Link.get_linked_entity_safe(
                         int(form.place_from.data),
                         'P53')})
            if form.place_to.data:
                data['links']['insert'].append({
                    'property': 'P26',
                    'range': Link.get_linked_entity_safe(
                        int(form.place_to.data),
                        'P53')})
    elif entity.class_.view in ['artifact', 'place']:
        data['gis'] = {}
        for shape in ['point', 'line', 'polygon']:
            data['gis'][shape] = getattr(form, f'gis_{shape}s').data
        if entity.class_.name == 'artifact':
            data['links']['delete'].add('P52')
            if form.actor.data:
                data['links']['insert'].append({
                    'property': 'P52',
                    'range': form.actor.data})
    elif entity.class_.view == 'reference_system':
        data['reference_system'] = {
            'website_url': form.website_url.data,
            'resolver_url': form.resolver_url.data,
            'placeholder': form.placeholder.data,
            'classes': form.classes.data if hasattr(form, 'classes') else None}
    elif entity.class_.view == 'source' and not origin:
        data['links']['delete_inverse'].add('P128')
        if form.artifact.data:
            data['links']['insert'].append({
                'property': 'P128',
                'range': form.artifact.data,
                'inverse': True})
    elif entity.class_.view == 'type' and 'classes' not in form:  # is sub type
        type_ = origin if isinstance(origin, Type) else entity
        root = g.types[type_.root[0]] if type_.root else type_
        super_id = g.types[type_.root[-1]] if type_.root else type_
        new_super_id = getattr(form, str(root.id)).data
        new_super = g.types[int(new_super_id)] if new_super_id else root
        code = 'P127' if entity.class_.name == 'type' else 'P89'
        if super_id != new_super.id:
            data['links']['delete'].add(code)
            data['links']['insert'].append({
                 'property': code,
                 'range': new_super})
    for link_ in data['links']['insert']:
        if isinstance(link_['range'], str):
            link_['range'] = form_string_to_entity_list(link_['range'])
    if origin and entity.class_.name not in ('administrative_unit', 'type'):
        data = process_origin_data(entity, origin, form, data)
    return data


def form_string_to_entity_list(string: str) -> List[Entity]:
    ids = ast.literal_eval(string)
    ids = [int(id_) for id_ in ids] if isinstance(ids, list) else [int(ids)]
    return Entity.get_by_ids(ids)


def process_origin_data(entity, origin, form, data):
    if origin.class_.view == 'reference':
        if entity.class_.name == 'file':
            data['links']['insert'].append({
                'property': 'P67',
                'range': origin,
                'description': form.page.data,
                'inverse': True})
        else:
            data['links']['insert'].append({
                'property': 'P67',
                'range': origin,
                'return_link_id': True,
                'inverse': True})
    elif entity.class_.name == 'file' \
            or entity.class_.view in ['reference', 'source']:
        data['links']['insert'].append({
            'property': 'P67',
            'range': origin,
            'return_link_id': entity.class_.view == 'reference'})
    elif origin.class_.view in ['place', 'feature', 'stratigraphic_unit']:
        if entity.class_.view == 'place' or entity.class_.name == 'artifact':
            data['links']['insert'].append({
                'property': 'P46',
                'range': origin,
                'inverse': True})
    elif origin.class_.view in ['source', 'file']:
        data['links']['insert'].append({
            'property': 'P67',
            'range': origin,
            'inverse': True})
    elif origin.class_.view == 'event':  # Involvement from actor
        data['links']['insert'].append({
            'property': 'P11',
            'range': origin,
            'return_link_id': True,
            'inverse': True})
    elif origin.class_.view == 'actor' and entity.class_.view == 'event':
        data['links']['insert'].append({  # Involvement from event
            'property': 'P11',
            'range': origin,
            'return_link_id': True})
    elif origin.class_.view == 'actor' and entity.class_.view == 'actor':
        data['links']['insert'].append({  # Actor actor relation
            'property': 'OA7',
            'range': origin,
            'return_link_id': True,
            'inverse': True})
    return data


def process_form_dates(form: FlaskForm) -> Dict[str, Any]:
    data = {
        'begin_from': None, 'begin_to': None, 'begin_comment': None,
        'end_from': None, 'end_to': None, 'end_comment': None}
    if hasattr(form, 'begin_year_from') and form.begin_year_from.data:
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
    if hasattr(form, 'end_year_from') and form.end_year_from.data:
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
