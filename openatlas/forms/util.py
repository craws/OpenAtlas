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
        if field.name in ['mail_recipients_feedback',
                          'file_upload_allowed_extension']:
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
        #if key in ['address', 'inverse', 'latitude', 'longitude']:
        #    continue  # These fields are processed elsewhere
        #if field_type in [
        #    'TreeField', 'TreeMultiField', 'TableField', 'TableMultiField']:
        #    if value:
        #        ids = ast.literal_eval(value)
        #        value = ids if isinstance(ids, list) else [int(ids)]
        #    else:
        #        value = []

        # Data mapping
        if field_type in ['StringField', 'TextAreaField']:
            if key in ['name', 'description']:
                data['attributes'][key] = form.data[key]
            else:  # pragma: no cover
                print('unknown field: ', field_type, key, value)
        else:  # pragma: no cover
            print('unknown form field type', field_type, key, value)
    return data
