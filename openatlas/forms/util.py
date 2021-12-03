from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Any, Dict, Optional as Optional_Type, Optional

from flask import g, session
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm

from openatlas.forms.field import TreeField
from openatlas.forms.setting import ProfileForm
from openatlas.models.entity import Entity
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
        'attributes': {},
        'links': [],
        'types': []}
    for key, value in form.data.items():

        # Data preparation
        field_type = getattr(form, key).type
        if field_type in ['CSRFTokenField', 'HiddenField', 'SubmitField']:
            continue

        # Data mapping
        if key in ['name', 'description']:
            data['attributes'][key] = form.data[key]
        else:  # pragma: no cover # Todo: throw an exception and log it
            print('unknown form field type', field_type, key, value)

    return data

    # if key in ['address', 'inverse', 'latitude', 'longitude']:
    #    continue  # These fields are processed elsewhere
    # if field_type in [
    #    'TreeField', 'TreeMultiField', 'TableField', 'TableMultiField']:
    #    if value:
    #        ids = ast.literal_eval(value)
    #        value = ids if isinstance(ids, list) else [int(ids)]
    #    else:
    #        value = []

    #     @staticmethod
    #     def save_entity_types(entity: Entity, form: Any) -> None:
    #         from openatlas.forms.field import TreeField
    #         from openatlas.forms.field import TreeMultiField
    #         from openatlas.forms.field import ValueFloatField
    #         # Can't use isinstance checks for entity here because it is
    #         always a
    #         # Entity at this point. So entity.class_.name checks have to be
    #         used.
    #         if hasattr(entity, 'types'):
    #             entity.delete_links(['P2', 'P89'])
    #         for field in form:
    #             if isinstance(field, ValueFloatField):
    #                 if entity.class_.name == 'object_location' \
    #                         or isinstance(entity, Type):
    #                     continue  # pragma: no cover
    #                 if field.data is not None:  # Allow 0 (zero)
    #                     entity.link('P2', g.types[int(field.name)],
    #                     field.data)
    #             elif isinstance(field, (TreeField, TreeMultiField)) and
    #             field.data:
    #                 try:
    #                     range_ = [g.types[int(field.data)]]
    #                 except ValueError:  # Form value was a list string e.g.
    #                 '[8,27]'
    #                     range_ = [
    #                         g.types[int(range_id)]
    #                         for range_id in ast.literal_eval(field.data)]
    #                 if g.types[int(field.id)].class_.name ==
    #                 'administrative_unit':
    #                     if entity.class_.name == 'object_location':
    #                         entity.link('P89', range_)
    #                 elif entity.class_.name not in ['object_location',
    #                 'type']:
    #                     entity.link('P2', range_)


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
